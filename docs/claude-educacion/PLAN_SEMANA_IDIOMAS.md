# Plan de la semana: versión esencial de it, ru, ko, ja y zh (desde el 06-10-2026)

Decisión del dueño (06-10): publicar cada idioma por separado en cuanto su versión esencial esté lista, y escalar la semana siguiente sin rehacer nada.

| Idioma | Esta semana | Siguiente semana (refuerzo) |
|---|---|---|
| it | Nivel 0 rehecho, f0, voces, N1–N4 esencial (200 clases) | N5–N10 + práctica independiente en N1–N4 |
| ru, ko, ja, zh | ficha del idioma, Nivel 0 de escritura, f0, mapa N1–N10, voces, N1–N2 esencial (100 clases) | N3–N10 + refuerzo |

## Reglas para no rehacer nada después
1. **Mapa de claves de los 10 niveles ya ahora:** los niveles nuevos se añaden detrás sin tocar lo publicado.
2. **Versión esencial = menos ítems, mismo rigor.** Mismos validadores que el alemán y `vocabularioEstricto: true` en todos los niveles; no se relaja ninguna regla que haya que reactivar después.
3. **El refuerzo solo añade:**
   - el paso `practica_independiente`, que la versión esencial no lleva;
   - tablas extra;
   - el resto de niveles.

   No reescribe ítems existentes.
4. **Nivel 0 y Fundamentos (f0) van completos y con calidad final en todos los idiomas.**
5. **El contenido viejo** (`nivel-0/1/2.json`, `ruta/a1-1.json` y el `ruta/f0.json` antiguo) se retira. Mientras un idioma no tiene ruta, la app muestra «En preparación».

## Clase esencial (`tools/ia/prompts/clase_autor_ligera.md`)

| Paso | Contenido |
|---|---|
| `explicacion` | 1 (más la de sonido o escritura en N1–N2) |
| `vocabulario` | todas las palabras de la ficha (6–12) |
| `ejemplos` | 4–5 |
| `tabla` | 0–1, más «Para leer» desde N3 |
| `practica_guiada` | 3 ítems, con pista |
| `situacion` | con la extensión que exige el validador por nivel + 1 pregunta |
| `evaluacion` | 4 ítems, ≥ 2 formatos |
| `erroresFrecuentes` | 1 |
| En toda la clase | ≥ 1 `escuchar`; `rom` en idiomas sin alfabeto latino |

## Producción
**Autores:** agentes de Claude que hacen de modelo en `tools/ia/openai_contenido.py --manual`. El programa deja cada encargo en `tools/ia/registro/manual/pendientes/`; el agente escribe el JSON en `respuestas/`; el programa monta, valida y pide reparación. No se usa la API de OpenAI.

```
openai_contenido.py mapa    XX N        --manual          # 10 niveles
openai_contenido.py outline XX N        --manual          # N1–N4 (it) / N1–N2 (resto)
openai_contenido.py plan    XX N                          # plan = esqueleto (sin fichas de ejercicios)
openai_contenido.py clases  XX N B      --manual --ligera
```

**Calidad:**
- `validar_bloque.py` + `chequeos.py` dan 0 errores por bloque.
- Claude revisa una muestra de 1 bloque por nivel e idioma.
- Antes de publicar: `integrar.py`, `validar_ruta.py`, `flutter test`.
- Despliegue por idioma, con autorización.

## Pendientes antes de las clases de ru, ko, ja y zh (06-10)
1. **Una sola convención de `rom` en los ítems.** HECHO (07-10): [ROMANIZACION.md](ROMANIZACION.md). Los 4 f0, los 4 Nivel 0, los validadores, `esquemas.py` (solo ru, ko, ja y zh) y la app la siguen.
2. **App y Nivel 0:**
   - añadir ru, ko, ja y zh a `idiomasConNivel0` (`lib/core/nivel0/nivel0.dart`) (zh, ja y ru: HECHO 07-10, con su f0 y N1–N2 integrados);
   - leer `rom` en `Palabra.fromJson` y en los pasos: HECHO (07-10);
   - que `escucha_letra` use la voz del idioma: HECHO (usa `Nivel0.idioma`).
3. **Revisión de muestras:**
   - f0 de ru, ko, ja y zh: revisar el «simnyuk» de 십육 en ko;
   - el teléfono de 9 cifras en el f0 de ja.
4. **Nombres repetidos entre clases del mismo bloque** (it N1: Paolo, Marco, Giulia…). El validador no lo marca; es menor.
