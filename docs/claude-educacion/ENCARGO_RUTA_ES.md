# Encargo: ruta de español N1–N10 para anglohablantes, 50 clases por nivel en 10 bloques

Equivale a `ENCARGO_RUTA_FR.md` para el español. Vale para todos los niveles con la tabla «Por nivel».

Lee antes:
- tu **paquete de contexto** (`tools/curriculo/paquete.py es N B`). Contiene tus 5 fichas de `curriculo/es/nX.json`, el reparto y los hechos, la nota del nivel y una clase modelo. Escribe exactamente lo que dicen las fichas: la gramática nueva es solo la de su `introduce`; lo ya visto va como repaso. Los ejercicios siguen su plan (`ejercicios`): mismo formato, misma clave, misma cosa evaluada. Puedes pulir la redacción y completar `aceptadas`, pistas y feedback;
- `curriculo/es/MAPA.md`: reglas del idioma, reparto canónico y cronología;
- `ESQUEMA_CONTENIDO.md` (esquema 2).

## Por nivel

| Nivel | cefr | nivelInterno | Duración | Sonido del día | Lectura en la situación |
|---|---|---|---|---|---|
| N1 | A1 | 1 | 10–12 min | sí (`sonido` de la ficha) | diálogo de 3–6 líneas |
| N2 | A2 | 2 | 12–15 min | no; nota de pronunciación si hace falta | 6–10 líneas (≈ 80–120 palabras) |
| N3–N4 | B1 | 3–4 | 15 min | no | 150–250 palabras |
| N5–N7 | B2 | 5–7 | 15–20 min | no | 300–500 palabras |
| N8–N10 | C1 | 8–10 | 20 min | no | 400–700 palabras |

## Archivo por bloque

`tools/contenido/ruta-es/nX-bYY.json` con `{"modulo": "es.nX-bYY", "unidades": [5 unidades]}`. La revisión va en `revision-nX-bYY.md`.

- **Ids:** `es.nX.c01` … `es.nX.c50`. **Orden:** 100·X + n. **Prerrequisitos:** N1 c01 → `es.f0.presentarse`; c01 de los demás niveles → la c50 del nivel anterior; cada clase → la anterior.
- **Textos de apoyo:** solo `{"en": …}`, en inglés americano. Compara con el inglés cuando ayude: ser/estar, género, «me gusta» frente a «I like», falsos amigos.
- **Guías de pronunciación en inglés:** las vocales son siempre cortas y puras (no «o-u»); j y ge/gi son «a strong h»; la d entre vocales suena como la «th» de «this»; la r simple, como la «tt» de «butter» en inglés americano; la rr es vibrante; h muda; ll/y como la «y» de «yes»; z y ce/ci como «s» (seseo).

## Cada clase

En orden: `explicacion` (en N1 abre con el sonido del día), `ejemplos` (5–8 con audio), `vocabulario` (6–12 palabras de la ficha, con artículo), `patron` o `tabla` (conjugaciones completas, ustedes incluido y sin vosotros), `practica_guiada` (3–5 con `pista`), `practica_independiente` (3–4), `situacion` (contexto, diálogo o texto, 1–2 preguntas), `evaluacion` (≥ 4 ítems puntuables y ≥ 2 formatos; los `escribir` abiertos no cuentan). Además: `erroresFrecuentes` ≥ 1, típicos de anglohablantes («Soy 25 años», «Estoy profesora», «Me gusto el café»). Recicla ≥ 30 % del vocabulario anterior y usa los seis formatos a lo largo del bloque.

## Reglas (las comprueba `validar_ruta.py es`; con `reglasAutoria` también las de calibración 4–5, la extensión de la lectura y los apellidos del reparto)

- **Nada sin enseñar.** Cada palabra española de respuestas, opciones, audios, diálogos y ordenar aparece antes en un paso de enseñanza (`ejemplos`, `vocabulario`, `patron`, `tabla`) de esta clase o de una anterior, incluidos Fundamentos (`es.f0.*`).
- **Ortografía:** ¿…? y ¡…!, tildes también en mayúsculas.
- **Hablantes:** el nombre del personaje del reparto o su papel en español («Mesera», «Recepcionista», «Taxista»).
- **Respuestas alternativas** en `aceptadas`: con y sin pronombre sujeto (no hace falta la variante sin tilde: la app ya la tolera y avisa), femenino y masculino cuando aplique, órdenes naturales en `ordenar`.

## Calibración heredada del francés

1. **Variedad:** carro, celular, computadora, departamento, jugo, boleto, mesero, manejar, estacionar, el vuelto, ustedes. Nunca vosotros, coche, ordenador, móvil, zumo, piso (vivienda) ni vale, salvo en las clases de nota de España, y allí solo para reconocer.
2. **La historia no se contradice.** Lee el reparto y los hechos; en el informe lista los hechos nuevos (`- es / en`) para que el revisor los confirme en «Hechos del reparto confirmados».
3. **Una sola respuesta** por ítem; si dos formas valen, la consigna fija cuál o `aceptadas` incluye todas.
4. **Opciones de comprensión** en español desde N3 (en N1–N2 pueden ir en inglés). No se pasan opciones al inglés para esquivar palabras no enseñadas: se enseña la palabra o se reformula.
5. **Tablas de lectura** (título «To read: …»): como máximo 15 filas, palabra + sentido + frase; los nombres propios no llevan fila. Si hacen falta más, la situación se reescribe con palabras ya enseñadas.
6. **Producción abierta:** en un `escribir` con `abierta: true`, el modelo tiene al menos `minimoPalabras` palabras.

## Validación

```bash
python3 tools/curriculo/validar_bloque.py es N B
```

0 errores del bloque. El revisor deja `revision-nX-bYY.md` con GO o REVISE, con «## Hechos del reparto confirmados» y «## Sin resolver».
