# Conectores y servicios externos

Este documento registra identificadores y comprobaciones, nunca secretos. La autenticación de un conector puede pertenecer a la cuenta de Codex; la cuenta nueva debe reautorizarla.

## Higgsfield

- Plugin: `Higgsfield`
- ID: `app-6a3293e129088191abf0875820e839da@openai-curated-remote`
- Versión encontrada localmente al crear este handoff: `2.1.0`.
- El paquete local contiene habilidades de Higgsfield, imagen, video, motion y edición. La presencia en caché no demuestra que la nueva cuenta esté autenticada ni que todas las herramientas MCP estén expuestas.
- En la cuenta nueva: instalar/conectar el plugin desde Codex, completar OAuth si aparece y pedir que enumere sus herramientas antes de generar.
- Referencia original de Mia: generación `7deb8fa0-fcbe-46b0-80a0-ce3c4838d416`.
- Video de referencia previo: `https://d8j0ntlcm91z4.cloudfront.net/user_3GYKg4yT6z80ijaVCbuhm6zNW5Y/hf_20260911_210525_43aea2a0-aa25-46c6-a889-5538cae9f1e9.mp4`.
- En una sesión anterior, un modelo `image_to_3d` rechazó `generate_image` y pidió `generate_3d`. No se confirmó que esa herramienta estuviera expuesta y no se obtuvo un GLB mediante ese flujo.
- Higgsfield sirve aquí para hojas de referencia, poses, expresiones, estilo 2D y pruebas de movimiento. No generar un video nuevo por cada respuesta del tutor: aumenta coste y latencia, y no crea un avatar reutilizable.

## Meshy y Blender

- Meshy se consideró para image-to-3D, pero no hay un conector Meshy comprobado en este repositorio.
- Blender está instalado como snap en `/snap/bin/blender`; Codex encontró antes un error de scope/DBus al lanzarlo desde el entorno. Verificar de nuevo antes de asumir control automatizado.
- No se encontraron archivos fuente `.blend` versionados. Los GLB actuales parecen derivados de MakeHuman y deben conservarse.
- Rig corporal no equivale a rig facial. Inspeccionar morph targets, mandíbula, labios, párpados, expresiones y animaciones antes de afirmar compatibilidad ARKit/visemas.

## OpenAI, Gemini y ElevenLabs

Variables esperadas, sin valores:

```text
IA_PROVEEDOR
OPENAI_API_KEY
OPENAI_MODELO
OPENAI_MODELO_EVALUACION
OPENAI_MODELO_TRANSCRIPCION
GEMINI_API_KEY
GEMINI_MODELO
GEMINI_TIMEOUT_MS
ELEVENLABS_API_KEY
ELEVENLABS_MODELO
AUDIO_DIR
VOZ_MAX_CARACTERES
```

- Archivos locales: `backend/.env` y `tools/contenido/.env`, ambos ignorados por Git.
- No abrir ni imprimir sus valores salvo necesidad operativa estricta. Para comprobar configuración, usar respuestas de estado, nombres de variables y hashes, no secretos.
- El frontend nunca debe llamar directamente a estos proveedores.

## Servidor

- SSH documentado: `ssh -F /dev/null root@167.235.20.41`.
- El acceso depende de la clave ya instalada en la máquina, no de la cuenta de Codex.
- Antes de usarlo, comprobar alcance y seguir `docs/DEPLOYMENT_RUNBOOK.md`.

## Micrófono y navegador

- Web necesita contexto seguro, permiso de micrófono, `getUserMedia` y `MediaRecorder`.
- La app solicita cancelación de eco, supresión de ruido y ganancia automática.
- Un conector autenticado no concede permisos de cámara/micrófono al navegador; deben revisarse por sitio y perfil.
