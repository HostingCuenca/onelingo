# Panel de administración: qué mide y de dónde sale

El panel (`panel/`, servido en `/panel`) lee la API `backend/src/routes/admin.ts`. Las funciones de cálculo y las tarifas están en `backend/src/lib/analitica.ts`. Los días se cuentan en hora de Ecuador (`ZONA_HORARIA`).

## Resumen (`GET /admin/resumen`)

| Métrica | Cómo se calcula |
|---|---|
| Registrados, nuevos hoy/7 d/30 d | `usuarios.creado_en`. «Demo» = `es_demo` (alta antigua sin contraseña). |
| Activos hoy / 7 d / 30 d (DAU, WAU, MAU) | Alumnos distintos con algún **día activo** en la ventana. Un día activo sale de: `eventos.fecha`, `conversaciones.fecha`, `progreso.estado.diasActividad` (días que guarda la app) y `usuarios.ultima_actividad`. |
| Plataforma, idioma meta y nativo, plan | `usuarios.plataforma` (vacío = «Sin dato»), `idioma_meta`, `idioma_nativo`, `plan_id` (vacío = prueba). «Agotaron la prueba» = sin plan y `trial_segundos` ≥ 60 min. |
| Registros y activos por día | Las mismas fuentes, día a día durante 30 días. |
| Embudo | Registrados → prueba de ubicación (evento `diagnostico` o `estado.diagnostico`) → 1 clase → 5 clases → volvieron otro día (algún día activo posterior al del registro). |
| Retención D1/D7/D30 | De quienes se registraron hace al menos N días, % con actividad el día N o después. |
| Clases completadas | Una clase cuenta cuando `estado.practicas['ruta:<unidad>:evaluacion'].aprobada` es `true` (ids como `ja.n3.c06`, `en.n1.class-01`, `en.f0.…`, `en.a1.…`). También cuentan las lecciones antiguas de `estado.completadas` (`L<n>-<nnn>`), asignadas al idioma que el alumno estudia ahora. |
| Tabla idioma × nivel | Idioma y nivel salen del id de la clase (`f0` = F0, `nN` = N, `a1` = N1). |
| Clases por día | Fecha de aprobación (`fechaAprobada`, hora del dispositivo). |
| Más completadas | Clases de la ruta con más alumnos que las aprobaron. Los títulos se leen del contenido publicado (`web/assets/assets/contenido` en el servidor o `assets/contenido` en el repositorio). |
| Dónde se abandona | Clases abiertas (`ruta:<unidad>:visto`) hace más de 2 días y nunca aprobadas. «Evaluaciones suspendidas»: intentos de evaluación sin aprobar. |
| Prueba de ubicación | Eventos `diagnostico`: pruebas, alumnos y nivel elegido medio por idioma. |
| Errores por habilidad | Tabla `errores`: total, alumnos, sin practicar y las 3 correcciones más repetidas. |
| Tutor IA | Tabla `conversaciones`: turnos, tokens de entrada/salida por modelo y por idioma. El coste usa `TARIFAS_IA` (USD por millón de tokens). Otras llamadas a IA (transcripción, revisión de escritura, preguntas y escritura de la ubicación) solo tienen recuento de eventos. |
| Voz | Tabla `audios`: audios, caracteres sintetizados y reproducciones por idioma. El coste usa `USD_POR_MIL_CARACTERES_VOZ`. |

Las tarifas son estimaciones: ajústalas en `backend/src/lib/analitica.ts` con la factura real.

## Alumnos

- `GET /admin/usuarios`: búsqueda (`q`), filtros `idioma`, `plataforma`, `estado` (`activos` = actividad en 7 días / `inactivos`), `plan` (`pago`/`prueba`), `orden` y `dir`. Devuelve `{ total, filas }` con clases completadas, nivel más alto con clases y fecha de la última.
- `GET /admin/usuarios.csv`: lo mismo en CSV (separador `;`, hasta 5000 filas).
- `GET /admin/usuarios/:id`: progreso por idioma y nivel (clases hechas / publicadas), últimas clases, clases empezadas sin terminar, pruebas de ubicación, conversaciones con su coste, errores y eventos. No envía hashes ni tokens de la cuenta.

## Rendimiento

`backend/sql/004_indices_panel.sql` añade índices sobre `eventos(fecha)`, `eventos(tipo, fecha)`, `conversaciones(fecha)`, `usuarios(creado_en)` y `errores(skill)`. Las clases se calculan recorriendo `progreso.estado.practicas` de todos los alumnos en cada carga del resumen. Con decenas de miles de alumnos convendría registrar un evento por clase aprobada (ver abajo).

## Conexiones (claves de API)

