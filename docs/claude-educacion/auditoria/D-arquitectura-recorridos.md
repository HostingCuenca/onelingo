# Auditoría D: arquitectura técnica y recorridos de usuario

Rama `claude/educacion-multilenguaje` · 26-09-2026 · solo lectura del código. Las pruebas temporales se ejecutaron desde el scratchpad, fuera del repositorio.

## Resumen

- **Hay dos productos distintos bajo "Aprender".** El inglés usa un camino nuevo: Fundamentos v1, gramática en código Dart, biblioteca, lectura, listening y situaciones. Los otros 9 idiomas usan el currículo antiguo: 10 niveles × 100 lecciones generadas. `levels_screen.dart:30` y `home_screen.dart:48,88-89` ramifican con `idiomaMeta == 'en'`.
- **Hay contenido en inglés dentro de cursos de otros idiomas.** En japonés o alemán, los niveles 3 a 10 usan `_bancoGenerico`, un banco con palabras en inglés (`curriculum.dart:453`). Las 20 unidades de cada nivel son idénticas: 1 vocabulario distinto de 20, verificado con una prueba. Además, el paso de imagen de todos los idiomas pregunta palabras inglesas como "Breakfast" (`curriculum.dart:578`). Desde Inicio, el diagnóstico y la biblioteca abren siempre la versión inglesa.
- **Un principiante de inglés se queda en `nivelActual = 0` para siempre.** `fundamentosPendientes` mide las lecciones antiguas `L0-xxx` (40 lecciones de letras y números), que en inglés no se pueden abrir. En cambio, el botón "Aprender hoy" abre Fundamentos v1, 6 microlecciones que nunca cierran el nivel 0. Está reproducido en la prueba R1.
- **Gramática que desaparece: se corrigió a medias.** La recomendación ya no oculta el área (corregido). Pero `GrammarScreen` no guarda ni recupera el tema en curso y no marca los temas practicados. Al reabrirla vuelve a "Tema 1", la evidencia queda en `practicas` pero la pantalla no la lee, y el borrador de "Crea" se pierde. Además, `go('/aprender')` y volver a tocar la pestaña Aprender cierran la pantalla. Está reproducido en la prueba R3. Sigue siendo el P0 del informe del 22-09.
- **Progreso.** Todo el estado se guarda en un único JSON en `onelingo.progress.v1` y se sube completo por `PUT /usuarios/me/progreso`, sin fusión: gana la última escritura. Hay dos riesgos principales:
  - Las claves `L1-001` no incluyen el idioma.
  - Un cliente antiguo **borra los campos que no conoce**: `toJson` solo escribe los campos conocidos.

  El modelo nuevo debe poder recalcularse a partir de `practicas` y usar campos opcionales.
- **`flutter analyze`: 9 avisos informativos**, sin errores ni advertencias (código de salida 1 por `fatal-infos`). **`flutter test`: 104 pruebas pasan, 1 se omite y ninguna falla, en 18,1 s.**

## Mapa técnico del contenido

### Archivos de contenido

Esquemas extraídos con python3 de los JSON reales.

| Archivo | Qué contiene (claves) | Quién lo consume | ¿Solo inglés? |
|---|---|---|---|
| `assets/contenido/<l>/nivel-0.json` (10 idiomas) | `{idioma, nivel, generado, unidades[8]{numero, tipo: escritura\|vocabulario, titulo, descripcion, items[]{simbolo, romanizacion, significado, ejemplo}, examen[]{pregunta, opciones[4], correcta, explicacion}}}`; entre 89 y 119 ítems | `Fundamentos.precargar` → `Fundamentos.lecciones` (L0-xxx), `comoUnits`, `banco` para la prueba de nivel | No (en inglés no se puede abrir desde la interfaz) |
| `assets/contenido/<l>/nivel-{1,2}.json` (10 idiomas) | `{idioma, nivel, generado, unidades[20]{numero, tema, titulo, objetivo, gramatica, vocab[8]{palabra, romanizacion, traduccion, ejemplo}, frases[6]{texto, romanizacion, traduccion}, dialogo[4]{quien, texto, romanizacion, traduccion}, errores_tipicos[2]{incorrecto, correcto, explicacion}, examen[3]{…}}}` | `ContenidoJson.precargar` → `UnidadJson` → `aUnit` → `unidadesDe`/`leccionesDe` (`curriculum.dart:429-495`), `ExamScreen`, `PruebaNivel` | No; solo llega a los niveles 1-2 |
| `en/biblioteca.json` | `{version, idioma, alcance, preguntas[116]{id: en-v1-NN-NNN, nivel, skill, tipo, tema, instruccion, texto, opciones, correcta, aceptadas, explicacion, version, fuente, dificultad, pasajeId, imagen, sectores[], objetivos[]}}`; comprensión 36, listening 30, gramática 20, escritura 20, vocabulario 10; unas 10 por nivel (26 en el N5) | `BancoDiag.precargar('en')` (`diagnostico.dart:203`), `LibraryScreen`, `RutaBiblioteca.seleccionar`, diagnóstico | Sí |
| `en/diagnostico.json` | `{idioma, generado, preguntas[87]{nivel, skill, tipo, tema, instruccion, texto, opciones, correcta, aceptadas, explicacion}}` | **Nadie.** En inglés, `BancoDiag` carga `biblioteca.json`; los demás idiomas buscan `diagnostico.json`, que no existe, y recurren a `PruebaNivel.bancoNivel` | Recurso muerto |
| `en/reading_units.json`, `en/listening_units.json` | `{version, units[20]{id, nivel, title, objective, vocabulary[4]{word, translation, example}, strategy, passage, questions[3]{id, prompt, options, answerIndex, explanation, evidence}}}`; 2 unidades por nivel | `learningUnitsProvider` (`learning_units.dart:67`, ruta fija `assets/contenido/en/`), `LearningUnitScreen` (`/estudiar`) | Sí |
| `en/situaciones.json` | `[50]{id, nombre, vocabulario[]{en, es}, objetivos[]{id, titulo, frase, traduccion}}` | `situation_units.dart:8` | Sí (claves `en`/`es` en el propio esquema) |
| `en/situational_vocabulary.json` | `{version, idioma, situations[50]{situacionId, nombre, objective, vocabulary[8]{id, en, es, example, category, nivelInicial}, patterns[]{template, translation, examples[]{en, es}}}}` | `situation_units.dart:9`, `SituationScreen` | Sí |
| `lib/core/content/foundations.dart` | 6 `FoundationUnit(id, title, goal, requires, cards[]{english, spanish, explanation, visual}, checks[]{prompt, options, answer, feedback, order})` | `FoundationsScreen` (`/fundamentos`), `LearningPath` | Sí (inglés escrito en código Dart) |
| `lib/core/content/grammar_guides.dart` | 43 `GrammarGuide(id, level, title, goal, rule, examples, commonError, checks[2])`; por nivel N1-N10: 5/6/4/5/5/5/4/4/3/2 | `GrammarScreen` (`/gramatica`) | Sí |
| `lib/core/content/grammar_production_tasks.dart` | Mapa `guideId → consigna` | `GrammarScreen` paso "Crea" | Sí |
| `lib/core/content/curriculum.dart` | `idiomas` (10), `niveles` (10 `Level`), `_unidadesNivel1` y `_bancoGenerico` (niveles 2 a 10, **palabras inglesas**), generador `_pasos` | Todo el currículo antiguo | Mezcla |
| `lib/core/content/idiomas.dart` | `bancoNivel1(idioma, unidad)`, `soloNativo`, `idiomasSinEspacios`, `chatNivelBajo` | Nivel 1 cuando falta el JSON | No |

