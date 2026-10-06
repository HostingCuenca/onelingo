# Plan del curso de alemán (de) N1–N10 para hispanohablantes

Estado: **completo** (06-10-2026): Nivel 0, Fundamentos (f0), ruta N1–N10 (500 clases; 100 bloques con GO), prueba de ubicación v2 (180 ítems, 10 GO) y «Mis verbos» (128); `de` en `idiomasConRuta`; `de.a1-1` retirado (el idioma no tenía ruta activa, así que no hay progreso de ruta que mapear). Diseño original (05-10-2026): Sigue DEC-034 (plan de clases antes del contenido; 10 niveles × 50 clases en bloques de 5; Fundamentos f0 de 8 unidades), con el **método ligero** descrito abajo. Nada de esto está integrado en la app todavía.

Hecho y validado:

| Pieza | Archivo | Validador | Resultado |
|---|---|---|---|
| Fundamentos | `curriculo/de/f0.json` | `validar_fundamentos.py de` | 0 errores · 8 unidades · 26 claves · 118 vocablos |
| Esqueleto N1 | `tools/curriculo/de/n1-outline.json` | `validar_outline_n1.py de` | 0 errores · 49 claves nuevas · 42 previos |
| Esqueletos N2–N10 | `tools/curriculo/de/nX-outline.json` | `validar_outline_nivel.py de X` | 0 errores · 48 claves nuevas por nivel |

Total: 523 claves únicas (16 de Nivel 0 + 26 de f0 + 49 de N1 + 48 × 9). Ninguna clave se repite entre niveles; ningún archivo menciona Ecuador ni ciudades ecuatorianas.

## 1. Método ligero: qué se quita respecto al portugués y por qué

El portugués (DEC-035) acumuló la mayoría de sus errores de revisión en el **canon**: protagonista fija, cronología, calendario de N1, hechos reales de Recife y apellidos del reparto. Cada bloque tenía que ser coherente con todos los anteriores y el revisor gastaba media revisión en «hechos del reparto». En alemán:

| Se quita | Se sustituye por |
|---|---|
| `MAPA.md`, reparto canónico, `personajes` y `hechosDelReparto` en `n1.json` | Nada. Cada clase es una **situación concreta autónoma** (una panadería, una reunión, una llamada a la aseguradora). |
| Protagonista y cronología continuas | Nombres genéricos alemanes por clase (Anna, Jonas, Frau Becker, Herr Wolf…) o el papel en alemán («Kellnerin», «Arzt», «Mitarbeiterin»). Un nombre no obliga a nada en la clase siguiente. |
| Hechos reales de una ciudad (líneas de metro, hospitales) | Lugares genéricos («der Bahnhof», «die Apotheke») o ciudades grandes sin datos verificables (Berlin, Hamburg, München, Köln, Leipzig). Sin direcciones, líneas ni precios «reales». |
| Sección «Hechos del reparto confirmados» en la revisión | Se elimina; el revisor dedica ese tiempo a la corrección del alemán. |
| Ficha larga con contexto narrativo | Ficha corta: `situacion` (1 línea), `tarea`, `gramatica`, `vocabulario`, `sonido`, `ejercicios`. |

Lo que **no** se simplifica: exigencias MCER por nivel, tipos de ejercicio y esquema (los mismos de fr/es/pt), reciclaje espaciado, reglas de «nada sin enseñar», una sola respuesta por ítem, apoyo bilingüe es/en. La simplificación está en la generación y la revisión, no en el nivel.

## 2. Alumno y variedad

