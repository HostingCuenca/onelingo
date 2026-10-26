-- Modo demo: los usuarios de prueba (@onelingo.demo) entran sin contraseña mientras
-- esté abierto. Cerrado, no se registran ni entran y no pueden usar al tutor. Idempotente.
ALTER TABLE ajustes_pago ADD COLUMN IF NOT EXISTS demo_activo boolean NOT NULL DEFAULT true;
