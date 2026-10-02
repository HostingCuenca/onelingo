# Plan de producción: francés y el resto de idiomas

Actualizado: 2026-10-01 · Responsable: Claude. **Este documento ordena todo lo que falta.** Las clases se escriben solo desde su ficha del plan (`PLAN_CLASES.md`, DEC-034). El detalle pedagógico del francés está en `PLAN_FRANCES.md` y la arquitectura en `docs/ARQUITECTURA_VIGENTE.md`.

## 0. Reglas que valen para todo

1. **50 clases por nivel** (10 bloques × 5) fuera del inglés (DEC-033).
2. **Contenido bilingüe desde que nace:** todo texto de apoyo `{es, en}` (DEC-032). Los validadores lo exigen.
3. **Una sola fuente por dato**, con copias generadas (situaciones, verbos, Nivel 0).
4. **Autor y revisor independientes:**
   - nada se integra sin `GO` del revisor y con 0 errores del validador;
   - los subagentes no usan git.
5. **Publicación:**
   - suite completa en verde, prueba en el navegador y despliegue con respaldo y rollback (`DESPLIEGUES.md`);
   - si cambian archivos del servidor, el reinicio de `onelingo-api` lo autoriza el cliente en cada despliegue.
6. **Versión inicial:** marca todo idioma sin revisión de una persona nativa (`curso.revision = "inicial"`).

## 1. Francés: estado y lo que falta

| Fase | Entregable | Estado | Criterio de terminado |
|---|---|---|---|
| FR-1 | Nivel 0 · Leer y pronunciar (F1–F10, 40 lecciones) | ✅ edu-31 | — |
| FR-2 | Fundamentos f0 (8 unidades) + Primeras frases a1-1 (9), con inglés | ✅ edu-31 | — |
| FR-3 | Mis verbos: 120 verbos, 5 tiempos × 6 personas | ✅ hecho (revisión GO: 3.000 formas cotejadas) | — |
| FR-4 | 50 situaciones × 3 tramos | ✅ hecho (5 revisiones GO); se publica con reinicio de la API | — |
| FR-5a | Plan de clases: marco común (`curriculo/marco.json`) y fichas del francés N1–N10 (`curriculo/fr/nX.json`) | en curso | `validar_plan.py fr` sin errores y revisión del plan con GO; N1–N2 antes de seguir con B5 |
| FR-5b | App: niveles de la ruta para cualquier idioma (`idiomasConRuta`) | ✅ hecho para el francés | Aprender muestra Nivel 0 → Fundamentos → N1… (superado / en curso / bloqueado) y prueba del nivel en francés; las lecciones antiguas se retiran del francés |
| FR-5c | N1: 50 clases en esquema 2 (`fr/ruta/n1-bXX.json`) | en curso: B1 con GO; B2–B4 escritos y en revisión; B5–B10 esperan sus fichas; integrador `tools/contenido/ruta-fr/integrar.py` | 10 bloques con GO y `validar_ruta.py fr` sin errores; se publica por tandas (B1–B3, B4–B6, B7–B10) |
| FR-6 | Prueba de ubicación v2 en francés | pendiente | `UbicacionScreen` por idioma; banco con 18 ítems por nivel publicado (N1 y luego N2); simulación de respuestas al azar → «desde cero» |
| FR-7 | N2 (A2): 50 clases | después de FR-5 | igual que FR-5c |
| FR-8 | N3–N10 | según demanda | — |
| FR-R | Revisión nativa | cuando haya revisor | lista por partes: Nivel 0 → situaciones → N1 |

**Orden de trabajo:**
1. Cerrar FR-3 y FR-4 y publicarlos.
2. FR-5b, el cambio en la app, que destraba la ruta francesa.
3. FR-5a: plan de clases completo (marco y fichas N1–N10).
4. FR-5c por bloques, en orden y desde las fichas, con FR-6 en paralelo cuando haya 3 bloques publicados.
5. FR-7 y siguientes, desde sus fichas.

## 2. Mapa de N1 francés (A1 completo, 50 clases)

Cada clase sigue la anatomía de `PLAN_FRANCES.md` §3.5 en esquema 2:
- explicación, ejemplos y vocabulario (6–10);
- patrón o tabla;
- práctica guiada (3–5) e independiente (3–4);
- situación con diálogo;
- evaluación (≥ 4 ítems, ≥ 2 formatos).

Cada clase recicla al menos un 30 % del vocabulario anterior y empieza recordando un sonido del Nivel 0.