- **Alumno:** hispanohablante adulto (EE. UU. y Latinoamérica); textos de apoyo en **español latino neutro con tú** e **inglés americano**. El inglés ayuda mucho en alemán (cognados germánicos: Haus/house, Wasser/water, trinken/drink; orden V2 parecido al inglés antiguo); la versión inglesa compara con el inglés cuando aclara.
- **Variedad:** **alemán estándar de Alemania** (bundesdeutsches Standarddeutsch). Ortografía de la reforma de 2006, con ß (Straße, groß). Léxico: Tschüss, Brötchen, Januar, Samstag, Sahne, Tomate, Kartoffel, Treppe, Abitur. Uhrzeit: «Viertel nach / vor», no «viertel acht».
- **Austria y Suiza:** solo **comprensión**, a partir de N8 (N8 b04: Perfekt con sein en sitzen/stehen/liegen, Jänner, heuer; estándar suizo sin ß, Velo, parkieren). Nunca como forma esperada en una respuesta.
- **Tratamiento:** **Sie** por defecto con adultos desconocidos y en el trabajo; **du** con amigos, familia, niños y en contextos juveniles. La ficha fija cuál. El paso del Sie al du se enseña (N4 b06, N9 b01).
- **Exámenes de referencia:** Goethe-Zertifikat A1 (Start Deutsch 1), A2, B1, B2, C1; telc Deutsch; ÖSD. La prueba de cierre de cada nivel imita el formato Goethe del MCER correspondiente.
- **Sin Ecuador.** Países de ejemplo: México, Colombia, España, Estados Unidos, Argentina, Chile, Perú, Suiza, Austria. En `curso.json` actual hay que quitar «Quito» de `palabrasLibres` (y cualquier «Ecuador» del vocabulario heredado).

## 3. Progresión gramatical N1–N10 (MCER A1→C1)

Cada nivel: 48 claves nuevas (c01–c48, una por clase), c49 proyecto, c50 prueba. N1 introduce 49 (su c49 aún enseña). Las claves exactas están en los esqueletos; aquí, el resumen por bloques.

| Nivel | MCER | Núcleo gramatical | Referencia |
|---|---|---|---|
| **Nivel 0** | — | Leer y pronunciar: alfabeto, Umlaut, ß, longitud vocálica, ie/ei/eu, ch (ich/ach), sch/sp/st, z/w/v, ensordecimiento final, r vocalizada, schwa, h de longitud, acento, mayúscula del sustantivo, oclusión glotal (16 claves) | — |
| **f0** | A1 inicial | Saludos y du/Sie, sein/heißen, género y artículos der/die/das/ein, kommen aus/wohnen in, nicht/kein y preguntas, deletreo y números 0–12, V2 básico, falsos amigos | Start Deutsch 1 |
| **N1** | A1 | Presente regular e irregular (e→i, a→ä), haben, posesivos en nominativo, plural, **acusativo** (artículos y pronombres de 3.ª), negación, doch, verbos **separables**, **inversión V2**, es gibt, **dativo** de lugar (in/an + dat.), modales (können, müssen, wollen, dürfen, möchten), imperativo Sie/du/ihr, aber/denn, Präteritum de sein/haben, **Perfekt** con haben y sein | Goethe A1 |
| **N2** | A2 | Reflexivos, preposiciones temporales, sollen, **weil/dass/wenn** (verbo final), Perfekt de separables/inseparables/-ieren, Präteritum de modales, **Wechselpräpositionen**, verbos de posición, dativo (artículos y pronombres), würde/könnte de cortesía, Futur I, comparativo y superlativo, **declinación del adjetivo** (tras artículo determinado, indeterminado y cero), preposiciones con acusativo y dativo, preguntas indirectas, lassen, zu + infinitivo, orden dativo-acusativo | Goethe A2 |
| **N3** | B1 | Präteritum regular e irregular, Plusquamperfekt, da-/wo-compuestos, als/wenn, während/bevor, **pasiva** (Präsens, Präteritum, con modal, con agente), **n-Deklination**, **oraciones de relativo** (nom., acus., dat., con preposición, dessen/deren, was/wo), **genitivo**, **Konjunktiv II** (presente y pasado), um…zu/damit, obwohl/trotzdem, je…desto, conectores dobles, discurso referido con dass/sollen | Goethe B1 |
| **N4** | B1+ | als ob, doble infinitivo, deseos irreales, modales subjetivos, Futur II, condicional sin wenn, Zustandspassiv, pasiva impersonal, Nominalstil básico, sich lassen / sein zu (sustitutos de pasiva), Partizip I, wer…der, indem, zwar…aber, registro du/Sie, carta formal, partículas modales avanzadas, hin/her, so…dass | Goethe B1 / telc B1 |
| **N5** | B2 | Funktionsverbgefüge, **Partizipialattribut extendido**, bekommen-Passiv, **Konjunktiv I** (estilo indirecto y sustitución), verbos de habla, distanciamiento (sollen/wollen), TeKaMoLo, Satzrelativ, nominal ↔ verbal, preposiciones de genitivo, conectores escritos B2 | Goethe B2 |
| **N6** | B2 | es sei denn, haben/sein zu, erfolgen, Konjunktiv II de atenuación, Spaltsatz, Ausklammerung, Gerundivum (die zu lösende Aufgabe), relativo con welch-, Erörterung, causa-efecto, prognosis con modales | Goethe B2 / telc B2 |
| **N7** | B2+ | Registro y connotación, consecutio temporum, ehe/indessen, irreal concesivo, angenommen/gesetzt, ohne dass + Konj. II, gelten als, atributos multinivel, metáforas e ironía, Präsens historicum, erlebte Rede, perspectiva narrativa, zumal, niveles de estilo | Goethe B2 |
| **N8** | C1 | Lengua hablada (reducciones, dislocación, weil + V2 oral), implicatura con partículas, lítotes, adverbios -erweise, figuras retóricas, framing, variedades (Austria, Suiza, regiones, jerga juvenil: solo comprensión), refranes y fórmulas binarias, Inhaltsangabe, futuro en el pasado, Ablaut y Konj. II literarios (lectura), reclamación C1, hedging académico, estilo impersonal | Goethe C1 |
| **N9** | C1 profesional | Networking, storytelling, comunicación ejecutiva, moderación y actas (Konj. I, pasiva), entrevistas STAR, informes con datos, riesgo y seguridad (Infinitiv als Imperativ), Behördendeutsch y Widerspruch, negociación por intereses, Ich-Botschaften, propuestas. Cada clase incrusta un punto gramatical en `gramatica`. | telc C1 Beruf |
| **N10** | C1 avanzado | Partículas de conversación, ritmo narrativo, ironía e hipérbole activas, diplomacia, escritura académica extensa, plan de negocio y contrato, crítica cultural, vida cotidiana compleja, **Sprachmittlung** (mediación oral, resumen para terceros, Leichte Sprache), proyecto final y prueba tipo Goethe C1 | Goethe C1 |

