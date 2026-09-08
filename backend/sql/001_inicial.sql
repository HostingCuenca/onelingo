CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS usuarios (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  nombre text NOT NULL,
  idioma_nativo text NOT NULL DEFAULT 'es',
  idioma_meta text NOT NULL DEFAULT 'en',
  nivel_inicial int NOT NULL DEFAULT 1,
  plan_id text NOT NULL DEFAULT '',
  tutor_id text NOT NULL DEFAULT 'mia',
  trial_inicio timestamptz,
  trial_segundos int NOT NULL DEFAULT 0,
  plataforma text NOT NULL DEFAULT '',
  creado_en timestamptz NOT NULL DEFAULT now(),
  ultima_actividad timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS progreso (
  usuario_id uuid PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
  estado jsonb NOT NULL,
  nivel_actual int NOT NULL DEFAULT 1,
  lecciones_completadas int NOT NULL DEFAULT 0,
  xp int NOT NULL DEFAULT 0,
  racha int NOT NULL DEFAULT 0,
  segundos_estudio int NOT NULL DEFAULT 0,
  actualizado_en timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS errores (
  id text NOT NULL,
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  skill text NOT NULL,
  original text NOT NULL,
  correccion text NOT NULL,
  explicacion text NOT NULL DEFAULT '',
  origen text NOT NULL DEFAULT '',
  practicado boolean NOT NULL DEFAULT false,
  fecha timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (usuario_id, id)
);

CREATE TABLE IF NOT EXISTS examenes (
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  nivel int NOT NULL,
  pct int NOT NULL,
  aprobado boolean NOT NULL,
  fecha timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (usuario_id, nivel)
);

CREATE TABLE IF NOT EXISTS eventos (
  id bigserial PRIMARY KEY,
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  tipo text NOT NULL,
  datos jsonb NOT NULL DEFAULT '{}',
  fecha timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS eventos_usuario_fecha ON eventos (usuario_id, fecha DESC);
CREATE INDEX IF NOT EXISTS usuarios_actividad ON usuarios (ultima_actividad DESC);
