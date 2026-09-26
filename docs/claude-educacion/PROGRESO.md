# Estado actual

Última actualización: 2026-09-26
Responsable: Claude (Claude Code) — Codex pausado durante esta fase
Rama o worktree: `claude/educacion-multilenguaje` en `/home/roggrt/Documents/onelingo` (sin worktree; Codex no escribe)
Fase actual: Fase 1 — Auditoría (4 agentes en paralelo)
Porcentaje aproximado: 5 %

## Trabajando ahora

- Tarea: auditoría curricular, vocabulario/situaciones, habilidades/evaluación y arquitectura/recorridos.
- Archivos: `docs/claude-educacion/auditoria/{A,B,C,D}-*.md` (un propietario por archivo, solo lectura del código).
- Resultado esperado: inventario real, brechas con evidencia, grafo, esquema común, modelo de dominio y migración de foundations-v1.
- Terminada cuando: los 4 informes existen y están consolidados en MAPA_CURRICULAR, COBERTURA, IDIOMAS, ESQUEMA_CONTENIDO y MIGRACION_FUNDAMENTOS.

## Terminado recientemente

- Checkpoint completo: rama `checkpoint/onelingo-before-multilang-2026-09-26`, commit `396333b`, tag `checkpoint-2026-09-26-pre-multilang` (314 archivos, sin `.env`/build/node_modules). 2026-09-26.
- Inventario de idiomas: 10 habilitados (`lib/core/content/curriculum.dart:11`). Ver IDIOMAS.md. 2026-09-26.
- El checkpoint reproduce producción exactamente: `main.dart.js` compilado = publicado (`caa2e8a452cf3de8…`) y 8 assets del home idénticos. 2026-09-26.

## Siguiente paso

1. Consolidar los 4 informes en los documentos maestros.
2. Implementar la estructura común (`lib/core/aprendizaje/`) con pruebas del grafo.
3. Ruta inicial de inglés como referencia; luego las otras 9.

## Bloqueos

- Ninguno técnico.
- Pendiente de decisión humana: destinatario del curso de español (la interfaz está solo en español). Ver DECISIONES DEC-004.

## Producción

- Versión desplegada: `home-layout17-assets` (desplegada por Codex, 2026-09-25 19:35 UTC). `main.dart.js` sha256 `caa2e8a452cf3de8…`.
- URL: https://onelingo.hostingcuenca.com
- Estado de salud: `/api/salud` OK (2026-09-26).
- Respaldo más reciente del servidor: `/var/www/onelingo/backups/home-layout17-assets-20260925T193557Z`.
- Rollback: restaurar `web/` desde el respaldo del release anterior (ver DESPLIEGUES.md). Ningún despliegue de esta fase todavía.
