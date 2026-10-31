-- Requisitos de Google Play (31-10-2026): eliminar la cuenta desde la app y denunciar respuestas de la IA.
-- Contrato: backend/src/lib/cuenta.ts (DELETE /usuarios/me) y backend/src/routes/reportes.ts (/reportes-ia).

-- Denuncias del alumno sobre una respuesta del tutor de IA (chat, videollamada…).
-- Se borran con la cuenta (ON DELETE CASCADE): quedan ligadas a quien las hizo.
CREATE TABLE IF NOT EXISTS reportes_ia (
  id bigserial PRIMARY KEY,
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  origen text NOT NULL CHECK (origen IN ('chat', 'llamada', 'situacion', 'ejercicio', 'otro')),
  motivo text NOT NULL CHECK (motivo IN ('ofensivo', 'incorrecto', 'inapropiado', 'otro')),
  -- Respuesta denunciada (máx. 2000) y comentario opcional del alumno (máx. 500).
  texto text NOT NULL,
  comentario text NOT NULL DEFAULT '',
  -- Idioma, tutor y situación de la conversación: {"idioma":"fr","tutorId":"mia","situacion":"…"}.
  contexto jsonb NOT NULL DEFAULT '{}',
  revisado boolean NOT NULL DEFAULT false,
  creado_en timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS reportes_ia_usuario_fecha ON reportes_ia (usuario_id, creado_en DESC);
CREATE INDEX IF NOT EXISTS reportes_ia_fecha ON reportes_ia (creado_en DESC);

-- Cuentas que su titular eliminó. Solo se guarda lo que la ley obliga a conservar de
-- una suscripción de pago (referencias de Stripe / Google Play, plan e importe), sin
-- nombre, correo ni teléfono. Las cuentas sin pagos no dejan fila.
CREATE TABLE IF NOT EXISTS cuentas_eliminadas (
  id bigserial PRIMARY KEY,
  eliminada_en timestamptz NOT NULL DEFAULT now(),
  origen_pago text NOT NULL CHECK (origen_pago IN ('stripe', 'google')),
  plan_id text NOT NULL DEFAULT '',
  estado_pago text NOT NULL DEFAULT '',
  modo text,
  stripe_cliente_id text,
  stripe_suscripcion_id text,
  google_pedido text,
  importe_centavos int,
  moneda text,
  meses int,
  -- Qué pasó con la suscripción al eliminar: 'cancelada_stripe', 'ya_cancelada', 'cancelar_en_google_play'…
  accion text NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS cuentas_eliminadas_fecha ON cuentas_eliminadas (eliminada_en DESC);
