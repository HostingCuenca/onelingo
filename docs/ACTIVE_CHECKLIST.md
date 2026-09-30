# Checklist activo de transferencia

## Al abrir el proyecto en otra cuenta

- [ ] Abrir `/home/roggrt/Documents/onelingo` como proyecto local existente.
- [ ] Leer `AGENTS.md` y `docs/CODEX_HANDOFF.md`.
- [ ] Ejecutar `git status --short --branch` y `git log --oneline -5`.
- [ ] Confirmar que se está en `claude/educacion-multilenguaje` o explicar cualquier diferencia.
- [ ] Tratar el árbol actual como deliberadamente sucio: inventariar cambios y no descartar ni sobrescribir archivos; el commit base esperado sigue siendo `d4e2dcd`.
- [ ] Verificar que Higgsfield aparece instalado y conectado en la cuenta nueva; reautorizar si lo solicita.
- [ ] No copiar tokens, cookies, `~/.codex`, `.env` o claves entre cuentas.
- [ ] Comprobar solamente los servicios necesarios para la tarea solicitada.

## Estado funcional por cerrar

- [x] Confirmar el estado de `20260926-edu-3-escrituras`: su alcance quedó absorbido por `20260929-edu-4-n1-runtime` y no debe desplegarse por separado.
- [x] Ejecutar M1 del plan editorial: dry-run reproducible de 36 unidades y 528 variantes, con 0 errores y sin aplicar activos.
- [x] Adoptar N1 = A1 completo y escala cliente versionada (DEC-020).
- [x] Implementar y probar aliases conservadores para diagnóstico y progreso históricos.
- [x] Integrar la biblioteca con estados por unidad `legacy → shadow → active`; N1 está `active`, consume la biblioteca real y fue publicado en `20260929-edu-4-n1-runtime`.
- [x] Producir el primer bloque de cinco clases de Inglés N1 con bancos separados de práctica, evaluación y repaso; permanece en `shadow`.
- [x] Producir y validar longitudinalmente el segundo bloque de Inglés N1, clases 6–10; permanece en `shadow`.
- [x] Producir y validar longitudinalmente el tercer bloque de Inglés N1, clases 11–15; permanece en `shadow`.
- [x] Completar el cuarto bloque de Inglés N1, clases 16–20; validado e integrado en `shadow` con cierre acumulativo.
- [x] Completar el bloque Inglés N1 21–25; integrado en `shadow` con 65 ejercicios, soporte visual opcional y sin tutor IA en runtime.
- [x] Completar el bloque Inglés N1 26–30; integrado en `shadow` con 65 ejercicios deterministas, dos ilustraciones espaciales nuevas y cierre acumulativo de instrucciones.
- [x] Completar el bloque Inglés N1 31–35; integrado en `shadow` con 65 ejercicios deterministas, lectura, audio TTS y evaluación mixta de cuatro formatos.
- [x] Completar el bloque Inglés N1 36–40; integrado en `shadow` con 65 ejercicios deterministas sobre rutinas, verbo base y orden de lugar/tiempo.
- [x] Completar el bloque Inglés N1 41–45; integrado en `shadow` con 65 ejercicios deterministas sobre tercera persona, terminaciones y concordancia.
- [x] Completar el bloque Inglés N1 46–50; integrado en `shadow` con 65 ejercicios deterministas sobre negación, respuestas cortas y preguntas `Do/Does`.
- [x] Completar el bloque Inglés N1 51–55; integrado en `shadow` con 65 ejercicios deterministas sobre preguntas WH, hora, `who` como sujeto y agendas de dos personas.
- [x] Completar el bloque Inglés N1 56–60; integrado en `shadow` con 65 ejercicios deterministas sobre frecuencia, posición con `be`, preposiciones temporales y calendario personal.
- [x] Completar el bloque Inglés N1 61–65; integrado en `shadow` con 65 ejercicios deterministas de producción de rutinas, lectura de horarios, escucha y evaluación mixta.
- [x] Completar el bloque Inglés N1 66–70; integrado en `shadow` con 65 ejercicios deterministas sobre capacidad, preguntas con `can` y gustos con sustantivos o actividades en `-ing`.
- [x] Completar el bloque Inglés N1 71–75; integrado en `shadow` con 65 ejercicios deterministas sobre pronombres objeto, sustitución de nombres, pronombres posesivos y pertenencia con `Whose`, más cierre acumulativo.
- [x] Completar el bloque Inglés N1 76–80; integrado en `shadow` con 65 ejercicios deterministas sobre contables/incontables, `some/any`, `How many/How much`, lista de compras y cantidades en el mercado, más cierre acumulativo.
- [x] Completar el bloque Inglés N1 81–85; integrado en `shadow` con 65 ejercicios deterministas sobre `I'd like`, `Can I have`, `Could I`, restaurante básico y diálogo cliente/mesero, más cierre acumulativo.
- [x] Completar el bloque Inglés N1 86–90; integrado en `shadow` con 65 ejercicios deterministas sobre presente continuo, contraste con presente simple y conectores.
- [x] Completar el bloque Inglés N1 91–95; integrado en `shadow` con 65 ejercicios deterministas de encuentros, cafetería, invitaciones, simulación y evaluación A1.
- [x] Completar el bloque Inglés N1 96–100; integrado en `shadow` con 65 ejercicios deterministas de repaso, evaluación final, conversación guiada y proyecto.
- [x] Sanear las remediaciones legacy C1/C3/C4/C5 y retirar el uso prematuro de `of` en C5. C6/C9/C10 y la cronología de `it`/`see` también están corregidas y validadas.
- [x] Completar Inglés N1 (100 clases, 1.300 ejercicios) antes de escalar a N2–N10 y a los demás idiomas.
- [x] Conectar Inglés N1 al recorrido real local: 100 unidades, metadatos de selección persistidos, repaso aislado y aliases históricos `a1-1`/`a1-2` hacia `n1`.
- [x] Rediseñar el mapa de Inglés N2 como 20 bloques completos de cinco fases, sin repetir mecánicamente la alternancia de destrezas del PDF.
- [x] Poblar y validar Inglés N2 C1–C15: 15 clases, 195 ejercicios, tres cierres acumulativos y simulaciones de cinco perfiles; permanece en `shadow`.
- [x] Poblar y validar Inglés N2 C16–C30 bajo `editorial-agent.v2`: 15 clases, 195 ejercicios, revisión cruzada, tres cierres acumulativos y validación longitudinal C1–C30; permanece en `shadow`.
- [x] Poblar Inglés N2 C31–C45 bajo `editorial-agent.v2`: 15 clases, 195 ejercicios, tres cierres acumulativos, revisión cruzada y validación longitudinal C1–C45; permanece en `shadow`.
- [x] Poblar y validar Inglés N2 C46–C60 con el contrato v2 y revisión cruzada; permanece en `shadow`.
- [x] Poblar y validar Inglés N2 C61–C75 con el contrato v2 y revisión cruzada; permanece en `shadow`.
- [x] Poblar y validar Inglés N2 C76–C90 con el contrato v2 y revisión cruzada; permanece en `shadow`.
- [x] Poblar y validar Inglés N2 C91–C100 con el contrato v2 y revisión cruzada; N2 queda completo con 100 clases y 1.300 ejercicios en `shadow`.
- [x] Diseñar y validar el mapa editorial v2 de Inglés N3: 100 clases, 20 ciclos y continuidad explícita desde N2 C100.
- [x] Poblar y validar Inglés N3 C1–C30: 30 clases y 390 ejercicios en `shadow`, con revisión independiente y validación longitudinal.
- [x] Poblar y validar Inglés N3 C31–C45: 15 clases y 195 ejercicios integrados en `shadow` tras GO independiente; incluye completar multiparte, umbrales parciales y partes obligatorias consumidas por la UI.
- [x] Poblar y validar Inglés N3 C46–C70: 25 clases y 325 ejercicios integrados en `shadow` tras corrección adversarial y GO independiente.
- [x] Poblar y validar Inglés N3 C71–C80: 10 clases y 130 ejercicios integrados en `shadow` tras auditoría iterativa, simulación de estudiantes y GO independiente.
- [x] Poblar y validar Inglés N3 C81–C90: 10 clases y 130 ejercicios integrados en `shadow`; incluye rúbricas deterministas para escritura libre, remediación por habilidad y GO independiente.
- [x] Auditar las 290 clases publicadas y pulirlas (auditoría 2026-09-30): app, enriquecimiento 290/290, pistas de completar, correcciones de ítems.
- [ ] Desplegar `20260930-edu-6-pulido` (build local listo; requiere autorización).
- [ ] Activar compresión gzip de JSON en Apache (requiere autorización; ~7 MB → ~1 MB).
- [ ] Separar el léxico de validación del vocabulario enseñado (auditoría #15).
- [ ] Producir Inglés N3 C91–C95 (`community-project`) en staging, con autoría, simulación, corrección y GO independiente.
- [ ] Producir Inglés N3 C96–C100 (`b1-entry-capstone`) y revisar el bloque completo por ser cierre de nivel.
- [ ] Auditar longitudinalmente N3 C1–C100 y, solo tras GO, ampliar el runtime de 290 a 300 clases.
- [ ] Crear y aprobar `mapa-n4-editorial-v2.json` antes de iniciar autoría de N4; repetir la puerta por cada nivel hasta N10.
- [ ] Vincular las 43 guías gramaticales a IDs del grafo.
- [ ] Modelar progreso de vocabulario por palabra y situación.
- [ ] Convertir «restaurante» en mini-ruta piloto y mapear las 50 situaciones.
- [ ] Pasar los metadatos de unidad al tutor IA.
- [ ] Probar voces y sonidos en dispositivo real.
- [ ] Revisar pedagógicamente los nueve idiomas marcados como versión inicial.

## Tutor/avatar

- [ ] Medir latencia STT, LLM y TTS en un turno real y guardar trazas de servidor/cliente.
- [ ] Pilotar un avatar humano 2D Rive reutilizable con estados y visemas temporizados.
- [ ] Resolver alineación fonética de ElevenLabs por idioma antes de declarar lip-sync.
- [ ] Mantener un botón explícito de detener grabación además del corte a 3 s de silencio.
- [ ] Conectar tutor, unidad, vocabulario, gramática y errores recientes del alumno.
- [ ] Decidir la experiencia Android; hoy el 3D solo funciona en web.

## Android y release

- [ ] Configurar firma release propia y segura.
- [ ] Incrementar `version`/`versionCode` en cada APK distribuida.
- [ ] Elegir estrategia de actualización: tienda o contenedor web controlado.
- [ ] Compilar y probar APK en dispositivo real antes de publicar.

## Antes de producción

- [x] Ejecutar validaciones pertinentes y registrar resultados para `20260929-edu-4-n1-runtime`.
- [x] Confirmar que el build usa `API_URL=https://onelingo.hostingcuenca.com/api`.
- [x] Crear lock y backup con nombre de release.
- [x] Preservar `web/apk/`, `web/avatar/`, `.env`, audio cache y servicios ajenos.
- [x] Validar `/api/salud`, rutas críticas y recorrido real del navegador.
- [x] Registrar backup, hash, resultado y rollback en `docs/claude-educacion/DESPLIEGUES.md`.
- [x] Publicar y verificar `20260930-edu-5-n2-n3-review`: N1 100, N2 100 y N3 90; 290 unidades activas/3.770 ejercicios; C91 ausente.
- [x] Confirmar visualmente `#/ruta/n2` y `#/ruta/n3`; preservar backend, `.env`, APK y avatar.
