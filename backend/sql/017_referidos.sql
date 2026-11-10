-- Referidos: cada vendedor tiene un código; el alumno lo escribe al registrarse
-- (o después, una sola vez) y el panel muestra quién trajo a quién y quién paga.
-- Solo seguimiento: no da descuentos ni premios automáticos.
CREATE TABLE IF NOT EXISTS referidos (
  codigo text PRIMARY KEY CHECK (codigo ~ '^[A-Z0-9-]{3,20}$'),
  vendedor text NOT NULL,
  nota text NOT NULL DEFAULT '',
  activo boolean NOT NULL DEFAULT true,
  creado_en timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS referido_codigo text REFERENCES referidos(codigo) ON UPDATE CASCADE;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS referido_en timestamptz;
CREATE INDEX IF NOT EXISTS usuarios_referido ON usuarios (referido_codigo);
