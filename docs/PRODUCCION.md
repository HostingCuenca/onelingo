# Lista para salir a producción

Estado al 29-10-2026. onelingo.org es el entorno previo al lanzamiento: no hay alumnos reales. Cada punto dice quién lo hace: **Bryan** (dueño de las cuentas), **Torisoftt** (código y servidor) o **ambos**.

## Bloquean el lanzamiento

| # | Qué | Quién | Estado |
|---|-----|-------|--------|
| 1 | **Política de privacidad y términos de uso** publicados en onelingo.org (Google Play exige la URL de la política; también Stripe). | Torisoftt redacta, Bryan aprueba | No existen |
| 2 | **Borrar la cuenta** desde la app y desde una página web (Google Play lo exige a toda app con registro). | Torisoftt | No existe |
| 3 | **Respaldos automáticos de la base de datos** (pg_dump diario fuera del servidor, con retención). | Torisoftt | Diario en el VPS (14 días) + semanal de Hostinger; falta copia fuera del VPS |
| 4 | **Panel de administración**: cuentas por persona y límite de intentos (hoy, usuario único y PIN genérico 2345). | Torisoftt | Pendiente |
| 5 | **http → https** en onelingo.org. | Torisoftt | Hecho (VPS nuevo) |
| 6 | **Modo demo apagado** (Panel → Planes → «Usuarios demo»). | Bryan o Torisoftt, al lanzar | Activo |
| 7 | **Prueba gratuita** con su duración real (Panel → Planes; hoy 1 minuto). | Bryan decide | 1 minuto |
| 8 | **Cobro real**: Stripe en modo real (¿dónde está registrada la cuenta? Stripe no acepta empresas de Ecuador) y Google Play Billing configurado (docs/PANEL_ADMIN.md → «Google Play»). | Bryan + Torisoftt | Stripe en test; Play sin app |

## Google Play (Bryan, con apoyo de Torisoftt)

1. Verificar el dispositivo Android y el teléfono en Play Console.
2. Perfil de pagos e inscripción al programa de comisión del 15 %.
3. Crear la app `com.torisoftt.onelingo` y subir el AAB (`shorebird release android`, sin `--artifact apk`).
4. Ficha de la tienda: ícono 512, gráfico destacado 1024×500, capturas de teléfono, descripciones en es/en.
5. Formularios: seguridad de los datos, clasificación de contenido, público objetivo, anuncios (no), URL de la política de privacidad y de borrado de cuenta.
6. Prueba cerrada: unos 12 testers durante 14 días antes de pedir producción (cuentas personales).
7. Suscripciones `plan_<id>` con planes base `mes-1/3/6/12`, cuenta de servicio y notificaciones RTDN.

## Conviene antes del lanzamiento

- Clave de Gemini: responde «project denied access» (el diagnóstico cae a OpenAI).
- Cuenta de Porkbun del dominio sin 2FA ni recuperación verificada.
- Shorebird: revisar el límite mensual del plan gratuito y firmar los parches (`--public-key-path`).
- Monitoreo: aviso si `/api/salud` deja de responder.
- Ocultar el panel de demo en la pantalla de entrada (solo Ana y Bryan quedan como demos).

## Hecho

- Servidor propio: VPS Hostinger KVM 2 `179.197.89.105` desde el 29-10-2026 (`docs/DEPLOYMENT_RUNBOOK.md`).
- Íconos de OneLingo en Android (adaptativo), web, favicon y página de descarga (`tools/imagenes/iconos_app.py`); nombre «OneLingo» en la app y en la web; íconos web en `web/iconos/` (Apache reserva `/icons/`).
- Shorebird configurado: la APK 0.5.4 en adelante recibe parches de código sin reinstalar.
- Planes con duraciones, Familiar, Empresarial; cobro en Android por Google Play y en la web por Stripe.
- Permiso del micrófono obligatorio para entrar al tutor.