Extensión de la lectura en la situación (`reglasAutoria`, igual que fr): N1 3–6 líneas; N2 60–160 palabras; N3–N4 130–300; N5–N7 270–560; N8–N10 360–770.

## 4. Retos del alemán para hispanohablantes

Cada uno tiene clase propia en el esqueleto y debe aparecer en `erroresFrecuentes` cuando toque.

1. **Casos (Nom., Akk., Dat., Gen.).** No existen en el español fuera de los pronombres (lo/le). Orden de entrada: nominativo (f0) → acusativo (N1 b03–b05) → dativo de lugar (N1 b07) → Wechselpräpositionen y dativo completo (N2 b03) → genitivo (N3 b03). Siempre con **tabla completa** de artículos y la pregunta del caso (Wen? Wem? Wessen?). Errores típicos: *«Ich habe ein Hund»*, *«mit der Freund»*, *«Ich helfe dich»*.
2. **Género gramatical arbitrario y distinto del español.** der Tisch (m) / la mesa, das Mädchen (n), die Sonne / el sol, der Mond / la luna. Todo sustantivo se enseña **con artículo y plural** («der Tisch, -e»). Pistas fiables: -ung/-heit/-keit/-ion → die; -chen/-lein → das; -er de agente → der. Los colores del artículo (azul der, rojo die, verde das) son opcionales y no se evalúan.
3. **Plural** con cinco patrones (-e, -er, -en, -n, -s, con o sin Umlaut). No se deduce: se enseña con cada sustantivo.
4. **Verbos separables** (anrufen → «Ich rufe dich an»; «…, weil ich dich anrufe»; «angerufen»; «anzurufen»). Clase propia en N1 b06 y N2 b02, repaso en subordinada (N2 b09). Inseparables be-, emp-, ent-, er-, ge-, miss-, ver-, zer- sin ge- en el participio.
5. **Orden de palabras.** V2 en la principal (*«Heute ich gehe»* → «Heute gehe ich»), **verbo final** en la subordinada (*«weil ich habe keine Zeit»*), **Satzklammer** con modales y Perfekt («Ich habe gestern Brot gekauft»), negación nicht al final o ante lo negado, TeKaMoLo (N5). En `ordenar`, las variantes de orden igualmente correctas (Vorfeld distinto) van en `aceptadas`.
6. **Umlaut y ß.** ä, ö, ü no tienen equivalente: ü ≈ «i» con labios de «u»; ö ≈ «e» con labios de «o». ß = «ss» tras vocal larga o diptongo. La corrección acepta **ae/oe/ue/ss** (teclados sin Umlaut) con aviso, salvo en clases de ortografía.
7. **Mayúscula de todos los sustantivos** (y de Sie de cortesía). Se enseña en Nivel 0 y f0; se evalúa desde N1 (ver §7, `mayusculasSignificativas`).
8. **Compuestos** (Krankenversicherung, Haustür). Se enseña a segmentar (Kranken-versicherung) y que el género lo da la última palabra. Las Fugen -s-, -n-, -en-, -e-, -er- se enseñan en N1 b07 y N5.
9. **Pronunciación:** longitud vocálica (Staat/Stadt), ch (ich/ach), sch/sp/st, z = «ts», w = «v», v = «f», ensordecimiento final (Tag → «tak»), r vocalizada («besser» ≈ «bessa»), schwa final átono, h muda tras vocal. Todo en Nivel 0, recordado en el «sonido del día» de N1.
10. **Falsos amigos** (⚠ obligatorio): also (entonces) ≠ «así que» en todos los casos, Chef (jefe) ≠ chef, Termin (cita) ≠ término, Gymnasium (instituto) ≠ gimnasio, eventuell (quizá) ≠ eventual, Karte (tarjeta/mapa/entrada) ≠ carta (Brief), bekommen (recibir) ≠ become, Rente (jubilación) ≠ renta, sensibel (sensible, delicado) ≠ «sensible» del inglés (vernünftig), Gift (veneno) ≠ gift, Rat (consejo) ≠ rata/rat, Blamage (vergüenza), Präservativ (preservativo, no conservante), Konkurrenz (competencia), Akt (desnudo artístico/expediente), aktuell (actual, no «actually»), spenden (donar) ≠ spend.
11. **Perfekt con haben o sein** (movimiento y cambio de estado con sein). El hispanohablante usa siempre haben.
12. **Präteritum frente a Perfekt:** Perfekt en lo oral; Präteritum de sein/haben/modales desde N1–N2 y narrativo en N3.

