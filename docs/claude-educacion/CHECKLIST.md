# Checklist — educación multilingüe

Leyenda: `[ ]` pendiente · `[~]` en curso · `[x]` terminado · `[!]` bloqueado

## Fase 1 — Auditoría
- [x] Checkpoint completo (`396333b`, tag `checkpoint-2026-09-26-pre-multilang`), idéntico a producción (`main.dart.js` `caa2e8a4…`).
- [x] Inventariar idiomas habilitados (10).
- [x] Agente A: inventario curricular, grafo gramatical inglés (111 nodos), sistemas lingüísticos y rutas por idioma.
- [x] Agente B: vocabulario, 50 situaciones, adaptación multilingüe, sistema de repaso.
- [x] Agente C: tipos de actividad, habilidades, diagnóstico, evaluación, certificaciones.
- [x] Agente D: mapa técnico, acoplamiento a inglés, progreso, bug de gramática, esquema, migración, recorridos.
- [x] MAPA_CURRICULAR.md, COBERTURA.md, IDIOMAS.md, ESQUEMA_CONTENIDO.md, MIGRACION_FUNDAMENTOS.md.

## Fase 2 — Fundamentos
- [x] Modelos comunes de ruta con textos por idioma de apoyo (`lib/core/aprendizaje/modelos.dart`).
- [x] Cargador por idioma sin `dart:io` (web y móvil).
- [x] Grafo de prerrequisitos con validación (ciclos, IDs, orden).
- [x] Estados de unidad, desbloqueo, aprobación, retención y repaso espaciado.
- [x] Migración de foundations-v1 por alias de lectura, sin pérdida.
- [x] Ruta inicial de inglés U0–U5.
- [x] Rutas iniciales de fr, it, pt.
- [x] Rutas iniciales de de, ru, es (es con apoyo en inglés, DEC-004).
- [x] Rutas iniciales de zh, ja, ko (fase de escritura y sonidos).
- [x] Pantalla de ruta y de unidad conectadas en `/fundamentos` (Aprender, tarjeta de camino, Inicio).
- [x] Nivel 0 = ruta; aprobarla desbloquea el Nivel 1 (DEC-007).
- [x] Persistencia de evidencia y de posición en la unidad (verificado en web).
- [ ] Revisión nativa de los 9 idiomas «inicial» (DEC-010).

## Fase 2b — A1 de inglés
- [x] Esqueleto contractual de 29 unidades (PLAN_A1_INGLES.md) con prerrequisitos del grafo.
- [x] Módulo a1-1 (12 u.), a1-2-presente (8 u.), a1-2-comunicar (9 u.) con integraciones.
- [x] Rutas por nivel `/ruta/:nivel` con secciones por módulo; niveles 1–2 de inglés enlazados.
- [x] Unidades omitibles según diagnóstico (DEC-011).
- [x] Validador: frases de error solo como distractor.

## Fase 2c — Profundización multilingüe
- [x] Paso `tabla` (validadores Python y Dart, interfaz con audio por casilla).
- [x] Escritura/sonidos completos en f0 de los 10 idiomas.
- [x] A1 «Primeras frases» con tablas de conjugación en los 9 idiomas; inglés con alfabeto y tablas.
- [x] Fallo en práctica → continuar + repetir al final del bloque.
- [x] Celebración (XP, precisión, tiempo) y sonido de nivel; también en lecciones antiguas.
- [x] Precarga de fuentes CJK/cirílico en web.
- [x] El alcance de `20260926-edu-3-escrituras` quedó absorbido y publicado en `20260929-edu-4-n1-runtime`; no desplegar la release 3 por separado.

## Fase 3 — Gramática
- [x] Verificar bug «gramática desaparece»: área corregida antes; pantalla no reanudaba ni marcaba (auditoría D).
- [x] Reanudar tema, marcar practicados en el Temario, guardar borradores, respetar nivel elegido.
- [ ] Vincular las 43 guías a IDs del grafo `en-g-*` (alias `grammar-guide-*`).
- [ ] Recolocar guías fuera de nivel (continuous, past-continuous, third-conditional).

## Fase 4 — Vocabulario
- [x] Vocabulario inicial por idioma enlazado a unidades (75–93 vocablos por idioma).
- [ ] Estados de vocabulario por palabra (visto → dominado) con id común de sentido.

## Fase 5 — Situaciones
- [x] Paso `situacion` con diálogo modelo en cada unidad f0 (10 idiomas).
- [ ] Convertir la situación «restaurante» en mini-ruta de 12 pasos (piloto).
- [ ] Mapa de las 50 situaciones al esquema 2 con nivel y gramática.

## Fase 6 — Habilidades
- [x] Formatos elegir, escuchar, ordenar, completar, escribir, relacionar.
- [ ] Pares mínimos/tonos como formato propio; dictado nuevo; lectura con varias preguntas en esquema 2.

## Fase 7 — Evaluación
- [x] Evaluación de fin de unidad (≥ 4 ítems, ≥ 2 formatos, 80 % a la primera, sin pistas).
- [x] Separar evidencia con ayuda (guiada) de evidencia sin ayuda (evaluación).
- [ ] Banco de evaluación separado del de práctica.
- [ ] Rediseñar el examen de ascenso de 10 preguntas.

