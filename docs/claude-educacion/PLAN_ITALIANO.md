# Plan del curso de italiano (it) N1–N10: producción masiva con OpenAI

Estado: **en preparación** (06-10-2026).
- Kit de producción listo en `tools/ia/`.
- Mapa de claves de N1 generado (pendiente de revisión).
- Piloto de clases pendiente.

## 1. Por qué cambiamos el método

Con alemán y portugués, el contenido lo escribieron agentes de Claude: un autor y un revisor por bloque, más revisiones de fichas por nivel. Funcionó, pero tiene dos problemas:

- **Coste:** el 02-10 los agentes gastaron 2.300 M de tokens en un día. Cada agente relee el encargo, el paquete y los validadores, y depura a mano.
- **Correcciones tardías:** el portugués acumuló muchos cambios de revisión por el canon narrativo (reparto, cronología, datos reales de Recife). El alemán quitó la historia y bajó mucho los errores. Aun así se repitieron los mismos fallos en todos los niveles:
  - `contexto.es` escrito en alemán;
  - `escribir` de transformación sin la frase de partida;
  - turnos seguidos del mismo hablante;
  - varias respuestas válidas;
  - pasos sin `id`;
  - español de España;
  - ⚠ en palabras que no son falsos amigos.

**Idea central:** lo mecánico lo hace el código y lo lingüístico, el modelo. Los fallos que ya conocemos los detecta un validador antes de que nadie revise, y el modelo los corrige en bucle. Claude interviene solo donde aporta criterio: el diseño, la revisión del mapa de claves y una muestra de clases.

## 2. Reparto de trabajo

| Quién | Hace | Coste |
|---|---|---|
| **Código** (`tools/ia/openai_contenido.py`) | ids, orden, bloques, `introduce`, `recicla` con repaso a +1/+2/+7, prerrequisitos, enlaces de vocabulario, montaje del JSON de la app, validación y bucle de reparación | 0 |
| **Validadores** (`validar_*.py`, `tools/ia/chequeos.py`) | estructura, «nada sin enseñar», una sola respuesta mecánica (ordenar, opciones), idioma de cada campo, español de España, Ecuador, Lumo, diálogos | 0 |
| **Modelo planificador** (`gpt-6-sol`) | mapa de claves por nivel y esqueletos (outline) | ≈ $0,15 por nivel y etapa |
| **Modelo autor** (`gpt-5.4-mini`; se decide en el piloto frente a `gpt-6-luna`) | fichas de ejercicios y clases completas, una llamada por clase | ver §5 |
| **Modelo revisor** (`gpt-6-sol`, esfuerzo alto) | revisa y corrige cada clase con la lista de criterios; deja `revision-nX-bYY.md` | ver §5 |
| **Claude** | diseño y prompts (hecho), revisión del mapa de claves de cada nivel, calibración del piloto y muestreo de 1 bloque por nivel | pocas decenas de agentes en todo el idioma |

## 3. Fases y puertas de calidad

Una fase no empieza hasta que la anterior pasa su puerta.

