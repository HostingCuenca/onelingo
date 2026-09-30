# Inventario curricular 10 × 100 por idioma

Estado: línea base de migración. Fecha: 2026-09-27.

## Objetivo fijo

- Diez idiomas: `en`, `es`, `fr`, `de`, `pt`, `it`, `zh`, `ja`, `ko`, `ru`.
- Diez niveles internos por idioma.
- Cien clases editoriales por nivel: 1.000 por idioma y 10.000 en total.
- Fundamentos (`f0`) se conserva como preparación adaptativa y no cuenta dentro de las 1.000 clases.
- Equivalencia vigente: niveles 1–2 A1, 3–4 A2, 5–6 B1, 7–8 B2 y 9–10 C1. C2 queda planificado fuera de este alcance.
- La IA conversacional puede existir como función opcional, pero no enseña, genera ni decide el contenido base, la evaluación o el repaso.

## Línea base medida

Los conteos siguientes proceden de `assets/contenido/<idioma>/ruta/`. No se suman los archivos `nivel-*.json` legados.

| Idioma | Revisión | F0 aparte | Clases N1–N10 | Niveles cubiertos | Cobertura / 1.000 | Faltan |
|---|---|---:|---:|---|---:|---:|
| Inglés | revisada | 7 | 29 | 1 y 2 | 2,9 % | 971 |
| Español | inicial | 8 | 9 | 1 | 0,9 % | 991 |
| Francés | inicial | 8 | 9 | 1 | 0,9 % | 991 |
| Alemán | inicial | 8 | 9 | 1 | 0,9 % | 991 |
| Portugués BR | inicial | 8 | 9 | 1 | 0,9 % | 991 |
| Italiano | inicial | 8 | 9 | 1 | 0,9 % | 991 |
| Chino | inicial | 13 | 9 | 1 | 0,9 % | 991 |
| Japonés | inicial | 16 | 8 | 1 | 0,8 % | 992 |
| Coreano | inicial | 9 | 9 | 1 | 0,9 % | 991 |
| Ruso | inicial | 10 | 9 | 1 | 0,9 % | 991 |

Totales:

- 204 unidades físicas en esquema 2.
- 95 unidades pertenecen a `f0`.
- 109 clases cuentan para el objetivo de 10.000: cobertura actual 1,09 %.
- Inglés es el único idioma que ya tiene contenido de Nivel 2.
- Los otros nueve idiomas requieren revisión nativa antes de considerarse definitivos.

## Lo que se conserva

- IDs estables, vocabulario, errores frecuentes, ejemplos, patrones, tablas y situaciones de las unidades válidas.
- Grafo de prerrequisitos y orden de enseñanza antes de práctica.
- Evidencia de progreso existente bajo claves `ruta:<unidad>:...`.
- Fundamentos específicos por escritura y pronunciación.
- Escala interna y equivalencias MCER.

Las unidades actuales no se borran ni se renombran durante el diseño. Cada una debe mapearse a una clase nueva como `conservar`, `dividir`, `reescribir`, `fusionar` o `retirar` antes de cambiar rutas publicadas.

## Diferencias obligatorias por idioma

La arquitectura y los resultados comunicativos pueden compartirse; la secuencia lingüística no se traduce desde inglés.

| Idioma | Ejes propios que gobiernan la secuencia |
|---|---|
| Inglés | auxiliares, tiempos y aspecto, orden, phrasal verbs, pronunciación no transparente |
| Español | ser/estar, género y concordancia, clíticos, conjugación, subjuntivo |
| Francés | género, liaison, contracciones, pronombres, passé composé/imparfait |
| Alemán | casos, género, orden V2/final, verbos separables, declinación |
| Portugués BR | nasalización, contracciones, pronombres, infinitivo personal, subjuntivo |
| Italiano | consonantes dobles, concordancia, clíticos, pasados, congiuntivo |
| Chino | pinyin, tonos, caracteres, clasificadores, partículas y aspecto |
| Japonés | kana/kanji, partículas, contadores, orden SOV y cortesía |
| Coreano | hangul, batchim, partículas, honoríficos y niveles de habla |
| Ruso | cirílico, casos, aspecto, movimiento y acento móvil |

Para `zh`, `ja`, `ko` y `ru`, escritura y lectura son prerrequisitos por competencia. Un diagnóstico oral alto no puede omitir automáticamente alfabetización no demostrada.

## Riesgos comprobados en la línea base

1. El validador acepta como «enseñada» una palabra solo por estar declarada en `vocabulario`, aunque ningún paso la muestre.
2. No verifica que el concepto o la regla objetivo se enseñe y se mida realmente.
3. Las habilidades declaradas no exigen evidencia de ejercicios del formato correspondiente.
4. El repaso reutiliza literalmente `practica_independiente` y `evaluacion`; no hay banco editorial separado.
5. Entre 21 % y 30 % de las respuestas de evaluación por idioma aparecen antes como respuestas de práctica. Sin variantes se puede medir memoria del ítem.
6. Un diagnóstico alto puede recomendar niveles sin contenido publicado.
7. El nivel global puede volver opcional una alfabetización que el alumno no domina.
8. Solo inglés tiene una biblioteca editorial propia; otros idiomas dependen de contenido derivado o fallback.

## Criterio de finalización por idioma

Un idioma no se considera poblado por tener 1.000 títulos. Debe cumplir:

- 1.000 IDs de clase únicos y alcanzables;
- cien clases por cada nivel 1–10;
- objetivos, vocabulario, reglas y prerrequisitos explícitos;
- enseñanza antes de práctica y evaluación;
- bancos editoriales separados para práctica, evaluación y repaso;
- cobertura verificable de lectura, escucha, escritura, conversación, pronunciación, vocabulario y gramática;
- evaluaciones sin exposición previa de sus familias de ítems;
- repasos con variantes no vistas;
- revisión lingüística/nativa registrada;
- simulación completa de alumno sin callejones sin salida;
- cero dependencia de IA generativa en la ruta base.