## 5. Tipos de ejercicio y esquema

Idénticos a fr/es/pt (esquema 2, `ESQUEMA_CONTENIDO.md`): pasos `explicacion`, `ejemplos`, `vocabulario`, `patron`/`tabla`, `practica_guiada` (3–5), `practica_independiente` (3–4), `situacion` (contexto + texto + 1–2 preguntas), `evaluacion` (≥ 4 ítems, ≥ 2 formatos); formatos `elegir`, `escuchar`, `ordenar`, `completar`, `escribir`, `relacionar`. Plan de ejercicios por ficha (`ejercicios`) como en pt: guiada 3–5, independiente 3–4, evaluación 4–8 con ≥ 3 formatos.

Usos propios del alemán:
- `completar` de **terminación** (artículo, adjetivo, verbo): un solo hueco por ítem; la pista nombra el caso («Akk., masc.»).
- `elegir` de caso/género con las tres opciones der/die/das (o den/dem/des): nunca dos defendibles.
- `ordenar` para V2, verbo final y separables; `aceptadas` con las variantes de Vorfeld.
- `relacionar` sustantivo ↔ artículo + plural; falsos amigos.
- `escuchar` para longitud vocálica, Umlaut y ch.

## 6. Plan de producción

Mismo flujo que pt, sin canon. Agentes con el perfil `onelingo-autor` (≤ 30 llamadas, paquete + validador por bloque).

