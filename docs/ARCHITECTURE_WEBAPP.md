# Arquitetura Web App - Monitor de Vagas UnB

## Visão geral

Arquitetura em 3 camadas:

1. **Frontend (Next.js + TypeScript)**: interface web, dashboard, CRUD de monitoramentos, histórico e notificações.
2. **API (FastAPI + SQLAlchemy + PostgreSQL)**: autenticação JWT, regras de negócio, persistência de monitoramentos/estados/notificações.
3. **Workers (Celery + Redis)**: varredura assíncrona das turmas, detecção de mudança, criação de eventos de notificação.

Fluxo principal:

`Usuário cria monitoramento -> API persiste -> Worker verifica SIGAA periodicamente -> salva estado -> detecta mudança -> cria notificação -> frontend lê atualizações`.

> Escopo ético: o sistema apenas consulta disponibilidade e envia alertas. Não automatiza matrícula.

## Estrutura de pastas

```text
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
    workers/
    main.py
  requirements.txt
frontend/
  src/app/
  src/components/
  src/lib/
  package.json
infra/
  docker-compose.yml
  backend.Dockerfile
  frontend.Dockerfile
docs/
  ARCHITECTURE_WEBAPP.md
```

## Modelo de dados

- `users`: id, email, password_hash, created_at.
- `monitorings`: id, user_id, discipline_code, discipline_name, class_group, semester, check_interval_seconds, query_url, active, timestamps.
- `class_states`: id, monitoring_id, total_seats, occupied_seats, available_seats, status, observed_at.
- `notifications`: id, user_id, type (telegram/email/browser), message, sent, created_at.

## Endpoints (MVP)

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/monitorings`
- `POST /api/monitorings`
- `PATCH /api/monitorings/{id}`
- `DELETE /api/monitorings/{id}`
- `GET /api/monitorings/{id}/history`
- `GET /api/notifications`
- `GET /health`
- `WS /ws?token=...`

## Notificações

- Notificação persistida em `notifications`.
- Canais planejados: Telegram, e-mail e browser push.
- Em tempo real: endpoint WebSocket (`/ws`) para consumo de eventos no dashboard.

## Deploy

1. Ajustar variáveis `.env` (segredo JWT, URLs, SMTP/Telegram).
2. Subir serviços:
   - `docker compose -f infra/docker-compose.yml up --build -d`
3. Rodar migrações (ou `Base.metadata.create_all` no MVP).
4. Configurar HTTPS (Nginx + certbot) para produção.
5. Escalar workers com múltiplas réplicas Celery e filas por prioridade.

## Melhorias futuras

- Fluxo de recuperação de senha com token e e-mail.
- Alertas inteligentes (ex.: alertar somente quando vagas_livres > 0).
- Preferências por disciplina/canal e janelas de silêncio.
- Observabilidade (OpenTelemetry + Prometheus + Grafana).
- Notificações push (Web Push API).
- Testes E2E (Playwright) e CI/CD.
