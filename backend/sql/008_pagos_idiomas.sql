-- Idiomas por suscripción (anexo pagos_contrato_idiomas.md). Idempotente.
-- Un plan incluye N idiomas (`planes.idiomas`; 0 = todos) y el alumno elige cuáles.

ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS idiomas text[] NOT NULL DEFAULT '{}';
-- Inicio del periodo de facturación actual (Stripe): la regla «uno_por_periodo» cuenta desde aquí.
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS periodo_inicio timestamptz;
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS ultimo_cambio_idiomas timestamptz;
-- Cortesía «todos los idiomas» aunque el plan tenga N (con un plan de 0 idiomas ya son todos).
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS todos_idiomas boolean NOT NULL DEFAULT false;

-- Regla para que el alumno cambie un idioma por otro: libre | uno_por_periodo | solo_admin.
ALTER TABLE ajustes_pago ADD COLUMN IF NOT EXISTS cambio_idiomas text NOT NULL DEFAULT 'uno_por_periodo';
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ajustes_pago_cambio_idiomas_check') THEN
    ALTER TABLE ajustes_pago ADD CONSTRAINT ajustes_pago_cambio_idiomas_check CHECK (cambio_idiomas IN ('libre', 'uno_por_periodo', 'solo_admin'));
  END IF;
  -- `planes.idiomas`: 0 = todos los idiomas; como mucho los 10 de la app.
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'planes_idiomas_check') THEN
    ALTER TABLE planes ADD CONSTRAINT planes_idiomas_check CHECK (idiomas BETWEEN 0 AND 10);
  END IF;
END $$;
