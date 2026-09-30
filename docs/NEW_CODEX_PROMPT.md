# Prompt para retomar OneLingo en otra cuenta de Codex

Copia desde «INICIO DEL PROMPT» hasta «FIN DEL PROMPT» en la nueva tarea.

--- INICIO DEL PROMPT ---

Vamos a continuar el proyecto OneLingo que ya existe en esta computadora. Abre como proyecto local `/home/roggrt/Documents/onelingo`. No empieces con un barrido completo ni reconstruyas la historia desde cero.

Primero lee `AGENTS.md` y `docs/CODEX_HANDOFF.md`. Después ejecuta `git status --short --branch` y `git log --oneline -5`. Lee únicamente los documentos que el handoff indique para la tarea activa. Verifica que el estado real coincida con el handoff y avísame de diferencias materiales antes de editar; no repitas una auditoría general si coincide.

Revisa `docs/ACTIVE_CHECKLIST.md`, `docs/ARCHITECTURE_MAP.md`, `docs/CONNECTORS_AND_SERVICES.md`, `docs/AVATAR_STRATEGY.md` y `docs/DEPLOYMENT_RUNBOOK.md` según corresponda. El trabajo educativo detallado está en `docs/claude-educacion/` y `docs/claude-educacion/HANDOFF.md` es la entrada.

Comprueba si el plugin Higgsfield está instalado y autenticado en esta cuenta. Su ID es `app-6a3293e129088191abf0875820e839da@openai-curated-remote`. Si requiere conexión/OAuth, indícamelo claramente; no copies tokens ni reutilices credenciales de otra cuenta. Cuando esté conectado, enumera las herramientas realmente expuestas antes de afirmar que existe `generate_3d`. La referencia de Mia y el uso previsto de Higgsfield están documentados en `docs/CONNECTORS_AND_SERVICES.md`.

No leas ni muestres valores de `.env`, claves SSH, cookies o tokens. No sobrescribas el logo oficial, iconos del home, imagen «Aprende hoy», `web/avatar`, APK publicados ni configuración del servidor. Antes de desplegar, sigue el runbook, crea backup y lock, conserva APK/avatar y registra el rollback.

Al terminar la toma de contexto, respóndeme con máximo 12 puntos: rama y commit; si el árbol está limpio; producción confirmada o no; release pendiente; estado educativo; estado de voz; estado de avatares; estado Android/APK; Higgsfield conectado o acción requerida; tres riesgos; y la siguiente acción concreta recomendada. No hagas cambios de producto hasta que yo indique la tarea siguiente, pero deja los conectores verificados hasta donde sea posible de forma segura.

--- FIN DEL PROMPT ---
