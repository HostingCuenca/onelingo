# OneLingo

App de aprendizaje de idiomas con IA: 10 idiomas, 10 niveles (más un Nivel 0 de
fundamentos), 100 lecciones por nivel, diagnóstico adaptativo, tutor conversacional y
voz natural. Flutter (Android, iOS, web) + backend Fastify/PostgreSQL + panel de
administración.

**Lee primero [DOCUMENTACION.md](DOCUMENTACION.md)**: estructura, cómo ejecutar cada
parte, variables de entorno, despliegue y pendientes.

```
lib/              app Flutter
backend/          API (Node 20 + Fastify + PostgreSQL)
panel/            panel de administración (Vite + React)
tools/contenido/  pipeline de contenido (semillas → JSON → assets)
```

## Arranque rápido

```bash
# Backend (necesita backend/.env, ver backend/.env.ejemplo)
cd backend && npm install && npm run migrate && npm run dev        # http://localhost:8091

# Panel
cd panel && npm install && npm run dev                              # http://localhost:5176

# App
flutter pub get && flutter run -d chrome --dart-define=API_URL=http://localhost:8091
flutter test
```

Producción: https://onelingo.hostingcuenca.com (panel en `/panel`, API en `/api`).

Las claves (`backend/.env`, `tools/contenido/.env`) no están en el repositorio; se
comparten por un canal privado.