| Fase | Comando | Puerta |
|---|---|---|
| 0. Herramientas `it` | (Claude) `conocida_it` en `validar_ruta.py` e `integridad.dart`, `POR_IDIOMA['it']`, `ruta-it/integrar.py`, `curso.json` | validadores en verde con un bloque de prueba |
| 0b. Nivel 0 + Fundamentos `it` | (Claude o modelo autor con el patrón de `curriculo/de/f0.json`) | `validar_fundamentos.py it` 0 errores + revisión |
| 1. Mapa de claves | `openai_contenido.py mapa it N` | **Claude revisa los 10 mapas** (≈ 480 líneas): progresión MCER, huecos (p. ej. el mapa N1 generado omitía el presente en ‑ere/‑ire, «fare» y «stare») y nada repetido |
| 2. Esqueleto | `openai_contenido.py outline it N` | `validar_outline_nivel.py it N` 0 errores |
| 3. Fichas | `openai_contenido.py fichas it N` | `validar_plan_detallado.py it` 0 errores |
| 4. Clases | `openai_contenido.py clases it N B` | `validar_bloque.py it N B` + `chequeos.py` 0 errores (≤ 2 rondas de reparación) |
| 5. Revisión | `openai_contenido.py revisar it N B` | GO del revisor y validadores en 0 |
| 6. Calibración | (Claude) revisión completa de N1 B1 y N6 B1 | ≤ 3 fallos de gravedad media por clase; si no, se ajustan los prompts y se repite el piloto |
| 7. Muestreo | (Claude) 1 bloque al azar por nivel | igual que la calibración; un fallo nuevo se convierte en regla del prompt o en chequeo |
| 8. Resto | diagnóstico v2, verbos, 50 situaciones × 3 tramos, voces it-IT (calibración como en alemán) | sus validadores |
| 9. Publicación | `integrar.py`, `flutter test`, **un solo commit** por ruta explícita | despliegue solo con autorización |

**Regla de mejora continua:** si un fallo aparece dos veces en revisión, se convierte en una regla de `tools/ia/idiomas/it.md` o de los prompts, o en un chequeo de `chequeos.py`. Así no se vuelve a corregir a mano.

## 4. Los prompts

Todos están en `tools/ia/prompts/` y llevan dentro la ficha del idioma (`tools/ia/idiomas/it.md`):

- `mapa_claves.md`: progresión gramatical del nivel, adaptada (no traducida) desde el francés publicado.
- `outline_nivel.md`: esqueleto de 5 clases por bloque.
- `fichas.md`: plan de ejercicios de cada clase, que funciona como contrato para el autor.
- `clase_autor.md`: la clase completa.
  - Lleva 15 reglas duras, cada una nacida de un fallo real de pt/de, y un repaso final obligatorio.
- `clase_revisor.md`: revisión con corrección directa y salida GO/REVISE.

La salida es **JSON estricto** (Structured Outputs). El modelo no puede devolver campos de más ni de menos, y los ids no los escribe él. Con eso desaparece por diseño el error que en alemán dejaba módulos sin cargar.

Para otro idioma basta con escribir `tools/ia/idiomas/<idioma>.md` y añadirlo a `NOMBRES`.

## 5. Coste estimado del italiano completo

Una clase ocupa ≈ 7 000 tokens de salida, más razonamiento. La entrada lleva la ficha, el contexto y la lista de lo ya enseñado (≈ 8–25 000 tokens), en buena parte en caché.

| Etapa | Llamadas | Modelo | Estimado |
|---|---|---|---|
| Mapas + esqueletos | 10 + 100 | gpt-6-sol | ≈ $15 |
| Fichas | 100 | gpt-5.4-mini | ≈ $5 |
| Clases + reparaciones | 500 + ≈ 300 | gpt-5.4-mini | ≈ $40–60 |
| Revisión | 500 | gpt-6-sol | ≈ $80–120 |
| **Total** | | | **≈ $140–200** (la mitad con la API Batch) |

Coste real del mapa N1: $0,13. El registro está en `tools/ia/registro/costos.jsonl` y se consulta con `python3 tools/ia/openai_contenido.py costos`.

## 6. Reglas que no cambian

- Variedad, alumno y tratamiento: los de `tools/ia/idiomas/it.md`.
- Método ligero, como el alemán: 10 niveles × 50 clases, sin historia ni reparto. Cada clase es una situación autónoma.
- Nunca Ecuador.
- Lumo nunca con otro personaje y nunca en pruebas de nivel.
- Español latino neutro con tú.
- No se generan imágenes.
- Un solo commit cuando el idioma esté completo y probado.
- Nada de push ni despliegue sin autorización.

## 7. Lecciones del piloto (06-10), ya aplicadas al kit

