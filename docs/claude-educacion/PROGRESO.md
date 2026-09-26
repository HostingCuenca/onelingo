# Estado actual

Última actualización: 2026-09-26 19:00 (UTC-5: 14:00)
Responsable: Claude (Claude Code) — Codex pausado durante esta fase
Rama o worktree: `claude/educacion-multilenguaje` en `/home/roggrt/Documents/onelingo` (sin worktree)
Fase actual: Release educativa 1 publicada; siguiente: A1 de inglés en esquema 2
Porcentaje aproximado: fundamentos multilingües 100 % (pendiente revisión nativa); currículo completo A1–C2 ≈ 10 % implementado

## Trabajando ahora

- Nada en curso. Release 1 cerrada y verificada.

## Terminado recientemente

- Auditoría con 4 agentes (A currículo, B vocabulario/situaciones, C habilidades/evaluación, D arquitectura/recorridos): `auditoria/`. 2026-09-26.
- Núcleo `lib/core/aprendizaje/` (esquema 2, estados, repaso, migración) y pantallas `lib/features/ruta/`. Pruebas `test/ruta_*`. 2026-09-26.
- Ruta f0 de 6 unidades en en, es, fr, de, pt, it, zh, ja, ko, ru (60 unidades, 75–93 vocablos y 72–93 ítems por idioma). 2026-09-26.
- Gramática inglesa: reanuda tema, marca practicados, guarda borradores. 2026-09-26.
- Release `20260926-edu-1-fundamentos` en producción. 2026-09-26.

## Siguiente paso

1. Migrar A1 de inglés (niveles 1–2) al esquema 2 con los nodos `en-g-*` de A1 y alias de las guías actuales.
2. Banco de evaluación separado del de práctica para las unidades f0.
3. Revisión nativa de los 9 idiomas «inicial» (DEC-010).

## Bloqueos

- Revisión nativa: requiere hablantes nativos o docentes (decisión humana).
- Niveles 3–10 fuera de inglés siguen con banco genérico en inglés (el usuario decidió resolverlo con contenido real, no ocultarlos).

## Producción

- Versión desplegada: `20260926-edu-1-fundamentos` · `main.dart.js` `ffefcc975f280e73…`
- Fecha: 2026-09-26 18:56 UTC
- URL: https://onelingo.hostingcuenca.com
- Estado de salud: `/api/salud` OK; `onelingo-api` online.
- Respaldo: `/var/www/onelingo/backups/20260926-edu-1-fundamentos/web-anterior`
- Rollback: ver DESPLIEGUES.md (dos `mv`).
