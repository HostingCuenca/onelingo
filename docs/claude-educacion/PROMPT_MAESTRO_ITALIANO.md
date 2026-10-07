# PROMPT MAESTRO: producir el curso de italiano de OneLingo

> Pega este documento entero como instrucciones para el agente (Codex u otro) que trabaja dentro del repositorio `onelingo`.

---

## 0. MODO DE TRABAJO: PRODUCIR, NO INVESTIGAR

Eres el **autor de contenido** del curso de italiano de OneLingo, una app para que hispanohablantes de Latinoamérica y Estados Unidos aprendan idiomas. El apoyo de cada clase va en español y en inglés.

**La planificación ya está hecha y aprobada:**
- qué enseña cada una de las 500 clases;
- el orden de los temas;
- las reglas de escritura;
- los formatos;
- los validadores.

Tu único trabajo es **escribir el contenido** y dejarlo validado.

- **No** explores la app ni el resto del repositorio, **no** re-analices el plan y **no** propongas cambios de enfoque.
- **No** preguntes, salvo que algo te bloquee de verdad. Si una regla te parece discutible, cúmplela y anótalo en el informe.
- **No** llames a ninguna API de pago para escribir contenido. El contenido lo escribes tú.
- **No** toques otros idiomas, el servidor ni los archivos `.env`; las claves solo se leen dentro de scripts, sin imprimirlas.
- **No** hagas commit, push ni despliegue. Eso lo hace el dueño cuando el italiano esté completo.
- **No** generes imágenes.

---

## 1. LO QUE YA ESTÁ HECHO (no lo rehagas)

| Pieza | Dónde |
|---|---|
| Ficha del idioma: variante, nombres permitidos, guías de pronunciación, errores típicos, falsos amigos | `tools/ia/idiomas/it.md` |
| Tema de las 500 clases: 48 claves por nivel, más el proyecto (c49) y la prueba (c50) | `tools/curriculo/it/mapa-n1.json` … `mapa-n10.json` |
| Plan de Nivel 0 y Fundamentos: 16 sonidos previos y 26 claves de salida | `curriculo/it/f0.json` |
| Fundamentos escritos: 8 unidades con apoyo es/en | `tools/contenido/ruta-it/borrador-f0.json` |
| N1 bloque 1: esqueleto, ejercicios y las 5 clases | `tools/curriculo/it/n1-outline.json`, `curriculo/it/n1.json`, `tools/contenido/ruta-it/n1-b01.json` |
| Instrucciones de cada etapa | `tools/ia/prompts/*.md` (te llegan dentro de cada encargo) |
| Programa que arma, valida y te devuelve los errores | `tools/ia/openai_contenido.py` en **modo `--manual`** |

---

## 2. CÓMO PRODUCES: EL CICLO DEL MODO MANUAL

El programa hace todo lo mecánico:
- ids y orden;
- repasos espaciados;
- montaje del formato de la app;
- validación.

Tú haces de «modelo»: escribes el contenido de cada encargo.

```
1. Ejecuta el comando de la etapa con --manual.
2. Si termina con «PENDIENTE: lee tools/ia/registro/manual/pendientes/<clave>.md»:
   a. Lee ese archivo entero. Trae las instrucciones completas, la entrada
      (la ficha de la clase y lo ya enseñado) y el esquema JSON obligatorio.
   b. Escribe SOLO el objeto JSON de respuesta en la ruta que indica el encargo:
      tools/ia/registro/manual/respuestas/<clave>.json
   c. Vuelve a ejecutar EXACTAMENTE el mismo comando.
3. El programa arma, valida y, si hay errores, crea un encargo de reparación
   con cada error explicado. Repites el paso 2 hasta que diga «0 errores».
4. Cuando el comando termina sin PENDIENTE, la etapa está hecha.
```