Página «Conexiones» del panel (`panel/src/paginas/Conexiones.tsx`). El administrador cambia las claves y modelos de **ElevenLabs** (voz), **OpenAI** (tutor, evaluación de escritura y transcripción) y **Gemini** (generación/diagnóstico de respaldo) sin tocar el servidor. Código: `backend/src/lib/conexiones.ts` y `backend/src/routes/conexiones.ts`.

- **Qué guarda y dónde**: tabla `conexiones` (`backend/sql/005_conexiones.sql`), una fila por proveedor. `datos` es un JSON cifrado con AES-256-GCM (clave = sha256(`'onelingo-conexiones:' + JWT_SECRET`)) que solo contiene lo que difiere del `.env`: clave, modelos y, en OpenAI, la Admin key opcional. `verificacion` guarda el resultado de la última verificación (sin claves).
- **Precedencia**: panel > `.env`. Al arrancar, `cargarConexiones()` (en `server.ts`, tras `migrar()`) aplica lo guardado sobre `config`. Al guardar se aplica en caliente: los consumidores leen `config` en cada llamada, así que no hace falta reiniciar. Los audios ya generados se conservan. `IA_PROVEEDOR` (tutor en uso) no cambia desde el panel.
- **Si cambia `JWT_SECRET`**: las filas no se pueden descifrar; se ignoran, se usa el `.env` y la página muestra un aviso para volver a guardar la clave.
- **Volver atrás**: «Volver a la configuración del servidor» (`DELETE`) borra la fila y restaura los valores del `.env` que había al arrancar.
- **Verificación** (antes de guardar, timeout 10 s, solo llamadas de lectura gratuitas):
  - Formato: una clave reconocible de otro proveedor se rechaza sin llamar a nadie («Esta clave es de OpenAI, no de ElevenLabs…»). Se quitan espacios, saltos de línea y comillas pegados. Formatos: ElevenLabs `sk_…` (o 32 hex), OpenAI `sk-proj-…`/`sk-svcacct-…`/`sk-…`, Admin key `sk-admin-…`, Gemini `AIza…` (39) o `AQ.…` (claves «auth» de AI Studio), Anthropic `sk-ant-…`.
  - ElevenLabs: `GET /v1/user/subscription` (cuota) y `GET /v1/models` (modelo). Una clave sin permiso «User» se acepta con aviso (no se verá el consumo). ElevenLabs responde 401 o 400 «API key is invalid» a una clave falsa.
  - OpenAI: `GET /v1/models` y comprobación de los tres modelos configurados (si falta uno: aviso). Admin key: `GET /v1/organization/costs`. La lista de modelos no comprueba el saldo.
  - Gemini: `GET /v1beta/models` (cabecera `x-goog-api-key`) y el modelo configurado; un 403 («project has been denied access») se muestra con el mensaje de Google.
  - Se guarda con `ok` o `aviso`; con `error` no se guarda nada. Clave vacía = conservar la actual (solo cambian los modelos).
- **Consumo** (`GET /admin/conexiones/consumo`, los tres en paralelo):
  - ElevenLabs: **real** (plan, caracteres usados/límite, renovación) + lo generado por OneLingo este mes según la tabla `audios` (coste estimado con `USD_POR_MIL_CARACTERES_VOZ`).
  - OpenAI: **real** si hay Admin key (Costs API del mes, por concepto); si no, **estimado** con los tokens de `conversaciones` y las tarifas de `analitica.ts` (no incluye transcripción ni evaluación).
  - Gemini: **estimado** si hay conversaciones con modelos `gemini*`; si no, enlace a Google AI Studio → Usage (Google no da el consumo por API).
- **Endpoints** (todos con sesión de administrador): `GET /admin/conexiones` (origen `panel`/`servidor`/`sin configurar`, clave enmascarada `sk_…a1b2`, modelos, última verificación, avisos), `POST /admin/conexiones/:proveedor/verificar` (sin guardar; cuerpo vacío = verifica lo actual), `PUT /admin/conexiones/:proveedor`, `DELETE /admin/conexiones/:proveedor`, `GET /admin/conexiones/consumo`. Ninguna respuesta ni log contiene claves completas.

## Lo que la app aún no registra

- **Clase aprobada como evento**: la ruta nueva solo sincroniza `practicas`; un evento `clase_aprobada` (unidad, aciertos, total) daría historial exacto en hora del servidor.
- **Apertura de la app / sesión**: no hay evento al abrir; la actividad depende de la sincronización del progreso.
- **Tokens de Gemini, transcripción y revisión de escritura**: no se guardan, así que su coste no se estima.
- **Pagos**: `plan_id` no guarda fecha ni importe, así que no hay ingresos ni conversión por fecha.
