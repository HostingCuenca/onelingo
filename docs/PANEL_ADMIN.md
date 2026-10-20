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

## Lo que la app aún no registra

- **Clase aprobada como evento**: la ruta nueva solo sincroniza `practicas`; un evento `clase_aprobada` (unidad, aciertos, total) daría historial exacto en hora del servidor.
- **Apertura de la app / sesión**: no hay evento al abrir; la actividad depende de la sincronización del progreso.
- **Tokens de Gemini, transcripción y revisión de escritura**: no se guardan, así que su coste no se estima.
- **Pagos**: `plan_id` no guarda fecha ni importe, así que no hay ingresos ni conversión por fecha.