### Modelos, providers, rutas y pantallas

| Capa | Elemento | Notas |
|---|---|---|
| Modelos | `models.dart`: `Skill`, `StepType` (10 tipos), `Level`, `Unit` (tuplas), `LessonStep`, `Lesson` (id `L{n}-{NNN}`), `Mistake` | Sin identificadores estables por concepto. `Unit` usa registros posicionales. |
| Modelos | `UnidadJson`, `UnidadFund`/`ItemFund`, `FoundationUnit`, `GrammarGuide`, `LearningUnit`, `PreguntaDiag` | **Seis modelos paralelos de "unidad"**, sin interfaz común. |
| Estado | `providers.dart`: `ProgressState` y `ProgressNotifier`; la variable global `idiomaContenido` (`curriculum.dart:417`) decide el idioma de todo el currículo antiguo | Un valor global mutable: el diagnóstico lo cambia en `diagnostico_screen.dart:139` y lo restaura en la línea 169. |
| Carga | `ContenidoJson.precargar(idioma)` carga el nivel 0 (vía `Fundamentos`), `BancoDiag` y los niveles 1 a 10 si existen. Cada idioma se intenta una sola vez. | Web y móvil usan `rootBundle`. `pubspec.yaml` declara `assets/contenido/<l>/` **sin subcarpetas**: Flutter no incluye subdirectorios de forma recursiva. |
| Rutas | Shell de 4 pestañas (`router.dart:57`). Rama Aprender: `/aprender`, `/aprender/nivel/:n`, `/fundamentos`, `/estudiar?skill&nivel`, `/gramatica?nivel`, `/biblioteca?skill&nivel`, `/leccion/:id`, `/examen/:n`. Rama Practicar: `/practicar`, `/situacion/:id`, `/chat`. | Tocar de nuevo la pestaña activa reinicia la rama (`router.dart:204`). |
| Pantallas | `HomeScreen`, `LevelsScreen` (inglés: `CaminoPersonalizado` más 10 enlaces a la biblioteca; otros idiomas: `_NivelCard`), `LevelScreen`, `LessonPlayerScreen`, `ExamScreen`, `FoundationsScreen`, `GrammarScreen`, `LearningUnitScreen`, `LibraryScreen`, `SituationScreen`, `ChatScreen`, `ProgressScreen` | |

## Acoplamiento a inglés

| Punto | Evidencia | Qué ve quien estudia japonés o alemán |
|---|---|---|
| El currículo de los niveles 3 a 10 es el `_bancoGenerico` inglés | `curriculum.dart:452-458`; la prueba R2 da `unidadesDe(3).first.vocab = [(Bigger, Más grande), (Enough, …)]` en `ja` y `de`, con 1 vocabulario distinto de 20 unidades | Lecciones de "Curso de japonés, Nivel 3" que enseñan palabras en inglés; 20 unidades iguales por nivel |
| Paso de imagen con palabras inglesas fijas | `curriculum.dart:578` (`palabrasImagen = ['Breakfast', 'Family', …]`), en la lección 4 de cada unidad | "Selecciona la imagen que corresponde a: 'Breakfast'" dentro del curso de alemán |
| La biblioteca solo existe en inglés | `library_screen.dart:172,190` (`BancoDiag('en')`), 283 (`'idioma': 'en'`), 318 ("Tu biblioteca de inglés"); el acceso está abierto a cualquier idioma en `home_screen.dart:76` | Preguntas de inglés desde el Inicio de un curso de japonés |
| El diagnóstico desde Inicio usa siempre inglés | `home_screen.dart:69-75` (`'idioma': 'en'`); `guardarDiagnostico` descarta el resultado si el idioma es distinto (`providers.dart:445-455`) | La persona hace una prueba de inglés que no cambia nada en su curso |
| Onboarding | `onboarding_screen.dart:148` diagnostica solo si `meta == 'en'`; los demás idiomas se autoevalúan | Sin diagnóstico real; el nivel es el declarado |
| Lectura y listening | `learning_units.dart:67-70` (ruta fija `en/`), audio `'en'` en `learning_unit_screen.dart:83` | No se muestran: `LearningPath` solo aparece en inglés |
| Fundamentos v1 | `foundations.dart`, con I/you escritos en código; `foundations_screen.dart:66,108` | No se muestran. Estos idiomas usan el nivel 0 antiguo (hiragana, hangul…), que sí existe |
| Gramática | `grammar_guides.dart` (43 guías en inglés), `grammar_screen.dart:44` (`'idioma': 'en'`) | Solo se llega a ella desde el camino de inglés; sin guía propia por idioma. La gramática de ja o de es un párrafo `gramatica` dentro de la lección "Frases" |
| Situaciones | `situation_units.dart` (claves `en`/`es`); `situation_screen.dart:104` muestra en otros idiomas solo un botón "Practicar con el tutor" | Pantalla casi vacía con un botón al chat |
| Perfil | `progress_screen.dart:128`: "Práctica de inglés" solo en inglés | Sin desglose por área |
| Idioma de apoyo | Todos los textos educativos asumen el español. El curso de español (`es/nivel-1.json`) explica en español: `traduccion: "la persona que habla"` | Quien tiene inglés como lengua materna recibe explicaciones en el idioma que está aprendiendo (lo cubre DEC-004) |
| Chat | `chat_screen.dart:191,229,334`: apertura distinta si no es inglés y nivel ≤ 3; el contexto del diagnóstico solo existe en inglés | Tutor sin contexto de dificultades |

## Progreso actual y foundations-v1 (claves exactas)

### Almacenamiento

| Clave de SharedPreferences | Contenido |
|---|---|
| `onelingo.progress.v1` | `jsonEncode(ProgressState.toJson())`, todo el estado |
| `onelingo.pending.<usuarioId>` | Cola persistente del último estado sin confirmar (`sync.dart:409-414`) |
| `onelingo.api.token` / `.usuarioId` / `.email` | Sesión |
| `onelingo.onboarding.draft.v2` | Borrador del onboarding |
| `onelingo.efectos.{animaciones,sonido,vibracion}` | Preferencias |

