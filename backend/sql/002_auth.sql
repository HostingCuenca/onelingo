ALTER TABLE usuarios
  ADD COLUMN IF NOT EXISTS password_hash text,
  ADD COLUMN IF NOT EXISTS google_id text UNIQUE,
  ADD COLUMN IF NOT EXISTS email_verificado boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS token_verificacion text,
  ADD COLUMN IF NOT EXISTS token_reset text,
  ADD COLUMN IF NOT EXISTS reset_expira timestamptz,
  ADD COLUMN IF NOT EXISTS es_demo boolean NOT NULL DEFAULT false;

CREATE TABLE IF NOT EXISTS correos (
  id bigserial PRIMARY KEY,
  para text NOT NULL,
  asunto text NOT NULL,
  cuerpo text NOT NULL,
  enviado boolean NOT NULL DEFAULT false,
  detalle text NOT NULL DEFAULT '',
  fecha timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversaciones (
  id bigserial PRIMARY KEY,
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  situacion_id int,
  nivel int NOT NULL,
  idioma text NOT NULL,
  tutor_id text NOT NULL,
  mensaje_alumno text NOT NULL,
  respuesta jsonb NOT NULL,
  modelo text NOT NULL DEFAULT '',
  tokens_entrada int NOT NULL DEFAULT 0,
  tokens_salida int NOT NULL DEFAULT 0,
  fecha timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS conversaciones_usuario ON conversaciones (usuario_id, fecha DESC);
