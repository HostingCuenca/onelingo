# OneLingo: arquitectura vigente

Actualizado: 2026-10-03 (portugués reiniciado; planificación de Nivel 0 y Fundamentos; DEC-035).

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
| Biblioteca (desde Inicio) | Mis palabras (repaso espaciado por palabra), Mis verbos (tablas, audio, práctica), Lecturas, Escuchas, Guías de gramática, Mapa de sonidos | `library/biblioteca_screen.dart`, `lexico/*`, `library/learning_unit_screen.dart`, `library/grammar_screen.dart` |
| Perfil | progreso, errores, planes | `progress/*`, `mistakes/*`, `plans/plans_screen.dart` |
| Entrada | bienvenida, registro, prueba de ubicación | `onboarding/*` (`ubicacion_screen.dart` v2 para idiomas con ruta y banco: inglés, francés; `diagnostico_screen.dart` resto) |

## 3. Fuentes canónicas

| Dominio | Fuente | Lógica | Validación |
|---|---|---|---|
| Curso por niveles (ruta, esquema 2) | `assets/contenido/<idioma>/ruta/curso.json` + módulos (`f0.json`, `nN-editorial.json`) | `lib/core/aprendizaje/` (`modelos`, `dominio`, `providers`) | `python3 tools/validar_ruta.py`, `test/ruta_*` |
| Ejercicios de las clases editoriales | `assets/contenido/en/exercise-library.json` + activación | `core/aprendizaje/biblioteca_adaptador.dart` | herramientas en `tools/contenido/` |
| Nivel 0 (leer y pronunciar), activo por idioma: en, fr | `assets/contenido/<idioma>/nivel0/{nivel0,sonidos}.json` (textos de interfaz en `textos`), `assets/img/emoji/` (Noto, `tools/contenido/descargar_emoji.py`). Francés: borradores revisados en `tools/contenido/nivel0-fr/` → `integrar.py`. Portugués está solo en staging editorial: `tools/contenido/nivel0-pt/borrador/`; no está activo ni habilitado en el runtime. | `core/nivel0/nivel0.dart` (`idiomasConNivel0`) | `tools/contenido/validar_nivel0.py <idioma>`, `test/nivel0_test.dart` |
| Fundamentos portugués en staging | Plan canónico: `curriculo/pt/f0.json` (8 fichas, 24 claves). Borrador ejecutable: `tools/contenido/ruta-pt/borrador-f0.json` (8 unidades, 102 vocablos, 104 ejercicios). Ninguno está activo. | El borrador se escribió desde las fichas sin recuperar el legado; F6 bloquea publicación hasta producir/revisar el audio A→B | `python3 tools/curriculo/validar_fundamentos.py pt`, `python3 tools/contenido/ruta-pt/validar.py` |
| Prueba de ubicación v2 (inglés; francés y demás idiomas con ruta según tengan banco) | `assets/contenido/<idioma>/diagnostico-v2.json` (fuente en `<idioma>/plan-editorial/diagnostico/`) | `core/aprendizaje/ubicacion.dart`, `bancoUbicacionProvider`; tope en el último nivel publicado (`nivelUbicacionRuta`) | `tools/contenido/validar_diagnostico.py [--idioma fr]`, `test/ubicacion*_test.dart` |
| Prueba de ubicación (otros idiomas, legado) | `assets/contenido/<idioma>/diagnostico.json` o lecciones | `core/diagnostico.dart` (con techo verificado, DEC-026) | `test/diagnostico_test.dart` |
| Prueba de cada nivel | ítems de evaluación de la propia ruta | `itemsPruebaNivel`, `nivelSuperado`, `nivelPorPruebas` en `dominio.dart` | `test/prueba_nivel_test.dart` |
| Situaciones (50 × 3 tramos) | `assets/contenido/situaciones/catalogo.json` (lista) + `assets/contenido/<idioma>/situaciones.json` (contenido por tramo). **Generados, no editar:** `lib/core/content/catalogo_situaciones.g.dart`, `web/avatar/topics.json`, `backend/src/content/situaciones-<idioma>.json` | `core/content/situaciones.dart`, `backend/src/lib/situaciones.ts` | `tools/contenido/validar_situaciones.py`, `generar_situaciones.py --comprobar`, `test/situaciones_v2_test.dart`, `backend/test/situaciones.test.ts` |
| Léxico único (índice) | No es otra fuente: se calcula desde la ruta (pasos de vocabulario), las situaciones y el Nivel 0 | `core/lexico/lexico.dart` (`lexicoProvider`, `misPalabrasProvider`, repaso por palabra en `practicas['lexico:<idioma>']`) | `test/lexico_test.dart` |
| Verbos («Mis verbos») | `tools/contenido/verbos/verbos-<idioma>.json` (revisada). **Generado:** `assets/contenido/<idioma>/verbos.json`, con tablas y nivel tomado de la ruta | `core/lexico/verbos.dart`; `tools/contenido/verbos/generar_verbos.py` | `generar_verbos.py --comprobar`, `test/lexico_test.dart` |
| Lecturas y escuchas | `assets/contenido/en/{reading,listening}_units.json` | `core/content/learning_units.dart` | `test/lectura_escucha_test.dart` |
| Guías de gramática | `lib/core/content/grammar_guides.dart` | — | `test/guias_gramatica_test.dart` |
| Voces nativas por idioma | `NATIVAS` en `backend/src/lib/voz.ts` (fr: Hélène narra, Nicolas dialoga) | `rolDeVoz` | `backend/test/voz-idioma.test.ts` |
| Tutores y voz | `backend/src/lib/ia.ts` (personas), `backend/src/lib/voz.ts`, `web/avatar/roster.json` | `backend/src/routes/chat.ts` | `backend/test/*` |
| Progreso del alumno | `ProgressState.practicas` (claves en `ClaveRuta`) | `core/state/providers.dart` | estados calculados, nunca guardados (DEC-006) |

