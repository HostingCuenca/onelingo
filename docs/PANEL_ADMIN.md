# Panel de administración: qué mide y de dónde sale

El panel (`panel/`, servido en `/panel`) lee la API `backend/src/routes/admin.ts`. Las funciones de cálculo y las tarifas están en `backend/src/lib/analitica.ts`. Los días se cuentan en hora de Ecuador (`ZONA_HORARIA`).

## Resumen (`GET /admin/resumen`)

| Métrica | Cómo se calcula |
|---|---|
| Registrados, nuevos hoy/7 d/30 d | `usuarios.creado_en`. «Demo» = `es_demo` (alta antigua sin contraseña). |
| Activos hoy / 7 d / 30 d (DAU, WAU, MAU) | Alumnos distintos con algún **día activo** en la ventana. Un día activo sale de: `eventos.fecha`, `conversaciones.fecha`, `progreso.estado.diasActividad` (días que guarda la app) y `usuarios.ultima_actividad`. |
| Plataforma, idioma meta y nativo, plan | `usuarios.plataforma` (vacío = «Sin dato»), `idioma_meta`, `idioma_nativo`, `plan_id` (vacío = prueba; derivado de `suscripciones`, ver «Planes y suscripciones»). «Agotaron la prueba» = sin plan y `trial_segundos` ≥ los minutos de prueba de `ajustes_pago` (60 por defecto). |
| Suscripciones | `suscripciones` (bloque `suscripciones` de la respuesta): activas de Stripe, MRR, nuevas y canceladas en 30 días, impagos y cortesías vigentes, del modo de Stripe en uso. |
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

## Planes y suscripciones

Fase 1 con **Stripe en modo test**. El administrador edita los planes, da acceso de cortesía y vincula Stripe pegando su clave; el alumno paga en Stripe Checkout y gestiona su suscripción en el Customer Portal. **El servidor es la autoridad del plan**: la app ya no se asigna planes (salvo los usuarios DEMO sin servidor).

Código: `backend/src/lib/pagos/` (`stripe.ts` cliente REST sin SDK + firma del webhook, `proveedor.ts` interfaz `ProveedorPagos` e implementación de Stripe, `planes.ts`, `suscripciones.ts`, `webhook.ts`), rutas `backend/src/routes/planes.ts` y `pagos.ts`, migraciones `backend/sql/006_pagos.sql`, `007_pagos_portal.sql`, `008_pagos_idiomas.sql` y `010_planes_duraciones_familia.sql` (`familia.ts` y `cotizaciones.ts` en `lib/pagos/`). Panel: «Planes», «Suscripciones», la sección «Suscripción» del alumno y la tarjeta Stripe de «Conexiones». Pruebas: `backend/test/pagos.test.ts` (crea una base temporal en el Postgres local y simula Stripe).

### Flujo

1. **Vincular** (Conexiones → Stripe): se pega `sk_test_…` o `rk_test_…` (una `pk_…` se rechaza: «Esta es la clave publicable; pega la secreta (sk_…)»). Al guardar: se verifica con `GET /v1/account` (o `GET /v1/balance` si es restringida) y se detecta el modo; se crea o reutiliza el webhook en `<URL de la app>/api/stripe/webhook` y se guarda su secreto cifrado; se sincronizan los planes y se configura el Customer Portal de OneLingo. La URL de la app por defecto es `PUBLIC_URL` sin `/api`.
2. **Planes**: cada plan es un Product (`metadata.plan_id`) con un Price recurrente. Cambiar precio, moneda o intervalo crea un Price nuevo (pasa a `default_price`) y archiva el anterior; **los suscriptores actuales conservan su precio** (no se toca ninguna suscripción). Si Stripe falla, el plan se guarda igual y queda «Sin sincronizar» con botón «Reintentar». Ocultar = no se ofrece; archivar = además se desactiva el Product; no hay borrado físico si alguien lo usa.
3. **Pago**: la app pide `POST /pagos/checkout { planId }` y abre la URL de Checkout. Al volver (`<URL app>/#/pago?estado=ok&session_id=…`) llama a `POST /pagos/confirmar { sessionId }`, que consulta la sesión en Stripe y sincroniza: **funciona sin webhook**. El webhook mantiene al día renovaciones, impagos y cancelaciones.
4. **Gestión y cambio de plan**: `POST /pagos/portal` abre el Customer Portal (en la app, «Cambiar de plan» para quien tiene una suscripción de Stripe en curso): cancelar al final del periodo, tarjeta, facturas y **cambio de plan con prorrateo** (`subscription_update`: `default_allowed_updates=[price]`, `proration_behavior=create_prorations`, `products` = Product y Price actual de cada plan visible, no archivado y sincronizado, por `orden`, máximo 10). Es una configuración propia (`metadata.origen=onelingo`, id en `ajustes_pago.stripe_portal_id`): la sesión la pide con `configuration`, sin tocar la configuración por defecto de la cuenta. Se actualiza cada vez que se sincroniza un plan (crear, editar, ocultar, archivar, «Reintentar») y al vincular Stripe; si falla, el plan se guarda igual y el panel avisa. Vuelve a `#/pago?estado=portal`; el webhook `customer.subscription.updated` trae el Price nuevo y cambia el plan.
5. **Cortesía**: en el detalle del alumno, «Dar acceso» con plan, idiomas (el que aprende ahora, una lista o «todos»), fecha opcional y nota; «Quitar cortesía». No se puede dar a quien tiene una suscripción de Stripe en curso (409).

