# OneLingo: guía para agentes (humanos o IA)

Este repositorio es la fuente de verdad. Lee en este orden y no más allá de lo que tu tarea necesita:

1. `docs/ARQUITECTURA_VIGENTE.md`: el mapa que manda (pantallas, fuentes canónicas, legado congelado, reglas de interfaz y hoja de ruta A–E).
2. `docs/claude-educacion/PROGRESO.md`: en qué estamos.
3. `docs/claude-educacion/DECISIONES.md`: lo que el cliente ya decidió (DEC-xxx). No lo reviertas sin preguntar.
4. Solo para tu área: el plan o contrato correspondiente (`ESQUEMA_CONTENIDO.md`, `DIAGNOSTICO_V2.md`, `NIVEL_0_INGLES.md`, `PLAN_FRANCES.md`…).

`docs/archivo/` es historia: no lo uses para decidir.

## Reglas que no se negocian

- **No dupliques.** Antes de crear una lista, un JSON o una pantalla, busca su fuente canónica en la arquitectura y extiéndela.
- **No amplíes el legado congelado** (sección 4 de la arquitectura). Arréglalo solo si se rompe.
- **Interfaz única:**
  - `BotonPrincipal` fijo abajo, `OpcionRespuesta` y `FeedbackDock`;
  - nunca pedir el nivel al alumno;
  - sin jerga interna;
  - nunca dos personajes a la vez.
  - `test/arquitectura_test.dart` lo vigila: si falla, corrige el código, no la prueba.
- **Imágenes:** no se generan. Se buscan con licencia de uso comercial y se registran sus créditos.
- **Secretos:** nunca copies, muestres ni reemplaces `backend/.env`, `tools/contenido/.env`, claves SSH ni tokens.
- **Producción:**
  - No reinicies Apache ni la API (PM2 `onelingo-api`) sin autorización expresa para ese despliegue.
  - Despliega con candado, respaldo, staging y cambio atómico (`docs/DEPLOYMENT_RUNBOOK.md`).
  - Registra cada release en `docs/claude-educacion/DESPLIEGUES.md`, con su rollback.
- **Conserva:** el logo, los seis iconos del home, `web/avatar/`, los APK publicados y la configuración del servidor.
- **Git:** los subagentes no ejecutan git.
- **Al cerrar una fase:** actualiza `PROGRESO.md`, y también `ARQUITECTURA_VIGENTE.md` si cambió la estructura.

## Validación

```bash
python3 tools/validar_ruta.py
~/flutter/bin/flutter analyze lib test
~/flutter/bin/flutter test
cd backend && npx tsx --test test/*.test.ts
```

Durante la iteración ejecuta solo lo pertinente. Antes de una release, todo lo que toque las capas afectadas.