**`ProgressState`** (`providers.dart:36-310`) contiene `onboardingDone`, `nombre`, `email`, `idiomaNativo`, `idiomaMeta`, `nivelInicial` (1 a 10), `fundamentos` (bool), `diagnostico` (mapa libre), `practicas` (mapa de id a evidencia), `sectores`, `objetivos`, `completadas` (conjunto de `L{n}-{NNN}` **sin idioma**), `puntuaciones`, `examenes` (nivel a porcentaje), `errores` (máximo 200), `xp`, `racha`, `ultimoDia`, `diasActividad`, `segundosEstudio`, `trialInicio`, `trialSegundos`, `tutorId` y `planId`. No tiene versión de esquema.

**Sincronización.** `_save` hace tres cosas: guarda en prefs, llama a `Sync.subir(toJson())` (espera 2 s, reintenta a los 5 s y conserva la cola por usuario) y precarga el idioma. El backend recibe `PUT /usuarios/me/progreso` con el esquema zod `Estado.passthrough()` (`backend/src/routes/usuarios.ts:16-40`), **reemplaza** la columna jsonb `estado` y recalcula `nivel_actual`, `lecciones_completadas`, `errores` y `examenes`. No fusiona: gana la última escritura. Al iniciar sesión, `iniciarSesionReal` sustituye el estado local por el del servidor.

**Evidencia.** `registrarPractica(id, evidencia)` guarda la última evidencia más `primeraCorrecta`, `primeraFecha`, `intentos` y `fecha`, y da +5 XP solo en el primer intento. Los prefijos de clave en uso son:
- `foundation-v1-…`
- `grammar-guide-<guideId>-<i>`
- `learn-<skill>-<unitId>-<qId>`
- `en-v1-NN-NNN` (biblioteca)
- `situacion-en-<id>-palabra-<i>`
- `situacion-<idioma>-<id>-<objetivo>`

**Significado de cada estado.**
- *Completada*: la lección se jugó hasta el final, con cualquier porcentaje de aciertos (`completarLeccion`). Es participación, no dominio.
- *Aprobado*: examen del nivel ≥ 65 %.
- *Fundamentos practicado*: todas las comprobaciones de la unidad tienen `resueltaConApoyo == true`.
- *Dominado* **no existe**. `RutaBiblioteca.nivelSugerido` solo ajusta el nivel sugerido ±1 con 3 o 4 primeras respuestas independientes, excluyendo `practica_guiada`, `comprobacion_guiada` y `conApoyo`.

### foundations-v1

`foundationKey = 'foundation-v1-<unit.id>-<índice>'` (`foundations.dart:254`). Son 6 unidades con 2 comprobaciones cada una, es decir, **12 claves**:

| Unidad (`id`, título) | Requiere | Claves |
|---|---|---|
| `i-you` Yo y tú | — | `foundation-v1-i-you-0`, `foundation-v1-i-you-1` |
| `i-am` Digo mi nombre | i-you | `foundation-v1-i-am-0`, `foundation-v1-i-am-1` |
| `you-are` Hablo contigo | i-am | `foundation-v1-you-are-0`, `foundation-v1-you-are-1` |
| `he-she` Presento a alguien | you-are | `foundation-v1-he-she-0`, `foundation-v1-he-she-1` |
| `feelings` Digo cómo estoy | he-she | `foundation-v1-feelings-0`, `foundation-v1-feelings-1` |
| `introduce` Mi primera presentación | feelings | `foundation-v1-introduce-0`, `foundation-v1-introduce-1` (tipo ordenar) |

Evidencia guardada (`foundations_screen.dart:107-120`): `{idioma: 'en', skill: 'vocabulario' (solo i-you) | 'gramatica', nivel: 1, ruta: 'fundamentos-v1', tema, tipo: 'comprobacion_guiada', conApoyo: true, correcta, resueltaConApoyo (se queda en true una vez alcanzado), respuesta, feedback}`, más `primeraCorrecta`, `primeraFecha`, `intentos` y `fecha`.

### Riesgos de pérdida

| # | Riesgo | Evidencia |
|---|---|---|
| P1 | Un cliente antiguo borra campos nuevos: `toJson` solo escribe los campos conocidos y `fromJson` ignora el resto. Un segundo dispositivo sin actualizar sube el estado sin esos campos y el servidor lo reemplaza. | `providers.dart:246-310`; PUT reemplaza el estado |
| P2 | Gana la última escritura entre dispositivos. `iniciarSesionReal` impone el estado del servidor sobre la actividad local no subida. | `usuarios.ts:70-80`, `providers.dart:398` |
| P3 | Si `fromJson` falla (por ejemplo `examenes` con un valor `double`, porque `v as int`), `_load` devuelve `ProgressState()` vacío. El siguiente `_save` sobrescribe prefs y además lo sube al servidor. | `providers.dart:318-331` |
| P4 | `completadas` y claves como `grammar-guide-*`/`learn-*` no llevan idioma. Si en el futuro se cambia de curso, el progreso colisiona. | `completadasEnNivel` usa `startsWith('L$n-')` |
| P5 | `practicas` crece sin límite y guarda textos completos de `feedback`: afecta al límite de localStorage en web y al tamaño del jsonb. | `registrarPractica` |
| P6 | El estado de la interfaz de gramática (tema, pregunta, `checked`, borradores de "Crea") y de `/estudiar` (`answered`) vive solo en memoria. | `grammar_screen.dart:23-30`, `learning_unit_screen.dart` |

## Bug "gramática desaparece": veredicto con evidencia

**Veredicto:** el síntoma original (el área de Gramática desaparecía de la recomendación) **está corregido**. El síntoma que describe el P0 del 22-09 ("los temas desaparecen tras entrenar", persistencia y navegación) **sigue ocurriendo**, con cinco causas concretas.

| # | Estado | Dónde | Evidencia |
|---|---|---|---|
| G0 | Corregido | `learning_path.dart:88-200`: recorre siempre las 5 áreas; la recomendación solo cambia el estilo. `learning_layout_test` comprueba que "Gramática" aparece con cualquier recomendación. | Documentado en AUDITORIA-PEDAGOGIA (antes `take(3)`) |
| G1 | **Abierto** | `GrammarScreen` inicia `topic = 0`, `question = 0` y `checked = {}` (`grammar_screen.dart:23-30`), **no lee `practicas`** y no marca los temas practicados en el Temario | **Prueba R3:** se responde el tema 1 (se guardan `grammar-guide-be-0/1`) y se pasa a "Tema 2 de 5". Al reabrir, la pantalla muestra "Tema 1 de 5" y ninguna marca. |
| G2 | **Abierto** | Navegación: `_switchTab` usa `initialLocation: index == currentIndex` (`router.dart:204`), y el Inicio usa `context.go('/aprender')` en "Ver ruta" y "Aprender" (`home_screen.dart:61,65`) | Cualquiera de las dos cierra `/gramatica` de la rama y se pierde la posición (G1) |
| G3 | **Abierto** | El nivel por defecto es `widget.nivel ?? nivelInicial` y `LearningPath` pasa `s.nivelActual` | Si el nivel cambia (nuevo diagnóstico), los temas del nivel anterior dejan de mostrarse por defecto; solo siguen accesibles con Temario → desplegable |
| G4 | **Abierto** | Biblioteca con `skill=gramatica`: `nivelSugerido` sube un nivel tras 3 o 4 primeros aciertos independientes (`biblioteca.dart:14-50`) | El conjunto de preguntas cambia sin aviso: se percibe como "desaparecer" |
| G5 | **Abierto** | Borradores del paso "Crea" (`drafts`) solo en memoria | Se pierden al salir |

