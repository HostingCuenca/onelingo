#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FLUTTER_BIN="${ONELINGO_FLUTTER:-/home/roggrt/flutter/bin/flutter}"
export CI=true
# Evita depender del directorio global del daemon Kotlin en entornos aislados.
export GRADLE_OPTS="${GRADLE_OPTS:-} -Dorg.gradle.project.kotlin.compiler.execution.strategy=in-process"
cd "$PROJECT_ROOT"
case "${1:-help}" in
  db)
    if docker container inspect onelingo-local-db >/dev/null 2>&1; then
      docker start onelingo-local-db
    else
      docker run -d --name onelingo-local-db --restart unless-stopped \
        --env-file "$PROJECT_ROOT/work/local/db.env" \
        -p 127.0.0.1:55432:5432 \
        -v onelingo-local-pgdata:/var/lib/postgresql/data postgres:17
    fi
    ;;
  backend) cd backend; exec npm run dev ;;
  panel) cd panel; exec npm run dev -- --strictPort ;;
  web) exec "$FLUTTER_BIN" --suppress-analytics run -d web-server --web-hostname 127.0.0.1 --web-port "${ONELINGO_WEB_PORT:-8088}" --dart-define=API_URL=http://localhost:8091 ;;
  android)
    : "${2:?Indica el identificador de adb, por ejemplo emulator-5556}"
    exec "$FLUTTER_BIN" --suppress-analytics run -d "$2" --dart-define=API_URL=http://10.0.2.2:8091
    ;;
  check)
    docker exec onelingo-local-db pg_isready -U onelingo -d onelingo
    curl -fsS http://127.0.0.1:8091/salud
    curl -fsS http://127.0.0.1:5176/api/salud
    curl -fsS -o /dev/null -w 'Web HTTP %{http_code}\n' "http://127.0.0.1:${ONELINGO_WEB_PORT:-8088}"
    ;;
  *) printf '%s\n' 'Usa: tools/dev-local.sh db|backend|panel|web|android <device>|check' ;;
esac