| Paso | Qué | Agentes | Tokens aprox. |
|---|---|---|---|
| 0 | Herramientas de §7 (paquete, validar_plan_detallado, morfología de en validar_ruta.py e integridad.dart, verbos-de, integrar) | 2–3 (o el orquestador) | 2–3 M |
| 1 | Nivel 0 «Leer y pronunciar» (~10 unidades con audio) y reescritura bilingüe de f0 a esquema 2 | 2 autores + 1 revisor | 1 M |
| 2 | Fichas planificadas `curriculo/de/nX.json` desde cada esqueleto (5 lotes de 10 fichas con `ejercicios`) + `validar_plan_detallado.py de` | 50 lotes + 10 revisores de plan | 12–15 M |
| 3 | **Piloto N1 b01–b02**: autor, revisor, ajuste del encargo (calibración) | 2 + 2 | 1 M |
| 4 | Contenido N1–N10: 100 bloques de 5 clases | 100 autores | 25–30 M |
| 5 | Revisión por bloque (GO/REVISE); se estima que ~50 % pide una segunda pasada | 100–150 revisores | 15–20 M |
| 6 | Cierre de nivel: `integrar.py de N`, `validar_ruta.py de`, prueba en la app | orquestador | 0,5 M |
| 7 | Banco de ubicación v2 (sin Lumo) por pares de niveles + revisión | 5 + 5 | 2–3 M |

**Total: ~270–330 ejecuciones, 55–70 M tokens.** Paralelismo recomendado: 5 bloques a la vez dentro de un nivel (los prerrequisitos de vocabulario encadenan los bloques; validar_bloque.py encadena borradores no integrados). Cerrar e integrar cada nivel antes de abrir el siguiente.

Otros pendientes de producción:
- **Voces de-DE** (`NATIVAS` en la herramienta de audio: narradora y narrador de Alemania; Lumo en alemán). Calibrar antes del piloto: Umlaut, ch, r vocalizada y longitud vocálica.
- **Situaciones:** 50 × 3 por nivel (las genera el autor desde `situacion` de la ficha; no hay canon que respetar).
- **`verbos-de.json`** (~130 verbos: los fuertes y mixtos de A1–B2, los modales, sein/haben/werden, separables frecuentes).
- **Retirar** el módulo heredado `de.a1-1` (y `nivel-0/1/2.json` legados) cuando N1 se publique; los ids `de.f0.*` se conservan donde coinciden (laute-gruesse, pronomen-du-sie, sein-heissen, der-die-das, nicht-kein-fragen, alphabet, vorstellen). `de.f0.vokale-konsonanten` pasa a Nivel 0 y se crea `de.f0.herkunft-wohnort`; `curso.json` debe mapear el id antiguo para no perder progreso.
- **`curso.json`:** `idiomasApoyo: ["es", "en"]`, `vocabularioEstricto: true`, `reglasAutoria` (como fr), `palabrasLibres` sin «Quito».

## 7. Herramientas a adaptar (diseño, sin implementar)

### 7.1 `tools/curriculo/paquete.py`
- `n1['personajes']` → `n1.get('personajes', [])` y omitir la sección «Reparto» y «Hechos» si están vacías.
- Clase modelo: mientras no haya bloque de alemán revisado, usa la de fr (ya cae ahí); después, la primera clase GO de de.

### 7.2 `tools/curriculo/validar_plan_detallado.py`
- Parametrizar por idioma el mensaje «situación no redactada íntegramente en pt-BR», la regex `ESPANOL_EN_SITUACION` (para de: detectar palabras españolas frecuentes en la situación: «el», «la», «que», «pero», «con», sin falsos positivos con «die», «oder», «also») y quitar el control especial `pt.n1.c50` para de (o generalizarlo a «c50 = prueba sin `introduce`»).

