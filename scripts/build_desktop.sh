#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPEC_FILE="$ROOT_DIR/desktop_app/SIGAAUnBMonitor.spec"

cd "$ROOT_DIR"

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller não encontrado no PATH. Instale com: pip install pyinstaller"
  exit 1
fi

pyinstaller --noconfirm --clean "$SPEC_FILE"

echo "Build concluído. Binário disponível em: dist/SIGAAUnBMonitor"
