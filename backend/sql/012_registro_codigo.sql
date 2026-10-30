-- Registro y recuperación con código de 6 dígitos por correo (OTP), y los datos
-- que se piden al registrarse: apellido y teléfono (con código de país).
ALTER TABLE usuarios
  ADD COLUMN IF NOT EXISTS apellido text NOT NULL DEFAULT '',
  ADD COLUMN IF NOT EXISTS telefono text NOT NULL DEFAULT '';

-- Un código vigente por correo y propósito. El código se guarda como HMAC, nunca
-- en claro; `datos` lleva el registro pendiente (con la contraseña ya cifrada).
CREATE TABLE IF NOT EXISTS codigos_correo (
  email text NOT NULL,
  proposito text NOT NULL CHECK (proposito IN ('registro', 'clave')),
  codigo_hash text NOT NULL,
  datos jsonb NOT NULL DEFAULT '{}',
  intentos int NOT NULL DEFAULT 0,
  envios int NOT NULL DEFAULT 1,
  primer_envio timestamptz NOT NULL DEFAULT now(),
  enviado_en timestamptz NOT NULL DEFAULT now(),
  expira timestamptz NOT NULL,
  PRIMARY KEY (email, proposito)
);
