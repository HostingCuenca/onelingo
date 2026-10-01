# OneLingo: arquitectura vigente

Actualizado: 2026-10-01 (fase A de la limpieza, DEC-026 y DEC-027).

**Este es el mapa que manda.** Si otro documento lo contradice, vale este. Los documentos de `docs/archivo/` son historia: no los uses para decidir. Si cambias la estructura, actualiza este archivo en el mismo commit.

## 1. Reglas de oro

1. **Una sola fuente por dato.** Antes de crear un JSON, una lista o una pantalla, busca la fuente canónica en la sección 3. Si existe, extiéndela; no la copies.
2. **El contenido es datos; la lógica no conoce idiomas.** Nada de `'en'` fijo en pantallas nuevas: el idioma sale de `progressProvider.idiomaMeta` o del curso cargado.
3. **El alumno nunca elige su nivel.** El nivel sale de la prueba de ubicación y de superar niveles (clases o prueba del nivel). Están prohibidos los desplegables de nivel en pantallas del alumno.
4. **Una sola estética.** La sección 5 se aplica a todas las pantallas nuevas o tocadas.
5. **Lo legado está congelado.** Se arregla si se rompe; no se amplía (sección 4).
6. **Decisiones del cliente** en `docs/claude-educacion/DECISIONES.md` (DEC-xxx). No se revierten sin preguntar.

## 2. Mapa del producto (navegación)

| Pestaña | Qué hay | Pantallas (`lib/features/…`) |
|---|---|---|
| Inicio | continuar, accesos (Academia, 50 situaciones, Tutor IA, Progreso, Prueba de nivel, Biblioteca) | `home/home_screen.dart` |
| Aprender | Nivel 0 (inglés desde cero) → Fundamentos → N1–N10 con estado (superado / en curso / bloqueado) y prueba de cada nivel | `course/levels_screen.dart`, `nivel0/*`, `ruta/ruta_screen.dart`, `ruta/unidad_screen.dart`, `ruta/prueba_nivel_screen.dart` |
| Practicar | 50 situaciones; tutores IA (chat y videollamada) | `practice/practice_screen.dart`, `situations/situation_screen.dart`, `chat/chat_screen.dart`, `plans/tutors_screen.dart`, `avatar/*` + `web/avatar/` |
| Biblioteca (desde Inicio) | Lecturas, Escuchas, Guías de gramática, Mapa de sonidos; luego «Mis palabras» y «Mis verbos» | `library/biblioteca_screen.dart`, `library/learning_unit_screen.dart`, `library/grammar_screen.dart` |
| Perfil | progreso, errores, planes | `progress/*`, `mistakes/*`, `plans/plans_screen.dart` |
| Entrada | bienvenida, registro, prueba de ubicación | `onboarding/*` (`ubicacion_screen.dart` inglés v2; `diagnostico_screen.dart` resto) |

## 3. Fuentes canónicas

| Dominio | Fuente | Lógica | Validación |
|---|---|---|---|
| Curso por niveles (ruta, esquema 2) | `assets/contenido/<idioma>/ruta/curso.json` + módulos (`f0.json`, `nN-editorial.json`) | `lib/core/aprendizaje/` (`modelos`, `dominio`, `providers`) | `python3 tools/validar_ruta.py`, `test/ruta_*` |
| Ejercicios de las clases editoriales | `assets/contenido/en/exercise-library.json` + activación | `core/aprendizaje/biblioteca_adaptador.dart` | herramientas en `tools/contenido/` |
| Nivel 0 inglés (leer y pronunciar) | `assets/contenido/en/nivel0/{nivel0,sonidos}.json`, `assets/img/emoji/` | `core/nivel0/nivel0.dart` | `test/nivel0_test.dart` |
| Prueba de ubicación inglés v2 | `assets/contenido/en/diagnostico-v2.json` (fuente en `plan-editorial/diagnostico/`) | `core/aprendizaje/ubicacion.dart` | `tools/contenido/validar_diagnostico.py`, `test/ubicacion*_test.dart` |
| Prueba de ubicación (otros idiomas, legado) | `assets/contenido/<idioma>/diagnostico.json` o lecciones | `core/diagnostico.dart` (con techo verificado, DEC-026) | `test/diagnostico_test.dart` |
| Prueba de cada nivel | ítems de evaluación de la propia ruta | `itemsPruebaNivel`, `nivelSuperado`, `nivelPorPruebas` en `dominio.dart` | `test/prueba_nivel_test.dart` |
| Situaciones (50) | `lib/core/content/catalog.dart` (lista), `assets/contenido/en/situaciones.json` y `situational_vocabulary.json`. Hay copias en `backend/src/content/` y `web/avatar/topics.json` | `core/content/situation_units.dart`, `backend/src/lib/situaciones.ts` | `backend/test/situaciones.test.ts` (fase C las unifica) |
| Lecturas y escuchas | `assets/contenido/en/{reading,listening}_units.json` | `core/content/learning_units.dart` | `test/lectura_escucha_test.dart` |
| Guías de gramática | `lib/core/content/grammar_guides.dart` | — | `test/guias_gramatica_test.dart` |
| Tutores y voz | `backend/src/lib/ia.ts` (personas), `backend/src/lib/voz.ts`, `web/avatar/roster.json` | `backend/src/routes/chat.ts` | `backend/test/*` |
| Progreso del alumno | `ProgressState.practicas` (claves en `ClaveRuta`) | `core/state/providers.dart` | estados calculados, nunca guardados (DEC-006) |

