-- Pagos, ajustes tras la fase 1 (idempotente): cambio de plan en el Customer Portal y p2 destacado.

-- p2 destacado («POPULAR» en la app) en bases donde 006 se aplicó con la semilla anterior.
-- Solo si la fila sigue intacta (nunca editada desde el panel: creado_en = actualizado_en)
-- y no hay otro destacado; así no pisa una decisión del administrador.
UPDATE planes SET destacado = true
  WHERE id = 'p2' AND NOT destacado AND creado_en = actualizado_en
    AND NOT EXISTS (SELECT 1 FROM planes WHERE destacado);

-- Historial de Prices de Stripe por plan (incluidos los archivados tras un cambio de precio):
-- el webhook encuentra el plan de un suscriptor por su Price aunque ya no sea el actual.
CREATE TABLE IF NOT EXISTS planes_precios (
  precio_id text PRIMARY KEY,
  plan_id text NOT NULL,
  modo text,
  firma text,
  creado_en timestamptz NOT NULL DEFAULT now(),
  archivado_en timestamptz
);
CREATE INDEX IF NOT EXISTS planes_precios_plan ON planes_precios (plan_id);
-- Prices ya guardados en `planes` antes de existir el historial.
INSERT INTO planes_precios (precio_id, plan_id, modo, firma)
  SELECT stripe_precio_id, id, stripe_modo, stripe_precio_firma FROM planes WHERE stripe_precio_id IS NOT NULL
  ON CONFLICT (precio_id) DO NOTHING;

-- Configuración del Customer Portal propia de OneLingo (con cambio de plan) y su modo.
ALTER TABLE ajustes_pago ADD COLUMN IF NOT EXISTS stripe_portal_id text;
ALTER TABLE ajustes_pago ADD COLUMN IF NOT EXISTS stripe_portal_modo text;
