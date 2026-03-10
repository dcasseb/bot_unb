# Monitor de Vagas SIGAA UnB (Consulta e Notificação)

Projeto full-stack para monitorar abertura/alteração de vagas em turmas universitárias (SIGAA/UnB) com interface web.

> **Escopo ético:** o sistema somente consulta mudanças e notifica. **Não** automatiza matrícula e não executa ações dentro do SIGAA.

## Stack

- **Frontend:** Next.js + TypeScript + Tailwind + Recharts.
- **Backend:** FastAPI + SQLAlchemy + JWT + PostgreSQL.
- **Assíncrono:** Celery + Redis.
- **Infra:** Docker Compose.

## Estrutura

```text
backend/   # API FastAPI, modelos, rotas, worker
frontend/  # App Next.js (dashboard e páginas)
infra/     # Dockerfiles e docker-compose
docs/      # Arquitetura, deploy e roadmap
```

Detalhes completos em `docs/ARCHITECTURE_WEBAPP.md`.

## Rodando com Docker

```bash
docker compose -f infra/docker-compose.yml up --build
```

Serviços:
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs

## Principais páginas

- `/login`
- `/register`
- `/dashboard`
- `/monitoramentos`
- `/monitoramentos/novo`
- `/monitoramentos/[id]`
- `/notificacoes`
- `/configuracoes`

## API principal

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET/POST /api/monitorings`
- `PATCH/DELETE /api/monitorings/{id}`
- `GET /api/monitorings/{id}/history`
- `GET /api/notifications`
- `WS /ws?token=...`

## Melhorias planejadas

- Recuperação de senha.
- Preferências avançadas de notificação por usuário.
- Push notifications no navegador.
- Observabilidade e métricas (Prometheus/Grafana).
- Testes automatizados de integração e E2E.