Claves de progreso: `ruta:<unidad>:<paso>:<item>`, `ruta:<unidad>:evaluacion`, `ruta:<unidad>:repaso`, `ruta:<idioma>.<nivel>:completa`, `ruta:<idioma>.<nivel>:prueba`, `nivel0:en:<leccion>`.

## 4. Legado congelado (no ampliar)

| Pieza | Por qué sigue | Se retira en |
|---|---|---|
| `lesson/lesson_player_screen.dart`, `course/level_screen.dart`, `exam/*`, `core/content/curriculum.dart`, `assets/contenido/<idioma>/nivel-N.json` | Cursos de los idiomas sin ruta 10×100 (francés, alemán…) | fase E, idioma por idioma |
| `onboarding/diagnostico_screen.dart` + `core/diagnostico.dart` | Ubicación de los idiomas sin prueba v2 | cuando cada idioma tenga su banco v2 |
| `core/biblioteca.dart` (`RutaBiblioteca.prioridades`) | Resumen del alumno para la IA (chat, llamada) | fase D (léxico y perfil únicos) |
| `situations/situation_screen.dart` | Pantalla actual de situaciones | fase C (situaciones por tramo) |

**Retirado en A** (no recrear; lo comprueba `test/arquitectura_test.dart`): `library/library_screen.dart`, `shared/widgets/learning_path.dart`, `shared/widgets/learning_primer.dart`, `foundations/foundations_screen.dart`, `core/content/foundations.dart`.

## 5. Reglas de interfaz

- **Acción principal:** `BotonPrincipal` (`shared/widgets/primary_button.dart`) **fijo abajo**: `Column[Expanded(contenido desplazable), pie con BotonPrincipal]`. Nunca dentro del `ListView`. Para ítems de la ruta, `ItemView(botonFijo: true)`.
- **Opciones de respuesta:** `OpcionRespuesta` (`ruta/opcion_respuesta.dart`). No crear `_Opcion` propias.
- **Feedback:** `FeedbackDock` / `AnswerFeedback` (`shared/widgets/feedback_experience.dart`) y `Efectos.correcto()/incorrecto()`.
- **Base:** `Tarjeta`, `Movil`, `Etiqueta`, `BarraProgreso` y colores `OL.*` (`app/theme.dart`). El tema también estiliza `FilledButton`, pero en pantallas nuevas se usa `BotonPrincipal`.
- **Personajes:** nunca dos a la vez. Sin rebotes ni movimientos raros. Sin Lumo en las pruebas de nivel. Nara es otra mascota.
- **Textos:** español neutro (tú), sin jerga interna. Prohibido: «nivel interno», «orientativo», «evidencia», «no certifica», «comprobación guiada», «banco piloto». El nivel se muestra como «Nivel N · A2»; nunca se pide.
- **Imágenes:** no se generan. Se buscan con licencia de uso comercial y se registran sus créditos.

## 6. Hoja de ruta (acordada 2026-10-01)

| Fase | Contenido | Estado |
|---|---|---|
| A | Limpieza visual y de legado; reglas vigiladas por prueba | **hecha** |
| B | Ubicación a prueba de azar y prueba para subir de nivel | **hecha** (DEC-026) |
| C | Situaciones v2: las mismas 50 en 3 tramos (Básico N1–3, Intermedio N4–6, Avanzado N7–10) con sus palabras, frases y objetivos; progreso y completada; prueba con final y nota; abrir la videollamada con el tema; una sola fuente de la lista | pendiente |
| D | Léxico único (id, nivel, situaciones, clases) + «Mis palabras» con repaso por palabra; «Mis verbos» con tablas y audio | pendiente |
| E | Francés sobre esta base: Fundamentos de lectura con el motor del Nivel 0, situaciones por tramo, léxico único (`PLAN_FRANCES.md`) | pendiente |

## 7. Validar antes de entregar

```bash
python3 tools/validar_ruta.py
~/flutter/bin/flutter analyze lib test
~/flutter/bin/flutter test
cd backend && npx tsx --test test/*.test.ts
```

Para desplegar: `docs/DEPLOYMENT_RUNBOOK.md` y registro en `docs/claude-educacion/DESPLIEGUES.md`.