Corrección mínima propuesta, para quien se encargue de la interfaz; no se debe tocar `home_screen.dart`:
1. Guardar `grammar.<idioma>.<nivel>.temaActual` y derivar "practicado" de `practicas` (`grammar-guide-<id>-*`).
2. Mostrar ✓ en el Temario.
3. Reanudar en el último tema.
4. Cambiar `/gramatica?nivel=` para que conserve el nivel elegido por la persona.

## Esquema de contenido propuesto (+ ejemplo JSON + modelos Dart)

### Principios

1. Un solo esquema para los 10 cursos. Los identificadores son **slugs estables con prefijo de idioma** (`de.a1.sein-vorstellen`); el orden va en un campo aparte.
2. `concepto` es un identificador independiente del idioma (`be-presentarse` ≈ `sein-vorstellen` ≈ `desu-presentarse`). Sirve para alinear cursos y dar contexto al tutor.
3. Los niveles con `estado: "planificado"` (C2) no tienen `nivelInterno` ni unidades obligatorias.
4. **DEC-004 (idioma de apoyo).** Todo texto educativo dirigido a la persona es un `TextoApoyo`:
   - Forma completa: `{"es": "...", "en": "..."}`.
   - Abreviatura: una cadena simple equivale a `{"es": ...}`.

   El contenido en el idioma meta (ejemplos, vocabulario) es una cadena simple con `rom` opcional. La traducción es un `TextoApoyo`.
5. Carga diferida por idioma y por módulo, solo con `rootBundle` (sin `dart:io`), válida en web y móvil.

### Ubicación

```
assets/contenido/<idioma>/ruta/curso.json          # índice ligero: niveles, módulos, unidades (id, título, prereqs, archivo)
assets/contenido/<idioma>/ruta/<modulo>.json       # detalle de las unidades del módulo (carga diferida, 20–80 KB)
lib/core/aprendizaje/texto_apoyo.dart              # TextoApoyo + resolución del idioma de apoyo
lib/core/aprendizaje/modelos.dart                  # Curso, NivelCurso, Modulo, UnidadRuta, Leccion, Paso (sealed)
lib/core/aprendizaje/cargador.dart                 # CargadorRuta: caché por idioma/módulo, rootBundle
lib/core/aprendizaje/grafo.dart                    # validación, orden topológico, desbloqueo
lib/core/aprendizaje/dominio.dart                  # EstadoUnidad calculado desde practicas
lib/core/aprendizaje/repaso.dart                   # repaso espaciado
lib/core/aprendizaje/migracion.dart                # alias foundation-v1 → unidades nuevas
lib/core/aprendizaje/providers.dart                # cursoProvider, moduloProvider, idiomaApoyoProvider, estadosProvider
```

**Hay que añadir `assets/contenido/<l>/ruta/` para cada idioma en `pubspec.yaml`**: los directorios de assets no son recursivos.

### `curso.json` (índice)

```json
{
  "esquema": 2, "idioma": "de", "version": "2026.10.0",
  "idiomasApoyo": ["es"], "apoyoPredeterminado": "es",
  "niveles": [
    {"id": "f0", "cefr": "Pre-A1", "nivelInterno": 0, "estado": "publicado", "titulo": {"es": "Fundamentos"}},
    {"id": "a1-1", "cefr": "A1", "nivelInterno": 1, "estado": "publicado", "titulo": {"es": "A1 · Primeros pasos"}},
    {"id": "c2", "cefr": "C2", "nivelInterno": null, "estado": "planificado", "titulo": {"es": "C2 · Maestría"}}
  ],
  "modulos": [
    {"id": "de.a1-1.m01", "nivel": "a1-1", "orden": 1, "titulo": {"es": "Presentarse"},
     "archivo": "a1-1-m01.json",
     "unidades": [
       {"id": "de.a1.sein-vorstellen", "orden": 1, "titulo": {"es": "Soy Ana: ich bin"},
        "prerequisitos": ["de.f0.pronomen-ich-du"], "concepto": "be-presentarse",
        "habilidades": ["gramatica", "vocabulario"], "estado": "publicado"}
     ]}
  ]
}
```

### Unidad mínima (dentro de `a1-1-m01.json`)

```json
{
  "id": "de.a1.sein-vorstellen", "idioma": "de", "nivel": "a1-1", "cefr": "A1", "nivelInterno": 1,
  "concepto": "be-presentarse", "version": 1,
  "objetivos": [{"id": "o1", "texto": {"es": "Decir tu nombre con ich bin.", "en": "Say your name with ich bin."}}],
  "prerequisitos": ["de.f0.pronomen-ich-du"],
  "habilidades": ["gramatica", "vocabulario", "conversacion"],
  "vocabulario": [
    {"id": "v-ich", "texto": "ich", "rom": "", "traduccion": {"es": "yo"}, "introducido": true},
    {"id": "v-bin", "texto": "bin", "traduccion": {"es": "soy (con ich)"}, "introducido": true}
  ],
  "gramaticaPermitida": ["pronombre-sujeto", "sein-presente-1sg"],
  "erroresFrecuentes": [
    {"id": "e1", "incorrecto": "Ich ist Ana.", "correcto": "Ich bin Ana.",
     "explicacion": {"es": "Con ich siempre va bin."}}
  ],
  "lecciones": [
    {"id": "l1", "titulo": {"es": "Me presento"}, "pasos": [
      {"id": "p1", "tipo": "explicacion", "texto": {"es": "Para decir quién eres: ich + bin + nombre."}},
      {"id": "p2", "tipo": "ejemplos", "items": [
        {"texto": "Ich bin Ana.", "traduccion": {"es": "Soy Ana."}, "audio": true}]},
      {"id": "p3", "tipo": "vocabulario", "refs": ["v-ich", "v-bin"]},
      {"id": "p4", "tipo": "practica_guiada", "items": [
        {"id": "c1", "formato": "elegir", "consigna": {"es": "Elige «Soy Ana»."},
         "opciones": ["Ich bin Ana.", "Ich ist Ana."], "respuesta": 0,
         "feedback": {"es": "Ich va con bin."}, "pista": {"es": "Mira el ejemplo."}}]},
      {"id": "p5", "tipo": "practica_independiente", "items": [
        {"id": "i1", "formato": "ordenar", "consigna": {"es": "Forma «Soy Leo»."},
         "tokens": ["Leo.", "bin", "Ich"], "respuesta": "Ich bin Leo."}]},
      {"id": "p6", "tipo": "situacion", "situacion": "conocer-companero", "objetivo": "o1",
       "consigna": {"es": "Preséntate a un compañero nuevo."}},
      {"id": "p7", "tipo": "evaluacion", "items": [
        {"id": "x1", "formato": "completar", "consigna": {"es": "Completa."},
         "texto": "Ich ___ Mia.", "respuesta": "bin", "aceptadas": ["bin"]}]}
    ]}
  ],
  "criterioDominio": {"minItems": 3, "umbral": 0.8, "sinApoyo": true, "formatosDistintos": 2, "retencionDias": 1},
  "repaso": {"intervalosDias": [1, 3, 7, 16, 35, 90], "itemsRepaso": ["i1", "x1"]},
  "tutor": {"objetivo": "o1", "vocabularioPermitido": ["v-ich", "v-bin"],
            "gramaticaPermitida": ["pronombre-sujeto", "sein-presente-1sg"],
            "erroresAVigilar": ["e1"], "longitudMaxFrase": 5}
}
```