### Duraciones, plan Familiar y plan Empresarial

- **Duraciones** (`planes.duraciones`, solo en planes mensuales): además del cobro mensual (`precio_centavos`), precios por 3, 6 o 12 meses (en el panel, «Precio por N meses»; vacío = no se ofrece). Cada una es un Price del mismo Product con `recurring.interval=month` e `interval_count=N`, guardado en `planes_precios` con `meses` y la firma `importe|moneda|mes:N`; si cambia el importe, Price nuevo y el anterior se archiva (los suscriptores lo conservan). `GET /planes` devuelve `duraciones: [{meses, precio}]` (incluida la de 1 mes) y `usuarios`. `POST /pagos/checkout { planId, idiomas, meses }` (por defecto 1; 400 si el plan no la ofrece). La suscripción guarda `meses` y el MRR la divide entre N. El Customer Portal ofrece por producto el Price mensual y los de sus duraciones. Semilla: p1 55/110/220, p2 85/170/320, p3 110/220/450 (3/6/12 meses).
- **Familiar** (`planes.usuarios > 1`; semilla `familiar`: 4 personas, 1 idioma por persona, $60 al mes y 165/335/600): el titular paga y desde la app (Planes → «Tu plan familiar») añade por correo a `usuarios − 1` personas (`familia_miembros`; un correo, una familia). Con cuenta, el acceso es inmediato; sin cuenta, se le envía un correo y el acceso llega cuando entra con ese correo (`GET /usuarios/me/suscripcion` vincula las invitaciones). Cada miembro tiene su fila en `suscripciones` con `origen='familia'` y `titular_id`, **reflejo del titular**: mismo plan; Stripe activa → sin fecha; cancelada → hasta el fin del periodo; cortesía → hasta su fecha; si el titular pierde el plan o pasa a uno de una persona, los miembros quedan sin plan (y vuelven si lo recupera). Cada miembro elige sus propios idiomas (al entrar, su idioma meta) y lleva su propio progreso. Nunca pisa una suscripción o cortesía propia vigente: quien ya paga lo suyo no se puede añadir y, si un miembro compra su propio plan o recibe una cortesía, sale de la familia. Rutas: `GET/POST /usuarios/me/familia` (`{ email }`), `POST /usuarios/me/familia/quitar` (`{ email }`), `POST /usuarios/me/familia/salir`. Panel → Suscripciones: filtro «Miembros de un plan familiar» y origen «Familia · paga …».
- **Empresarial**: no es un plan de Stripe sino una cotización. La app envía `POST /cotizaciones { empresa, empleados, idiomas, nombre, email, telefono, mensaje }` (con o sin sesión; 5 por hora por IP, con `X-Forwarded-For`); el solicitante recibe un correo de confirmación. Panel → **Cotizaciones**: lista con estado (nueva, contactada, cerrada) y nota interna (`GET /admin/cotizaciones?estado=`, `PUT /admin/cotizaciones/:id`).

### Idiomas por suscripción

Un plan incluye N idiomas (`planes.idiomas`, 1–10; **0 = todos**, «Todos los idiomas» en el panel) y el alumno elige cuáles. Códigos: `en fr es pt de it zh ja ru ko`.

