# Plan de implementación — currículo editorial 10 × 100

Estado: plan aprobado para ejecución por fases. Este documento no activa contenido ni cambia el comportamiento de la aplicación.

## 1. Objetivo y reglas no negociables

Cada uno de los diez idiomas tendrá 10 niveles de 100 clases. Fundamentos (`f0`) se conserva como preparación adaptativa y no cuenta dentro de las 1.000 clases por idioma.

- La ruta base funciona sin tutor IA y sin generación de ejercicios en tiempo de ejecución.
- Enseñanza, práctica, evaluación y repaso son contenido editorial versionado.
- El repaso usa un banco `review` propio; no reutiliza preguntas ya vistas en práctica o evaluación.
- Cada idioma conserva una secuencia lingüística propia. Se comparte el contrato, no se traduce mecánicamente el curso inglés.
- El esquema 2 y el progreso existente permanecen disponibles durante toda la migración.
- No se publica un lote por tener títulos: debe contener actividades, respuestas, trazabilidad y revisión.
- No se despliega a producción durante las fases de planificación, importación en seco o modo sombra.

## 2. Línea base comprobada

La ruta activa contiene 204 unidades, de las cuales 109 pertenecen a N1–N10 y el resto corresponde a Fundamentos. El inventario de ítems embebidos que debe clasificarse antes de ampliar el currículo es:

| Idioma | Enseñanza | Guiada | Práctica | Aplicación | Evaluación | Total |
|---|---:|---:|---:|---:|---:|---:|
| Inglés | 150 | 139 | 104 | 67 | 218 | 528 |
| Español | 100 | 81 | 67 | 35 | 102 | 285 |
| Francés | 108 | 79 | 62 | 34 | 104 | 279 |
| Alemán | 104 | 80 | 65 | 34 | 111 | 290 |
| Portugués | 108 | 80 | 62 | 33 | 105 | 280 |
| Italiano | 99 | 80 | 63 | 33 | 104 | 280 |
| Chino | 132 | 88 | 84 | 43 | 137 | 352 |
| Japonés | 125 | 96 | 92 | 47 | 145 | 380 |
| Coreano | 115 | 72 | 71 | 38 | 111 | 292 |
| Ruso | 115 | 94 | 75 | 42 | 116 | 327 |
| **Total** | **1.156** | **889** | **745** | **406** | **1.253** | **4.449** |

Los 4.449 registros son elementos de los pasos actuales, no equivalen necesariamente a 4.449 ejercicios publicables: la importación debe detectar explicaciones, tablas, duplicados, pistas y contenido que requiera edición. El número de elementos interactivos actuales es 3.293 al excluir los 1.156 elementos de enseñanza.

## 3. Estrategia de activación transparente

Cada unidad tendrá un estado explícito en un manifiesto de activación:

| Estado | Fuente que ve el alumno | Trabajo de la biblioteca nueva | Condición de salida |
|---|---|---|---|
| `legacy` | Pasos embebidos actuales | Ninguno obligatorio | Manifiesto importado y validado |
| `shadow` | Pasos embebidos actuales | Carga, valida y selecciona en paralelo; registra diferencias | Cero errores críticos, revisión editorial y simulaciones aprobadas |
| `active` | `exercise-library/1` | Fuente de actividades de la unidad | Monitoreo y métricas estables |

Reglas:

- Una biblioteca ausente o inválida nunca rompe una unidad `legacy` o `shadow`.
- En `shadow`, cualquier diferencia se informa pero no altera progreso ni interfaz.
- En `active`, la ausencia del pool `review` es un error bloqueante para esa unidad. No se mezcla silenciosamente con `evaluation` ni `practice`.
- La reversión consiste en devolver la unidad a `legacy`; no se borran pasos embebidos ni progreso histórico.
- La activación es por unidad, no por idioma completo, para limitar el radio de riesgo.

## 4. Frentes de trabajo y dependencias

### A. Contrato e importador

Crear primero una herramienta aislada, con `dry-run` como modo predeterminado. Lee únicamente contenido activo del esquema 2, incluido `f0`; no importa inicialmente los `nivel-*.json` legados desconectados de la ruta.

Entregables:

- IDs estables de familia y variante, independientes de la posición física.
- Origen completo: archivo, unidad, paso, índice y clave histórica.
- Hash canónico SHA-256 y detección de duplicados exactos y cercanos.
- Clasificación de pasos actuales en `teaching`, `practiceGuided`, `practice` y `evaluation`.
- Ningún ejercicio se convierte automáticamente en `review`; ese pool se redacta y aprueba editorialmente.
- Informes reproducibles: `manifest.json`, `classification.csv`, `duplicates.json`, `integrity.json`, `migration-map.json` y `progress-impact.json`.
- Aplicación idempotente, escritura atómica y prohibición de sobrescribir revisiones publicadas.

Convención inicial de identidad:

```text
familia: ex.onelingo.<idioma>.<unidad>.<paso>.<slug-estable>
variante: <familyId>:v<revision>:<pool>
```

Cambiar texto, respuesta, formato o lógica de corrección crea una revisión nueva. Reordenar opciones no crea una variante nueva.