### Modelos Dart (resumen)

```dart
// texto_apoyo.dart (sin dart:io)
class TextoApoyo {
  const TextoApoyo(this.porIdioma);
  final Map<String, String> porIdioma;
  factory TextoApoyo.fromJson(Object? j) => j is String
      ? TextoApoyo({'es': j})
      : TextoApoyo(Map<String, String>.from(j as Map));
  /// Cadena: nativo → apoyoPredeterminado del curso → 'es' → primero disponible.
  String en(List<String> cadena) {
    for (final l in cadena) { final t = porIdioma[l]; if (t != null && t.isNotEmpty) return t; }
    return porIdioma.values.firstOrNull ?? '';
  }
}
List<String> cadenaApoyo(String nativo, Curso c) => [nativo, c.apoyoPredeterminado, 'es'];

// modelos.dart
enum EstadoNivel { publicado, planificado }
class NivelCurso { final String id, cefr; final int? nivelInterno; final EstadoNivel estado; final TextoApoyo titulo; }
class Curso { final int esquema; final String idioma, version, apoyoPredeterminado;
  final List<String> idiomasApoyo; final List<NivelCurso> niveles; final List<ModuloIndice> modulos; }
class UnidadIndice { final String id, concepto; final int orden; final TextoApoyo titulo;
  final List<String> prerequisitos, habilidades; }
class UnidadRuta { final String id, idioma, nivel, cefr, concepto; final int? nivelInterno;
  final List<Objetivo> objetivos; final List<String> prerequisitos, habilidades, gramaticaPermitida;
  final List<Vocablo> vocabulario; final List<ErrorFrecuente> erroresFrecuentes;
  final List<Leccion> lecciones; final CriterioDominio criterio; final ConfigRepaso repaso; final MetaTutor tutor; }
sealed class Paso { String get id; }
final class PasoExplicacion extends Paso { … TextoApoyo texto; }
final class PasoEjemplos extends Paso { … }            // texto meta + traducción TextoApoyo
final class PasoVocabulario extends Paso { … }         // refs a Vocablo
final class PasoPractica extends Paso { final bool guiada; final List<Item> items; }
final class PasoSituacion extends Paso { … }
final class PasoEvaluacion extends Paso { final List<Item> items; }
String claveEvidencia(UnidadRuta u, Paso p, Item i) => 'ruta:${u.id}:${p.id}:${i.id}';
```

**Dónde se resuelve el idioma de apoyo.** Hay un solo punto: `idiomaApoyoProvider` (Riverpod), igual a `cadenaApoyo(progress.idiomaNativo, curso)`. Los widgets llaman a `texto.en(ref.watch(idiomaApoyoProvider))`. Los modelos conservan todos los idiomas, así que un cambio del idioma nativo se aplica sin recargar. Los metadatos del tutor también envían `idiomaApoyo`.

En esta fase, los 9 cursos publican `es` y el curso `es` publica `en` con `apoyoPredeterminado: "en"`. Un hablante nativo de francés en el curso de español recibe inglés; `es` queda como último recurso.

**Cómo se prueba:**
1. Prueba unitaria de `TextoApoyo.en`: se usa el nativo si existe, si no el predeterminado, si no `es`; una cadena simple equivale a `es`.
2. Prueba de integridad: cada `TextoApoyo` del curso X tiene todos los idiomas de `curso.idiomasApoyo`, y ninguno está vacío.
3. Prueba de widget: curso `es` con nativo `en` muestra la explicación en inglés; curso `de` con nativo `fr` muestra `es`.

*Alternativa más ligera*, si más adelante hay más de 3 idiomas de apoyo: archivos superpuestos `ruta/apoyo/<nativo>/<modulo>.json` indexados por la ruta del texto. Así solo se carga el idioma necesario. Por ahora se recomienda el mapa en línea, más fácil de validar.

## Modelo de dominio, desbloqueo, repaso y migración

### Estados por unidad

Se calculan con funciones puras a partir de `practicas`, así que se pueden recalcular siempre.

| Estado | Regla |
|---|---|
| `bloqueada` | Algún prerequisito no está en ≥ `practicada`. **Sigue visible y se puede abrir para leer**, pero no se recomienda (principio de `LearningPath`: recomendar no quita el acceso). |
| `disponible` | Prerequisitos cumplidos y sin evidencia. |
| `expuesta` | Existe `ruta:<u>:visto` (explicación y ejemplos vistos). |
| `practicada` | Todos los ítems de `practica_guiada` tienen `resueltaConApoyo`. Equivale a `foundationPracticed`. |
| `dominada` | Se cumple `criterioDominio`: ≥ `minItems` ítems de `practica_independiente` o `evaluacion` con `conApoyo != true`, un porcentaje de `primeraCorrecta` ≥ `umbral` en ≥ `formatosDistintos` formatos, **y** un acierto independiente ≥ `retencionDias` días después del primero. |
| `repasar` | Estaba `dominada` y `hoy ≥ proximoRepaso`, o hay ≥ 2 errores independientes entre sus últimas 4 respuestas. |

Los aciertos guiados o con apoyo nunca dan `dominada` ni cambian el nivel. Esto sigue el criterio que ya comprueba `learning_content_test`.

**Desbloqueo por grafo.** `grafo.dart` valida que no haya ciclos (Kahn) y que existan todos los IDs. Una unidad está disponible cuando `prerequisitos.every(estado ≥ practicada)`. Si se exige `dominada` o no es una decisión humana. El nivel "actual" pasa a ser el nivel de la primera unidad no dominada del orden topológico. El examen de nivel sigue decidiendo el **ascenso formal**.

