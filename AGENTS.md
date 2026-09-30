# OneLingo: guía para agentes

Este repositorio es la fuente de verdad. Para retomar el proyecto en una cuenta o tarea nueva, empieza por `docs/CODEX_HANDOFF.md`; contiene el estado comprobado, el mapa de documentos y las prioridades.

## Reglas operativas

- Antes de editar, ejecuta `git status --short --branch` y lee solo los documentos vinculados al área que vas a tocar.
- No hagas un barrido completo del repositorio si el handoff y las pruebas focalizadas responden la pregunta.
- Nunca copies, muestres ni reemplaces `backend/.env`, `tools/contenido/.env`, claves SSH, tokens o credenciales. Las conexiones externas se reautorizan en la cuenta nueva.
- Conserva el logo oficial, los seis iconos del home, `home-aprende-hoy.webp`, `web/avatar/`, los APK publicados y la configuración del servidor salvo instrucción explícita.
- No despliegues desde un árbol con cambios ajenos sin separar el alcance. Antes de producción sigue `docs/DEPLOYMENT_RUNBOOK.md` y registra el resultado en `docs/claude-educacion/DESPLIEGUES.md`.
- El contenido educativo usa el esquema 2 de `lib/core/aprendizaje/` y `assets/contenido/<idioma>/ruta/`; valida con `python3 tools/validar_ruta.py`.
- Los avatares 3D actuales son un prototipo web. No afirmes que tienen rig facial ARKit o sincronización fonética: compruébalo en cada GLB. La estrategia vigente está en `docs/AVATAR_STRATEGY.md`.
- Actualiza `docs/ACTIVE_CHECKLIST.md` y `docs/CODEX_HANDOFF.md` al cerrar una fase importante.

## Validación por alcance

```bash
python3 tools/validar_ruta.py
~/flutter/bin/flutter analyze lib
~/flutter/bin/flutter test
cd backend && npx tsx --test test/*.test.ts
```

Ejecuta únicamente lo pertinente durante la iteración y el conjunto completo antes de una release que afecte varias capas.