**Reglas del ciclo:**
- Un encargo cada vez. Lee el encargo entero antes de escribir: las reglas están dentro y se cumplen al pie de la letra.
- Si el programa dice «TU RESPUESTA NO CUMPLE EL ESQUEMA», corrige ese mismo archivo de respuesta. En el esquema todos los campos son obligatorios y lo opcional va como `null`.
- En una reparación corrige **todos** los errores listados sin romper lo demás, y devuelve el objeto completo.
- Si una clase sigue con errores tras 3 reparaciones, anótala en el informe y sigue con la siguiente.

---

## 3. ORDEN DE TRABAJO EXACTO

### Paso 1. Fundamentos (f0): revisión final
1. Lee `tools/contenido/ruta-it/borrador-f0.json` (8 unidades) contra las reglas del §4 y corrige directamente lo que falle.
2. Valida con `python3 tools/contenido/ruta-it/validar.py`: 0 errores. El script no escribe en `assets/`.

### Paso 2. Nivel 0 «Leer y pronunciar italiano», rehecho en formato nuevo
El archivo publicado `assets/contenido/it/nivel-0.json` está obsoleto: formato viejo, solo español, guías de pronunciación erróneas y 5 sonidos sin enseñar.

1. Crea `tools/contenido/nivel0-it/generar.py` copiando la **estructura** de `tools/contenido/nivel0-de/generar.py`, nunca su contenido alemán.
2. El script escribe `assets/contenido/it/nivel0/nivel0.json` y `assets/contenido/it/nivel0/sonidos.json`.
3. **Contenido:** los 16 sonidos de `previos` en `curriculo/it/f0.json`:
   - sound-text, alphabet, full-vowels, open-closed-vowels;
   - c-g-soft-hard, ch-gh-hard, gn-gli, sc-sound, qu-sound, z-sound;
   - s-voicing, r-tap-trill, b-v-distinction, double-consonants, h-silent, stress-accents.
4. **Unidades:** se agrupan en 9 unidades más una prueba de salida (u10), como el alemán.
5. **Reglas del Nivel 0:**
   - Las guías de pronunciación salen **solo** de `tools/ia/idiomas/it.md`.
   - Apoyo bilingüe {es, en}.
   - Lumo aparece solo en la bienvenida (u01, lección 1), nunca en la evaluación.
   - Solo emoji que ya existen en `assets/img/emoji/`.
6. Valida con `python3 tools/contenido/validar_nivel0.py it assets/contenido/it/nivel0/nivel0.json --bilingue`: 0 errores.

### Paso 3. Voces italianas en ElevenLabs (pronunciación)
Todo el audio de la app sale de ElevenLabs desde `backend/src/lib/voz.ts`. Hoy el italiano usa las voces genéricas, que no son nativas. Haz lo mismo que se hizo con el alemán (Petra y Julius):

1. **Candidatas:**
   - Con un script que lea `ELEVENLABS_API_KEY` de `backend/.env` sin imprimirla, busca en la biblioteca de voces de ElevenLabs voces **nativas de Italia** con acento estándar: 3 femeninas para narrar y 3 masculinas para los diálogos.
   - Puedes filtrar con `GET https://api.elevenlabs.io/v1/shared-voices?language=it` y por acento.
2. **Prueba de pronunciación:**
   - Sintetiza con cada candidata, con el modelo y el `language_code: "it"` que ya usa `voz.ts`, estas frases:
     - «Gnocchi, famiglia, figlio, sciarpa, pizza, zio, rosa, casa, caro, carro, perché, città, pesca (pèsca/pésca)»
     - «Buongiorno, mi chiamo Giulia e abito a Bologna.»
     - «Ho ventitré anni; il treno parte alle diciassette e quindici.»
   - Transcríbelas de vuelta con el speech-to-text de ElevenLabs (`/v1/speech-to-text`).
   - Elige la narradora y el narrador con mejor resultado.
   - Guarda las muestras en `tools/contenido/voces-it/` para que el dueño las escuche.