### B. Cargador, adaptador y persistencia

Este frente comienza cuando el contrato del importador está congelado.

Entregables:

- Asset opcional por idioma para `exercise-library/1` y cargador con caché.
- Distinción entre archivo ausente y archivo inválido.
- Conversión pura y probada `ExerciseVariant ↔ Item` para los seis formatos actuales.
- Resolución por unidad y pool mediante selector determinista.
- Referencia persistida con `variantId`, `libraryVersion`, `selectionId` y fuente, conservando las claves históricas.
- Soporte de manifiesto `legacy/shadow/active`.
- Diagnóstico visible de cobertura y fallback; ningún fallback silencioso.

### C. Producción editorial

El contenido se trabaja en bloques de cinco clases. Cada bloque tiene una ficha de alcance con resultados, conceptos, vocabulario, habilidades y prerrequisitos.

Por clase se redactan y separan:

1. exposición y ejemplos;
2. práctica guiada con ayuda;
3. práctica independiente;
4. evaluación sin pistas;
5. variantes de repaso diferido nunca vistas en los pasos anteriores.

La cantidad exacta por pool se calibra en el piloto, pero ninguna clase puede activarse con evaluación o repaso vacíos, referencias rotas o una única variante repetida.

### D. QA pedagógico y lingüístico

Cada lote pasa por cuatro funciones separadas:

- diseñador curricular: fija objetivo comunicativo, MCER, conceptos y prerrequisitos;
- editor de ejercicios: redacta y versiona las familias de cada pool;
- QA estructural: comprueba esquema, IDs, enlaces, alcanzabilidad, conteos y duplicados;
- QA pedagógico: comprueba progresión, carga cognitiva, espiral, transferencia y correspondencia entre objetivo y evidencia;
- revisor lingüístico: comprueba naturalidad, registro, escritura y respuestas;
- auditor adversarial: busca filtraciones, ambigüedad, duplicados y saltos de dificultad;
- simulador de estudiante: recorre perfiles y verifica desbloqueo, refuerzo y retención.
- responsable humano curricular: única autoridad para aprobar la publicación.

El autor no aprueba su propio lote. Para los nueve idiomas marcados como versión inicial, la activación pública requiere revisión competente en ese idioma. El lote de cinco clases es indivisible para la aprobación: si falla una clase, se corrige y se valida de nuevo el lote completo.

## 5. Hitos ejecutables

### M0 — Congelar línea base y contrato

Estado: completado en diseño.

- Inventario 10 × 100 y plan de Inglés N1.
- Núcleo aislado `exercise-library/1` y selector determinista.
- Validadores cronológicos y simulaciones base.
- Decisiones DEC-017 a DEC-019.

Puerta: validación de 10 idiomas sin errores y suite vigente verde.

### M1 — Importador reproducible en seco

- Implementar CLI sin conexión a la interfaz.
- Importar todo el contenido activo de inglés, incluido `f0`.
- Generar los seis informes y revisar manualmente una muestra.
- Probar dos ejecuciones idénticas: la segunda debe producir cero cambios.

Puerta: 100 % de elementos clasificados o marcados explícitamente para revisión; cero colisiones de ID; cero pérdida de referencias.

### M2 — Cargador y modo sombra

- Implementar cargador, adaptador, metadatos de evidencia y manifiesto de activación.
- Mantener todas las unidades en `legacy` al integrar.
- Pasar una unidad inglesa a `shadow` y comparar selección, corrección y progreso.

Puerta: diferencia cero en aprobación, retención, fechas y desbloqueos; un error de biblioteca revierte de forma segura al comportamiento actual.

### M3 — Piloto editorial inglés, un bloque de cinco clases

- Elegir el primer bloque de Inglés N1 definido en `PLAN_NIVEL1_INGLES_100.md`.
- Completar sus cinco pools, especialmente el banco nuevo de `review`.
- Revisar contenido, ejecutar simulaciones y activar primero una unidad, luego el bloque.
- Observar errores de corrección, abandonos, repetición y tiempo por clase.

Puerta: cinco clases aprobadas por los cuatro roles, 0 fugas entre pools, 0 referencias rotas y progreso histórico intacto.

### M4 — Completar Inglés N1 (100 clases)

- Producir 19 bloques restantes, uno a la vez.
- Cada bloque avanza `legacy → shadow → active` de forma independiente.
- Realizar auditoría acumulativa al cerrar cada 25 clases.

Puerta: exactamente 100 clases activas, secuencia completa, 100 % de pools requeridos y revisión editorial registrada.

### M5 — Inglés N2–N10

- Elaborar mapa de resultados y prerrequisitos de cada nivel antes de redactar clases.
- Ejecutar lotes de cinco y auditorías de cierre por nivel.
- No usar la velocidad de producción de N1 como sustituto de validación pedagógica.

Puerta por nivel: 100 clases completas y simulación longitudinal desde el nivel anterior.

### M6 — Los otros nueve idiomas