- **Acceso por idioma**: el pago da acceso solo en los idiomas de `suscripciones.idiomas`, o en todos si el plan es de 0 o la cortesía es «todos» (`todos_idiomas`). En los demás el alumno sigue en la prueba gratuita, que es única (los minutos se suman entre idiomas). `GET /usuarios/me/suscripcion` devuelve `idiomas`, `todosLosIdiomas`, `idiomasPorElegir`, `cambioIdiomas {regla, permitido, proximoCambio}`, `accesoPorIdioma` (los 10) y `acceso` = acceso de pago **en el idioma meta actual** (`usuarios.idioma_meta`); `accesoPlan` es el acceso general y `planId` sigue siendo el plan con acceso.
- **Al suscribirse**: `POST /pagos/checkout { planId, idiomas }` exige exactamente N códigos válidos sin repetir (lista vacía en un plan de 0); si no, 400 con el motivo. Viajan en `metadata.idiomas` de la Checkout Session y de la suscripción (`"en,fr"`) y se guardan en el webhook y en «Confirmar».
- **Cambio de plan en el portal**: se conservan los idiomas de la fila (no los de la metadata, que se queda con los de la compra). Al subir de 2 a 3, el tercero queda «por elegir»; al bajar de 3 a 2, quedan los 2 primeros. El servidor nunca guarda más que los del plan.
- **Cambiar un idioma** (`PUT /usuarios/me/suscripcion/idiomas { idiomas }`, entre 1 y N): según el ajuste `cambioIdiomas` (Planes → «Cambiar un idioma por otro»): `libre`; `uno_por_periodo` (por defecto: un cambio por periodo de facturación, desde `periodo_inicio`; en una cortesía, uno cada 30 días desde el último); `solo_admin`. Completar los «por elegir» o reordenar no cuenta como cambio. Si no está permitido: 403 `{ error, proximoCambio }` (ISO o null). Cada edición queda en `eventos` (`cambio_idiomas`, con `antes`, `despues` y `cambio`).
- **El administrador** edita los idiomas desde el detalle del alumno («Editar idiomas», `PUT /admin/usuarios/:id/suscripcion/idiomas`): sin la regla de cambios ni gastar el cambio del alumno, pero con el máximo del plan (evento `cambio_idiomas_admin`, que no cuenta como actividad del alumno).
- **Panel**: Suscripciones tiene columna «Idiomas», filtro por idioma y la tabla «Por idioma» (suscriptores de Stripe y cortesías con acceso por idioma; MRR repartido a partes iguales entre los idiomas elegidos de cada suscripción; filas aparte para «todos» y «sin idiomas elegidos»). En el detalle del alumno, el progreso por idioma marca «De pago» o «Prueba».

### Tablas

| Tabla | Qué guarda |
|---|---|
| `planes` | Nombre, descripción y ventajas en es/en, idiomas, `precio_centavos`, moneda, `intervalo` (`mes`/`anio`), destacado, visible, orden, archivado; ids de Stripe con su modo, firma del precio sincronizado (`importe|moneda|intervalo`), `stripe_sincronizado` y último error. Semilla: p1 $20, p2 $30 (destacado, «POPULAR» en la app), p3 $40 al mes (ventajas de `catalog.dart` y `en.json`). 007 destaca p2 en bases donde 006 se aplicó antes, solo si la fila no se editó y no hay otro destacado. |
| `planes_precios` | Historial de Prices de Stripe de cada plan (con fecha de archivado): un suscriptor con un Price antiguo o archivado se asocia igualmente a su plan. |
| `suscripciones` | Una fila por alumno: plan, `origen` (`stripe`/`google`/`cortesia`/`familia`), `estado` (`activa`, `prueba_stripe`, `impago`, `cancelada`, `vencida`), `cancela_al_final`, `periodo_fin`, ids de cliente/suscripción/precio de Stripe, `modo`, nota, importe e intervalo reales del suscriptor (para el MRR), alta y cancelación; `idiomas text[]`, `todos_idiomas` (cortesía «todos»), `periodo_inicio` (inicio del periodo de Stripe) y `ultimo_cambio_idiomas`. |
| `pagos_eventos` | Id de cada evento de Stripe recibido (idempotencia), tipo, si se procesó y el error. |
| `familia_miembros` | Plan familiar: titular, correo invitado (único) y `usuario_id` cuando existe la cuenta. |
| `cotizaciones` | Solicitudes del plan Empresarial: empresa, empleados, idiomas, contacto, mensaje, alumno que la envió (si tenía sesión), estado y nota. |
| `ajustes_pago` | Minutos de prueba gratuita (60), moneda por defecto (`usd`), regla `cambio_idiomas` (`uno_por_periodo`), `demo_activo` (usuarios demo, `true`) e id y modo de la configuración del Customer Portal de OneLingo. |

