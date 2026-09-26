# Despliegue UI y mascotas — 19 septiembre 2026

Publicación: https://onelingo.hostingcuenca.com/?release=ui-mascotas-20260919

- Web release con API_URL=https://onelingo.hostingcuenca.com/api.
- Interfaz y aprendizaje, tabs persistentes, tipografía y tarjetas, mascotas transparentes.
- Lumo de Inicio usa idle reutilizable de parpadeo: movimiento breve con ~3.2s de pausa; WebP transparente320px, ~204KiB, repetición continua. Respeta movimiento reducido, ajuste local y TickerMode.
- Backend: únicamente lib/situaciones.ts y content/situational-vocabulary-en.json diferían; validados TypeScript local y staging. Cuatro pruebas del contenido/contexto pasaron. Reiniciado solo onelingo-api.
- Sin cambios de esquema ni dependencias. .env verificado por checksum. APK y directorio avatar existentes conservados.
- Respaldo: /var/www/onelingo/backups/ui-mascotas-20260919 (web y src backend). Web anterior adicional en /var/www/onelingo/staging/ui-mascotas-20260919/previous-web.
- Script con rollback: work/deploy/ui-mascotas-activate.sh.
- Hash main.dart.js: 8ed5666f4242f04cccb0a6dfcca9e5a8e6c2a99e74fcc3ec8f049da4cec572ff.
- Hash lumo-idle-alpha.webp: d3c22d8331b78e13ef01ee97ec833e3945a05d5191dab9ce85bead5d10f87719.
- Activación y salud pública confirmadas. Diez tests UI anteriores y cuatro tests focalizados de navegación/mascotas antes de publicación.

Referencia: https://blog.duolingo.com/new-duolingo-home-screen-design/ y https://blog.duolingo.com/world-character-visemes/ . Su diseño comunica una siguiente acción dentro de un camino y usa personajes con animaciones de reposo. OneLingo todavía funciona más como panel de accesos por áreas; dar prioridad a un único CTA Continuar sigue siendo una mejora pendiente, sin confundir práctica guiada con dominio.
