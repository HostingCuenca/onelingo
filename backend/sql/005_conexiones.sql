-- Conexiones con proveedores (ElevenLabs, OpenAI, Gemini) configuradas desde el panel.
-- `datos` = JSON cifrado (AES-256-GCM) con las claves y modelos; ver backend/src/lib/conexiones.ts.
-- Una fila aquí tiene prioridad sobre el .env del servidor; borrarla vuelve al .env.
CREATE TABLE IF NOT EXISTS conexiones (
  proveedor text PRIMARY KEY,
  datos text NOT NULL,
  actualizado_en timestamptz DEFAULT now(),
  verificacion jsonb
);