- Crear primero un mapa propio por idioma y nivel, incluyendo escritura, fonología, morfología, registro y situaciones.
- Importar sus activos actuales mediante el mismo proceso reproducible.
- Pilotar cinco clases y ajustar reglas específicas antes de escalar.
- Prioridad operativa sugerida: español, francés, alemán, portugués, italiano, chino, japonés, coreano y ruso; puede cambiar por disponibilidad de revisores.

Puerta por idioma: revisión lingüística competente, perfiles de escritura pertinentes y 10 niveles completos sin traducir mecánicamente la secuencia inglesa.

### M7 — Consolidación

- Retirar el fallback de una unidad solo cuando lleve un ciclo estable en `active`.
- Conservar aliases y lectores históricos mientras existan usuarios con progreso antiguo.
- Decidir en una fase separada cuándo retirar físicamente los pasos embebidos; no forma parte de la primera migración.

## 6. Pruebas y puertas automáticas

Cada cambio técnico debe cubrir:

- biblioteca válida, ausente y malformada;
- IDs y hashes estables ante reordenamiento;
- segunda importación sin cambios;
- referencias, conceptos, habilidades y prerrequisitos válidos;
- cero duplicados exactos sin resolver;
- cero contaminación entre `practice`, `evaluation` y `review`;
- cero pistas o respuestas expuestas en evaluación y repaso;
- selección determinista con el mismo `seed`;
- progreso, aprobación irreversible, retención y fechas preservados;
- revisión nueva sin heredar falsamente dominio del ítem anterior;
- flujo de repaso exclusivamente desde `review` en unidades `active`;
- rutas no latinas para chino, japonés, coreano y ruso;
- smoke test de los diez idiomas y simulación longitudinal.

Cada lote editorial debe cumplir además:

- cinco clases exactas, únicas, alcanzables y enlazadas;
- todo concepto evaluado fue enseñado antes y ningún prerrequisito se usa prematuramente;
- toda habilidad declarada tiene evidencia observable;
- evaluación con al menos cuatro variantes y dos formatos;
- repaso con variantes no vistas que exigen recuperación o transferencia, no repetición literal;
- resultado comunicativo verificable, no solo reconocimiento mecánico;
- 100 % de clases con revisión lingüística registrada antes de publicación;
- ninguna llamada de IA necesaria para recorrer, aprobar o repasar la ruta base.

Comandos mínimos antes de integrar un lote:

```bash
python3 tools/validar_ruta.py
~/flutter/bin/flutter analyze lib
~/flutter/bin/flutter test
```

Un lote no avanza con errores. Los avisos editoriales solo pueden quedar abiertos si tienen propietario, motivo, fecha y no afectan corrección, seguridad pedagógica ni secuencia.

## 7. Perfiles de simulación

Los recorridos automáticos deben cubrir al menos:

- principiante total que empieza en Fundamentos;
- alumno ubicado por diagnóstico dentro del contenido realmente publicado;
- alumno oral alfabetizado y no alfabetizado en zh/ja/ko/ru;
- alumno que falla práctica, vuelve a intentarlo y continúa;
- alumno que aprueba y falla un repaso diferido;
- alumno que abandona y reanuda a mitad de unidad;
- alumno con progreso previo a la migración;
- alumno que completa un nivel y cruza sus prerrequisitos al siguiente.

Para cada perfil se verifica siguiente paso accionable, ausencia de bloqueos, conservación de historial, exposición previa de ítems, recuperación tras error, tiempo, cobertura de habilidades y coherencia de dificultad.

## 8. Organización de agentes y propiedad

Los agentes de bajo consumo se usan para tareas acotadas y verificables: inventarios, detección de duplicados, borradores por bloque, auditoría adversarial y simulación. No editan simultáneamente el mismo archivo ni deciden por separado el contrato común.

No se paralelizan:

- esquema e IDs globales;
- grafo de prerrequisitos;
- manifiesto de activación;
- aplicación de migraciones;
- secuencia de niveles dentro de un mismo idioma;
- evaluación y repaso antes de congelar enseñanza y práctica;
- aprobación lingüística final.

Cada entrega de agente incluye archivos revisados, supuestos, incidencias y validaciones. La integración y la puerta de calidad permanecen bajo un único responsable.

## 9. Reversión y trazabilidad

- El importador escribe primero a temporal y aplica solo un manifiesto aprobado.
- Cada ejecución conserva versión, fecha, hash y mapa legacy → variante.
- Nunca se elimina progreso ni se afirma dominio de una variante nueva por similitud incierta.
- Ante una regresión, se cambia la unidad a `legacy`, se conserva la evidencia nueva para diagnóstico y se corrige fuera del camino del alumno.
- No se despliega desde un árbol con cambios ajenos ni sin seguir `DEPLOYMENT_RUNBOOK.md`.

## 10. Próxima tarea de implementación

Implementar **M1 — importador reproducible en seco para inglés**, sin conectar aún la biblioteca a la interfaz. Es la menor unidad de trabajo que reduce incertidumbre: fija IDs, descubre duplicados, cuantifica edición pendiente y permite aprobar el manifiesto antes de tocar progreso o experiencia del alumno.