### 7.3 `tools/validar_ruta.py` y `lib/core/aprendizaje/integridad.dart` (deben dar el mismo resultado)
1. **`PUNTUACION` / normalización:** añadir „ ‚ ‘ ’ › ‹ (comillas alemanas) en Python, Dart y en la normalización de la corrección. Hoy «„Hallo“» deja «„hallo» como palabra desconocida.
2. **`conocida_de(palabra, conocidas, formas_verbales)`** con despacho `idioma == 'de'` (Python `meta()` y Dart `ruta.curso.idioma`):
   - comparación sin distinguir mayúsculas (la mayúscula se controla aparte);
   - **sustantivos:** plural -e, -er, -en, -n, -s, -nen y reversión de Umlaut (Häuser → Haus, Äpfel → Apfel, Mütter → Mutter); dativo plural -n; genitivo -s/-es; n-Deklination (-en/-n: Kollegen → Kollege);
   - **adjetivos:** -e, -en, -em, -er, -es; comparativo -er y superlativo -st-/-est- con y sin Umlaut (älter → alt, größte → groß);
   - **verbos:** presente -e, -st, -est, -t, -et, -en, -n; Präteritum débil -te, -test, -ten, -tet; Partizip II ge-…-t/-et; inseparables (be-, emp-, ent-, er-, ge-, miss-, ver-, zer-) sin ge-; -ieren → -iert; **zu-Infinitiv** (anzurufen → anrufen); formas fuertes e irregulares solo vía `verbos-de.json`;
   - **separables:** enseñar «aufstehen» hace conocidas «stehe … auf», «aufgestanden», «aufzustehen»; la partícula suelta (auf, an, mit, ein, aus, zurück…) cuenta como conocida si el verbo separable lo es;
   - **contracciones:** im, am, ins, zum, zur, vom, beim, ans, aufs = sus partes;
   - **compuestos:** si la palabra no es conocida, segmentar en partes conocidas (≥ 3 letras) con Fugen -s-, -es-, -n-, -en-, -e-, -er-; resultado **aviso**, no error ni paso silencioso (el autor debe enseñar el compuesto si es vocabulario de la clase).
3. **Control de mayúsculas** (solo de): sustantivo conocido escrito en minúscula en mitad de frase → error; homógrafos (essen/Essen, leben/Leben, laut/Laut) se ignoran; nombres propios y `palabrasLibres` exentos.
4. **`TITULOS`:** añadir Herr, Frau, Dr., Prof. (para los nombres genéricos de las clases).
5. **Símbolos:** «€» y «%» en texto de audio → aviso «escribe Euro / Prozent».
6. **Corrección en la app:** opción de curso `mayusculasSignificativas: true` (en de, «haus» se acepta con aviso «Los sustantivos van con mayúscula»), y tolerancia **ae/oe/ue/ss ↔ ä/ö/ü/ß** con aviso. Mientras no exista la morfología del punto 2, el encargo exige que **toda forma flexionada** aparezca antes en una `tabla` o en `ejemplos`.

### 7.4 `tools/contenido/verbos/generar_verbos.py` → `verbos-de.json`
- Entrada `IDIOMAS['de']`: personas `ich, du, er/sie/es, wir, ihr, sie/Sie` (con es/en); tiempos `praesens`, `praeteritum`, `perfekt`, `futur1`, `konjunktiv2` (+ `imperativ` du/ihr/Sie como formas aparte).
- Campos extra por verbo: `auxiliar` (haben/sein), `trennbar` (prefijo separable o null), `partizip2`, `praeteritum3sg`.
- `CargadorRuta.formasVerbales` (Dart) y `validar_ruta.py` leen `verbos-de.json` igual que `verbos-pt.json`.

### 7.5 `tools/contenido/ruta-de/integrar.py`
Copia de `ruta-pt/integrar.py` con: `IDIOMA='de'`, `ULTIMA_F0='de.f0.vorstellen'`, `NOMBRES_LIBRES` con un banco de nombres alemanes genéricos (Anna, Jonas, Lena, Paul, Mia, Felix, Sophie, Lukas, Frau Becker, Herr Wolf…), `curso_base()` con `idiomasApoyo ["es","en"]`, `vocabularioEstricto`, `reglasAutoria` y `palabrasLibres` sin Quito; exige `revision-nX-bYY.md` con GO; encadena prerrequisitos; retira `de.a1-1` al publicar N1; termina con `validar_ruta.py de`. Sin lógica de reparto.

### 7.6 `validar_outline_*.py`, `validar_plan.py`, `validar_fundamentos.py`, `validar_bloque.py`
Ya aceptan `de` sin cambios (probado).

## 8. Reglas de producto que se mantienen

- Lumo nunca aparece con otro personaje a la vez y nunca en las pruebas de ubicación.
- Ilustraciones solo con emoji Noto; no se generan imágenes.
- Sin menciones a Ecuador (mercado EE. UU. + Latinoamérica).
