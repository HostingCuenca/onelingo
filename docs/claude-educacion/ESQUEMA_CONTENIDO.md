# Esquema de contenido de rutas (v2)

Contrato único para los 10 cursos. La lógica vive en `lib/core/aprendizaje/`; cada idioma aporta solo datos. Validación: `python3 tools/validar_ruta.py <idioma>` y `test/ruta_*_test.dart`.

## Archivos

```
assets/contenido/<idioma>/ruta/curso.json   índice del curso: metadatos, niveles, módulos
assets/contenido/<idioma>/ruta/<modulo>.json unidades completas de un módulo (hoy: f0.json)
```

Jerarquía: idioma → nivel → módulo → unidad → pasos → ítems. Una unidad es una lección corta y completa (enseña → practica → aplica → evalúa).

## Textos de apoyo (DEC-004)

Todo texto dirigido al alumno (consignas, explicaciones, traducciones, feedback, pistas, títulos) es un **TextoApoyo**: `{"es": "…", "en": "…"}`. Debe contener **todos** los idiomas de `curso.idiomasApoyo`. Se resuelve con la cadena: nativo del alumno → `apoyoPredeterminado` → `es` → primero disponible.
Los textos en el **idioma meta** son cadenas simples; si la escritura no es latina se añade `rom` (romanización) aparte.

## curso.json

```json
{
  "esquema": 2,
  "idioma": "de",
  "version": "2026.09.0",
  "revision": "inicial",
  "idiomasApoyo": ["es"],
  "apoyoPredeterminado": "es",
  "palabrasLibres": ["Ana", "Leo", "Mia"],
  "niveles": [
    {"id": "f0", "cefr": "Pre-A1", "nivelInterno": 0, "estado": "publicado", "titulo": {"es": "Fundamentos"}},
    {"id": "c2", "cefr": "C2", "nivelInterno": null, "estado": "planificado", "titulo": {"es": "C2 · Maestría"}}
  ],
  "modulos": [
    {"id": "de.f0", "nivel": "f0", "archivo": "f0.json", "titulo": {"es": "Fundamentos"}}
  ]
}
```

- `revision`: `"inicial"` muestra la etiqueta «Versión inicial» (contenido sin revisión nativa). Inglés: `"revisada"`.
- `palabrasLibres`: nombres propios y otros tokens del idioma meta permitidos sin enseñanza previa.
- `nivelInterno: null` + `estado: "planificado"` = nivel reservado (C2, DEC-002). No se muestra al alumno.

Un nivel puede tener varios módulos (p. ej. `a1-2` = `en.a1-2.presente` + `en.a1-2.comunicar`); la pantalla de ruta los muestra como secciones. Los prerrequisitos pueden cruzar módulos y niveles; `orden` es global en el curso. Si un módulo no carga, el curso sigue funcionando sin él (`CargadorRuta.modulosConError`) y las pruebas fallan.

## <modulo>.json

```json
{"modulo": "de.f0", "unidades": [ UNIDAD, ... ]}
```

## Unidad

| Campo | Tipo | Obligatorio | Uso |
|---|---|---|---|
| `id` | string `<idioma>.<nivel>.<slug>` | sí | estable; nunca se reutiliza |
| `orden` | int | sí | orden de presentación (coherente con prerrequisitos) |
| `titulo`, `objetivo` | TextoApoyo | sí | objetivo comunicativo medible |
| `cefr`, `nivelInterno` | string, int | sí | equivalencia orientativa |
| `concepto` | string | sí | id neutral para alinear cursos y tutor (`saludos`, `pronombres`, `copula`, …) |
| `prerequisitos` | [id] | sí | ids de unidades del mismo curso |
| `habilidades` | [string] | sí | `vocabulario`, `gramatica`, `lectura`, `escucha`, `escritura`, `conversacion`, `pronunciacion` |
| `gramatica` | [string] | no | nodos del grafo (`en-g-be-affirm`), informativo |
| `vocabulario` | [Vocablo] | sí | todo lo que la unidad enseña |
| `erroresFrecuentes` | [ErrorFrecuente] | sí (≥1) | errores típicos del hispanohablante |
| `pasos` | [Paso] | sí | secuencia didáctica |
| `criterioDominio` | `{"umbral": 0.8}` | sí | aciertos a la primera en la evaluación |
| `repaso` | `{"intervalosDias": [1,3,7,16,35,90]}` | no | valores por defecto si falta |
| `tutor` | objeto | no | metadatos opcionales para práctica conversacional; nunca requisito de la ruta base (DEC-017) |
| `guias` | [string] | no | ids de guías de `grammar_guides.dart` relacionadas (enlace con el contenido antiguo) |

**Vocablo**: `{"id": "v-hello", "texto": "hello", "rom": "…"?, "traduccion": TextoApoyo, "nota": TextoApoyo?}`
**ErrorFrecuente**: `{"incorrecto": "I is Ana.", "correcto": "I am Ana.", "explicacion": TextoApoyo}`

## Pasos (`tipo`)

Orden obligatorio: primero **enseñar** (`explicacion`, `ejemplos`, `vocabulario`, `patron`, `tabla`), luego `practica_guiada`, luego `practica_independiente`, luego `situacion`, y al final `evaluacion`.

