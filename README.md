# Monitor de Vagas SIGAA UnB (Somente Consulta)

Projeto em Python para monitorar turmas/disciplina no SIGAA da UnB e emitir alertas quando houver alteração de estado (ex.: abertura de vaga).

## Aviso ético e escopo

Este projeto foi desenhado para **consulta e notificação apenas**.

- Não automatiza matrícula.
- Não faz submissão de formulários.
- Não tenta burlar autenticação, CAPTCHA ou MFA.
- Não contorna bloqueios do sistema.

Use intervalos de checagem razoáveis para respeitar o serviço.

## Arquitetura

- `main.py`: CLI com comandos de cadastro/listagem/remoção/execução/histórico.
- `config.py`: carregamento de variáveis de ambiente (`.env`).
- `monitor.py`: busca da página, parsing, comparação de estados, decisão de alerta.
- `parser.py`: extração dos campos do HTML (ajustável a seletores reais do SIGAA).
- `storage.py`: persistência SQLite (turmas, último estado, histórico).
- `notifier.py`: notificações por console, Telegram, e-mail e desktop.
- `utils.py`: retry com backoff simples.

## Pré-requisitos

- Python 3.11+

## Instalação

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
```

## Configuração

Edite `.env` conforme necessidade.

Principais variáveis:

- `SIGAA_BASE_URL`: URL base do SIGAA (referência).
- `CHECK_INTERVAL_SECONDS`: intervalo entre verificações.
- `REQUEST_TIMEOUT_SECONDS`: timeout de requisição HTTP.
- `MAX_RETRIES` e `BACKOFF_SECONDS`: retentativas em falhas temporárias.
- `DRY_RUN=true|false`: com `true`, notificações externas são suprimidas.

### Notificações opcionais

- Telegram: habilite `TELEGRAM_ENABLED=true` e preencha token/chat id.
- E-mail: habilite `EMAIL_ENABLED=true` e configure SMTP.
- Desktop: `DESKTOP_NOTIFICATIONS_ENABLED=true`.

## Ajuste do parser para o HTML real do SIGAA

O arquivo `parser.py` usa seletores fictícios:

- `#total-vagas`
- `#vagas-ocupadas`
- `#vagas-disponiveis`
- `.status-turma`

Você deve abrir a página real da turma e ajustar esses seletores para os elementos corretos.

## Uso da CLI

Adicionar turma:

```bash
python main.py add \
  --code CIC0001 \
  --name "Algoritmos" \
  --class-group A \
  --term 2026.1 \
  --campus Darcy \
  --url "https://sigaa.unb.br/.../consulta_turma?id=123"
```

Listar:

```bash
python main.py list
```

Remover:

```bash
python main.py remove --id 1
```

Rodar um ciclo de verificação:

```bash
python main.py run --once
```

Rodar continuamente (com intervalo customizado):

```bash
python main.py run --interval 90
```

Histórico recente:

```bash
python main.py history --limit 30
```

## Exemplo de execução

```text
$ python main.py run --once
2026-03-10 10:00:00 | INFO | monitor | total_seats: 40 -> 45; available_seats: 0 -> 5. Estado atual: {'total_seats': 45, 'occupied_seats': 40, 'available_seats': 5, 'status': 'ABERTA'}
[DRY-RUN] Mudança detectada: CIC0001 TA: total_seats: 40 -> 45; available_seats: 0 -> 5. Estado atual: {'total_seats': 45, 'occupied_seats': 40, 'available_seats': 5, 'status': 'ABERTA'}
```

## Melhorias futuras

- Exportação de histórico para CSV.
- Interface web simples para gerenciamento das turmas.
- Regras avançadas de alerta (ex.: só avisar quando `available_seats > 0`).
- Testes automatizados (unit + integração com HTML mockado).
- Suporte opcional a Playwright **somente para leitura** em páginas que exigem renderização JS.
