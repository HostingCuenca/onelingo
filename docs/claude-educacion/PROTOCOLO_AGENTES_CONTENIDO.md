# Protocolo de agentes editoriales v2

Estado: obligatorio para contenido nuevo desde Inglés N2 C16. Complementa `CONTRATO_LOTE_INGLES.md`; no sustituye el mapa curricular ni autoriza activación en runtime.

## Objetivo

Usar agentes para aumentar cobertura sin convertir el currículo en una plantilla repetitiva. La unidad de trabajo es **una clase**. El lote de quince sirve para planificación y QA transversal, no para saltarse la revisión incremental.

## Roles separados

1. **Planificador**: congela mapa, prerrequisitos, conceptos disponibles, vocabulario reservado y resultado comunicativo.
2. **Autor**: produce una clase en staging. Nunca escribe en el directorio editorial final ni decide `GO`.
3. **Revisor lingüístico/pedagógico**: comprueba naturalidad, nivel A2, progresión, carga y correspondencia entre objetivo y evidencia.
4. **Revisor adversarial**: busca respuestas filtradas, consignas irresolubles, distractores ambiguos, duplicación y evaluación derivada de la práctica.
5. **Simulador**: recorre la clase como principiante, alumno con carga alta, fallo total, acierto total y reingreso.
6. **Integrador**: único rol autorizado para copiar un candidato aprobado a `assets/contenido/`.

Un mismo agente puede volver a corregir su borrador, pero no puede aprobarlo ni integrarlo.

## Paquete mínimo de entrada

El autor recibe únicamente:

- especificación de la clase en el mapa editorial;
- resumen de conceptos, patrones y vocabulario disponibles;
- vocabulario reservado para clases posteriores;
- firmas normalizadas del bloque para evitar duplicación;
- digest del mapa y de la clase anterior;
- contrato de salida y comandos de validación.

No recibe todo el repositorio ni todas las clases completas si basta un resumen. Esto reduce consumo de contexto y copia involuntaria.

## Salida del autor

El borrador debe incluir:

- JSON de clase con esquema `onelingo.editorial.class.v1`;
- `status: shadow` y `runtimeAi: false`;
- evidencia de conteos, formatos, conceptos y habilidades;
- lista de vocabulario introducido y reutilizado;
- firmas `estímulo + respuesta` del candidato;
- supuestos y dudas pendientes;
- resultado de la validación individual.

El autor devuelve `DRAFT`, nunca `GO`.

## Política verificable `editorial-agent.v2`

Toda clase nueva declara en `qualityPolicy`:

```json
{
  "chronologyTokens": "enforce",
  "answerReuseAcrossEarlyReserved": "forbid",
  "answerEvidenceReuseAcrossPools": "forbid",
  "agentContract": "editorial-agent.v2",
  "minChoices": 3,
  "maxPromptCharacters": 90,
  "feedbackReuseWithinClass": "forbid",
  "minClassFormats": 4
}
```

El validador común rechaza el candidato si la declaración y el contenido no coinciden. También exige accesibilidad completa, recuperación determinista, cobertura de `usesVocabulary`/`usesPatterns`, feedback no repetido y consignas de hasta 90 caracteres.

## Límites editoriales

- Cero repetición normalizada de `estímulo + respuesta` dentro de una clase.
- Cero reutilización de evidencia entre práctica y evaluación/repaso.
- Evaluación y repaso usan contextos inéditos.
- `elegir` y `escuchar` tienen al menos tres opciones desde C16; dos opciones solo se toleran en contenido histórico.
- Cada feedback explica el patrón o el error del ítem; no se repite dentro de la clase.
- Cada clase usa al menos cuatro formatos.
- La posición correcta de actividades seleccionables usa al menos dos índices y ninguno supera el 60 % dentro de una clase.
- No se repiten exactamente consignas, feedback ni firmas semánticas dentro del bundle v2.
- Los objetivos deben ser específicos y distintos entre las clases del bundle.
- La clase declara su `phase`; `production` y `transfer` incluyen en evaluación o repaso una escritura de al menos ocho tokens y dos variantes aceptadas. Para producciones extensas, `origin.scoring` declara `wordRange` y `evidenceGroups`: una frase alternativa por grupo basta, pero todos los criterios curriculares deben estar presentes.
- En completar multiparte, `requiredParts.length <= minimumCorrect`; si el canónico usa `|`, cada parte acepta también una formulación natural sin ese separador.
- Si declara `escucha` o `escritura`, aporta evidencia real del formato correspondiente; cada concepto aparece en enseñanza, práctica guiada y evaluación.
- Todo vocabulario declarado aparece de forma observable en enseñanza o ejercicios; no basta incluirlo en `usesVocabulary`.
- Se rechazan referencias sin antecedente visible como «idea trabajada», «modelo de la clase», «contexto nuevo» o «frase indicada».
- Una respuesta de un token solo puede repetirse si cambia de forma sustancial el contexto y la operación cognitiva.
- El cierre C20/C25/C30 demuestra los cinco conceptos del bloque en evaluación real.
- Una imagen es opcional: solo se añade cuando reduce ambigüedad y debe tener alt text; no se fuerza una cuota visual.

## Rechazo temprano

Se rechaza antes de revisión profunda si falla cualquiera:

- ID, nivel, fase o prerrequisito distintos del mapa;
- esquema, hashes o conteos inválidos;
- contenido futuro no autorizado;
- activación distinta de `shadow` o dependencia de IA en runtime;
- pistas fuera de práctica guiada;
- respuesta incorrecta, dos respuestas defendibles o consigna incompleta;
- remediación rota;
- estímulo de evaluación copiado de práctica;
- cierre sin cobertura acumulativa completa;
- cambio del digest de entrada.

## Flujo de quince clases

```text
planificar C16–C30
  C16 → validar → revisar → simular → corregir → GO
  ...
  C20 → puerta longitudinal C16–C20
  C21–C25 → misma puerta
  C26–C30 → misma puerta
auditoría transversal C16–C30
regeneración y comparación de hashes
informe QA
integración única en shadow
```

La autoría puede repartirse por bloques en staging aislado. La integración siempre respeta el orden y revalida las dependencias longitudinales. Ningún agente edita el mismo archivo que otro.

## Resultado del revisor

El revisor devuelve solo `GO`, `REVISE` o `REJECT`, con incidencias estructuradas:

```json
{
  "decision": "REVISE",
  "issues": [
    {
      "severity": "P1",
      "path": "pools.evaluation[1]",
      "rule": "AMBIGUOUS_DISTRACTOR",
      "evidence": "Dos opciones son válidas en el contexto.",
      "requiredChange": "Añadir un marcador temporal que deje una sola respuesta."
    }
  ]
}
```

P0/P1 bloquean integración. P2 requiere corrección o justificación editorial registrada. P3 no bloquea, pero se conserva en el informe.

## Comandos mínimos

```bash
python3 tools/contenido/validar_bundle_editorial.py \
  --file <clase-o-bundle.json> --start <n> --end <n> --level 2

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s test_tools
PYTHONDONTWRITEBYTECODE=1 python3 tools/validar_ruta.py
```

El último comando valida el producto, no aprueba por sí solo la calidad lingüística o pedagógica.