| Tipo | Campos | Qué ve el alumno |
|---|---|---|
| `explicacion` | `titulo`?, `texto` (TextoApoyo), `icono`? | concepto en su idioma |
| `ejemplos` | `items: [{texto, rom?, traduccion, nota?}]` | frases modelo con audio |
| `vocabulario` | `refs: [idVocablo]` | tarjetas con audio y traducción |
| `patron` | `formula: [{texto, nota?}]`, `ejemplos: [...]`, `texto`? | cómo se construye la frase |
| `tabla` | `titulo`?, `texto`? (TextoApoyo), `columnas`? ([TextoApoyo]), `filas: [[celda]]`; celda = `{texto (meta), rom?}` o `{apoyo: TextoApoyo}` | cuadros de escritura (kana, hangul, cirílico, pinyin) y conjugaciones; cada celda meta se puede escuchar. Las celdas meta cuentan como enseñadas |
| `practica_guiada` | `items: [Item]` (con `pista`) | ejercicios con ayuda; no cuentan para dominio |
| `practica_independiente` | `items: [Item]` (sin `pista`) | menos ayuda |
| `situacion` | `contexto` (TextoApoyo), `dialogo: [{hablante, texto, rom?, traduccion}]`, `items: [Item]` | aplicación comunicativa con diálogo modelo |
| `evaluacion` | `items: [Item]` (≥ 4, ≥ 2 formatos) | comprobación sin ayuda; decide «aprobada» |

## Ítems (`formato`)

Campos comunes: `id` (único en la unidad), `formato`, `consigna` (TextoApoyo), `feedback` (TextoApoyo, se muestra acierte o falle), `pista` (TextoApoyo, solo práctica guiada).

| Formato | Campos | Corrección |
|---|---|---|
| `elegir` | `pregunta`? (meta) o `preguntaApoyo`? (TextoApoyo), `opciones` ([string meta] o [TextoApoyo]), `respuesta` (índice) | índice |
| `escuchar` | `audio` (texto meta que se reproduce), `opciones`, `respuesta` | índice |
| `ordenar` | `tokens` [string], `respuesta` (frase) | comparación normalizada |
| `completar` | simple: `texto` con un `___`, `respuesta`, `aceptadas`?, `opciones`?; multiparte editorial: `textosPartes`, `respuestasPartes`, `partesPuntuables`, `minimoCorrectas` | simple normalizada; multiparte corrige cada campo y aplica el umbral declarado |
| `escribir` | `respuesta`, `aceptadas`?, `audio`? (dictado); editorial extensa: `minimoPalabras`, `maximoPalabras`, `evidenciasEscritura` adaptados desde `origin.scoring.wordRange/evidenceGroups` | normalizada; con rúbrica, rango + una frase válida de cada grupo |
| `relacionar` | `pares: [[texto meta, TextoApoyo]]` (3–5) | todos los pares |

Normalización para corregir: minúsculas, apóstrofos tipográficos → `'`, se elimina la puntuación `.,!?¡¿;:。、！？「」…"“”«»` en cualquier posición y se colapsan los espacios. Formas alternativas válidas (contracciones, variantes) van en `aceptadas`.

## Reglas pedagógicas que el validador comprueba

1. IDs únicos; prerrequisitos existentes; grafo sin ciclos; `orden` coherente con prerrequisitos.
2. Cada TextoApoyo tiene todos los `idiomasApoyo`, sin cadenas vacías.
3. La unidad empieza enseñando y respeta el orden de pasos; hay `practica_guiada`, `situacion` y `evaluacion` (≥ 4 ítems, ≥ 2 formatos); la evaluación es el último paso.
4. **Nada sin enseñar y en orden cronológico**: una palabra del idioma meta cuenta como disponible después de aparecer en un paso de enseñanza (`ejemplos`, `vocabulario`, `patron` o `tabla`) o en un prerrequisito transitivo. Declararla en la lista `vocabulario` no basta. Respuestas, opciones, ordenar, completar, audios y diálogos solo pueden usar lo ya expuesto; las formas `incorrecto` de `erroresFrecuentes` valen únicamente como distractores. Las frases de varias palabras cuentan palabra a palabra. En `zh` y `ja` se mantiene la convención de separar palabras con espacios en los datos.
5. `respuesta` de `elegir`/`escuchar` es un índice válido; `ordenar` usa exactamente los `tokens`.

Los ejercicios nuevos se separarán en la biblioteca `exercise-library/1`; contrato y migración en `BIBLIOTECA_EJERCICIOS_V1.md`. Hasta completar el adaptador, los pasos embebidos siguen siendo la fuente compatible.

## Estados de unidad (se calculan desde `practicas`, DEC-006)

`bloqueada` (prerrequisito sin practicar; se ve, no se hace) → `disponible` → `enCurso` (vio la explicación) → `practicada` (práctica guiada resuelta) → `aprobada` (evaluación ≥ umbral a la primera en ese intento) → `dominada` (aprobada + repaso acertado ≥ 1 día después). `repasar` = aprobada/dominada con repaso vencido.
Desbloqueo: todos los prerrequisitos ≥ `practicada` u **omitibles**. Nivel completo: todas sus unidades ≥ `aprobada`.
Omitible (DEC-011): unidad de un nivel interno inferior al del diagnóstico (`nivelBase = fundamentos ? 0 : nivelInicial`) y no aprobada. Cuenta como prerrequisito cumplido, no se recomienda y se muestra «Opcional · según tu nivel»; se puede estudiar igual.

## Claves de evidencia (en `ProgressState.practicas`)

- Ítem: `ruta:<unidadId>:<pasoId>:<itemId>`
- Vista: `ruta:<unidadId>:visto`
- Evaluación (resumen del último intento, `aprobada` es permanente): `ruta:<unidadId>:evaluacion`
- Repaso: `ruta:<unidadId>:repaso` (`caja`, `proximo`)
- Nivel completo: `ruta:<idioma>.f0:completa`

Se guardan en `practicas` porque las versiones antiguas de la app lo conservan intacto al sincronizar.
