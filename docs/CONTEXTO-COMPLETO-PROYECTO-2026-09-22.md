# OneLingo — contexto completo del proyecto

**Fecha de corte:** 22 de septiembre de 2026  
**Estado revisado:** código local, arquitectura, experiencia pedagógica, tutor de voz, avatares, despliegue y producción  
**Producción:** <https://onelingo.hostingcuenca.com/>  
**Proyecto local:** `/home/roggrt/Documents/onelingo`

> Este documento sirve como punto de entrada para continuar el proyecto sin reconstruir toda la conversación. No contiene claves, contraseñas, tokens ni valores secretos. Los proveedores y variables se nombran únicamente para describir la arquitectura.

## 1. Visión del producto

OneLingo es una plataforma de aprendizaje de idiomas centrada inicialmente en inglés. Busca combinar una ruta pedagógica estructurada con personalización mediante IA, práctica contextual, diagnóstico progresivo, comprensión auditiva, lectura, escritura y conversación por voz.

La aplicación no debe convertirse en un chat abierto que improvisa todo el contenido. La estructura pedagógica, los objetivos de cada nivel y las reglas de progresión deben ser deterministas. La IA se usa para adaptar explicaciones, ejemplos, práctica, retroalimentación y conversación al perfil y a las debilidades del estudiante.

Objetivos principales:

- Enseñar antes de evaluar.
- Introducir vocabulario y gramática antes de pedir producción libre.
- Dar retroalimentación inmediata después de cada respuesta.
- Medir habilidades por separado: vocabulario, gramática, lectura, listening, escritura y speaking.
- Construir un perfil de dominio por habilidad, no asignar un nivel solamente por el promedio.
- Personalizar ejemplos y situaciones según sector profesional, condición de estudiante y objetivos.
- Mantener sesiones breves, dinámicas y visualmente claras.
- Preparar posteriormente rutas de certificación con bancos y criterios propios del examen elegido.

## 2. Decisiones de alcance vigentes

- **Idioma prioritario:** inglés. Los demás idiomas se muestran y conservan en la arquitectura, pero el contenido profundo se está construyendo primero para inglés.
- **Trabajo sin conexión:** queda previsto para una fase posterior. La arquitectura de contenidos debe permitir bancos locales, pero no es un requisito inmediato.
- **Diagnóstico:** debe ser adaptativo. Parte del nivel declarado por el usuario, sube la dificultad si responde bien y la reduce o finaliza si acumula evidencia suficiente de dificultad.
- **Contenido:** se combinan bancos controlados con generación o evaluación mediante IA. No se debe depender de generación remota para cada pregunta.
- **Niveles internos:** la aplicación puede usar una progresión más granular que A1–C2, pero cada nivel interno debe mantener una equivalencia explícita con MCER/CEFR.
- **Certificaciones:** TOEFL, Cambridge, IELTS u otras requieren rutas separadas. No se debe afirmar preparación o predicción de aprobación basándose únicamente en ejercicios generales.
- **Avatares:** son personajes reutilizables renderizados en tiempo real. No se generarán videos nuevos para cada intervención del tutor.
- **Producción:** ya existe y se usa para pruebas; todo cambio debe probarse localmente antes del despliegue.

## 3. Arquitectura técnica

### Frontend principal

- Flutter y Dart.
- Gestión de estado con Riverpod.
- Persistencia ligera con `SharedPreferences`.
- Compilación web para producción y Android/APK para dispositivos.
- El módulo 3D del tutor se integra como experiencia web con Three.js dentro de un `iframe` del frontend Flutter web.

Directorios relevantes:

```text
lib/                  aplicación Flutter
assets/               imágenes, fuentes, sonidos y contenidos empaquetados
content/              contenido por idioma
web/avatar/           experiencia 3D y conversación del tutor
test/                  pruebas Flutter
```

### Backend

- Node.js 20.
- TypeScript.
- Fastify 5.
- PostgreSQL.
- Autenticación JWT.
- Procesos administrados con PM2.
- Apache sirve el frontend y actúa como proxy para la API.

Directorios relevantes:

```text
backend/src/           servidor y módulos de API
backend/sql/           esquemas o migraciones SQL
backend/test/          pruebas del backend
backend/audio/         almacenamiento/caché relacionado con audio
```