Claves de progreso: `ruta:<unidad>:<paso>:<item>`, `ruta:<unidad>:evaluacion`, `ruta:<unidad>:repaso`, `ruta:<idioma>.<nivel>:completa`, `ruta:<idioma>.<nivel>:prueba`, `nivel0:<idioma>:<leccion>`, `situacion:<idioma>:<id>:<tramo>:prueba`, `situacion-<idioma>-<id>-<objetivoId>`, `lexico:<idioma>` (`{palabras: {clave: [caja, fecha]}}`), `verbo:<idioma>:<id>`.

Nivel del alumno para todo lo que no es la ruta (situaciones, biblioteca): `nivelAlumnoProvider` (ubicación o siguiente al último nivel superado).

## 4. Legado congelado (no ampliar)

| Pieza | Por qué sigue | Se retira en |
|---|---|---|
| `lesson/lesson_player_screen.dart`, `course/level_screen.dart`, `exam/*`, `core/content/curriculum.dart`, `assets/contenido/<idioma>/nivel-N.json` | Cursos de los idiomas sin ruta 10×100 (francés, alemán…) | fase E, idioma por idioma |
| `onboarding/diagnostico_screen.dart` + `core/diagnostico.dart` | Ubicación de los idiomas sin prueba v2 | cuando cada idioma tenga su banco v2 |
| `core/biblioteca.dart` (`RutaBiblioteca.prioridades`) | Resumen del alumno para la IA (chat, llamada) | cuando el perfil del alumno se unifique |

**Retirado en A** (no recrear; lo comprueba `test/arquitectura_test.dart`): `library/library_screen.dart`, `shared/widgets/learning_path.dart`, `shared/widgets/learning_primer.dart`, `foundations/foundations_screen.dart`, `core/content/foundations.dart`.

## 5. Reglas de interfaz

