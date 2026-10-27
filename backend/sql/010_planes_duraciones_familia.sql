-- Duraciones, plan familiar y cotizaciones para empresas (docs/PANEL_ADMIN.md → «Planes y suscripciones»).
-- Se aplica una vez (schema_migrations); la semilla solo entra al crear las columnas.

-- Duraciones extra del plan, además del cobro mensual de `precio_centavos`:
-- [{"meses":3,"precio_centavos":5500}, …]. Cada una tiene su Price en Stripe
-- (recurrente cada N meses), guardado en `planes_precios` con su firma.
-- `usuarios`: personas que cubre el plan (Familiar: el titular y 3 miembros).
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'planes' AND column_name = 'duraciones') THEN
    ALTER TABLE planes ADD COLUMN duraciones jsonb NOT NULL DEFAULT '[]';
    ALTER TABLE planes ADD COLUMN usuarios int NOT NULL DEFAULT 1 CHECK (usuarios BETWEEN 1 AND 10);
    UPDATE planes SET duraciones = '[{"meses":3,"precio_centavos":5500},{"meses":6,"precio_centavos":11000},{"meses":12,"precio_centavos":22000}]' WHERE id = 'p1' AND intervalo = 'mes';
    UPDATE planes SET duraciones = '[{"meses":3,"precio_centavos":8500},{"meses":6,"precio_centavos":17000},{"meses":12,"precio_centavos":32000}]' WHERE id = 'p2' AND intervalo = 'mes';
    UPDATE planes SET duraciones = '[{"meses":3,"precio_centavos":11000},{"meses":6,"precio_centavos":22000},{"meses":12,"precio_centavos":45000}]' WHERE id = 'p3' AND intervalo = 'mes';
    INSERT INTO planes (id, nombre, descripcion, incluye, idiomas, precio_centavos, moneda, intervalo, destacado, visible, orden, usuarios, duraciones) VALUES
      ('familiar', '{"es":"Familiar","en":"Family"}',
       '{"es":"Perfecto para familias. Cada uno con su propio perfil y progreso.","en":"Perfect for families. Everyone gets their own profile and progress."}',
       '{"es":["4 usuarios: tú y 3 personas más","1 idioma a elegir por cada usuario","Cada uno con su propio perfil y progreso","Todo lo del plan de 1 idioma"],
         "en":["4 users: you and 3 more people","Choose 1 language for each user","Everyone gets their own profile and progress","Everything in the 1-language plan"]}',
       1, 6000, 'usd', 'mes', false, true, 4, 4,
       '[{"meses":3,"precio_centavos":16500},{"meses":6,"precio_centavos":33500},{"meses":12,"precio_centavos":60000}]')
    ON CONFLICT (id) DO NOTHING;
  END IF;
END $$;

-- Planes de varios meses en Stripe: meses del periodo del Price del suscriptor.
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS meses int;
ALTER TABLE planes_precios ADD COLUMN IF NOT EXISTS meses int NOT NULL DEFAULT 1;

-- Miembros del plan familiar: el acceso del miembro es un reflejo del titular
-- (`suscripciones.origen = 'familia'`, `titular_id`). Una persona, una familia.
ALTER TABLE suscripciones ADD COLUMN IF NOT EXISTS titular_id uuid REFERENCES usuarios(id) ON DELETE CASCADE;
ALTER TABLE suscripciones DROP CONSTRAINT IF EXISTS suscripciones_origen_check;
ALTER TABLE suscripciones ADD CONSTRAINT suscripciones_origen_check CHECK (origen IN ('stripe', 'cortesia', 'familia'));
CREATE TABLE IF NOT EXISTS familia_miembros (
  titular_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  -- Correo invitado; `usuario_id` se rellena cuando existe la cuenta con ese correo.
  email text NOT NULL UNIQUE,
  usuario_id uuid UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
  creado_en timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (titular_id, email)
);

-- Plan Empresarial: solicitudes de cotización (se atienden desde el panel).
CREATE TABLE IF NOT EXISTS cotizaciones (
  id bigserial PRIMARY KEY,
  empresa text NOT NULL,
  empleados int NOT NULL CHECK (empleados > 0),
  idiomas text[] NOT NULL DEFAULT '{}',
  mensaje text NOT NULL DEFAULT '',
  nombre text NOT NULL DEFAULT '',
  email text NOT NULL,
  telefono text NOT NULL DEFAULT '',
  usuario_id uuid REFERENCES usuarios(id) ON DELETE SET NULL,
  estado text NOT NULL DEFAULT 'nueva' CHECK (estado IN ('nueva', 'contactada', 'cerrada')),
  nota text NOT NULL DEFAULT '',
  creado_en timestamptz NOT NULL DEFAULT now(),
  actualizado_en timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS cotizaciones_estado ON cotizaciones (estado, creado_en DESC);
