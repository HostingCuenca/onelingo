#!/bin/bash
# Corte de OneLingo: Hetzner (167.235.20.41) → VPS Hostinger (179.197.89.105, `ssh onelingo`).
# Se corre desde la máquina de Torisoftt. Deja la API vieja parada, la base y los
# audios copiados al VPS y el puente de Hetzner reenviando al VPS mientras cambia el DNS.
# Vuelta atrás (antes de cambiar el DNS): ./corte.sh atras
set -euo pipefail
VIEJO=(ssh root@167.235.20.41)
NUEVO=(ssh onelingo)
AQUI=$(cd "$(dirname "$0")" && pwd)
TMP=${TMPDIR:-/tmp}/onelingo-corte; mkdir -p "$TMP"
R=(--resolve onelingo.org:443:179.197.89.105)

if [ "${1:-}" = atras ]; then
  "${VIEJO[@]}" 'pm2 delete onelingo-puente 2>/dev/null; pm2 start onelingo-api && rm -f /tmp/onelingo-deploy.lock'
  echo "Hetzner vuelve a atender con su base (lo escrito en el VPS después del corte no está ahí)."; exit 0
fi

"${VIEJO[@]}" 'set -e; [ ! -e /tmp/onelingo-deploy.lock ] || { cat /tmp/onelingo-deploy.lock; exit 1; }; echo "corte claude $(date -Is)" > /tmp/onelingo-deploy.lock'
# El código y la web tienen que ser los mismos en los dos lados.
huella='cd /var/www/onelingo && export LC_ALL=C && { sha256sum web/main.dart.js web/version.json; find backend/src backend/sql panel -type f -print0 | sort -z | xargs -0 sha256sum; } | sha256sum'
[ "$("${VIEJO[@]}" "$huella")" = "$("${NUEVO[@]}" "$huella")" ] || { echo "web/backend/panel difieren: sincronizar antes"; "${VIEJO[@]}" 'rm -f /tmp/onelingo-deploy.lock'; exit 1; }

echo "== API vieja parada (empieza la pausa)"; date
"${VIEJO[@]}" 'pm2 stop onelingo-api >/dev/null'
"${VIEJO[@]}" 'sudo -u postgres pg_dump -Fc onelingo' > "$TMP/hetzner-corte.dump"
"${NUEVO[@]}" 'sudo -u onelingo -H pm2 stop onelingo-api >/dev/null; cat > /var/backups/onelingo/hetzner-corte.dump' < "$TMP/hetzner-corte.dump"
"${NUEVO[@]}" 'set -e; cd /tmp; sudo -u postgres dropdb onelingo; sudo -u postgres createdb -O onelingo -E UTF8 --locale=en_US.UTF-8 -T template0 onelingo
  sudo -u postgres pg_restore --no-owner --role=onelingo -d onelingo < /var/backups/onelingo/hetzner-corte.dump'
conteo='cd /tmp; for t in usuarios progreso suscripciones; do printf "%s=" $t; sudo -u postgres psql -d onelingo -Atc "select count(*) from $t" 2>/dev/null || echo -; done | tr "\n" " "'
v=$("${VIEJO[@]}" "$conteo"); n=$("${NUEVO[@]}" "$conteo"); echo "Hetzner: $v"; echo "VPS:     $n"
[ "$v" = "$n" ] || { echo "Los conteos no cuadran: revisar antes de seguir (./corte.sh atras)"; exit 1; }

echo "== Audios"
rsync -a root@167.235.20.41:/var/www/onelingo/audio/ "$TMP/audio/"
rsync -a "$TMP/audio/" onelingo:/var/www/onelingo/audio/
"${NUEVO[@]}" 'chown -R onelingo:onelingo /var/www/onelingo/audio && sudo -u onelingo -H pm2 start onelingo-api >/dev/null && sleep 5 && curl -fsS http://127.0.0.1:8091/salud'; echo

echo "== Puente en Hetzner"
scp -q "$AQUI/puente.mjs" root@167.235.20.41:/var/www/onelingo/puente.mjs
"${VIEJO[@]}" 'cd /var/www/onelingo && pm2 start puente.mjs --name onelingo-puente >/dev/null && pm2 save >/dev/null && sleep 2 && curl -fsS http://127.0.0.1:8091/salud'; echo
date; echo "== Fin de la pausa. Comprobaciones:"
for p in /api/salud /api/planes /; do printf '%-14s Hetzner %s · VPS %s\n' $p \
  "$(curl -s -o /dev/null -w '%{http_code}' https://onelingo.org$p --resolve onelingo.org:443:167.235.20.41)" \
  "$(curl -s -o /dev/null -w '%{http_code}' "${R[@]}" https://onelingo.org$p)"; done
echo "Siguiente: registros A de onelingo.org y www → 179.197.89.105 (Porkbun) y onelingo.hostingcuenca.com (Cloudflare)."
echo "El lock de Hetzner queda puesto: no desplegar ahí."
