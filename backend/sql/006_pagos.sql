-- Planes y suscripciones (fase 1, Stripe en modo test). Contrato: docs/PANEL_ADMIN.md → «Planes y suscripciones».
-- El servidor es la autoridad del plan: `suscripciones` decide el acceso; `usuarios.plan_id` es un dato derivado.
-- Idempotente: se puede ejecutar más de una vez sin efecto.

CREATE TABLE IF NOT EXISTS planes (
  id text PRIMARY KEY,
  nombre jsonb NOT NULL DEFAULT '{"es":"","en":""}',
  descripcion jsonb NOT NULL DEFAULT '{"es":"","en":""}',
  incluye jsonb NOT NULL DEFAULT '{"es":[],"en":[]}',
  idiomas int NOT NULL DEFAULT 1,
  precio_centavos int NOT NULL CHECK (precio_centavos >= 0),
  moneda text NOT NULL DEFAULT 'usd',
  intervalo text NOT NULL DEFAULT 'mes' CHECK (intervalo IN ('mes', 'anio')),
  destacado boolean NOT NULL DEFAULT false,
  visible boolean NOT NULL DEFAULT true,
  orden int NOT NULL DEFAULT 0,
  archivado boolean NOT NULL DEFAULT false,
  stripe_producto_id text,
  stripe_precio_id text,
  -- Sincronización con Stripe: modo de los ids guardados (los de test no valen en live),
  -- importe/moneda/intervalo del Price guardado (para saber si hay que crear otro) y último error.
  stripe_modo text,
  stripe_precio_firma text,
  stripe_sincronizado boolean NOT NULL DEFAULT false,
  stripe_error text,
  creado_en timestamptz NOT NULL DEFAULT now(),
  actualizado_en timestamptz NOT NULL DEFAULT now()
);

INSERT INTO planes (id, nombre, descripcion, incluye, idiomas, precio_centavos, moneda, intervalo, destacado, visible, orden) VALUES
  ('p1', '{"es":"Un idioma","en":"One language"}', '{"es":"","en":""}',
   '{"es":["1 idioma a elegir","10 niveles con todas sus clases","50 situaciones de práctica","Conversación libre con IA","Corrección de errores y progreso"],
     "en":["Choose 1 language","10 levels with all their classes","50 practice situations","Free conversation with AI","Mistake correction and progress"]}',
   1, 2000, 'usd', 'mes', false, true, 1),
  ('p2', '{"es":"Dos idiomas","en":"Two languages"}', '{"es":"","en":""}',
   '{"es":["2 idiomas a elegir","Todo lo del plan de 1 idioma","Cambia de idioma cuando quieras","Progreso independiente por idioma"],
     "en":["Choose 2 languages","Everything in the 1-language plan","Switch languages whenever you want","Independent progress for each language"]}',
   2, 3000, 'usd', 'mes', true, true, 2),
  ('p3', '{"es":"Tres idiomas","en":"Three languages"}', '{"es":"","en":""}',
   '{"es":["3 idiomas a elegir","Todo lo del plan de 2 idiomas","Tutores con todas las personalidades","Certificado al completar cada nivel"],
     "en":["Choose 3 languages","Everything in the 2-language plan","Tutors with every personality","Certificate when you complete each level"]}',
   3, 4000, 'usd', 'mes', false, true, 3)
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS suscripciones (
  usuario_id uuid PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
  plan_id text NOT NULL,
  origen text NOT NULL CHECK (origen IN ('stripe', 'cortesia')),
  estado text NOT NULL CHECK (estado IN ('activa', 'prueba_stripe', 'impago', 'cancelada', 'vencida')),
  cancela_al_final boolean NOT NULL DEFAULT false,
  periodo_fin timestamptz,
  stripe_cliente_id text,
  stripe_suscripcion_id text,
  stripe_precio_id text,
  modo text CHECK (modo IN ('test', 'live')),
  nota text NOT NULL DEFAULT '',
  -- Importe real del Price del suscriptor (puede ser un precio antiguo del plan): para el MRR.
  importe_centavos int,
  moneda text,
  intervalo text CHECK (intervalo IN ('mes', 'anio')),
  creado_en timestamptz NOT NULL DEFAULT now(),
  cancelada_en timestamptz,
  actualizado_en timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS suscripciones_stripe_sub ON suscripciones (stripe_suscripcion_id);
CREATE INDEX IF NOT EXISTS suscripciones_stripe_cliente ON suscripciones (stripe_cliente_id);
CREATE INDEX IF NOT EXISTS suscripciones_estado ON suscripciones (estado);

-- Idempotencia del webhook: un evento de Stripe se procesa una sola vez.
CREATE TABLE IF NOT EXISTS pagos_eventos (
  id text PRIMARY KEY,
  tipo text NOT NULL,
  recibido_en timestamptz NOT NULL DEFAULT now(),
  procesado boolean NOT NULL DEFAULT false,
  error text
);

-- Ajustes de pago (una sola fila).
CREATE TABLE IF NOT EXISTS ajustes_pago (
  id boolean PRIMARY KEY DEFAULT true CHECK (id),
  prueba_minutos int NOT NULL DEFAULT 60 CHECK (prueba_minutos >= 0),
  moneda text NOT NULL DEFAULT 'usd',
  actualizado_en timestamptz NOT NULL DEFAULT now()
);
INSERT INTO ajustes_pago (id) VALUES (true) ON CONFLICT (id) DO NOTHING;