### Producción

- Dominio: `onelingo.hostingcuenca.com`.
- Servidor utilizado durante los despliegues actuales: `167.235.20.41`.
- El servidor actual es operativo para esta etapa, pero no se considera necesariamente la infraestructura definitiva de la aplicación.
- El frontend debe compilarse indicando la API pública:

```bash
flutter build web --release \
  --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
```

No se deben registrar credenciales de SSH, contraseñas, claves privadas ni valores de `.env` en este documento o en Git.

## 4. Proveedores de IA y voz

### OpenAI

- Tutor conversacional: `gpt-4.1-mini`.
- Evaluación de escritura: `gpt-4.1` en las rutas que requieren análisis más profundo.
- STT: `gpt-4o-mini-transcribe`.
- El tutor usa respuestas estructuradas y el backend puede exponer el resultado al cliente por SSE.

### Gemini

- Modelo usado para generación económica de contenido: `gemini-flash-latest`.
- Su función prevista es ayudar a generar variaciones, contenido contextual o material que después debe validarse y almacenarse.

### ElevenLabs

- TTS de producción actual: `eleven_flash_v2_5`.
- Se conservaron las voces ya asociadas a los tutores.
- El audio se entrega como MP3 y existe transmisión progresiva/caché en la integración actual.
- El modelo anterior, `eleven_multilingual_v2`, tenía una latencia inicial notablemente mayor para conversación interactiva.

## 5. Flujo actual de conversación por voz

```text
usuario activa el micrófono
→ MediaRecorder captura audio
→ medición de amplitud en cliente
→ detección de silencio o parada manual
→ se cierra el archivo de audio completo
→ HTTP al endpoint de transcripción
→ OpenAI STT
→ texto transcrito
→ HTTP/SSE al endpoint de chat
→ OpenAI LLM genera respuesta del tutor
→ se recibe primero el texto útil de respuesta
→ petición al endpoint de voz
→ ElevenLabs Flash genera MP3
→ reproducción progresiva con MediaSource cuando está disponible
→ amplitud del audio anima boca/rostro y aparecen ondas de voz
```

Comportamiento del fin de turno:

- El usuario puede detener manualmente la grabación.
- La detección automática usa amplitud y espera aproximadamente **3 segundos de silencio**.
- Hay un límite máximo aproximado de **60 segundos** por grabación.
- Si no se detecta voz, existe un cierre de seguridad cercano a **15 segundos**.
- La grabación actual no es STT continuo: el servidor comienza la transcripción después de cerrar el archivo.
- La detección por amplitud no equivale a un VAD semántico robusto y puede verse afectada por ruido, micrófonos de baja ganancia o pausas naturales.

### Inicio del tutor

- El tutor inicia la conversación automáticamente cuando el avatar y la experiencia están listos.
- También presenta el contexto al cambiar de situación.
- La interfaz distingue estados como `pensando`, `preparando voz` y `hablando`.
- Durante la voz se muestran ondas animadas para evitar silencios visualmente ambiguos.

## 6. Latencia observada

Mediciones realizadas durante las pruebas:

| Etapa | Tiempo observado |
|---|---:|
| Espera fija por silencio | ~3000 ms |
| STT | ~850–2690 ms |
| LLM hasta respuesta útil | ~660–1540 ms; algunos saludos ~2150 ms |
| ElevenLabs Multilingual, primer byte | ~1838 ms |
| ElevenLabs Multilingual, completo | ~1875 ms |
| ElevenLabs Flash, primer byte | ~166 ms |
| ElevenLabs Flash, completo | ~278 ms |
| Saludo completo sin caché, primera voz | ~2634 ms |
| Saludo completo con caché, primera voz | ~1958 ms |

Prueba de producción registrada para la versión `voice-waves16`:

```json
{
  "autoGreeting": true,
  "situationGreeting": true,
  "waves": true,
  "phase": "speaking",
  "replyReadyMs": 1751,
  "firstAudioMs": 1958,
  "errors": []
}
```