1. **El razonamiento del autor se queda en «low».**
   - Con «medium», el 90 % de la salida del modelo autor era razonamiento interno: ≈ $0,19 por llamada de fichas.
   - Con «low» baja a ≈ $0,02 y la calidad es la misma. Los errores los ataja el bucle de validación.
   - Esfuerzo por etapa: mapa «high», outline y revisor «medium», autor «low». Se cambia con `--esfuerzo`.
2. **Lo mecánico, al código, también dentro de los ejercicios.** El modelo barato fallaba en tareas mecánicas, no en las lingüísticas:
   - el estímulo desordenado de `relacionar`;
   - los tokens de `ordenar`.

   Ahora el modelo da la solución y el código construye el estímulo.
3. **Los mensajes del validador se traducen a instrucciones** (`EXPLICA`) y los repetidos se localizan por ítem. Si solo recibe «2 ejemplos repetidos» sin decir dónde, el modelo repite el error.
4. **La reparación no rehace lo que está bien.**
   - Solo se sustituyen las clases con error.
   - Si el bloque ya existe, se entra directamente en modo reparación (`--rehacer` fuerza regenerar).
5. **Las ambigüedades del prompt se pagan.** «→ opción correcta» hizo que el modelo escribiera la letra en vez del texto: 31 errores. Con un ejemplo «bien / mal», los errores bajaron a 2.
6. **La revisión de Claude de los mapas es imprescindible.**
   - Los mapas generados nivel a nivel no veían el contexto completo.
   - La revisión hizo 50 cambios: ≈ 190 dependencias rotas tras regenerar N1, duplicados entre niveles y huecos (fechas, sapere/conoscere, pronombres tónicos, farcela/andarsene, ce l'ho…).
   - El veredicto quedó en `tools/curriculo/it/revision-mapas.md`, con GO.
   - Sin esta puerta, esos fallos se habrían multiplicado en 500 clases.

7. **Calibración de Claude sobre N1 B1** (revisión a ciegas, antes de leer la revisión automática):

   | Ronda | ALTA | MEDIA | BAJA | Total | Coste OpenAI del bloque |
   |---|---|---|---|---|---|
   | v1 | 3 | 25 | 23 | 51 | ≈ $0,75 |
   | v2 (prompts + chequeos nuevos) | 3 | 14 | 22 | 39 | ≈ $0,90 |

   - El italiano es correcto. Los fallos que quedan son de lógica de los ítems:
     - respuesta que no sale de la consigna;
     - «ustedes» resuelto con noi;
     - `aceptadas` incompletas;
     - un `contexto` que no ocurre en el diálogo.
   - Cada patrón encontrado ya es regla del prompt o chequeo. Desaparecieron:
     - ustedes = noi;
     - falta de `escuchar`;
     - desbordes de vocabulario y ejemplos;
     - errores frecuentes inventados;
     - «gafete» y la guía de sonido en inglés en el texto `es`.
   - Las 3 ALTA de v2 (tokens rellenados para llegar a 3 y una respuesta atribuida al hablante equivocado) ya las detecta `chequeos.py`.
   - **Puerta para producir en masa:** una calibración con 0 ALTA y ≤ 5 MEDIA por bloque, en N1 B1 y en N6 B1 (B2, textos largos). Hasta entonces, cada bloque generado pasa además por una revisión de Claude que corrige. Aun así, sale mucho más barato que autor + revisor de Claude.

## 8. Hallazgos al calibrar `chequeos.py` con lo ya publicado (06-10)

`chequeos.py` se probó contra todos los bloques de-fr-pt-es para afinar los falsos positivos. Además encontró:

- **Alemán:** 13 «coche» y algún «ordenador», «móviles» y «sois» en el español de apoyo (sin desplegar todavía).
- **Francés y español publicados:** ≈ 990 y ≈ 1 800 menciones de Ecuador/Quito en `assets/contenido/{fr,es}/ruta`. Son anteriores a la regla «sin Ecuador»; queda pendiente decidir su limpieza.
