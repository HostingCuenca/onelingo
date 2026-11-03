-- Ajustes del tutor IA editables desde el panel (Panel → Tutor IA).
-- Cada guardado es una versión nueva; la última es la activa y las anteriores
-- quedan para comparar o restaurar.
CREATE TABLE IF NOT EXISTS ajustes_tutor (
  id bigserial PRIMARY KEY,
  datos jsonb NOT NULL,
  nota text NOT NULL DEFAULT '',
  creado_en timestamptz NOT NULL DEFAULT now()
);
