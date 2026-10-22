# Encargo: variación ligera de frases para las clases de refuerzo

Entrada: `tools/contenido/refuerzo/<idioma>/nX-bYY.paquete.json`.
Salida: `tools/contenido/refuerzo/<idioma>/nX-bYY.variantes.json`, escrita con **una sola** llamada a Write.

```json
{
  "fr.n1.r01.g2": {"variante": "Bonsoir, madame !", "es": "¡Buenas noches, señora!", "en": "Good evening, ma'am!"}
}
```

## Reglas

1. **Cambia un solo elemento** de cada frase: el nombre, la persona, el lugar, la hora, el objeto, la nacionalidad o el adjetivo. Ajusta solo la concordancia que ese cambio exija, por ejemplo `il est français` → `elle est française`. Como máximo cambian 3 palabras.
2. **Conserva el punto de gramática.** Si la frase trae `conservar`, esa palabra debe aparecer **exactamente una vez** en la variante, escrita igual. Es la palabra del hueco.
3. **Solo palabras ya enseñadas.** En el paquete de un nivel, `palabrasPorBloque` trae las palabras que se suman en cada bloque. Una frase del bloque `bYY` puede usar las palabras de `b01` hasta `bYY`, nunca las de bloques posteriores. Los nombres propios del curso también valen. No uses ninguna palabra nueva, aunque sea sencilla.
4. **Mantén la puntuación y la tipografía del original**: espacio fino antes de `! ? ;` en francés, apóstrofo `’`.
5. **Sin Ecuador.** No introduzcas Ecuador, Quito, Cuenca ni nada ecuatoriano: la app es para EE. UU. y Latinoamérica. Si el original los trae, cámbialos por un lugar del país del idioma.
6. **Que tenga sentido en una situación real.** No mezcles un saludo de llegada con una despedida y no pongas plurales raros. No cambies una frase de modo que se contradiga (un plazo «más corto» a costa de «esperar»).
6b. **No toques hechos reales.** Si la frase habla de personas, monumentos, fechas históricas, instituciones o costumbres reales (quién inventó algo, qué organismo emite un documento, en qué año pasó algo), omite la clave: un cambio volvería falso el dato. Tampoco cambies refranes ni juegos de palabras que dependen de la forma exacta.
6c. **Concordancia completa del idioma.** En alemán, el caso y el género del artículo y del adjetivo (`den Bahnhof` → `die Post`) y mayúscula en todos los sustantivos; en portugués e italiano, el género del artículo y de la contracción (`no` / `na`, `del` / `della`).
7. **Traducciones `es` y `en` naturales** de la variante, no de la original.
8. **Si no hay un cambio seguro con esas palabras, omite la clave.** Es mejor omitirla que forzarla, porque el script deja la frase original.
9. **No hagas nada más.** No leas otros archivos, no ejecutes comandos ni git, y no expliques: escribe el JSON y termina.

Un script valida cada variante: palabras enseñadas, de 1 a 3 palabras cambiadas, la palabra del hueco y las traducciones. Si una variante falla, se descarta sin pedir corrección.