Conclusión actual: el cambio a ElevenLabs Flash resolvió gran parte de la latencia del TTS. El mayor tiempo evitable permanece en el fin de voz y en el envío posterior del archivo completo al STT. Para acercarse de forma estable a 1–2 segundos después de hablar, la siguiente mejora estructural será un canal de audio continuo con VAD y STT en streaming, o una arquitectura Realtime/WebRTC equivalente.

## 7. Tutor 3D y avatares

Existe una biblioteca de diez tutores, cinco mujeres y cinco hombres, con diversidad visual y cultural:

- Amara
- Sofía
- Lucía
- Clara
- Mei
- Malik
- Mateo
- Owen
- Daniel
- Kenji

Estado técnico:

- Los personajes se cargan en formato GLB.
- Cada modelo pesa aproximadamente 20–25 MB.
- Se descarga un solo avatar al seleccionar el tutor; no deben cargarse los diez simultáneamente.
- Three.js renderiza el modelo en navegador.
- La tasa visual se limitó a 30 fps para reducir carga sin perder fluidez útil.
- Los brazos se corrigen en tiempo de ejecución para evitar una presentación permanente en A-pose/T-pose.
- Hay mejoras de piel, ojos, boca, lengua, dientes, cabello, prendas y logotipo.
- La ropa usa variantes con contraste y el logo de OneLingo integrado en el pecho.
- El movimiento de boca actual se apoya en amplitud/morphs disponibles.

Límite importante: no se ha verificado que todos los GLB incluyan un rig facial completo de 52 ARKit ni un conjunto profesional de visemas. No debe afirmarse que existe esa cobertura. El resultado actual es útil como prototipo conversacional, pero una sincronización labial precisa requiere morph targets faciales comprobados y tiempos de fonemas/visemas.

Higgsfield se evaluó para referencias visuales y videos de comparación. Generar un video por respuesta no es viable por coste, latencia y falta de reutilización. El camino correcto para producción es un personaje reutilizable con rig facial adecuado, voz separada y animación en tiempo real.

## 8. Onboarding y perfil del estudiante

El onboarding debe capturar:

- Idioma que desea aprender.
- Nivel que cree tener.
- Sector profesional o condición de estudiante, mediante opciones múltiples controladas.
- Objetivos: conversación, trabajo, viajes, certificación, estudios u otros objetivos definidos.
- Preferencia de tutor cuando corresponda.

Todos los idiomas deben ser visibles sin una pantalla incómoda de desplazamiento. La información del perfil se utiliza para adaptar situaciones, ejemplos, vocabulario y conversación. La personalización no debe reemplazar las competencias obligatorias del nivel.

## 9. Diagnóstico adaptativo

El diagnóstico debe producir un perfil de habilidades, no solamente un número.

Flujo esperado:

1. Comienza cerca del nivel declarado.
2. Incluye preguntas estratégicas de vocabulario, gramática, lectura y listening.
3. Incorpora producción escrita evaluada por IA.
4. Si el usuario domina su nivel, agrega entre 5 y 8 preguntas de dificultad superior.
5. Si falla repetidamente fuera de su rango, deja de escalar y consolida la evidencia.
6. Entrega retroalimentación después de cada respuesta sin revelar respuestas futuras.
7. Al finalizar, estima el nivel y muestra fortalezas y áreas de mejora por habilidad.

Dos estudiantes clasificados como B1 pueden recibir rutas diferentes: uno puede necesitar más listening y otro más gramática. El diagnóstico debe alimentar la ruta inicial y quedar accesible para repetirlo en pruebas o depuración.

## 10. Modelo pedagógico objetivo

Cada unidad o situación debe seguir una secuencia como esta:

```text
objetivo comunicativo
→ vocabulario y expresiones
→ explicación breve
→ ejemplos comprensibles
→ punto gramatical necesario
→ práctica guiada
→ lectura o listening contextual
→ producción del estudiante
→ prueba con ejemplos nuevos
→ retroalimentación
→ repaso espaciado
```

Para un principiante absoluto, la ruta debe introducir antes de exigir:

- Pronombres personales.
- Verbo `to be` afirmativo, negativo e interrogativo.
- Artículos y sustantivos básicos.
- Demostrativos y posesivos esenciales.
- Formación de oraciones sencillas.
- Preguntas y respuestas de identidad, origen, edad y ocupación.
- Vocabulario de alta frecuencia con audio e imagen cuando ayuden.

