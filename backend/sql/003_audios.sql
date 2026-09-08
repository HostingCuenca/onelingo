-- Audios de voz (ElevenLabs) generados una sola vez y reutilizados.
CREATE TABLE IF NOT EXISTS audios (
  hash text PRIMARY KEY,
  idioma text NOT NULL,
  voz text NOT NULL,
  voz_id text NOT NULL,
  modelo text NOT NULL,
  texto text NOT NULL,
  caracteres int NOT NULL,
  bytes int NOT NULL,
  usos int NOT NULL DEFAULT 1,
  creado_en timestamptz NOT NULL DEFAULT now(),
  ultimo_uso timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS audios_idioma ON audios (idioma, creado_en DESC);
