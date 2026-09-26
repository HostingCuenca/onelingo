# Despliegue OneLingo · 8 de septiembre de 2026

Actualización publicada en https://onelingo.hostingcuenca.com/.

- Identificador: 20260908T185618Z.
- Web Flutter release compilada con API_URL=https://onelingo.hostingcuenca.com/api.
- Backend verificado con TypeScript antes de activar; reinicio únicamente de onelingo-api.
- Panel compilado y actualizado.
- 100 ilustraciones incluidas. Código web y biblioteca publicados coinciden por SHA-256 con la compilación local.
- Credenciales .env conservadas (checksum verificado). APK anteriores y lista de archivos de audio conservadas.
- Dependencias y migraciones idénticas: no se instalaron dependencias ni se aplicaron cambios de esquema.
- Copia de seguridad en el servidor: /var/www/onelingo/backups/20260908T185618Z, incluido volcado PostgreSQL onelingo.dump y copias de backend, web y panel.
- Verificado: salud de API pública, HTTP 200 de web y panel, navegador real en bienvenida sin errores de ejecución ni recursos fallidos. Prueba sin llamadas a proveedores IA o voz.

No se generó una APK nueva en este despliegue. El servidor sigue siendo el destino provisional indicado por el usuario.