**Repaso espaciado.** Es un sistema de cajas tipo Leitner con intervalos de `[1, 3, 7, 16, 35, 90]` días:
- Acierto independiente en repaso: caja + 1.
- Fallo: caja = máx(0, caja − 2) y el estado pasa a `repasar`.

Se guarda en el campo opcional `aprendizaje.repaso[<unidadId>] = {caja, proximo, ultimo}`. Si no existe (porque un cliente antiguo lo borró), se reconstruye con la caja 0 y `proximo = ultima fecha + 1 d`: se degrada sin perder datos.

### Convivencia con `ProgressState`

1. Los campos nuevos son **opcionales**:
   - `esquema` (int, 1 por defecto).
   - `aprendizaje: {v: 2, repaso: {...}, temaActual: {...}, migraciones: [...]}`.

   `fromJson` usa valores por defecto; `copyWith` y `toJson` solo los escriben si no son nulos.
2. **Toda la evidencia nueva va en `practicas`** con claves `ruta:<unidadId>:<pasoId>:<itemId>`. Las versiones antiguas ya conservan ese mapa tal cual (`cast<String,dynamic>`), así que un dispositivo sin actualizar no la borra (mitiga P1).
3. Añadir `extras` para conservar las claves desconocidas en `fromJson`/`toJson` a partir de ahora.
4. En el backend, fusionar `aprendizaje` si el PUT entrante no lo trae (con `COALESCE` o fusión jsonb), sin cambiar el esquema zod (`passthrough`).
5. No tocar `completadas`, `examenes` ni `L{n}-{NNN}`: el currículo antiguo convive mientras se migran los cursos.
6. Las claves nuevas llevan el idioma dentro del ID de la unidad, lo que evita P4.

### Migración de foundations-v1

Es un alias de lectura, puro e idempotente: no escribe ni borra nada.

| Clave antigua | Clave nueva equivalente | Unidad nueva |
|---|---|---|
| `foundation-v1-i-you-0` / `-1` | `ruta:en.f0.yo-tu:p4:c1` / `:c2` | `en.f0.yo-tu` |
| `foundation-v1-i-am-0` / `-1` | `ruta:en.f0.soy-nombre:p4:c1` / `:c2` | `en.f0.soy-nombre` (prereq `en.f0.yo-tu`) |
| `foundation-v1-you-are-0` / `-1` | `ruta:en.f0.tu-eres:p4:c1` / `:c2` | `en.f0.tu-eres` |
| `foundation-v1-he-she-0` / `-1` | `ruta:en.f0.el-ella:p4:c1` / `:c2` | `en.f0.el-ella` |
| `foundation-v1-feelings-0` / `-1` | `ruta:en.f0.como-estoy:p4:c1` / `:c2` | `en.f0.como-estoy` |
| `foundation-v1-introduce-0` / `-1` | `ruta:en.f0.presentacion:p4:c1` / `:c2` | `en.f0.presentacion` |

Reglas de la migración:
- `evidenciaDe(clave)` busca primero la clave nueva y, si no existe, la antigua mediante `aliasFoundationV1` (constante).
- La evidencia migrada conserva `tipo: comprobacion_guiada` y `conApoyo: true`. Por tanto, **como máximo llega a `practicada`, nunca a `dominada`**, y no da XP (no se llama a `registrarPractica`).
- Si se decide materializarla, `migrarFoundationV1(practicas)` copia sin sobrescribir las claves nuevas existentes, añade `'foundation-v1→ruta-v2'` a `aprendizaje.migraciones` y no hace nada en una segunda ejecución.

Prueba de la migración: con las 12 claves de `foundation_test`, las 6 unidades quedan `practicada`, ninguna `dominada`, la XP no cambia, dos ejecuciones dan el mismo resultado, las claves antiguas siguen presentes, y el estado sobrevive a `toJson` → `fromJson` y a una "versión antigua" (`ProgressState.fromJson` sin `aprendizaje`).

Otras migraciones:
- `grammar-guide-<id>-<i>` → alias a `ruta:en.<nivel>.<id>:p4:c<i+1>` cuando la gramática pase al esquema.
- Los prefijos `learn-*` y `en-v1-*` siguen siendo del banco de la biblioteca.

## Resultados analyze/test

| Comando | Resultado |
|---|---|
| `flutter analyze` | **9 issues, todos `info`** (`curly_braces_in_flow_control_structures`): 7 en `lib/core/api/sync.dart` (77, 228, 257, 285, 317…), 1 en `test/situation_units_test.dart` y 1 en `test/silencio_test.dart`. Sin errores ni advertencias. 7,8 s. Código de salida 1, porque los `info` son fatales por defecto. |
| `flutter test` | **104 pasan, 1 se omite (`exportar_semilla_test`, solo con EXPORTAR=1), 0 fallan**. 18,1 s de reloj. |
| Prueba temporal en el scratchpad (no está en el repo) | R1, R2 y R3 pasan, es decir, **confirman los defectos** descritos arriba. |

**Pruebas actuales relacionadas con aprendizaje:**
- `foundations_test` (Fundamentos v1 completo, ×1 y ×2 escala)
- `fundamentos_test` (nivel 0 en los 10 idiomas; hiragana y hangul)
- `grammar_guides_test`
- `learning_content_test` (5: assets reales, nivel manual, lo guiado no asciende)
- `learning_layout_test` (las 5 áreas visibles; Fundamentos sin confundir práctica con dominio)
- `learner_flow_test`
- `biblioteca_test` (9)
- `contenido_json_test` (3)
- `idiomas_test` (2)
- `placement_test` (4)
- `diagnostico_test` (9)
- `diagnostico_personalizado_test` (4)
- `progreso_integridad_test` (6)
- `navigation_refresh_test` (niveles 1, 5 y 9 conservan las pestañas)
- `situation_units_test`, `situation_vocabulary_test`
- `widget_test` (100 lecciones por nivel, desbloqueo, examen al 65 %)

**Ninguna prueba cubre:** reanudar la gramática, contenido del idioma meta en los niveles 3 a 10, que el nivelActual de inglés salga del nivel 0, la biblioteca o el diagnóstico en otros idiomas, un grafo de prerequisitos, ni vocabulario usado antes de enseñarse.

## Recorridos: principiante (en), otro idioma (ja, de), intermedio/avanzado (en)

Se simularon leyendo el código y con las pruebas R1 a R3. Tipos de hallazgo: **A** asume conocimientos no enseñados, **D** presenta demasiado, **I** instrucción confusa, **E** evalúa antes de enseñar, **B** bloquea, **P** pierde progreso, **O** oculta temas o hace desaparecer la gramática.

### Principiante de inglés (nativo es)

