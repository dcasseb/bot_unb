from __future__ import annotations

import logging
import tkinter as tk
from queue import Empty, Queue
from tkinter import messagebox, ttk

from app_services import AddClassInput, MonitoringAppService
from config import load_config
from desktop_app.monitor_controller import MonitorController, MonitorEvent
from monitor import MonitorService, SIGAAFetcher
from notifier import NotifierHub
from storage import MonitoredClass, Storage

logger = logging.getLogger(__name__)


class DesktopApp:
    def __init__(self, root: tk.Tk, service: MonitoringAppService, interval: int) -> None:
        self.root = root
        self.service = service
        self.interval = interval
        self.selected_class_id: int | None = None
        self.monitor_events: Queue[MonitorEvent] = Queue()
        self.monitor_controller = MonitorController(service, self.monitor_events)

        self.root.title("SIGAA UnB Monitor")
        self.root.geometry("1200x700")
        self._build_ui()
        self.refresh_classes()
        self._poll_monitor_events()

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(1, weight=1)

        controls = ttk.Frame(self.root, padding=10)
        controls.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.run_status = tk.StringVar(value="Parado")
        ttk.Label(controls, text="Monitoramento:").pack(side="left")
        ttk.Label(controls, textvariable=self.run_status).pack(side="left", padx=(6, 20))
        ttk.Button(controls, text="Executar ciclo", command=self.run_once).pack(side="left", padx=4)
        ttk.Button(controls, text="Iniciar", command=self.start_monitoring).pack(side="left", padx=4)
        ttk.Button(controls, text="Parar", command=self.stop_monitoring).pack(side="left", padx=4)

        table_frame = ttk.LabelFrame(self.root, text="Monitoramentos", padding=10)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ("id", "code", "name", "group", "term", "campus")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        labels = {
            "id": "ID",
            "code": "Código",
            "name": "Nome",
            "group": "Turma",
            "term": "Período",
            "campus": "Campus",
        }
        for col in columns:
            self.tree.heading(col, text=labels[col])
            self.tree.column(col, stretch=True, width=120)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select_class)

        form_frame = ttk.LabelFrame(self.root, text="Criar / Editar", padding=10)
        form_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        form_frame.columnconfigure(1, weight=1)

        self.fields: dict[str, tk.StringVar] = {}
        form_specs = [
            ("id", "ID (edição)"),
            ("code", "Código"),
            ("name", "Nome"),
            ("class_group", "Turma"),
            ("term", "Período"),
            ("campus", "Campus"),
            ("query_url", "URL de consulta"),
        ]
        for row, (field, label) in enumerate(form_specs):
            var = tk.StringVar()
            self.fields[field] = var
            ttk.Label(form_frame, text=label).grid(row=row, column=0, sticky="w", pady=4)
            ttk.Entry(form_frame, textvariable=var).grid(row=row, column=1, sticky="ew", pady=4)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(form_specs), column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Button(btn_frame, text="Salvar (novo)", command=self.save_class).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Remover selecionado", command=self.remove_selected).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_form).pack(side="left", padx=4)

        history_frame = ttk.LabelFrame(self.root, text="Histórico recente do item", padding=10)
        history_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        history_frame.rowconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)

        hist_columns = ("observed_at", "status", "available", "changed", "summary")
        self.history_tree = ttk.Treeview(history_frame, columns=hist_columns, show="headings")
        hist_labels = {
            "observed_at": "Observado em",
            "status": "Status",
            "available": "Vagas",
            "changed": "Mudou?",
            "summary": "Resumo",
        }
        for col in hist_columns:
            self.history_tree.heading(col, text=hist_labels[col])
            self.history_tree.column(col, stretch=True, width=180)
        self.history_tree.grid(row=0, column=0, sticky="nsew")

    def refresh_classes(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.service.list_classes():
            self.tree.insert(
                "",
                "end",
                iid=str(item.id),
                values=(item.id, item.code, item.name or "-", item.class_group, item.term, item.campus or "-"),
            )

    def on_select_class(self, _: object = None) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        class_id = int(selected[0])
        self.selected_class_id = class_id
        monitored_class = next((c for c in self.service.list_classes() if c.id == class_id), None)
        if monitored_class is None:
            return

        self.fields["id"].set(str(monitored_class.id))
        self.fields["code"].set(monitored_class.code)
        self.fields["name"].set(monitored_class.name or "")
        self.fields["class_group"].set(monitored_class.class_group)
        self.fields["term"].set(monitored_class.term)
        self.fields["campus"].set(monitored_class.campus or "")
        self.fields["query_url"].set(monitored_class.query_url)

        self.refresh_history(class_id)

    def refresh_history(self, class_id: int) -> None:
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        for row in self.service.history_for_class(class_id, limit=25):
            self.history_tree.insert(
                "",
                "end",
                values=(
                    row["observed_at"],
                    row["status"],
                    row["available_seats"],
                    "Sim" if row["changed"] else "Não",
                    row["change_summary"] or "-",
                ),
            )

    def save_class(self) -> None:
        payload = AddClassInput(
            code=self.fields["code"].get().strip(),
            name=self.fields["name"].get().strip() or None,
            class_group=self.fields["class_group"].get().strip(),
            term=self.fields["term"].get().strip(),
            campus=self.fields["campus"].get().strip() or None,
            query_url=self.fields["query_url"].get().strip(),
        )
        if not payload.code or not payload.class_group or not payload.term or not payload.query_url:
            messagebox.showerror("Campos obrigatórios", "Preencha código, turma, período e URL.")
            return

        existing_id = self.fields["id"].get().strip()
        if existing_id:
            self.service.remove_class(int(existing_id))
        class_id = self.service.add_class(payload)
        self.refresh_classes()
        self.fields["id"].set(str(class_id))
        messagebox.showinfo("Sucesso", f"Monitoramento salvo com ID {class_id}.")

    def remove_selected(self) -> None:
        if self.selected_class_id is None:
            messagebox.showwarning("Seleção", "Selecione um monitoramento para remover.")
            return
        if self.service.remove_class(self.selected_class_id):
            self.refresh_classes()
            self.clear_form()

    def clear_form(self) -> None:
        self.selected_class_id = None
        for var in self.fields.values():
            var.set("")
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

    def run_once(self) -> None:
        summary = self.service.run_cycle()
        if summary["checked"] == 0:
            messagebox.showinfo("Execução", "Nenhuma turma cadastrada para monitoramento.")
        else:
            messagebox.showinfo(
                "Execução",
                f"Ciclo concluído. Itens verificados: {summary['checked']} | erros: {summary['errors']}",
            )
        if self.selected_class_id is not None:
            self.refresh_history(self.selected_class_id)

    def start_monitoring(self) -> None:
        if self.monitor_controller.is_running:
            return
        self.run_status.set("Em execução")
        self.monitor_controller.start(interval=self.interval)

    def stop_monitoring(self) -> None:
        if not self.monitor_controller.is_running:
            return
        self.monitor_controller.stop()

    def _poll_monitor_events(self) -> None:
        while True:
            try:
                event = self.monitor_events.get_nowait()
            except Empty:
                break

            if event.event_type == "cycle_result":
                if self.selected_class_id is not None:
                    self.refresh_history(self.selected_class_id)
            elif event.event_type == "cycle_error":
                logger.error("Erro no ciclo de monitoramento: %s", event.payload)
            elif event.event_type == "stopped":
                self.run_status.set("Parado")

        self.root.after(250, self._poll_monitor_events)


def build_desktop_service() -> tuple[MonitoringAppService, int]:
    config = load_config()
    storage = Storage(config.db_path)
    storage.init_db()
    fetcher = SIGAAFetcher(config)
    notifier = NotifierHub(config)
    monitor_service = MonitorService(storage, fetcher, notifier, config)
    return MonitoringAppService(storage, monitor_service), config.check_interval_seconds


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    service, interval = build_desktop_service()
    root = tk.Tk()
    app = DesktopApp(root, service, interval=interval)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_monitoring(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
