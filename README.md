# Monitor de Vagas SIGAA UnB (Consulta e Notificação)

Projeto para monitorar abertura/alteração de vagas em turmas universitárias (SIGAA/UnB).

> **Escopo ético:** o sistema somente consulta mudanças e notifica. **Não** automatiza matrícula e não executa ações dentro do SIGAA.

## Execução local (Desktop UI - padrão)

A entrada principal para usuário final é a interface desktop em `tkinter`.

```bash
python -m desktop_app.main
```

Funcionalidades da UI:
- Lista de monitoramentos cadastrados.
- Formulário de criação/edição de monitoramento.
- Histórico recente por item selecionado.
- Controles de execução (executar ciclo, iniciar e parar monitoramento contínuo).

## CLI (opcional / compatibilidade)

A CLI antiga continua disponível em `main.py`:

```bash
python main.py --help
```

Comandos principais:
- `add`
- `list`
- `remove`
- `history`
- `run`

## Configuração

As variáveis de ambiente são carregadas via `.env` por `config.py`.
Exemplos:
- `DB_PATH`
- `CHECK_INTERVAL_SECONDS`
- `DRY_RUN`
- opções de notificação (`TELEGRAM_*`, `EMAIL_*`, `DESKTOP_NOTIFICATIONS_ENABLED`)

## Web app (opcional)

O repositório também mantém uma versão web:

- **Frontend:** Next.js + TypeScript + Tailwind + Recharts.
- **Backend:** FastAPI + SQLAlchemy + JWT + PostgreSQL.
- **Assíncrono:** Celery + Redis.
- **Infra:** Docker Compose.

Rodando com Docker:

```bash
docker compose -f infra/docker-compose.yml up --build
```

Serviços:
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs

Detalhes completos em `docs/ARCHITECTURE_WEBAPP.md`.