| Bloque | Clases | Tema | Gramática y sonido | Números y verbos |
|---|---|---|---|---|
| B1 | 1–5 | Saludar y presentarse | tu/vous, je m'appelle, ça va, el alfabeto y deletrear, nacionalidades (el femenino hace sonar la consonante) | être |
| B2 | 6–10 | Hablar de mí | pronombres sujeto (on), -er en presente (4 formas que suenan igual), aimer + artículo | parler, habiter, aimer, travailler |
| B3 | 11–15 | Personas y cosas | un/une, le/la/les, el plural se oye en el artículo (les‿amis), avoir, edad, familia, posesivos | 0–20 · avoir |
| B4 | 16–20 | Preguntar y negar | ne…pas, pas de, c'est / il est, qui est-ce / qu'est-ce que c'est, il y a, est-ce que, interrogativos, quel(le) | 21–69 · teléfono |
| B5 | 21–25 | Café y compras | je voudrais, partitivo como frase hecha, precios en euros, colores y ropa, ce/cet/cette/ces | 70–99 |
| B6 | 26–30 | Gustos y rutina | aimer/préférer + infinitivo, faire du / jouer à, días, la hora, verbos pronominales (se lever) | faire, la hora |
| B7 | 31–35 | Describir y ubicarse | adjetivos (concordancia y posición), la ciudad, aller/venir + au/du, ciudades y países | aller, venir |
| B8 | 36–40 | Verbos frecuentes y comida | prendre, vouloir, pouvoir, devoir, finir; cantidades, beaucoup de, il faut | 100–1.000 · ordinales |
| B9 | 41–45 | Moverse y planes | indicaciones, imperativo, preposiciones de lugar, futur proche, venir de, invitar, aceptar y rechazar | — |
| B10 | 46–50 | Mi fin de semana y cierre | passé composé (introducción, avoir/être), jamais, depuis / il y a; repaso y evaluación tipo DELF A1 + proyecto «Ma vie en français» | — |

Las 9 unidades de `a1-1` (Primeras frases) se reutilizan como material de B1–B3. Cuando N1 esté publicado, el módulo `fr.a1-1` sale de `curso.json`; el archivo se conserva por trazabilidad.

### Autoría de N1 (por bloque)

1. El autor escribe `assets/contenido/fr/ruta/n1-bXX.json`: 5 unidades `fr.n1.c01…`, `nivelInterno: 1`, prerrequisito en cadena y textos de apoyo `{es, en}`.
2. Lo valida con `python3 tools/validar_ruta.py fr`.
3. Un revisor distinto (francés de Francia, inglés y español) deja `revision-bXX.md` con GO.
4. El coordinador registra el módulo en `curso.json` y publica por tanda.
5. Cada tanda trae la suite en verde y una prueba en el navegador con la interfaz en español y en inglés.

## 3. Resto de idiomas: misma plantilla, un idioma cada vez

**Orden sugerido:**
1. **Portugués e italiano:** latinos, la lectura se parece al español y son rápidos.
2. **Alemán.**
3. **Japonés, chino, coreano y ruso:** escrituras propias; su Fundamentos f0 ya enseña la escritura.
4. **Español para anglohablantes:** el curso es ya existe con apoyo en inglés, así que primero se revisa y amplía.

**Plantilla por idioma:**

| Paso | Qué | Reutiliza |
|---|---|---|
| 1 | Voces nativas (narradora y narrador) en `NATIVAS` de `voz.ts` | probar las voces con el script |
| 2 | Nivel 0 de lectura: solo donde la ortografía lo exige (alemán sí; portugués e italiano, versión corta; escrituras no latinas: ya cubierto por f0) | motor del Nivel 0, `validar_nivel0.py --bilingue` |
| 3 | 50 situaciones × 3 tramos | esquema genérico, `validar_situaciones.py`, `integrar_lotes.py <idioma>` |
| 4 | Verbos (tablas propias) | `generar_verbos.py` (añadir personas y tiempos del idioma en `IDIOMAS`) |
| 5 | N1 de 50 clases (mapa → bloques → GO) | esquema 2, `validar_ruta.py` |
| 6 | Ubicación v2 | banco por nivel |
| 7 | N2… | — |

## 4. Piezas comunes todavía pendientes

| Pieza | Para qué | Cuándo |
|---|---|---|
| Ruta de niveles para cualquier idioma (FR-5b) | quitar el legado de lecciones fuera del inglés | ahora, con el francés |
| «Repite» dentro de las clases (micrófono + IA) | práctica oral en cada clase (plan §3.5) | con N1 francés |
| Lectura graduada por bloque | comprensión lectora | con N1 francés (mini lectura en la situación) |
| Prueba de ubicación v2 genérica (FR-6) | ubicar en cualquier idioma | en paralelo con N1 |
| Adaptar ejemplos al nativo (p. ej. «je parle anglais» para anglohablantes) | naturalidad | después; anotado |
