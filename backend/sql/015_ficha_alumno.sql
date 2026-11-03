-- Ficha que el tutor IA lleva de cada alumno por idioma: quién es, qué domina,
-- sus errores de siempre, cómo aprende mejor y su plan. Se actualiza en segundo
-- plano con las conversaciones nuevas (hasta `ultima_conversacion`).
CREATE TABLE IF NOT EXISTS ficha_alumno (
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  idioma text NOT NULL,
  datos jsonb NOT NULL,
  ultima_conversacion bigint NOT NULL DEFAULT 0,
  actualizado_en timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (usuario_id, idioma)
);