La aplicación debe separar tres estados:

- **Expuesto:** el usuario vio la explicación.
- **Completado:** terminó la actividad.
- **Dominado:** demostró el conocimiento con ejemplos nuevos y retención posterior.

Completar una pantalla no equivale a dominar el tema.

## 11. Gramática y vocabulario

La gramática debe organizarse por nivel y prerequisitos. La interfaz no debe mostrar un temario enorme como una lista plana, porque abruma al estudiante. Debe presentar unidades cortas, progreso, próximos pasos y temas bloqueados o recomendados.

La base auditada contiene alrededor de **116 preguntas**, una cantidad útil como semilla pero insuficiente para un producto escolar completo o una preparación de certificación. Cada objetivo necesita múltiples ejemplos, distractores, modalidades y versiones de evaluación.

El vocabulario se organiza por:

- Nivel.
- Frecuencia y utilidad.
- Situación comunicativa.
- Función: reconocer, comprender, producir y reutilizar.
- Historial de errores y repasos.

Los bancos externos o unidades de libros sirven como referencia curricular. No deben copiarse sin revisar licencias. El contenido debe reescribirse, alinearse con los objetivos de OneLingo y someterse a revisión pedagógica.

Documentos relacionados:

- `docs/CURRICULO-INGLES-COMPLETO.md`
- `docs/CURRICULO-INGLES-INVENTARIO.md`
- `docs/PLAN-PEDAGOGICO-APRENDIZAJE.md`
- `docs/auditoria/`

## 12. Las 50 situaciones

Las situaciones son contextos de uso, no simples temas de chat. Cada una debe contener:

- Objetivos comunicativos.
- Vocabulario y expresiones funcionales.
- Gramática necesaria.
- Ejemplos modelo.
- Actividades de selección, ordenamiento, completar y relacionar.
- Lectura o listening breve.
- Producción hablada o escrita.
- Prueba y retroalimentación.
- Criterios de dominio y repaso.

Ejemplo para restaurante:

```text
vocabulario de menú y alimentos
→ expresiones para pedir y preguntar
→ cuantificadores o estructuras necesarias
→ diálogo guiado
→ comprensión de una orden
→ simulación con tutor
→ corrección
→ nueva situación de transferencia
```

El tutor recibe la situación, nivel, perfil y progreso relevante para conversar dentro del objetivo. No debe sustituir la enseñanza previa con una conversación libre sin andamiaje.

## 13. Lectura, listening, escritura y speaking

### Lectura

- Presentar vocabulario imprescindible antes del texto.
- Alternar textos con ilustración y textos sin imagen.
- Hacer varias preguntas sobre un mismo texto: idea principal, detalles, inferencia, vocabulario y propósito.
- Ajustar extensión y complejidad por nivel.

### Listening

- Introducir el contexto antes del audio.
- Permitir repetición controlada y velocidad adecuada al nivel.
- Reutilizar audios para contener el coste de TTS.
- Evaluar comprensión global y detalles.
- Evitar que la transcripción visible convierta la actividad en lectura.

### Escritura

- Empezar con construcción guiada y avanzar a producción libre.
- Evaluar claridad, cumplimiento de tarea, gramática, vocabulario y coherencia.
- La IA debe explicar correcciones y ofrecer una versión mejorada sin borrar la voz del estudiante.

### Speaking

- Dar tiempo suficiente para hablar y tolerar pausas naturales.
- Mostrar claramente cuándo escucha, procesa y habla el tutor.
- Usar contextos y objetivos concretos.
- Evaluar inteligibilidad, fluidez, adecuación y recursos lingüísticos sin penalizar acento por sí mismo.

## 14. Progreso, memoria y ruta de aprendizaje

La ruta debe comportarse como un grafo de competencias con prerequisitos, no como una lista decorativa. Las reglas mínimas son:

