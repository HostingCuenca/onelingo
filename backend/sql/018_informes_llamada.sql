-- Informe de cada videollamada para la retroalimentación del alumno y del tutor:
-- el resumen que ve el alumno, la evaluación pedagógica del tutor (cómo habló y
-- cómo enseñó, con citas) y los datos técnicos (escucha en vivo o pulsar,
-- cortes, voz de ElevenLabs o de respaldo). Se borra con la cuenta.
CREATE TABLE IF NOT EXISTS informes_llamada (
  id bigserial PRIMARY KEY,
  usuario_id uuid NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  idioma text NOT NULL,
  nivel int NOT NULL,
  tutor_id text NOT NULL,
  explica text NOT NULL DEFAULT 'meta',
  turnos int NOT NULL DEFAULT 0,
  resumen jsonb,
  evaluacion jsonb,
  tecnico jsonb NOT NULL DEFAULT '{}',
  nota numeric(3,1),
  creado_en timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS informes_llamada_usuario ON informes_llamada (usuario_id, creado_en DESC);
CREATE INDEX IF NOT EXISTS informes_llamada_fecha ON informes_llamada (creado_en DESC);
CREATE INDEX IF NOT EXISTS informes_llamada_tutor ON informes_llamada (tutor_id, creado_en DESC);