| Paso | Hallazgo | Tipo |
|---|---|---|
| Onboarding → "¿Cuál es tu nivel?" → "Empiezo desde cero" | En el paso 5 se lanza **siempre** el diagnóstico si el idioma es inglés (`onboarding_screen.dart:148`), aunque se haya elegido "desde cero". La persona responde preguntas de inglés antes de recibir enseñanza, aunque el motor empiece en el nivel 0 y no dicte. | E |
| Resultado del diagnóstico | "Fundamentos: letras y sonidos, números, colores" (`diagnostico.dart:900`), pero `/fundamentos` en inglés enseña I/you/am (v1). Las lecciones de letras (L0) no son accesibles en inglés. | I |
| `terminarOnboarding` | `fundamentos = nivelInicial == 0` y `nivelInicial` se ajusta a 1 | — |
| Inicio → "Aprender hoy" | `go('/fundamentos')`: bien para un principiante | — |
| Fundamentos v1 | Buena secuencia enseñar → practicar con ayuda. Fallar no bloquea. Los 6 pasos quedan guardados (`foundations_test`). | — |
| Tras los 6 pasos | La tarjeta dice "Repasa tus primeros pasos" y **no indica el siguiente paso** (gramática N1 "be"). `nivelActual` **se queda en 0** (R1): la cabecera muestra "Nivel 0 · Pre-A1", no hay examen alcanzable y nunca asciende salvo con otro diagnóstico. | B, I |
| Aprender → Gramática N1 "be" | Vuelve a enseñar am/is/are sin reconocer lo hecho en v1. Hay 5 temas con 2 comprobaciones cada uno. En la primera comprobación, "My name ___ Leo" usa "my" y "name", que v1 no enseñó. | A, D |
| Salir y volver a Gramática | Vuelve al "Tema 1 de 5" sin marcas (R3). El borrador de "Crea" se pierde. Tocar Aprender o "Ver ruta" cierra la pantalla. | **P, O** |
| Vocabulario, Lectura y Listening N1 | 2 unidades por nivel con 4 palabras. "Vocabulario" usa el mismo `reading_units` que Lectura (`learning_units.dart:67`). | D (poca variedad) |
| Lecciones antiguas (si se llegara a ellas) | La lección 1 enseña 3 palabras con tarjetas y pregunta la 4.ª (`elige(3)`, `parejas(0)` usa vv(0..3)); "ordenar" pide frases que no se mostraron antes (`curriculum.dart:612-620`). En los ejemplos de N1-N2, entre el 39 % (en) y el 49 % (de) de las palabras no se habían enseñado antes (heurística python, incluye nombres y flexiones). | E, A |

### Otro idioma: japonés (nativo es)

| Paso | Hallazgo | Tipo |
|---|---|---|
| Onboarding | Sin diagnóstico ("disponible primero para inglés"); nivel autodeclarado | — |
| "Desde cero" → Inicio | `fundamentos = true`, `nivelActual = 0` y la lección diaria L0-001 "Descubre: Hiragana". Tiene 8 unidades y 119 ítems en bloques de 6. Es correcto. | — |
| Nivel 1, unidad 1 "Pronombres personales" | Usa **kanji** 私/彼女, que el nivel 0 no enseña (solo muestra la romanización), y el ejemplo 私 は アナ です. "Alfabeto y sonidos" es la **unidad 3**, después de los pronombres. | A |
| Lección 4 de cada unidad | "Selecciona la imagen que corresponde a: 'Breakfast'", en inglés | A, I |
| Niveles 3 a 10 | **Contenido en inglés** (Bigger, Enough…); 20 unidades idénticas (R2) | A, D |
| Inicio → Biblioteca / Diagnóstico | "Tu biblioteca de inglés"; el diagnóstico en inglés no se aplica al curso | I |
| Practicar → Situación | Solo un botón al chat | O |
| Gramática y Fundamentos v1 | No se muestran | O |

### Otro idioma: alemán (nativo es)

Igual que en japonés, más estos puntos:
- Nivel 0 con A-Z, ä/ö/ü/ß: correcto.
- La unidad 1 del nivel 1 usa "Ich bin Ana", "Du bist mein Freund", "Er ist Arzt" antes de la unidad 14 "Verbo ser/estar" (A).
- El 49 % de las palabras de los ejemplos no se había enseñado antes (A).
- Los niveles 3 a 10 están en inglés (A).
- La explicación gramatical es un solo párrafo dentro de la lección "Frases" y no hay práctica específica de casos o género (D).

### Inglés intermedio y avanzado (B1–C1, niveles 5 a 9)

| Aspecto | Hallazgo | Tipo |
|---|---|---|
| Diagnóstico | Adaptativo y con escritura (35 %). Da `skills` por habilidad y un plan. Distingue perfiles del mismo nivel mediante `nivelSugerido`, que ajusta ±1 por habilidad, y `prioridades`, que marca la recomendada. Los `sectores` y `objetivos` solo cambian el orden (−2/−1 en la puntuación). | Parcial |
| Inicio → "Aprender hoy" | **Siempre `/fundamentos`** (I/you), también para C1 (`home_screen.dart:47-50`) | I |
| Profundidad por nivel | Gramática: N5 tiene 5 temas, N7 4, N8 4, N9 3 y N10 2, con 2 comprobaciones por tema. Lectura y listening: 2 unidades de 3 preguntas por nivel. Biblioteca: unas 10 preguntas por nivel (26 en N5). **Se agota en 1 o 2 sesiones.** | D (falta profundidad) |
| Repetición | `seleccionar` penaliza lo ya acertado (+30) pero lo vuelve a servir cuando se agota. No hay repaso espaciado ni variantes nuevas del mismo objetivo (REVISOR-CRITICO lo lista como pendiente). | — |
| Ascenso | En inglés, el examen de nivel exige 100 lecciones L{n} completadas, **que no son accesibles** (`LevelsScreen` en inglés no las lista). Solo se asciende repitiendo el diagnóstico. | B |
| Mismo nivel, perfiles distintos | Dos personas B1 con distinta debilidad (escritura frente a listening) ven la misma lista de temas. Solo cambia el área marcada "RECOMENDADO" y el nivel sugerido de la biblioteca. No hay rutas por objetivo (trabajo, examen). | Parcial |

## Pruebas necesarias

