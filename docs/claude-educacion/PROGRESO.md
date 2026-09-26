# Estado actual

Última actualización: 2026-09-26 19:00 (UTC-5: 14:00)
Responsable: Claude (Claude Code) — Codex pausado durante esta fase
Rama o worktree: `claude/educacion-multilenguaje` en `/home/roggrt/Documents/onelingo` (sin worktree)
Fase actual: Release educativa 2 publicada (A1 de inglés, voz por idioma, sonidos); siguiente: A2 de inglés o A1 de otro idioma
Porcentaje aproximado: fundamentos 10 idiomas 100 % (revisión nativa pendiente); inglés pre-A1+A1 100 %; currículo completo A1–C2 ≈ 20 % implementado

## Trabajando ahora

- Nada en curso. Release 1 cerrada y verificada.

## Terminado recientemente

- A1 de inglés: 29 unidades en 3 módulos (plan en PLAN_A1_INGLES.md), rutas por nivel, unidades omitibles según diagnóstico. 2026-09-26.
- Pronunciación por idioma corregida (DEC-012) y sonidos/feedback visual al estilo de la app (DEC-013). 2026-09-26.
- Release `20260926-edu-2-a1-voz` en producción. 2026-09-26.

- Auditoría con 4 agentes (A currículo, B vocabulario/situaciones, C habilidades/evaluación, D arquitectura/recorridos): `auditoria/`. 2026-09-26.
- Núcleo `lib/core/aprendizaje/` (esquema 2, estados, repaso, migración) y pantallas `lib/features/ruta/`. Pruebas `test/ruta_*`. 2026-09-26.
- Ruta f0 de 6 unidades en en, es, fr, de, pt, it, zh, ja, ko, ru (60 unidades, 75–93 vocablos y 72–93 ítems por idioma). 2026-09-26.
- Gramática inglesa: reanuda tema, marca practicados, guarda borradores. 2026-09-26.
- Release `20260926-edu-1-fundamentos` en producción. 2026-09-26.

## Siguiente paso

1. A2 de inglés (niveles 3–4) con el mismo método (esqueleto contractual + 3 agentes).
2. Banco de evaluación separado del de práctica; comprobación breve de prerrequisitos en el diagnóstico.
3. Revisión nativa de los 9 idiomas «inicial» (DEC-010) y escucha real de los sonidos nuevos (DEC-013).

## Bloqueos

- Revisión nativa: requiere hablantes nativos o docentes (decisión humana).
- Niveles 3–10 fuera de inglés siguen con banco genérico en inglés (el usuario decidió resolverlo con contenido real, no ocultarlos).

## Producción

- Versión desplegada: `20260926-edu-2-a1-voz` · `main.dart.js` `b772bd8c96388c55…` · backend `voz.ts` `fe3852934581990a…`
- Fecha: 2026-09-26 20:08 UTC
- URL: https://onelingo.hostingcuenca.com
- Estado de salud: `/api/salud` OK; `onelingo-api` online.
- Respaldo: `/var/www/onelingo/backups/20260926-edu-2-a1-voz/` (web anterior y 2 archivos de backend)
- Rollback: ver DESPLIEGUES.md (restaurar 2 archivos + pm2 restart + dos `mv`).