3. **Cifras:**
   - Prueba «Il 15 marzo 1921», «alle 17:15», «23 anni», «4,50 euro».
   - Si alguna se lee mal, crea `backend/src/lib/numeros_it.ts` siguiendo `numeros_de.ts` y úsalo en `textoParaVoz` para `it`.
4. **Configuración:**
   - En `voz.ts`, añade las dos voces a `VOCES`, con un comentario de la fecha y por qué se eligieron.
   - Añade `it: { narradora: '<id>', narrador: '<id>' }` a `NATIVAS`.
   - Comprueba que `npx tsc --noEmit` pasa en `backend/`.
   - **No reinicies nada en el servidor.**

### Paso 4. N1 completo (bloques 2 a 10; el 1 ya está escrito)
```
python3 tools/ia/openai_contenido.py outline it 1 --bloques 2-10 --manual
python3 tools/ia/openai_contenido.py fichas  it 1 --bloques 2-10 --manual
python3 tools/ia/openai_contenido.py clases  it 1 <B> --manual       # B = 2 … 10, en orden
python3 tools/ia/openai_contenido.py revisar it 1 <B> --manual       # B = 1 … 10, en orden
```
- En **`revisar`** haces de revisor exigente de tu propio trabajo:
  - lee cada ítem como un alumno listo;
  - corrige en la clase devuelta;
  - el veredicto es «GO» solo si no queda nada grave ni medio.
- Cada revisión deja `tools/contenido/ruta-it/revision-n1-bYY.md` con GO o REVISE.

### Paso 5. N2 a N10, nivel por nivel y en orden
Para cada nivel N:
```
python3 tools/ia/openai_contenido.py outline it N --manual
python3 tools/ia/openai_contenido.py fichas  it N --manual
python3 tools/ia/openai_contenido.py clases  it N <B> --manual       # B = 1 … 10
python3 tools/ia/openai_contenido.py revisar it N <B> --manual       # B = 1 … 10
```
- Al cerrar el outline de un nivel, el programa ejecuta su validador, que debe dar 0 errores.
- Cada bloque termina con validador en 0 y revisión GO.

**Control de calidad sobre la marcha** (no te detiene):
- Al terminar N1 bloque 1 y N6 bloque 1, haz una lectura crítica completa de esos 5 + 5 ítems por clase con la lista del §4.
- Si encuentras un fallo que se repite, anótalo en el informe como «patrón» y evítalo desde ese momento.

### Paso 6. Piezas de apoyo
Cada pieza copia la **estructura** del alemán, que está publicado y completo, y escribe contenido italiano propio.

| Pieza | Modelo alemán | Salida italiana | Validador (0 errores) |
|---|---|---|---|
| Prueba de ubicación v2 | `assets/contenido/de/plan-editorial/diagnostico/n1.json` … `n10.json` | `assets/contenido/it/plan-editorial/diagnostico/n1.json` … `n10.json` | `validar_diagnostico.py --idioma it`, y al final `--idioma it --compilar` (escribe `assets/contenido/it/diagnostico-v2.json`) |
| «Mis verbos» | `assets/contenido/de/verbos.json` | `assets/contenido/it/verbos.json` | (estructura igual al alemán) |
| 50 situaciones × 3 tramos | `assets/contenido/de/situaciones.json` y `backend/src/content/situaciones-de.json` | `assets/contenido/it/situaciones.json` y `backend/src/content/situaciones-it.json` | `validar_situaciones.py assets/contenido/it/situaciones.json` |

- La prueba de ubicación va **sin Lumo**.
- «Mis verbos» lleva los verbos de uso frecuente con su conjugación completa: essere, avere, andare, fare, stare, venire, potere, volere, dovere, sapere, dire, dare, uscire, rimanere y los regulares -are/-ere/-ire.

