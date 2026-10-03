# Plan del español para anglohablantes

Actualizado: 2026-10-03 · DEC-034. Mismo método que el francés (`PLAN_FRANCES.md`, `PLAN_CLASES.md`): ninguna clase se escribe fuera de su ficha.

## 1. Decisiones (2026-10-03)

| Tema | Decisión |
|---|---|
| Variedad | Español latinoamericano neutro: ustedes, tú entre jóvenes y amigos, usted con mayores y en trámites. Notas breves de España desde B1, solo de reconocimiento (vosotros, perfecto de hoy, leísmo, distinción z/s). |
| Apoyo | Inglés americano (`idiomasApoyo: ["en"]`): consignas, explicaciones, pistas y feedback en `{"en": …}`. |
| Historia | Emma García, estadounidense de Chicago, llega a Quito en septiembre de 2026 y vive con la familia Andrade. Reparto y cronología: `curriculo/es/MAPA.md`. |
| Contenido existente | Se conserva Fundamentos (`es/ruta/f0.json`, 8 unidades) y se retira `a1-1` cuando se publique N1. |
| Modelos | Fichas con Sonnet; piloto en N1: un bloque con autor Sonnet medio y otro con autor alto, mismo revisor; se fija el modelo según las correcciones. |

## 2. Fuentes

- `curriculo/es/MAPA.md`: reglas del idioma, reparto, cronología y **las claves que introduce cada bloque** (478, sin repetir). `validar_plan.py` y `validar_parte.py` lo hacen cumplir.
- `curriculo/es/nX.json`: las 50 fichas de cada nivel con su plan de ejercicios.
- `docs/claude-educacion/ENCARGO_RUTA_ES.md`: el encargo para los autores de clases.
- Exámenes de referencia: DELE A1–C1 (y SIELE).

## 3. Hoja de ruta

| Paso | Qué | Estado |
|---|---|---|
| ES-1 | Voces nativas latinoamericanas (narradora y narrador) en `NATIVAS.es` de `backend/src/lib/voz.ts`; hoy el español usa las voces por defecto | pendiente (deploy de backend: requiere autorización) |
| ES-2 | Fundamentos: revisión. Hecho el 03-10: Emma es de Estados Unidos (no de Canadá) y el jefe de la unidad 4 es el señor Torres (no García, el apellido de Emma) | revisión parcial |
| ES-3 | Nivel 0 corto «Leer y pronunciar» (5 unidades: vocales, letras que cambian para un anglohablante —h, j/g, ll/y, ñ, r/rr, c/z/qu, b/v, d—, acento y tilde, diptongos, prueba). La ortografía española es transparente: basta una versión corta | propuesta |
| ES-4 | Las 50 situaciones × 3 tramos en español (`assets/contenido/es/situaciones.json`) | pendiente |
| ES-5 | «Mis verbos» en español (`verbos-es.json`, unos 120 verbos con 6 personas y los tiempos de A1–B2) | pendiente |
| ES-6 | Plan N1–N10: 500 fichas con plan de ejercicios, revisión del plan y página para aprobar | aprobado el 03-10 (10 GO, `revision-nX.md`); cronología N9–N10 fijada en `MAPA.md` |
| ES-7 | N1 (A1): piloto de modelos en B1 (Sonnet 21 correcciones vs Haiku 53 → autor Sonnet), después B2–B10 en paralelo con revisión GO; se retira `a1-1` | **hecho** el 03-10 (50 clases, 10 GO, integrado; falta deploy) |
| ES-8 | Prueba de ubicación v2 en español (banco por nivel) | después |
| ES-9 | N2–N10 con el mismo flujo (10 autores Sonnet en paralelo, revisor por bloque, integrar) | N2–N7 **hechos** el 03-10 (integrados; falta deploy); N8 en autoría |

**Validador (hecho el 03-10):** `curso.json` del español lleva `vocabularioEstricto` y `reglasAutoria`. Con esta última, `tools/validar_ruta.py` exige en las clases del plan (`es.nX.cNN`) lo que causó cerca del 30 % de las correcciones del francés: tablas de lectura de ≤ 15 filas y sin nombres propios ni celdas sueltas, opciones de comprensión en español desde N3, extensión de la lectura por nivel y apellidos del reparto bien usados.
