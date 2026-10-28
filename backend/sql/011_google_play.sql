-- Suscripciones compradas dentro de la app Android con Google Play Billing (docs/PANEL_ADMIN.md → «Google Play»).
-- `origen = 'google'`: el token de compra identifica la suscripción en Google; el servidor la consulta
-- (API Google Play Developer, purchases.subscriptionsv2) al verificarla y con cada notificación RTDN.
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS google_token text;
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS google_producto text;
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS google_plan_base text;
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS google_pedido text;
ALTER TABLE suscripciones DROP CONSTRAINT IF EXISTS suscripciones_origen_check;
ALTER TABLE suscripciones ADD CONSTRAINT suscripciones_origen_check CHECK (origen IN ('stripe', 'google', 'cortesia', 'familia'));
CREATE INDEX IF NOT EXISTS suscripciones_google_token ON suscripciones (google_token);
