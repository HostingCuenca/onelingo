# Google Play · respuestas de los formularios de la consola

Cuenta: BRYAN FONSECA (personal, ID 8093461524306553231), `infoonelingo@gmail.com`.
Paquete: `com.torisoftt.onelingo`. Textos de la ficha en `textos.json`, gráficos en `graficos/`.

## Crear la app
- Nombre: OneLingo: idiomas con IA · Idioma predeterminado: Español (Latinoamérica) – es-419
- Tipo: App · Gratis (con suscripciones dentro de la app)
- Declaraciones: Políticas del Programa para Desarrolladores y leyes de exportación de EE. UU. (las acepta el dueño de la cuenta).

## Acceso a la app (revisores)
Toda la app requiere iniciar sesión. Instrucciones para el revisor:
- Usuario: `ana@onelingo.demo` (cuenta demo con plan completo y sin vencimiento; no se puede borrar).
- Contraseña: no se escribe en la consola. En producción Ana no tiene contraseña: entra por el panel DEMO del login (la tarjeta «Ana Torres» rellena correo y clave). Si se apaga el modo demo, darle antes una contraseña real y actualizar «Detalles de acceso».
- Pasos: «Ya tengo una cuenta · Iniciar sesión» → recuadro amarillo DEMO → tarjeta «Ana Torres» → ENTRAR → Inicio. Videollamada: Inicio → «Tutor con IA» → «Videollamada con …» (pide el micrófono).

## Anuncios
No contiene anuncios.

## Clasificación de contenido (IARC)
Categoría: Referencia, noticias o educación.
- Violencia, miedo, sexualidad, lenguaje soez, drogas, juegos de azar: No.
- Interacción entre usuarios / chat entre personas: No (el chat es con un tutor de IA, no con otros usuarios).
- Comparte la ubicación: No. · Compras digitales: Sí (suscripciones).
- Contenido generado por IA: Sí, con filtro del proveedor y botón «Reportar respuesta».

## Público objetivo
13–15, 16–17 y 18+. No dirigida a menores de 13. No atrae especialmente a niños (sin personajes infantiles como foco; Lumo es la mascota, se declara si la consola pregunta).

## Seguridad de los datos
Cifrado en tránsito: Sí (HTTPS). Los usuarios pueden pedir que se borren sus datos: Sí (en la app: Perfil → Eliminar cuenta; web: https://onelingo.org/eliminar-cuenta/).
No se comparten datos con terceros para sus propios fines (OpenAI, ElevenLabs, Stripe y Google actúan como proveedores de servicio).

| Tipo de dato | Recopilado | Compartido | Efímero | Obligatorio | Finalidad |
|---|---|---|---|---|---|
| Nombre | Sí | No | No | Sí | Funcionalidad, gestión de la cuenta |
| Correo electrónico | Sí | No | No | Sí | Funcionalidad, gestión de la cuenta, comunicaciones |
| Teléfono | Sí | No | No | Sí | Gestión de la cuenta |
| ID de usuario | Sí | No | No | Sí | Funcionalidad, gestión de la cuenta |
| Historial de compras | Sí | No | No | Sí (si compra) | Funcionalidad, gestión de la cuenta |
| Grabaciones de voz | Sí | No | Sí | Sí (llamada/hablar) | Funcionalidad (transcripción en tiempo real; no se guarda el audio) |
| Otros mensajes en la app (mensajes al tutor) | Sí | No | No | Sí | Funcionalidad |
| Interacciones en la app (progreso, clases) | Sí | No | No | Sí | Funcionalidad, estadísticas propias |

No se recopilan: ubicación, contactos, fotos, archivos, calendario, salud, identificadores de publicidad, registros de fallos de terceros.

## Permisos sensibles
- `RECORD_AUDIO`: hablar con el tutor y ejercicios de pronunciación (se pide al usarlo).
- `com.android.vending.BILLING`: suscripciones con Google Play.
- `USE_BIOMETRIC`/`USE_FINGERPRINT`: vienen de un plugin; revisar si se usan antes de publicar.

## Suscripciones (Monetización → Suscripciones)
Una suscripción por plan, ids exactos (ver docs/PANEL_ADMIN.md → «Google Play»): `plan_p1`, `plan_p2`, `plan_p3`, `plan_familiar`; planes base `mes-1`, `mes-3`, `mes-6`, `mes-12` con renovación automática.
Precios web de referencia (USD): p1 20/55/110/220 · p2 30/85/170/320 · p3 40/110/220/450 · familiar 60/165/335/600 (1/3/6/12 meses).
Requiere además la cuenta de servicio y Pub/Sub del servidor (pasos 1–3 de PANEL_ADMIN.md).

## Prueba cerrada obligatoria (cuenta personal nueva)
Antes de producción: prueba cerrada con al menos 12 verificadores que acepten y mantengan la app 14 días seguidos. Grupo de verificadores en Administra la cuenta → Grupos de verificadores (lista de correos de Gmail).

## Estado (31-10-2026)
App creada (id de consola 4976299517917417654). Completos: contenido de la app (todas las declaraciones), categoría Educación, contacto, fichas es-419 y en-US con gráficos.
- AAB 2014 (0.5.8) subido. Se subió desde el navegador con fetch + DataTransfer (el archivo pesa 175 MB y la herramienta solo admite 10 MB); el AAB se expuso unos minutos en onelingo.org con CORS temporal, que ya se retiró.
- Prueba interna: publicada y activa, sin revisión. Enlace: https://play.google.com/apps/internaltest/4698621163456524849
- Prueba cerrada «Alpha»: 178 países, versión 2014 y lista de verificadores. Enviada a revisión de Google el 31-10 (suele tardar hasta 7 días). Enlace: https://play.google.com/apps/testing/com.torisoftt.onelingo
- Lista de correos «Verificadores OneLingo»: 15 Gmail (12 del chat de WhatsApp más hostingcuenca, torisoftt y torisofttcuenca), asignada a las dos pruebas. Comentarios a infoonelingo@gmail.com.
- Los 14 días de la prueba cerrada empiezan a contar cuando Google la apruebe y al menos 12 verificadores se unan.
- Falta: darle contraseña a Ana antes de apagar el modo demo.

## Pagos con Google Play (01-11-2026)
- Suscripciones `plan_p1`, `plan_p2`, `plan_p3`, `plan_familiar`, cada una con `mes-1`, `mes-3`, `mes-6`, `mes-12` (renovación automática, 178 países, precio base en USD). Las 16 están activas.
- Corea del Sur tiene un tope de 600.000 KRW: en `plan_p3/mes-12` y `plan_familiar/mes-12` se dejó ese precio a mano (lápiz en la fila del país).
- Cuenta de servicio `play-pagos@onelingo-513218.iam.gserviceaccount.com` (proyecto de Cloud `onelingo-513218`, API Google Play Android Developer activada), invitada en Usuarios y permisos como Administrador. La llave está solo en el servidor (`/var/www/onelingo/secretos/`, ruta en `GOOGLE_PLAY_CUENTA_SERVICIO`). Comprobado desde el servidor: lista las 16 bases activas.
- Prueba de licencia (Administra la cuenta → Prueba de licencia): lista «Verificadores OneLingo» marcada, respuesta RESPOND_NORMALLY. Esos correos compran en la prueba sin cargo.
- Sin hacer (opcional): Pub/Sub para notificaciones en tiempo real (RTDN). Sin ellas, `GET /usuarios/me/suscripcion` vuelve a consultar a Google cada 10 minutos como máximo.
- Pagos web con Stripe: `/api/planes` sigue con `pagos.disponible: false`.
