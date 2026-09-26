# Estado actual

Última actualización: 2026-09-26 19:00 (UTC-5: 14:00)
Responsable: Claude (Claude Code) — Codex pausado durante esta fase
Rama o worktree: `claude/educacion-multilenguaje` en `/home/roggrt/Documents/onelingo` (sin worktree)
Fase actual: Release educativa 3 lista (escrituras completas + A1 «Primeras frases» ×10, recompensa, repetición de fallos); despliegue pendiente de acceso SSH
Porcentaje aproximado: fundamentos 10 idiomas completos (escritura/sonidos) · A1 inicial 10 idiomas · inglés A1 completo · currículo A1–C2 ≈ 25 %

## Trabajando ahora

- Nada en curso. Release 1 cerrada y verificada.

## Terminado recientemente

- Escrituras/sonidos completos y A1 «Primeras frases» en 10 idiomas (204 unidades), paso `tabla` (DEC-015). 2026-09-26.
- Fallo en práctica ya no bloquea: repetición al final del bloque (DEC-014). 2026-09-26.
- Celebración al completar unidad/nivel y precarga de fuentes CJK en web (DEC-016). 2026-09-26.

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

- SSH a 167.235.20.41 sin respuesta desde ~2026-09-26 21:10 UTC (HTTPS OK). Causa probable: bloqueo temporal por número de conexiones (fail2ban). Acción: reintento automático; si persiste, revisar el firewall del servidor.
- Revisión nativa de 9 idiomas (decisión humana).

## Producción

- Versión desplegada: `20260926-edu-2-a1-voz` · `main.dart.js` `b772bd8c96388c55…` · backend `voz.ts` `fe3852934581990a…`
- Fecha: 2026-09-26 20:08 UTC
- URL: https://onelingo.hostingcuenca.com
- Estado de salud: `/api/salud` OK; `onelingo-api` online.
- Respaldo: `/var/www/onelingo/backups/20260926-edu-2-a1-voz/` (web anterior y 2 archivos de backend)
- Rollback: ver DESPLIEGUES.md (restaurar 2 archivos + pm2 restart + dos `mv`).
