# Checklist — educación multilingüe

Leyenda: `[ ]` pendiente · `[~]` en curso · `[x]` terminado · `[!]` bloqueado

## Fase 0 — Preparación
- [x] Crear checkpoint completo (`396333b`, tag `checkpoint-2026-09-26-pre-multilang`).
- [x] Crear rama `claude/educacion-multilenguaje`.
- [x] Verificar que el checkpoint no contiene `.env` ni secretos.
- [x] Comparar assets del home con producción (8/8 idénticos).
- [x] Comparar `main.dart.js` del checkpoint con producción: idéntico (sha256 `caa2e8a452cf3de8…`).
- [x] Crear `docs/claude-educacion/` con los archivos de seguimiento.

## Fase 1 — Auditoría
- [x] Inventariar idiomas habilitados (10).
- [~] Agente A: inventario curricular, grafo gramatical inglés, sistemas lingüísticos y rutas por idioma.
- [~] Agente B: vocabulario, 50 situaciones, adaptación multilingüe, sistema de repaso.
- [~] Agente C: tipos de actividad, habilidades, diagnóstico, evaluación, certificaciones.
- [~] Agente D: mapa técnico, acoplamiento a inglés, progreso, bug de gramática, esquema, migración, recorridos.
- [ ] Consolidar MAPA_CURRICULAR.md.
- [ ] Consolidar COBERTURA.md.
- [ ] Completar IDIOMAS.md con estados por idioma.
- [ ] Redactar ESQUEMA_CONTENIDO.md.
- [ ] Redactar MIGRACION_FUNDAMENTOS.md.

## Fase 2 — Fundamentos
- [ ] Implementar modelos comunes de ruta (`lib/core/aprendizaje/`).
- [ ] Implementar grafo de prerrequisitos con validación (sin ciclos, IDs existentes).
- [ ] Implementar estados de unidad y desbloqueo.
- [ ] Implementar migración de foundations-v1 sin pérdida de progreso.
- [ ] Ruta inicial de inglés (U0–U5) en datos.
- [ ] Rutas iniciales de fr, de, pt, it.
- [ ] Rutas iniciales de zh, ja, ko, ru (con fase de escritura/sonidos).
- [ ] Ruta inicial de es (según DEC-004).
- [ ] Pantalla de ruta conectada desde Aprender (sin tocar el home).
- [ ] Verificar persistencia al cerrar y reabrir la app.

## Fase 3 — Gramática
- [ ] Verificar bug «gramática desaparece tras entrenar» con evidencia.
- [ ] Corregir el bug si sigue ocurriendo, con prueba de regresión.
- [ ] Vincular guías de gramática inglesa existentes a IDs del grafo.

## Fase 4 — Vocabulario
- [ ] Estados de vocabulario (visto → dominado) en el modelo.
- [ ] Vocabulario inicial por idioma enlazado a unidades.

## Fase 5 — Situaciones
- [ ] Plantilla de situación como mini-ruta en el esquema.
- [ ] Mapa de las 50 situaciones con nivel y gramática requerida.

## Fase 6 — Habilidades
- [ ] Tipos de actividad de la ruta inicial: ordenar, completar, relacionar, escuchar y elegir, producción corta.

## Fase 7 — Evaluación
- [ ] Evaluación de fin de unidad con criterio de dominio.
- [ ] Separar evidencia con ayuda (práctica) de evidencia sin ayuda (evaluación).

## Fase 8 — Personalización
- [ ] Metadatos de unidad disponibles para el tutor IA (sin integración visual).

## Fase 9 — Pruebas
- [ ] Prueba: grafo sin ciclos y sin referencias rotas (10 idiomas).
- [ ] Prueba: ninguna unidad vacía.
- [ ] Prueba: ningún ejercicio usa vocabulario/gramática no enseñados antes.
- [ ] Prueba: desbloqueo correcto.
- [ ] Prueba: migración de foundations-v1 idempotente.
- [ ] Prueba: progreso persistente tras reinicio.
- [ ] Prueba: temas visibles después de practicar.
- [ ] `flutter analyze` sin errores nuevos.
- [ ] `flutter test` completo en verde.
- [ ] Recorrido manual web + emulador Android.

## Fase 10 — Producción
- [ ] Confirmar que se conservan home, logo, 6 iconos, «Aprende hoy», voz, avatares, backend y APK.
- [ ] Bloqueo de despliegue en el servidor.
- [ ] Respaldo identificable del servidor.
- [ ] Despliegue atómico de web.
- [ ] Verificar `/api/salud` y recorrido publicado.
- [ ] Registrar release y rollback en DESPLIEGUES.md.