### Paso 7. Integración (sin commit)
1. Ejecuta `python3 tools/contenido/ruta-it/integrar.py`. Pasa f0 y los N1–N10 a `assets/contenido/it/ruta/`; la N1 c01 cuelga de la última unidad de f0.
2. Añade `'it'` a `idiomasConRuta` en `lib/core/aprendizaje/providers.dart`.
3. Pasan `python3 tools/validar_ruta.py` y `flutter test`.
4. Entrega el informe final. El commit y el despliegue los hace el dueño.

---

## 4. LAS REGLAS QUE MÁS SE ROMPEN (repásalas en cada respuesta)

Cada encargo trae sus reglas completas. Estas son las que más fallaron en portugués, alemán y en el piloto italiano:

1. **Nada sin enseñar.**
   - Cada palabra italiana de un ejercicio, un audio o un diálogo ya apareció tal cual en ejemplos, vocabulario o tablas de esta clase o de una anterior.
   - Las formas flexionadas cuentan como palabras nuevas: «andata», «nella», «gli».
2. **Una sola respuesta.**
   - Si caben dos respuestas, la segunda va en `aceptadas` o la consigna precisa la persona, el tiempo o el comienzo.
   - Ningún distractor es correcto.
3. **La consigna da los datos de la respuesta:** nombres, números, lugares y persona gramatical.

   | Consigna | Italiano |
   |---|---|
   | «tú» | tu |
   | «usted» | Lei |
   | «ustedes» | voi |
   | «nosotros» | noi |

4. **`ordenar`:**
   - Los tokens son exactamente las palabras de la respuesta, sin puntuación y sin palabras de relleno.
   - Al menos 3 tokens.
5. **Diálogos:**
   - Nunca dos líneas seguidas del mismo hablante.
   - Hablantes con nombre (nunca «A» y «B»).
   - El cierre va al final.
   - Todo lo que dice el `contexto` ocurre en el diálogo.
   - El `contexto` va en español y en inglés, nunca en italiano.
6. **Español latino neutro con tú.** Nunca: vosotros, vale, móvil, coche, ordenador, zumo, patata, coger, aparcar, gafete.
7. **El inglés es americano natural** y el texto `es` no lleva palabras inglesas.
8. **Nombres y lugares, solo de la ficha del idioma:**
   - Nombres: Marco, Giulia, Luca, Chiara, Sofia, Matteo, Francesca, Alessandro, Elena, Paolo, Anna, Giorgio, Sara, Davide, Martina.
   - Apellidos: Rossi, Bianchi, Ferrari, Esposito, Moretti, Marchetti, Lombardi, Mancini, Rinaldi, Ferraro.
   - Ciudades: Roma, Milano, Napoli, Torino, Firenze, Bologna, Venezia, Genova, Palermo, Verona.
   - **Nunca Ecuador ni sus ciudades.**
9. **Lumo, la mascota de la app,** nunca aparece en clases ni pruebas, salvo la bienvenida del Nivel 0.
10. **Nada inventado:** ni reglas, ni datos reales, ni falsos amigos que no lo son.
11. **En audios y respuestas no van cifras ni símbolos:** los números se escriben en palabras.
12. **Límites por clase:**
    - como máximo 12 palabras de vocabulario y 8 ejemplos;
    - al menos un `escuchar`;
    - todas las pistas, solo en la práctica guiada.

---

## 5. CUÁNDO TE DETIENES

Solo en estos casos:
- Un comando falla con un error de Python (no un PENDIENTE): copia el error en el informe y para.
- Un bloque entero no llega a 0 errores de validador.
- Te falta un archivo de los del §1.

En cualquier otro caso, sigues.

---

## 6. INFORME (al cerrar cada nivel y al final)

Escríbelo en `tools/contenido/ruta-it/INFORME.md`, añadiendo una sección por nivel:
- bloques y clases terminados, con su veredicto GO o REVISE;
- clases que quedaron con errores y por qué;
- patrones de fallo que encontraste y cómo los evitaste;
- pasos 1–3 y 6–7: qué se hizo y el resultado de cada validador.