**Acceso**: estado `activa` o `prueba_stripe`; `cancelada` con `periodo_fin` futuro; o cortesía sin fecha o con fecha futura; familia: `activa`/`prueba_stripe` sin fecha o con fecha futura, `cancelada` con fecha futura. `usuarios.plan_id` es un dato derivado (plan con acceso o vacío) que se actualiza en cada cambio y se refresca al abrir el resumen y la lista de alumnos (cortesías o periodos caducados). A quien no tiene fila en `suscripciones` no se le toca el `plan_id` antiguo. **Plan de una suscripción de Stripe**: por su Price actual (`planes.stripe_precio_id` o el historial `planes_precios`, que incluye los archivados), luego `metadata.plan_id` del Price, el Product del plan y, por último, `metadata.plan_id` de la suscripción, que tras un cambio en el portal sigue diciendo el plan de la compra. Estados de Stripe: `active` → activa, `trialing` → prueba_stripe, `past_due`/`unpaid`/`incomplete` → impago, `canceled` → cancelada (hasta `ended_at`), el resto → vencida.

**Prueba gratuita**: `PUT /usuarios/me/progreso` ignora el `planId` del cliente y guarda `trial_segundos` = máximo entre lo guardado y lo que manda la app (nunca baja). Login, Google y `GET /usuarios/me/progreso` devuelven `estado` con el `planId` del servidor y esa prueba.

**El servidor hace cumplir la prueba** (`requierePractica` en `suscripciones.ts`). Afecta a `POST /chat`, `POST /chat/voz` y `POST /llamada/token`.
- **Sin plan ni cortesía y con `trial_segundos` ≥ minutos de prueba:** responde 402 `{error: 'prueba_agotada'}`. Es un respaldo del bloqueo de la app.
- **Prueba restante:** sale de lo que reporta la app; una app modificada podría no reportarla.
- **`/chat/resumen` queda libre:** así se cierra el resumen de una conversación ya empezada.

**Modo demo** (Panel → Planes → «Usuarios demo»; `demoActivo` en `PUT /admin/pagos/ajustes` y en `GET /planes`). Los usuarios demo son los `@onelingo.demo`, que entran sin contraseña.
- **Activo:** cualquiera puede crear uno nuevo y usar al tutor durante la prueba.
- **Desactivado:**
  - `POST /usuarios/registro` y `POST /usuarios/login` responden 403 `demo_cerrado`;
  - los demo ya creados reciben 403 `demo_cerrado` en el tutor;
  - la app oculta el panel demo del login.
- **Antes de publicar:** desactivarlo.

### Endpoints (sin `/api`: Apache lo quita)

- Públicos y del alumno: `GET /planes` (sin sesión; solo visibles y no archivados, por `orden`; `pagos.disponible=false` si Stripe no está vinculado → la app muestra «Próximamente»), `GET /usuarios/me/suscripcion`, `PUT /usuarios/me/suscripcion/idiomas`, `POST /pagos/checkout` (`{ planId, idiomas }`) (409 si ya tiene una suscripción de Stripe en curso, 503 sin Stripe), `POST /pagos/confirmar`, `POST /pagos/portal`.
- Webhook: `POST /stripe/webhook`, cuerpo crudo (parser propio solo en esa ruta), firma `Stripe-Signature` HMAC-SHA256 con tolerancia de 5 min. Eventos: `checkout.session.completed`, `customer.subscription.created|updated|deleted`, `invoice.paid`, `invoice.payment_failed`. Un evento repetido responde 200 sin reprocesarse; uno que falla responde 500 y Stripe lo reintenta. Los eventos del otro modo (test/live) se ignoran.
- Panel (administrador): `GET/POST /admin/planes`, `PUT /admin/planes/:id`, `POST /admin/planes/:id/archivar` (`{ archivado:false }` restaura), `POST /admin/planes/:id/sincronizar`, `DELETE /admin/planes/:id` (solo si nadie lo usa), `GET /admin/suscripciones?estado=&q=&idioma=` (filas con idiomas y resumen con `porIdioma`: activas, MRR en USD con anuales /12 e importe real de cada suscriptor, nuevas y canceladas en 30 días, impagos, cortesías), `POST/DELETE /admin/usuarios/:id/cortesia` (`{ planId, idiomas?: string[] | 'todos', hasta?, nota }`), `PUT /admin/usuarios/:id/suscripcion/idiomas`, `GET/PUT /admin/pagos/ajustes` (con `cambioIdiomas`).

