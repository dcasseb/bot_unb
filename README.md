# Monitor de Vagas SIGAA UnB (Consulta e Notificação)

Projeto para monitorar abertura/alteração de vagas em turmas universitárias (SIGAA/UnB).

> **Escopo ético:** o sistema somente consulta mudanças e notifica. **Não** automatiza matrícula e não executa ações dentro do SIGAA.

## Modo principal: Desktop/Local

O fluxo recomendado para uso diário é a aplicação desktop (Tkinter), rodando localmente no seu computador.

### Instalação local

1. **Clone o repositório** e entre na pasta do projeto.
2. **Crie e ative um ambiente virtual (`venv`)**.
3. **Instale as dependências**.
4. **Configure o `.env`** com os parâmetros desejados.
5. **Execute a interface desktop**.

Exemplo (Linux/macOS):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m desktop_app.main
```

Exemplo (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m desktop_app.main
```

Funcionalidades da UI:
- Lista de monitoramentos cadastrados.
- Formulário de criação/edição de monitoramento.
- Histórico recente por item selecionado.
- Controles de execução (executar ciclo, iniciar e parar monitoramento contínuo).

## Empacotamento desktop com PyInstaller

Foi adicionado um fluxo explícito para gerar um executável da interface desktop (`desktop_app/main.py`) com PyInstaller.

### Pré-requisitos

- Ambiente virtual ativo.
- Dependências do projeto instaladas (`pip install -r requirements.txt`).
- PyInstaller instalado no ambiente (`pip install pyinstaller`).

### Build do binário

Use o script versionado:

```bash
./scripts/build_desktop.sh
```

Esse script executa o PyInstaller com o arquivo de especificação `desktop_app/SIGAAUnBMonitor.spec` e gera o binário em `dist/SIGAAUnBMonitor`.

### Arquivo `.spec` versionado

O arquivo `desktop_app/SIGAAUnBMonitor.spec` define:

- Nome do executável: `SIGAAUnBMonitor`.
- Inclusão de dados necessários no build (`.env.example`).
- Build em modo janela (`console=False`), adequado para Tkinter (`--windowed`).

### Execução do binário gerado

Após o build, execute:

```bash
./dist/SIGAAUnBMonitor
```

No Windows, o executável correspondente será gerado com extensão `.exe` no diretório `dist`.

## Configuração local (`.env`)

As variáveis de ambiente são carregadas automaticamente via `python-dotenv` em `config.py`.

### Banco local
- `DB_PATH`: caminho do arquivo SQLite usado para persistir monitoramentos/histórico.
  - Exemplo: `DB_PATH=monitor.db`

### Intervalo e comportamento de execução
- `CHECK_INTERVAL_SECONDS`: intervalo (em segundos) entre ciclos no modo contínuo.
- `REQUEST_TIMEOUT_SECONDS`: timeout de chamadas HTTP.
- `MAX_RETRIES`: número de tentativas em falhas transitórias.
- `BACKOFF_SECONDS`: espera base entre tentativas.
- `DRY_RUN`: quando `true`, suprime envio real de notificações externas.

### Notificações
- Desktop:
  - `DESKTOP_NOTIFICATIONS_ENABLED=true|false`
- Telegram:
  - `TELEGRAM_ENABLED`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- E-mail (SMTP):
  - `EMAIL_ENABLED`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM`, `SMTP_TO`, `SMTP_USE_TLS`

## Troubleshooting de notificações desktop

### Linux
- Erro comum: nada acontece ao disparar notificação desktop.
- Verifique se o utilitário `notify-send` está instalado e no PATH:
  ```bash
  which notify-send
  ```
- Em distribuições Debian/Ubuntu, instale via:
  ```bash
  sudo apt install libnotify-bin
  ```
- Em sessões sem servidor gráfico (headless/WSL sem GUI), notificações desktop podem não aparecer.

### Windows
- O backend desktop usa a biblioteca `win10toast` para toast notifications.
- Se aparecer aviso de biblioteca ausente, instale manualmente no ambiente virtual:
  ```powershell
  pip install win10toast
  ```
- Confirme se as notificações do sistema estão habilitadas em **Configurações > Sistema > Notificações**.

## CLI (opcional / compatibilidade)

A CLI continua disponível para uso avançado/compatibilidade:

```bash
python main.py --help
```

Comandos principais:
- `add`
- `list`
- `remove`
- `history`
- `run`

## Arquitetura web (legado/opcional)

A arquitetura web (frontend Next.js + backend FastAPI + workers + Docker Compose) permanece no repositório como opção secundária/histórica.

Consulte a documentação dedicada em:

- `docs/ARCHITECTURE_WEBAPP.md`

Para subir a stack web com Docker:

```bash
docker compose -f infra/docker-compose.yml up --build
```
