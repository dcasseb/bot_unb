from __future__ import annotations

import argparse
import logging
from threading import Event

from app_services import AddClassInput, MonitoringAppService
from config import load_config
from monitor import MonitorService, SIGAAFetcher
from notifier import NotifierHub
from storage import Storage


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


def cmd_add(service: MonitoringAppService, args: argparse.Namespace) -> None:
    class_id = service.add_class(
        AddClassInput(
            code=args.code,
            name=args.name,
            class_group=args.class_group,
            term=args.term,
            campus=args.campus,
            query_url=args.url,
        )
    )
    print(f"Turma adicionada com ID {class_id}")


def cmd_list(service: MonitoringAppService) -> None:
    items = service.list_classes()
    if not items:
        print("Nenhuma turma cadastrada")
        return
    for item in items:
        print(
            f"[{item.id}] {item.code} | {item.name or '-'} | Turma {item.class_group} | "
            f"{item.term} | {item.campus or '-'} | {item.query_url}"
        )


def cmd_remove(service: MonitoringAppService, class_id: int) -> None:
    if service.remove_class(class_id):
        print(f"Turma {class_id} removida")
    else:
        print(f"Turma {class_id} não encontrada")


def cmd_history(service: MonitoringAppService, limit: int) -> None:
    rows = service.history(limit)
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


def cmd_run(service: MonitoringAppService, interval: int, once: bool) -> None:
    if once:
        summary = service.run_cycle()
        if summary["checked"] == 0:
            print("Nenhuma turma cadastrada para monitoramento")
        return
    service.run_loop(interval=interval, stop_event=Event())


def main() -> None:
    setup_logging()
    config = load_config()
    storage = Storage(config.db_path)
    storage.init_db()

    parser = build_parser()
    args = parser.parse_args()

    fetcher = SIGAAFetcher(config)
    notifier = NotifierHub(config)
    monitor_service = MonitorService(storage, fetcher, notifier, config)
    app_service = MonitoringAppService(storage, monitor_service)

    if args.command == "add":
        cmd_add(app_service, args)
        return
    if args.command == "list":
        cmd_list(app_service)
        return
    if args.command == "remove":
        cmd_remove(app_service, args.id)
        return
    if args.command == "history":
        cmd_history(app_service, args.limit)
        return

    if args.command == "run":
        interval = args.interval if args.interval is not None else config.check_interval_seconds
        cmd_run(app_service, interval=interval, once=args.once)


if __name__ == "__main__":
    main()