### Modo test → modo real

Basta con pegar en Conexiones la clave `sk_live_…` o `rk_live_…` (con los mismos permisos) y guardar: se crea el webhook de modo real, se crean en modo real los productos y precios (los ids de test no sirven en live) y la tarjeta muestra «MODO REAL». No hay que cambiar código. Antes, la cuenta de Stripe debe estar activada para cobrar. Las suscripciones de test quedan en la tabla con `modo='test'` y no cuentan en el resumen del modo real. «Desvincular Stripe» borra la clave (la app vuelve a «Próximamente»); el webhook queda creado en Stripe y se reutiliza o recrea al volver a vincular.

Clave restringida recomendada (permisos mínimos; fuentes: docs.stripe.com/keys/restricted-api-keys y docs.stripe.com/stripe-apps/reference/permissions): Checkout Sessions = Write, Customers = Write, Subscriptions = Read, Products = Write, Prices = Write, Webhook Endpoints = Write, Customer portal = Write, Balance = Read.

### Si el webhook falla

- Con una URL local o sin https, Stripe no puede entregar el webhook: el guardado avisa y sigue. El pago se confirma igual con **«Confirmar»** cuando el alumno vuelve de Checkout (`POST /pagos/confirmar`), pero las renovaciones, impagos y cancelaciones no se actualizan solas.
- Si el webhook responde error, Stripe lo reintenta durante días; el motivo queda en `pagos_eventos.error` y en el log del servidor. En el Dashboard de Stripe (Developers → Webhooks → el endpoint de OneLingo) se ven los intentos y se pueden reenviar.
- Si se cambió `JWT_SECRET` o se perdió el secreto del webhook, vuelve a guardar la clave en Conexiones: el webhook se recrea con un secreto nuevo.
- Para probar en local sin webhook: Checkout con la tarjeta `4242 4242 4242 4242` y vuelta a la app con `session_id`.

### Google Play (cobro dentro de la app Android)

En Android la app **no usa Stripe**: compra con Google Play Billing (`in_app_purchase`). La web sigue con Stripe. Las dos conviven en la misma tabla: `suscripciones.origen = 'google'` (migración `backend/sql/011_google_play.sql`: `google_token`, `google_producto`, `google_plan_base`, `google_pedido`). Código: `backend/src/lib/pagos/google.ts` (API Google Play Developer sin SDK, JWT RS256 de la cuenta de servicio) y `sincronizarDesdeGoogle`/`refrescarGoogle` en `suscripciones.ts`; app: `lib/core/pagos/google_play.dart`. Pruebas: `backend/test/google-play.test.ts` y el grupo «Google Play (Android)» de `test/pagos_test.dart`.

**Ids en Play Console** (deben coincidir exactamente): una suscripción por plan con id `plan_<id del plan>` (`plan_p1`, `plan_p2`, `plan_p3`, `plan_familiar`…; el panel no los crea) y dentro, un **plan base** por duración ofrecida: `mes-1` (mensual), `mes-3`, `mes-6` (cada 3 o 6 meses) y `mes-12` (anual), con renovación automática. El precio lo pone Play Console (la app muestra el precio localizado de Google, no el del panel). `GET /planes` devuelve en cada plan `google: { producto, planesBase }` y `google: { disponible, paquete }`.

**Variables del servidor** (`backend/.env`):
- `GOOGLE_PLAY_CUENTA_SERVICIO`: ruta al JSON de una cuenta de servicio de Google Cloud (o el JSON en una línea). Sin ella, `google.disponible=false` y la app muestra «Pagos próximamente».
- `GOOGLE_PLAY_PAQUETE`: por defecto `com.torisoftt.onelingo`.
- `GOOGLE_PLAY_RTDN_TOKEN`: secreto largo para la URL de notificaciones.

**Puesta en marcha** (una vez):
1. Google Cloud: crear un proyecto, habilitar «Google Play Android Developer API», crear una cuenta de servicio y descargar su clave JSON (va al servidor, nunca al repositorio).
2. Play Console → Usuarios y permisos → invitar el correo de la cuenta de servicio con permiso de **ver información financiera y gestionar pedidos y suscripciones**.
3. Pub/Sub: crear un tema, dar a `google-play-developer-notifications@system.gserviceaccount.com` el rol Publicador y una suscripción **push** a `https://<dominio>/api/pagos/google/rtdn?token=<GOOGLE_PLAY_RTDN_TOKEN>`. En Play Console → Monetización → Configuración de monetización, poner el tema y «Enviar notificación de prueba» (responde 200 `ignorado`).
4. Subir un AAB con la biblioteca de facturación (pista de prueba interna o cerrada) y crear las suscripciones y planes base con los ids de arriba. Los testers de licencias compran sin cobro real (`modo = 'test'`).