| Área | Prueba | Tipo |
|---|---|---|
| Grafo | Todos los `prerequisitos` existen en el curso (o en otro curso declarado); no hay ciclos (Kahn); cada unidad es alcanzable desde una raíz; el orden topológico respeta el `orden` de los módulos | unitaria, sobre los 10 cursos |
| Integridad | Ninguna unidad sin lecciones o pasos; cada paso de práctica o evaluación tiene ≥ 1 ítem; `respuesta` está en el rango de `opciones`; los `refs` de vocabulario y errores existen; los IDs son únicos en todo el curso; `nivelInterno == null` si y solo si `estado == planificado` (C2) | unitaria |
| Idioma de apoyo (DEC-004) | Cada `TextoApoyo` cubre `idiomasApoyo` y ningún texto está vacío; la cadena de resolución nativo → predeterminado → es funciona; widget del curso es con nativo en | unitaria y de widget |
| Enseñado antes de usado | Cada palabra del idioma meta usada en práctica o evaluación aparece en `vocabulario` de la unidad o de sus prerequisitos (lista blanca de nombres propios); gramática de los ítems ⊆ `gramaticaPermitida` acumulada | unitaria (heurística por idioma; ja y zh con tokens separados por espacios) |
| Evaluar antes de enseñar | En cada lección, `explicacion` o `ejemplos` van antes de cualquier `practica_*` o `evaluacion`; ningún ítem pregunta algo no mostrado antes en la misma lección o en los prerequisitos | unitaria |
| No filtrar inglés | Para `l ≠ en`, ningún asset `ruta/` contiene claves `en:` como contenido meta; `unidadesDe(3..10)` no devuelve el `_bancoGenerico` (regresión de R2) | unitaria |
| Acceso tras practicar | Tras practicar el tema k, reabrir `/gramatica` reanuda en k, el Temario marca ✓ y todos los temas siguen listados; `go('/aprender')` y volver a tocar la pestaña no pierden la marca (regresión de R3) | widget y router |
| Persistencia | Viaje de ida y vuelta `toJson`/`fromJson` con `aprendizaje` y `esquema`; un "cliente v1" (`fromJson` → `toJson` de la versión actual) conserva `practicas ruta:*`; un `examenes` con `double` no reinicia el estado; `extras` conserva claves desconocidas | unitaria |
| Desbloqueo y dominio | Solo lo guiado da como máximo `practicada`; `dominada` exige independiente + umbral + retención; un error tras dominar lleva a `repasar`; desbloquear no oculta nada | unitaria |
| Repaso | Intervalos de las cajas; un fallo baja 2 cajas; sin `aprendizaje` se reconstruye la caja 0 | unitaria |
| Migración | Las 12 claves de v1 dejan 6 unidades `practicada`; idempotente; sin cambio de XP; no borra claves antiguas | unitaria |
| Nivel actual | Principiante inglés con v1 completo: `nivelActual` ≥ 1 o camino claro al siguiente paso (regresión de R1) | unitaria |
| Recorridos | Widget de extremo a extremo para 3 perfiles (en desde cero, ja desde cero, en B1) con aserciones de "sin inglés en ja", "sin evaluar antes de enseñar" y "siguiente paso visible" | widget |
| Sincronización | PUT sin `aprendizaje` no borra el del servidor (prueba del backend en `backend/test`) | backend |

## Archivos a crear/modificar (propietario sugerido por archivo)

| Archivo | Acción | Propietario sugerido |
|---|---|---|
| `lib/core/aprendizaje/{texto_apoyo,modelos,cargador,grafo,dominio,repaso,migracion,providers}.dart` | Crear | Arquitectura (D) |
| `assets/contenido/<l>/ruta/curso.json` y `<modulo>.json` | Crear (empezar por `en.f0` a partir de `foundations.dart`, y `de`/`ja` f0 y a1-1) | Contenido y pedagogía |
| `pubspec.yaml` | Añadir `assets/contenido/<l>/ruta/` en los 10 idiomas | Arquitectura |
| `lib/core/state/providers.dart` | Campos opcionales `esquema`, `aprendizaje` y `extras`; `fromJson` tolerante (`num` → int) sin reiniciar el estado | Arquitectura |
| `backend/src/routes/usuarios.ts` | Fusionar `aprendizaje` cuando el PUT no lo trae | Backend |
| `lib/features/library/grammar_screen.dart` | Reanudar el tema, marcar ✓ desde `practicas`, guardar borradores | Interfaz |
| `lib/app/router.dart` | Revisar el reinicio de rama al volver a tocar la pestaña (u ofrecer "continuar donde lo dejé") | Interfaz |
| `lib/core/content/curriculum.dart` | Dejar de servir `_bancoGenerico` y `palabrasImagen` en otros idiomas: marcar esos niveles como "en preparación" | Arquitectura y contenido |
| `lib/core/state/providers.dart` (`fundamentosPendientes`) | Para inglés, considerar v1 o las unidades `en.f0.*` en lugar de L0 | Arquitectura |
| `lib/features/course/levels_screen.dart`, nueva `lib/features/ruta/ruta_screen.dart` | Mapa de ruta común a los 10 idiomas con los estados de unidad | Interfaz |
| `lib/features/foundations/foundations_screen.dart` | Leer el contenido del esquema (multilingüe) en lugar de `foundationUnits` fijos | Interfaz y arquitectura |
| `assets/contenido/en/diagnostico.json` | Decidir si se elimina o se reutiliza (hoy no se usa) | Contenido |
| `test/aprendizaje_*_test.dart` (grafo, integridad, apoyo, migración, dominio, reanudación de gramática, recorridos) | Crear | QA y arquitectura |
| `lib/features/home/home_screen.dart` | **No modificar** en esta fase. Registrar como deuda: hero siempre en `/fundamentos` para inglés, diagnóstico y biblioteca fijos en `en`, `go('/aprender')` | — (quien sea responsable del Inicio) |

## Decisiones que requieren revisión humana

1. **Desbloqueo:** ¿el prerequisito basta con `practicada` o exige `dominada`? ¿Las unidades bloqueadas se pueden leer? Se recomienda que sí.
2. **Criterio de dominio por defecto:** umbral 0,8, mínimo 3 a 5 ítems, 2 formatos y 1 día de retención. ¿Es igual para todos los niveles?
3. **Niveles 3 a 10 fuera de inglés:** ¿se ocultan ya ("en preparación") o se mantienen hasta tener contenido? Hoy muestran inglés.
4. **Fundamentos:** ¿v1 (microlecciones) sustituye al nivel 0 antiguo (letras y números) en inglés, o se suman? ¿Y en los otros 9 idiomas? ¿Cómo sale un principiante de inglés del nivel 0?
5. **Ascenso en inglés:** ¿se hace por dominio del grafo, por examen de nivel con banco propio o por nuevo diagnóstico? Hoy el examen no es alcanzable.
6. **Identificadores:** slugs con prefijo de idioma y `concepto` compartido. ¿Quién mantiene la lista de conceptos?
7. **Materializar la migración** o dejarla solo como alias de lectura (recomendado: alias).
8. **Sincronización:** ¿se aceptan la fusión en el backend y `extras` en el cliente, o un endpoint de progreso por dominio?
9. **DEC-004:** confirmar la cadena de respaldo nativo → `apoyoPredeterminado` → `es`, y si en el curso `es` se muestra inglés a quien no habla inglés.
10. **Home:** el Inicio nuevo no se puede tocar, pero contiene tres acoplamientos a inglés (hero, diagnóstico, biblioteca). ¿Quién los corrige y cuándo?
