import { crearApp } from './app.js';
import { config } from './lib/config.js';
import { migrar } from './migrate.js';
const app = await crearApp();
try {
  await migrar();
  await app.listen({ port: config.port, host: '0.0.0.0' });
} catch (e) { app.log.error(e); process.exit(1); }