## Fase 8 — Personalización
- [x] Metadatos `tutor` por unidad en el contenido (sin integración visual).
- [ ] Pasar esos metadatos al tutor IA (fase de avatares).

## Fase 8b — Voz y feedback
- [x] `language_code` en ElevenLabs, caché por idioma, zh/ja sin espacios (DEC-012).
- [x] Sílabas sueltas no latinas con voz nativa del sistema.
- [x] Sonidos Kenney revisados + toque de selección (DEC-013).
- [x] Opciones con pedestal y animación; botones con `BotonPrincipal`.
- [ ] Escuchar y validar los sonidos y voces en dispositivo real.

## Fase 9 — Pruebas
- [x] Grafo sin ciclos y sin referencias rotas (10 idiomas).
- [x] Ninguna unidad vacía; ninguna palabra sin enseñar (Python y Dart).
- [x] Desbloqueo, aprobación irreversible, retención y repaso.
- [x] Migración de foundations-v1.
- [x] Progreso persistente (toJson/fromJson y almacenamiento web).
- [x] Gramática reanuda el tema tras volver.
- [x] Recorrido de principiante U0 completo (widget test) y navegación con pestañas.
- [x] `flutter analyze`: sin errores ni avisos nuevos (7 info previos en sync.dart).
- [x] `flutter test --no-pub`: 155 pasan, 1 omitida, 0 fallos; herramientas Python: 40 pasan; rutas de 10 idiomas: 0 errores (2026-09-28). Backend conserva las 11 pruebas documentadas.
- [x] Build web local con API pública generado; `main.dart.js` SHA-256 `71d06ed85241a61ff340e6b2c34ec84b3543100030f76fecb42a78ea8ad1af19`.
- [x] Recorrido manual web (inglés) y emulador Android (japonés).

## Fase 10 — Producción
- [x] Release educativa 1 `20260926-edu-1-fundamentos` publicada y verificada.
- [x] Release educativa 2 `20260926-edu-2-a1-voz` publicada y verificada (ver DESPLIEGUES.md).

## Fase 11 — Replanteamiento editorial 10 × 100
- [x] Inventario real por idioma: 109/10.000 clases de N1–N10; F0 separado.
- [x] Decidir 10 niveles × 100 clases para cada idioma (DEC-018).
- [x] Excluir tutor/generación IA del camino base (DEC-017).
- [x] Diseñar Inglés Nivel 1 como 20 bloques × 5 clases.
- [x] Diseñar pools editoriales separados: enseñanza, guiada, práctica, evaluación y repaso.
- [x] Auditar secuencia con perfiles de estudiante y sistemas de escritura.
- [x] Implementar núcleo aislado `exercise-library/1`: parser, pools, IDs, validación y selector determinista.
- [x] Integrar cargador y adaptador retrocompatible del esquema 2; una unidad `active` consume exclusivamente la biblioteca y conserva metadatos de selección.
- [ ] Importar y clasificar los ejercicios actuales con IDs globales estables.
- [x] Corregir el repaso para usar solo variantes editoriales del pool `review`; la selección es determinista y se registra.
- [x] Fortalecer validador Python: exposición cronológica, evidencia de habilidades y contaminación entre práctica/evaluación.
- [x] Crear simulaciones automatizadas para diagnóstico, saltos, alfabetización, retorno y refuerzo.
- [x] Ajustar diagnósticos por encima del contenido al mayor nivel realmente publicado.
- [x] Impedir que el diagnóstico global omita alfabetización zh/ja/ko/ru sin evidencia.
- [x] Priorizar repaso/refuerzo vencido antes de contenido nuevo y conservar la aprobación histórica.
- [x] Consolidar el plan de migración por hitos, con estados `legacy → shadow → active`, puertas de calidad y reversión por unidad.
- [x] Extraer el PDF maestro a un manifiesto verificable: 10 niveles, 1.000 especificaciones e IDs únicos; ninguna IA requerida en ejecución.
- [x] M1: importador reproducible en seco; 36 unidades, 528 familias/variantes, seis informes y 0 errores; no aplicado al producto.
- [x] M2: cargador, adaptador, diagnóstico, persistencia de metadatos y recorrido conectados; pruebas de datos y widget cubren N1 C1 y C100.
- [x] Adoptar escala cliente: N1 = A1 completo, progresión hasta C1 avanzado en N10 y equivalencia histórica conservadora (DEC-020).
- [x] Implementar versionado y migración de diagnóstico/progreso sin sobrescribir valores históricos.
- [x] M3: la integración técnica se amplió a las 100 clases de Inglés N1, quedó `active` y fue publicada en `20260929-edu-4-n1-runtime`; la revisión humana registrada sigue siendo requisito para los niveles en `shadow`.
- [x] Poblar las 100 clases de Inglés Nivel 1 (1.300 ejercicios) y validarlas antes de activar la nueva versión.
- [~] Poblar Inglés N2–N10 por lotes: N2 completo con C1–C100 (1.300 ejercicios, `shadow`); mapa N3 v2 validado y C1–C90 integradas (1.170 ejercicios, `shadow`); C91–C100 avanzan en cadena editorial. Luego continuar N3–N10 y cada idioma con su mapa propio.
- [ ] Registrar revisión pedagógica y lingüística por lote antes de publicar.
