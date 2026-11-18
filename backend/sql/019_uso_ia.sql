-- Cada llamada a OpenAI con su función (tutor, corrector, evaluación…): para
-- saber en qué se va el gasto. `cache` = tokens de entrada servidos desde la
-- caché de OpenAI (cuestan ~10 veces menos); `razonamiento` va dentro de `salida`.
CREATE TABLE IF NOT EXISTS uso_ia (
  id bigserial PRIMARY KEY,
  fecha timestamptz NOT NULL DEFAULT now(),
  funcion text NOT NULL,
  modelo text NOT NULL,
  entrada int NOT NULL DEFAULT 0,
  cache int NOT NULL DEFAULT 0,
  salida int NOT NULL DEFAULT 0,
  razonamiento int NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS uso_ia_fecha ON uso_ia (fecha DESC);