- **Acción principal:** `BotonPrincipal` (`shared/widgets/primary_button.dart`) **fijo abajo**: `Column[Expanded(contenido desplazable), pie con BotonPrincipal]`. Nunca dentro del `ListView`. Para ítems de la ruta, `ItemView(botonFijo: true)`.
- **Opciones de respuesta:** `OpcionRespuesta` (`ruta/opcion_respuesta.dart`). No crear `_Opcion` propias.
- **Feedback:** `FeedbackDock` / `AnswerFeedback` (`shared/widgets/feedback_experience.dart`) y `Efectos.correcto()/incorrecto()`.
- **Base:** `Tarjeta`, `Movil`, `Etiqueta`, `BarraProgreso` y colores `OL.*` (`app/theme.dart`). El tema también estiliza `FilledButton`, pero en pantallas nuevas se usa `BotonPrincipal`.
- **Personajes:** nunca dos a la vez. Sin rebotes ni movimientos raros. Sin Lumo en las pruebas de nivel. Nara es otra mascota.
- **Interfaz multilingüe (I18N.md):**
  - todo texto visible pasa por `tr('texto en español')` y su traducción va en `assets/i18n/<idioma>.json`;
  - los datos se muestran con `trDato`;
  - el contenido lleva su apoyo en el propio JSON (`TextoApoyo`), no `tr()`.
- **Textos:** español neutro (tú), sin jerga interna. Prohibido: «nivel interno», «orientativo», «evidencia», «no certifica», «comprobación guiada», «banco piloto». El nivel se muestra como «Nivel N · A2»; nunca se pide.
- **Imágenes:** no se generan. Se buscan con licencia de uso comercial y se registran sus créditos.

## 6. Hoja de ruta (acordada 2026-10-01)

| Fase | Contenido | Estado |
|---|---|---|
| A | Limpieza visual y de legado; reglas vigiladas por prueba | **hecha** |
| B | Ubicación a prueba de azar y prueba para subir de nivel | **hecha** (DEC-026) |
| C | Situaciones v2: las mismas 50 en 3 tramos (Básico N1–3, Intermedio N4–6, Avanzado N7–10), con progreso, prueba con nota y videollamada con el tema (`SITUACIONES_V2.md`) | **hecha** (DEC-028) |
| D | Léxico único + «Mis palabras» con repaso por palabra + «Mis verbos» con tablas, audio y práctica | **hecha** (DEC-029) |
| I1 | Interfaz en inglés y selector de idioma en Perfil (`I18N.md`) | **hecha** (DEC-031) |
| I2 | Contenido con apoyo en inglés para anglohablantes (francés primero) | pendiente |
| E | Francés sobre esta base (`PLAN_FRANCES.md`): voces nativas y Nivel 0 F1–F5 hechos; siguen F6–F10, situaciones y verbos en francés, y N1 | **en curso** (DEC-030) |
| P | Portugués pt-BR (`PLAN_PORTUGUES.md`): Nivel 0, Fundamentos, ruta N1–N10 (500 clases, bloques con GO) y prueba de ubicación v2 (180 ítems); `pt` en `idiomasConRuta` | **completo** (DEC-035, 06-10) |
| D | Alemán (`PLAN_ALEMAN.md`, método ligero sin historia): Nivel 0, Fundamentos (f0), ruta N1–N10 (500 clases, 100 bloques con GO), prueba de ubicación v2 (180 ítems) y «Mis verbos» (128); `de` en `idiomasConRuta`; módulo heredado `de.a1-1` retirado | **completo** (06-10) |

## 7. Validar antes de entregar

```bash
python3 tools/validar_ruta.py
~/flutter/bin/flutter analyze lib test
~/flutter/bin/flutter test
cd backend && npx tsx --test test/*.test.ts
```

Para desplegar: `docs/DEPLOYMENT_RUNBOOK.md` y registro en `docs/claude-educacion/DESPLIEGUES.md`.
