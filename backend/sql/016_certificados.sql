-- Certificado de cada nivel superado (N1–N10) por alumno e idioma. El código es
-- la dirección pública de verificación: /certificado/<codigo>.
CREATE TABLE IF NOT EXISTS certificados (
  codigo text PRIMARY KEY,
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  idioma text NOT NULL,
  nivel text NOT NULL,
  nombre text NOT NULL,
  via text NOT NULL,
  lengua text NOT NULL DEFAULT 'es',
  logrado_en timestamptz,
  emitido_en timestamptz NOT NULL DEFAULT now(),
  UNIQUE (usuario_id, idioma, nivel)
);