**Flujo**: la app compra con `obfuscatedAccountId` = id del alumno y envía el token a `POST /pagos/google/verificar { token, idiomas }`. El servidor consulta `purchases.subscriptionsv2`, comprueba que la compra es de ese alumno (403 si es de otro), guarda la suscripción y la **reconoce** (Google la reembolsa si nadie la reconoce en 3 días); solo entonces la app la completa. Si la app se cierra antes, la compra pendiente se reintenta al abrirla. Renovaciones, cancelaciones, impagos y reembolsos llegan por RTDN (`POST /pagos/google/rtdn`: 403 sin token válido, 500 si falla para que Pub/Sub reintente); además, `GET /usuarios/me/suscripcion` vuelve a consultar Google (como mucho cada 10 min) si el periodo pasó o está en impago, así funciona aunque falte la notificación. Cambio de plan o de duración: la app usa el reemplazo de Play con prorrateo y el token nuevo trae `linkedPurchaseToken` (una notificación atrasada del token viejo no pisa la fila).

**Estados y acceso**: `ACTIVE` y `IN_GRACE_PERIOD` → activa (acceso hasta `periodo_fin` + 1 día de margen para la renovación); `CANCELED` → cancelada (acceso hasta `periodo_fin`); `ON_HOLD`/`PENDING` → impago; `EXPIRED`/`PAUSED` → vencida. Quien tiene una suscripción de Google en curso no puede pagar con Stripe ni recibir cortesía (409); la gestiona en Google Play (la app abre `play.google.com/store/account/subscriptions?sku=…&package=…`). Quien paga en la web ve en Android «Tu suscripción se gestiona en la web». El plan Familiar funciona igual: el titular paga en Play y los miembros reflejan su fila.

**Panel**: Suscripciones muestra el origen «Google Play» con el número de pedido (`GPA.…`, se puede buscar), el filtro «Pagadas en Google Play» y el KPI «Activas (Google Play)»; su MRR suma al total (importe que informa Google, en su moneda).

## Tutor IA y Conversaciones IA

- **Tutor IA**: cómo enseña el tutor (enfoque, preguntas de dos opciones, eco, pedir repetir, frases prohibidas, indicaciones extra), con «Probar un turno» (compara borrador y guardado; puede responder como un alumno con ficha) e historial de versiones con «Cargar». Rutas: `GET/PUT /admin/tutor`, `POST /admin/tutor/probar`, `GET /admin/fichas`.
- **Conversaciones IA**: los turnos agrupados por llamada (mismo alumno y tutor, sin pausas de más de 20 min) con preguntas repetidas, eco, misma apertura, muletillas y porcentaje de «¿X o Y?»; al tocar una llamada se ve con las repeticiones marcadas. Ruta: `GET /admin/practicas?dias=N`. Una respuesta que el alumno interrumpió se descarta en la app pero queda guardada.
- **Detalle del alumno → Lo que el tutor sabe de este alumno**: su ficha por idioma y «Actualizar ahora». Rutas: `GET /admin/usuarios/:id/fichas`, `POST /admin/usuarios/:id/fichas/:idioma`.

## Certificados de nivel

En el detalle de cada alumno, «Certificados de nivel» lista los que recibió: idioma y nivel, el nombre impreso (el alumno puede corregirlo desde la app; el código y la fecha no cambian), si lo logró con todas las clases o con la prueba del nivel, y el enlace a su página pública de verificación (`/certificado/<código>`, sin indexar en buscadores). Se emiten desde la app (`POST /certificados`) y solo si el progreso guardado en el servidor confirma el nivel superado.

## Lo que la app aún no registra

- **Clase aprobada como evento**: la ruta nueva solo sincroniza `practicas`; un evento `clase_aprobada` (unidad, aciertos, total) daría historial exacto en hora del servidor.
- **Apertura de la app / sesión**: no hay evento al abrir; la actividad depende de la sincronización del progreso.
- **Tokens de Gemini, transcripción y revisión de escritura**: no se guardan, así que su coste no se estima.
- **Conversión de la prueba al pago por fecha**: hay fechas de alta y cancelación de cada suscripción, pero no un evento «vio los planes» para medir el embudo prueba → pago.
