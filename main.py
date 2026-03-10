from __future__ import annotations

import argparse
import logging
import time

from config import load_config
from monitor import MonitorService, SIGAAFetcher
from notifier import NotifierHub
from storage import MonitoredClass, Storage



def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor de vagas de turmas SIGAA UnB (somente consulta)")
    sub = parser.add_subparsers(dest="command", required=True)

    add_cmd = sub.add_parser("add", help="Adicionar turma para monitoramento")
    add_cmd.add_argument("--code", required=True, help="Código da disciplina")
    add_cmd.add_argument("--name", required=False, help="Nome da disciplina")
    add_cmd.add_argument("--class-group", required=True, help="Turma")
    add_cmd.add_argument("--term", required=True, help="Semestre/período")
    add_cmd.add_argument("--campus", required=False, help="Campus")
    add_cmd.add_argument("--url", required=True, help="URL de consulta da turma")

    sub.add_parser("list", help="Listar turmas monitoradas")

    rm_cmd = sub.add_parser("remove", help="Remover turma monitorada")
    rm_cmd.add_argument("--id", type=int, required=True)

    run_cmd = sub.add_parser("run", help="Iniciar monitoramento contínuo")
    run_cmd.add_argument("--interval", type=int, help="Intervalo entre checagens em segundos")
    run_cmd.add_argument("--once", action="store_true", help="Executa apenas um ciclo")

    hist_cmd = sub.add_parser("history", help="Mostrar histórico recente")
    hist_cmd.add_argument("--limit", type=int, default=20)

    return parser



def cmd_add(storage: Storage, args: argparse.Namespace) -> None:
    class_id = storage.add_monitored_class(
        MonitoredClass(
            id=None,
            code=args.code,
            name=args.name,
            class_group=args.class_group,
            term=args.term,
            campus=args.campus,
            query_url=args.url,
        )
    )
    print(f"Turma adicionada com ID {class_id}")



def cmd_list(storage: Storage) -> None:
    items = storage.list_monitored_classes()
    if not items:
        print("Nenhuma turma cadastrada")
        return
    for item in items:
        print(
            f"[{item.id}] {item.code} | {item.name or '-'} | Turma {item.class_group} | "
            f"{item.term} | {item.campus or '-'} | {item.query_url}"
        )



def cmd_remove(storage: Storage, class_id: int) -> None:
    if storage.remove_monitored_class(class_id):
        print(f"Turma {class_id} removida")
    else:
        print(f"Turma {class_id} não encontrada")



def cmd_history(storage: Storage, limit: int) -> None:
    rows = storage.recent_history(limit)
    if not rows:
        print("Sem histórico")
        return
    for row in rows:
        print(
            f"#{row['id']} class_id={row['class_id']} {row['code']} T{row['class_group']} {row['term']} "
            f"total={row['total_seats']} occupied={row['occupied_seats']} avail={row['available_seats']} "
            f"status={row['status']} changed={bool(row['changed'])} at={row['observed_at']} "
            f"summary={row['change_summary']}"
        )



def cmd_run(storage: Storage, service: MonitorService, interval: int, once: bool) -> None:
    while True:
        classes = storage.list_monitored_classes()
        if not classes:
            print("Nenhuma turma cadastrada para monitoramento")
            if once:
                return
            time.sleep(interval)
            continue

        for monitored_class in classes:
            try:
                service.check_once(monitored_class)
            except Exception as exc:  # noqa: BLE001
                logging.getLogger(__name__).error(
                    "Erro ao verificar %s T%s: %s",
                    monitored_class.code,
                    monitored_class.class_group,
                    exc,
                )

        if once:
            return

        time.sleep(interval)



def main() -> None:
    setup_logging()
    config = load_config()
    storage = Storage(config.db_path)
    storage.init_db()

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        cmd_add(storage, args)
        return
    if args.command == "list":
        cmd_list(storage)
        return
    if args.command == "remove":
        cmd_remove(storage, args.id)
        return
    if args.command == "history":
        cmd_history(storage, args.limit)
        return

    if args.command == "run":
        interval = args.interval if args.interval is not None else config.check_interval_seconds
        fetcher = SIGAAFetcher(config)
        notifier = NotifierHub(config)
        service = MonitorService(storage, fetcher, notifier, config)
        cmd_run(storage, service, interval=interval, once=args.once)


if __name__ == "__main__":
    main()
