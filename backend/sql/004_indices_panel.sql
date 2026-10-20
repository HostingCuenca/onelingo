-- Índices para las analíticas del panel de administración (docs/PANEL_ADMIN.md).
CREATE INDEX IF NOT EXISTS eventos_fecha ON eventos (fecha DESC);
CREATE INDEX IF NOT EXISTS eventos_tipo_fecha ON eventos (tipo, fecha DESC);
CREATE INDEX IF NOT EXISTS conversaciones_fecha ON conversaciones (fecha DESC);
CREATE INDEX IF NOT EXISTS usuarios_creado ON usuarios (creado_en DESC);
CREATE INDEX IF NOT EXISTS errores_skill ON errores (skill);