- Recomendar el siguiente tema según el diagnóstico y el rendimiento reciente.
- Reforzar errores mediante repetición espaciada.
- Intercalar vocabulario, gramática y habilidades.
- Pedir transferencia a un ejemplo nuevo antes de declarar dominio.
- Mantener disponibles los temas ya estudiados.
- No ocultar gramática completada; moverla a repaso o dominio.
- Usar rachas y recompensas como motivación secundaria, sin premiar respuestas al azar.

La IA puede interpretar el perfil y proponer contenido contextual. La aplicación conserva la autoridad sobre prerequisitos, objetivos, frecuencia de repaso y criterios de avance.

## 15. Interfaz y sistema visual

Principios acordados:

- Conservar la paleta e identidad propias de OneLingo.
- Inspirarse en la claridad, ritmo y retroalimentación de Duolingo sin copiar su identidad visual.
- Tipografía legible y textos ligeramente más grandes.
- Tarjetas consistentes, con buen uso del ancho y sin espacios vacíos accidentales.
- Navegación inferior persistente donde corresponda.
- Estados de carga con skeletons, iconos animados y mensajes útiles.
- Sonido y animación inmediata para respuesta correcta o incorrecta.
- Mascotas Lumo y Nara como guías en puntos concretos de la experiencia.
- Animaciones breves, reutilizables y livianas; evitar videos para microinteracciones repetitivas.
- Aviso comprensible cuando no hay conexión.

En la pantalla de inicio existe un acceso destacado a “Práctica con tutores IA”, con rostros de varios tutores. La experiencia del avatar se añade como módulo separado y no elimina la práctica anterior.

## 16. Endpoints funcionales relevantes

Los nombres exactos deben confirmarse contra las rutas del backend antes de cambios mayores. Las áreas relevantes son:

- Salud del servicio: `/api/salud`.
- Estado de voz: `/api/voz/estado`.
- Generación/transmisión de voz: rutas bajo `/api/voz/`.
- Transcripción: endpoint de STT usado por el tutor.
- Chat del tutor: endpoint con respuesta estructurada/SSE.
- Autenticación y perfil.
- Diagnóstico, progreso y actividades.

El audio del usuario y las llamadas a proveedores pasan por el backend para proteger credenciales, aplicar reglas, registrar métricas y administrar caché.

## 17. Archivos clave para revisión

```text
lib/features/avatar/avatar_screen_web.dart   integración Flutter/iframe
web/avatar/index.html                        interfaz del tutor 3D
web/avatar/practice.js                       conversación, micrófono y estados
web/avatar/avatar.js                         carga/render/animación del GLB
backend/src/lib/config.ts                    configuración validada del backend
docs/avatar-ia.md                            notas específicas de avatar y voz
work/browser/avatar-waves-report.json        evidencia de QA de producción
```

Para localizar la implementación actual sin depender de nombres asumidos:

```bash
rg -n "transcrib|eleven|gpt-4o-mini-transcribe|eleven_flash|MediaRecorder|MediaSource|EventSource|replyReadyMs|firstAudioMs" \
  backend/src web/avatar lib
```

## 18. Validación y despliegue

Comprobaciones recomendadas antes de producción:

```bash
# Backend
cd backend
npm run typecheck
npm test

# Flutter
cd ..
flutter analyze
flutter test
flutter build web --release \
  --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
```

Después del despliegue:

- Verificar que PM2 mantenga `onelingo-api` en línea.
- Consultar `/api/salud`.
- Consultar `/api/voz/estado` y confirmar `eleven_flash_v2_5`.
- Abrir producción con un parámetro de versión para evitar caché durante QA.
- Probar onboarding, inicio, fundamentos, gramática, una actividad, tutor IA, micrófono, transcripción y audio.
- Revisar consola y red del navegador.
- Comparar hashes de los archivos críticos si el despliegue fue manual.
- Crear respaldo antes de sustituir artefactos de producción.

Último respaldo registrado para esta fase:

```text
/var/www/onelingo/backups/avatar-voice-waves16-20260922
```

## 19. Estado de la última versión de producción

Versión de referencia:

```text
https://onelingo.hostingcuenca.com/?release=voice-waves16#/avatar
```

Cambios confirmados:

- El tutor inicia la conversación.
- Vuelve a iniciar con contexto al cambiar de situación.
- Hay ondas y estados visibles durante la respuesta.
- Se miden `replyReadyMs` y `firstAudioMs`.
- ElevenLabs usa `eleven_flash_v2_5`.
- El render del avatar está limitado a 30 fps.
- PM2 y los endpoints de salud/voz respondieron correctamente.
- No se observaron errores en la prueba automatizada principal.

## 20. Riesgos y deuda prioritaria

### P0 — antes de considerar el flujo pedagógico confiable

1. Completar la secuencia enseñar → practicar → comprobar en el contenido inicial.
2. Evitar preguntas que asumen pronombres, `to be` u otros fundamentos no enseñados.
3. Corregir persistencia/navegación de gramática para que los temas no desaparezcan tras entrenar.
4. Validar el diagnóstico por habilidad y su efecto real en la ruta.
5. Instrumentar latencia por etapa en conversación de voz.

### P1 — calidad de aprendizaje y conversación

1. Expandir bancos de gramática y vocabulario por nivel y situación.
2. Implementar repaso espaciado y dominio por evidencia.
3. Mejorar fin de voz con VAD robusto y, después, STT continuo.
4. Reducir y estructurar el contexto enviado al LLM.
5. Confirmar licencias y trazabilidad de imágenes, sonidos, modelos y contenido.
6. Mejorar rig facial/visemas si el avatar 3D pasa de prototipo a producto central.

### P2 — escalado institucional

1. Panel y reportes para docentes/escuelas.
2. Currículo trazable por estándares y objetivos.
3. Evaluaciones de ascenso con bancos separados de la práctica.
4. Rutas específicas para exámenes de certificación.
5. Estrategia offline y sincronización posterior.
6. Observabilidad, costes, retención, privacidad y borrado de datos.

## 21. Plan recomendado de continuación

### Fase A — fundamentos completos

- Cerrar la primera ruta para principiante absoluto.
- Enseñar pronombres, `to be`, vocabulario básico y formación de frases.
- Asegurar explicación, práctica, prueba y repaso.
- Probar con usuarios simulados y personas reales sin conocimientos previos.

### Fase B — currículo y situaciones

- Definir matriz de competencias por nivel interno y equivalencia CEFR.
- Poblar gramática y vocabulario con cobertura y variantes suficientes.
- Convertir las 50 situaciones en unidades estructuradas.
- Medir dominio por habilidad.

### Fase C — tutor conversacional

- Mantener el TTS Flash y la reproducción progresiva.
- Añadir VAD mejorado y STT en streaming.
- Comprimir historial y contexto del LLM.
- Afinar interrupciones, turnos, caché y fallos de red.
- Evaluar rig facial profesional frente al beneficio pedagógico real.

### Fase D — escuela y certificaciones

- Incorporar gestión de clases y reportes.
- Crear evaluaciones estandarizadas y calibradas.
- Separar claramente aprendizaje general de preparación TOEFL/Cambridge/IELTS.
- Validar predicción y criterios con datos suficientes.

## 22. Reglas para futuras modificaciones

- Revisar primero el estado real del código y los documentos existentes.
- No sustituir contenido determinista por llamadas de IA sin una razón pedagógica.
- No exponer claves de proveedores en Flutter o JavaScript público.
- No afirmar capacidades de rig facial, offline o certificación que no estén verificadas.
- No desplegar una compilación web sin `API_URL` de producción.
- Mantener un respaldo y una ruta de reversión.
- Probar el flujo como principiante, no solamente como desarrollador que ya conoce la respuesta.
- Medir latencias por etapa antes de atribuir el problema a un proveedor.
- Tratar accesibilidad, legibilidad y estados de red como requisitos del producto.
- Actualizar este documento cuando cambien arquitectura, proveedores, modelos o prioridades.

## 23. Documentos relacionados

Revisar también:

```text
docs/avatar-ia.md
docs/CURRICULO-INGLES-COMPLETO.md
docs/CURRICULO-INGLES-INVENTARIO.md
docs/PLAN-PEDAGOGICO-APRENDIZAJE.md
docs/auditoria/
docs/voz/
```

Este archivo es el índice general. Los documentos especializados deben conservar evidencia, inventarios y decisiones detalladas sin duplicar secretos ni presentar prototipos como funciones terminadas.
