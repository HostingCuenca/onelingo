# Contrato de enriquecimiento de clases (Inglés N1–N3)

Actualizado: 2026-09-30 · Motivo: auditoría del 2026-09-30 (`auditoria/AUDITORIA_2026-09-30.md`).

Las 290 clases publicadas practican y evalúan, pero no **explican** la gramática, su paso «situación» es un relleno automático y sus «errores frecuentes» son falsos. Este contrato añade una capa editorial por clase, sin tocar los ejercicios aprobados ni sus hashes.

## Archivo

`assets/contenido/en/editorial/<nivel>/enriquecimiento-<ini>-<fin>.json` (bloques de 5 clases, p. ej. `enriquecimiento-16-20.json`):

```json
{
  "schema": "onelingo.editorial.enrichment.v1",
  "level": "n1",
  "range": {"start": 16, "end": 20},
  "classes": {
    "en.n1.class-20": {
      "explicacion": {
        "titulo": "Tener: have got y has got",
        "texto": "Regla en español, 2–5 frases: forma, significado, cuándo se usa y en qué se diferencia del español."
      },
      "patron": {
        "texto": "Sujeto + have/has got + cosa:",
        "formula": [
          {"texto": "My mother", "nota": "sujeto: una persona (he/she)"},
          {"texto": "has got", "nota": "he/she/it → has got"},
          {"texto": "brown eyes.", "nota": "lo que tiene"}
        ]
      },
      "tabla": {
        "columnas": ["Sujeto", "Forma"],
        "filas": [[{"texto": "I / you / we / they"}, {"texto": "have got"}], [{"texto": "he / she / it"}, {"texto": "has got"}]]
      },
      "erroresFrecuentes": [
        {"incorrecto": "My mother have got brown eyes.", "correcto": "My mother has got brown eyes.", "explicacion": "Con he/she/it (my mother) se usa has."},
        {"incorrecto": "I have got 20 years.", "correcto": "I am 20 years old.", "explicacion": "La edad se dice con be, no con have."}
      ],
      "situacion": {
        "contexto": "Ana le enseña a Tom una foto de su familia.",
        "dialogo": [
          {"hablante": "Tom", "texto": "Is this your mother?", "traduccion": "¿Es tu madre?"},
          {"hablante": "Ana", "texto": "Yes. She has got brown eyes.", "traduccion": "Sí. Tiene ojos marrones."},
          {"hablante": "Tom", "texto": "And your father?", "traduccion": "¿Y tu padre?"},
          {"hablante": "Ana", "texto": "He has got short hair.", "traduccion": "Tiene el pelo corto."}
        ],
        "item": {
          "formato": "elegir",
          "consigna": "Según el diálogo, ¿qué tiene el padre de Ana?",
          "opciones": ["He has got short hair.", "He has got brown eyes.", "He has got long hair."],
          "respuesta": 0,
          "feedback": "Ana dice: «He has got short hair»."
        }
      },
      "ejemplos": [
        {"indice": 2, "en": "Frase inglesa real", "es": "Traducción fiel", "nota": "Nota breve en español"}
      ]
    }
  }
}
```

- `tabla` y `ejemplos` son opcionales. `ejemplos` sustituye, por posición (0 = primero), ejemplos de enseñanza defectuosos: instrucciones o metalenguaje en inglés («Use present passive for…»), traducciones que resumen en lugar de traducir o notas en inglés.
- Opciones del ítem: en inglés como texto (`"He has got a book."`) o en español como objeto (`{"es": "Del padre de Ana."}`); las españolas comprueban comprensión sin exigir producir inglés.
- Palabras: las inglesas deben estar enseñadas antes (se aceptan flexiones regulares: plural, 's, -ed, -ing, -er/-est). Los nombres propios nuevos se añaden a `palabrasLibres` de `curso.json`. `python3 tools/validar_ruta.py` debe quedar en 0 errores.
- `item.formato`: `elegir` o `escuchar` (con `"audio"`: línea del diálogo o variante breve), siempre con 3 opciones y `respuesta` como índice. No copiar ejercicios existentes de la clase.

## Reglas de calidad

1. **Explicar antes de practicar.** `explicacion.texto` en español claro para un hispanohablante de 12 años en adelante: forma, significado y uso; contraste con el español cuando haya trampa (sujeto obligatorio, orden del adjetivo, `have` para la edad, `does` en preguntas…). Sin jerga innecesaria. Si la clase es de cierre, integración o comprensión, explicar la estrategia y recordar las formas que se integran.
2. **Patrón visible.** 2–5 segmentos en inglés, con nota en español en cada uno. Debe coincidir con la estructura que practican los ejercicios de la clase.
3. **Errores reales.** Exactamente 2 errores típicos de hispanohablantes con esa estructura; nunca «frase + ?». El incorrecto debe ser un error plausible, y el correcto, una frase natural.
4. **Situación real.** Contexto de una frase; diálogo de 3–6 líneas entre personajes con nombre (Ana, Leo, Mia, Tom, Carlos, Sara o personajes del mismo estilo), apto para niños y adultos y cotidiano, sin trámites de oficina. Solo vocabulario y gramática ya enseñados hasta esa clase (mismo nivel o anteriores), más la estructura de la clase. El ítem se responde **leyendo el diálogo**, no por sentido común.
5. **Inglés natural y correcto**, con traducciones fieles (no resúmenes). Nada de calcos.
6. **No tocar** ejercicios, respuestas, ids ni archivos de clase. Solo el archivo de enriquecimiento.
7. **Independencia.** Quien redacta no aprueba. Un revisor distinto emite `GO` o `REVISE` con hallazgos concretos.

## Revisión

El revisor independiente añade al archivo `"review": {"status": "GO", "reviewer": "…", "date": "AAAA-MM-DD", "notes": […]}` solo cuando no quedan hallazgos P0/P1. El compilador ignora los archivos sin `GO`.

## Integración

`tools/contenido/generar_runtime_n1.py` fusiona los archivos de enriquecimiento. La explicación y el patrón (y la tabla) se colocan antes del vocabulario; los errores sustituyen al relleno, y la situación sustituye a la copia del ejercicio de práctica. Las clases sin enriquecimiento conservan el formato anterior hasta completarse.
