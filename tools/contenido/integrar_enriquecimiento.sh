#!/usr/bin/env bash
# Integra los archivos de enriquecimiento con GO: compila el runtime y exige
# 0 errores en ambos validadores y pruebas de ruta en verde. Sale con error
# si algo falla (no se debe hacer commit en ese caso).
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 tools/contenido/validar_enriquecimiento.py > /tmp/onelingo-enriq.txt || { grep ERROR /tmp/onelingo-enriq.txt; echo "Enriquecimiento con errores (los borradores sin GO no se integran, pero deben corregirse)"; }
python3 tools/contenido/generar_runtime_n1.py
salida=$(python3 tools/validar_ruta.py || true)
echo "$salida" | tail -1
echo "$salida" | tail -1 | grep -q "· 0 error(es)" || { echo "$salida" | grep '^\[' | head -20; exit 1; }
~/flutter/bin/flutter test --no-pub test/ruta_contenido_test.dart test/ruta_recorrido_test.dart test/simulacion_estudiantes_test.dart test/pulido_ruta_test.dart
python3 - <<'PY'
import json, glob
go = sum(len(json.load(open(f))["classes"]) for f in glob.glob("assets/contenido/en/editorial/n*/enriquecimiento-*.json")
         if json.load(open(f)).get("review", {}).get("status") == "GO")
import sys
sys.path.insert(0, "tools/contenido")
import generar_runtime_n1 as c
total = sum(spec["count"] for spec in c.LEVELS)
print(f"Clases enriquecidas con GO: {go} · clases publicadas: {total}")
PY
