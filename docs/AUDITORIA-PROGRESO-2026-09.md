# Auditoría de progreso — septiembre 2026

## Cambios conservadores

- `ProgressState.rachaVigente` calcula la racha visible: último día hoy/ayer conserva la cadena; anteriores muestran cero. `rachaEn(DateTime)` permite probar límites civiles sin esperas. Se conserva `racha` histórico.
- `diasActividad` guarda fechas de actividad reales, se serializa y no reconstruye semanas supuestas. Migración de estado antiguo sólo incorpora `ultimoDia` conocido.
- Repetir una lección mantiene el mejor porcentaje y no vuelve a otorgar XP. `completadas` conserva significado histórico de participación: no representa dominio. No se borran lecciones ni XP existentes.
- Los exámenes conservan el mejor resultado y un aprobado no se revoca por fallar el repaso. XP por primer intento fallido: 20; por primera aprobación: 200. Repeticiones posteriores: cero. El evento de examen sigue enviando la nota del intento; el mapa persistido representa mejor resultado.
- Prácticas aceptan `habilidad` como alias de `skill`. `primeraCorrecta` y `primeraFecha` conservan primera evidencia. Si un registro antiguo sólo tuvo un intento, esa evidencia puede conservarse; si ya se repitió no se inventa su primera respuesta. XP por ítem sigue concediéndose una sola vez; repetir sí es actividad para la racha.

No se reducen puntajes existentes ni se recalculan logros históricos. El backend acepta campos nuevos por esquema passthrough, pero todavía no es autoridad de estos premios.

## Hallazgos pendientes

1. El inicio muestra tres habilidades prioritarias. Una habilidad puede desaparecer de esa recomendación tras éxitos aunque permanezca en biblioteca. Accesos permanentes y recomendación deben distinguirse.
2. Inglés usa biblioteca, mientras indicadores de perfil aún usan lecciones del sistema antiguo. Debe unificarse el progreso por idioma, nivel y objetivo.
3. Completar con cero aciertos sigue significando completar actividad. Es necesario añadir dominio separado, no reinterpretar retrospectivamente `completadas`.
4. Examen legacy: diez preguntas principalmente selección múltiple/gramática. No demuestra listening, escritura o conversación. Umbral65% equivale en la práctica a siete respuestas sobre diez.
5. Examen dirige a errores sin registrar los fallos individuales. Es necesaria revisión específica.
6. Backend reemplaza instantánea de progreso sin versión: posible pérdida entre dispositivos. Necesita eventos idempotentes o control de concurrencia.
7. Revisar rutas antiguas `/usuarios/login` y `/usuarios/registro`: código admite acceso por correo sin contraseña. No se probó exposición en producción. Revisar también aceptación de `planId`, XP y calificaciones enviados por cliente antes de confiar en ellos.
8. `vocabularioAprendido` suma exposiciones y puede repetir palabras. Etiquetar como practicado hasta contar recuperación independiente y retención.

## Semántica propuesta

Actividad registra esfuerzo; finalización registra participación; dominio requiere evidencia independiente y retención. Un repaso fallido crea refuerzo, no borra el camino. Secuencia de unidad: vocabulario → explicación y ejemplos → práctica guiada → lectura/listening contextual → prueba nueva → repaso espaciado.

## Validación

Archivo `test/progreso_integridad_test.dart`: límites de racha, migración de fechas sin inventar historial, repetición de exámenes y lecciones, XP idempotente, persistencia de primera evidencia y ausencia de falsificación de intentos antiguos. El agente preparó archivos fuera del proyecto por aislamiento de permisos; la ejecución y resultado final de estas pruebas corresponde a integración por el agente principal.


## Estado final de integración

Consultar PLAN-APRENDIZAJE-2026-09-19.md para el resultado actualizado. La entrega pasó de 20 a 43 temas de gramática y amplió las 50 situaciones a 550 entradas. Se corrigieron transcripción de apoyo persistente entre unidades, orden de opciones léxicas, nivel fijo en agrupación de lecturas, acceso permanente a las cinco áreas y preferencia de animaciones/texto grande en racha. Estos documentos conservan hallazgos de la revisión inicial; no todos siguen pendientes.
