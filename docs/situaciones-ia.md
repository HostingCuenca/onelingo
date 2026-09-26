# Situaciones y memoria del tutor

Implementación: 11 de septiembre de 2026. Foco curricular: inglés.

## Experiencia

Las tarjetas de inicio y práctica abren `/situacion/:id`. La unidad ofrece Vocabulario, Aprender, Practicar y Pruebas. Cada una tiene tres objetivos seleccionables, tres entradas de vocabulario y tres frases bilingües. Son unidades iniciales, no cursos exhaustivos de todos los niveles. El tutor adapta la complejidad a nivel, diagnóstico y respuestas; el glosario inicial es común a los niveles.

La práctica abre `/chat?situacion=1&objetivo=s1-o2&modo=practica`; la prueba usa `modo=prueba` y oculta las pistas. La apertura procede de la IA para el objetivo seleccionado. La prueba es práctica comunicativa sin ayudas sugeridas, con feedback, sin puntuación ni promoción automática. El retrato del tutor mide 108 × 138 en la unidad, 86 × 110 en chat y 104 × 136 en selección. El encabezado de chat se retira cuando se abre el teclado para dejar espacio al intercambio.

## Currículo

`assets/contenido/en/situaciones.json` y `backend/src/content/situaciones-en.json` son copias idénticas verificadas por un test. Los identificadores de objetivos son estables. Cambiar el currículo requiere actualizar ambos archivos y ejecutar el test. El backend rechaza objetivos ajenos a la situación y usa sus propios títulos y frases; no confía en el nombre enviado por el cliente para definir la misión.

## Evidencias y memoria

Los registros usan `progreso.estado.practicas` existente, con prefijos `situacion-en-…`. Las comprobaciones registran reconocimiento de vocabulario, acierto, intentos y hasta cinco resultados anteriores. Se excluyen del cálculo general de nivel por habilidad. El chat guarda objetivo, modo, uso de ayuda, correcciones y cinco resúmenes anteriores, sin XP ni marcar dominio.

El backend recupera el progreso del usuario autenticado: diagnóstico del idioma correspondiente, últimas ocho lecciones registradas y hasta cuatro evidencias de la situación (3500 caracteres máximo en el resumen). Al abrir una sesión recupera hasta dos turnos anteriores de esa cuenta, idioma y situación. Los turnos antiguos pueden pertenecer a otro objetivo; el objetivo seleccionado tiene prioridad. No se añade otra llamada a un modelo para resumir. La persistencia depende de la sincronización normal de progreso; no garantiza que un cambio recién realizado en otro dispositivo ya esté sincronizado. El historial de conversaciones se guarda después de emitir la respuesta final, como antes.

La memoria representa evidencia, no dominio certificado. El texto de STT no permite valorar pronunciación ni concluir que hubo comprensión auditiva. No se deduce una debilidad de listening solo de un error escrito. Los datos guardados se delimitan como datos, no como instrucciones.

## Latencia y compatibilidad

Una llamada LLM por turno. Conserva SSE `reply`/`final`, voz HTTP progresiva y caché existente. Se añade lectura local de PostgreSQL antes del LLM; contexto acotado. No se ha establecido un nuevo promedio de latencia ni un SLA de 1–2 segundos. El endpoint JSON anterior y otros idiomas siguen disponibles. No requiere migración de esquema ni nuevas dependencias.

## Verificación

Tests de integridad de las 50 unidades, objetivos válidos, igualdad frontend/backend, aislamiento por usuario/idioma/situación, memoria acotada, persistencia sin conceder dominio, recomendación por metas, diseño móvil 390/430 px y regresión del streaming. TypeScript y análisis Flutter de los módulos modificados. Los detalles de publicación y QA web se agregan tras ejecutarlos.

## Pendiente deliberado

Banco amplio y calibrado por nivel, evaluación estructurada de misión cumplida, algoritmo de repaso espaciado y medición real de speaking/listening. No se afirma que estén implementados. La recomendación de situación retoma la última practicada o usa una meta personal; las prioridades diagnósticas orientan al tutor y el camino de habilidades existente, no un supuesto plan generado por IA.

## Publicación y prueba real

Publicado en https://onelingo.hostingcuenca.com el 2026-09-11. Backup: `/var/www/onelingo/backups/situations-20260911-1730`. Se validó TypeScript en staging antes de activar backend/web; salud pública correcta.

30 tests Flutter y 7 backend aprobados. Navegador Chrome, cuenta QA, ancho 390: unidades 1, 20 y 50, cuatro secciones, comprobación de palabra y selección de tutores sin errores de página. Las 50 unidades están cubiertas por validación estática; no se afirma haber conversado manualmente con todas.

Chat real: objetivo `s1-o2` llegó al backend, se oyó la apertura y la respuesta al mensaje escrito de prueba. En una sesión nueva recordó la restricción de lácteos indicada antes. Un objetivo perteneciente a otra situación devolvió HTTP 400. Capturas e informes: `work/browser/situation-*.png`, `situations-report.json`, `situation-voice-report.json`.

Mediciones aisladas desde petición HTTP hasta evento `playing`: apertura 4465 ms; respuesta al mensaje 2696 ms. Son dos observaciones, no promedio ni medición desde fin de habla; el micrófono físico no formó parte de esta prueba. El objetivo de 1–2 segundos no se considera alcanzado por estas mediciones.

La QA también detectó una apertura que preguntaba por una mesa pese a tener seleccionado pedir/modificar platos. Se reforzó la instrucción para empezar directamente en el objetivo activo, dando por resueltas las etapas previas. Verificado en producción, modo prueba: «Hello! What would you like to order today?». Backup de este ajuste de prompt: `/var/www/onelingo/backups/situations-goal-20260911-1740`. Informe: `work/browser/situation-opening-report.json`.
