# Migración de foundations-v1 → ruta en.f0

Fecha: 2026-09-26 · Código: `lib/core/aprendizaje/migracion.dart` · Prueba: `test/ruta_dominio_test.dart` («Migración foundations-v1»).

## Qué había

Ruta `/fundamentos` con `FoundationsScreen` (solo inglés): 6 microlecciones con 2 comprobaciones guiadas cada una, 12 claves en `ProgressState.practicas`:
`foundation-v1-{i-you,i-am,you-are,he-she,feelings,introduce}-{0,1}` con `conApoyo: true` y `resueltaConApoyo`.

## Qué hay ahora

`/fundamentos` abre `RutaScreen` (10 idiomas). Inglés: 6 unidades `en.f0.*` que amplían lo anterior (saludos, 7 pronombres, am/is/are + contracciones, negación, preguntas con respuestas cortas, presentarse).

## Tabla de equivalencias (alias de lectura)

| Clave antigua | Cuenta como | Unidad nueva |
|---|---|---|
| `foundation-v1-i-you-0` | `ruta:en.f0.pronombres:p4:g1` (I) | Pronombres |
| `foundation-v1-i-you-1` | `ruta:en.f0.pronombres:p4:g2` (you) | Pronombres |
| `foundation-v1-he-she-0` | `ruta:en.f0.pronombres:p4:g3` (she) | Pronombres |
| `foundation-v1-i-am-0/1` | `ruta:en.f0.be-afirmativo:p6:g1` (I am) | To be afirmativo |
| `foundation-v1-you-are-0/1` | `ruta:en.f0.be-afirmativo:p6:g2` (you are) | To be afirmativo |
| `foundation-v1-he-she-1` | `ruta:en.f0.be-afirmativo:p6:g3` (is) | To be afirmativo |
| `foundation-v1-feelings-0/1` | `ruta:en.f0.be-afirmativo:p6:g4` (I am tired) | To be afirmativo |
| `foundation-v1-introduce-0/1` | `ruta:en.f0.presentarse:p4:g3` (ordenar) | Presentarte |

## Reglas

1. **Solo lectura**: `evidenciaDe()` busca la clave nueva y, si no existe, sus alias antiguos. No se escribe ni se borra nada → idempotente, sin paso de migración, compatible con clientes antiguos.
2. La evidencia antigua era guiada: aporta como máximo a **practicada**, nunca a aprobada ni dominada, y no concede XP otra vez.
3. Cobertura parcial honesta: v1 no enseñaba it/we/they, contracciones, negación ni preguntas. Un alumno de v1 conserva sus ejercicios resueltos pero debe completar los que faltan y aprobar la evaluación de cada unidad.
4. La primera unidad (`primer-contacto`) es nueva: el alumno de v1 la hace (es corta); no se omite automáticamente.
5. `FoundationsScreen` y `lib/core/content/foundations.dart` se conservan en el código (sin ruta) porque la migración y `test/foundations_test.dart` los usan. Retirar el widget es una decisión posterior.

## Otros idiomas

No tenían foundations-v1 (solo lecciones `L0-NNN` del nivel 0 antiguo). Esas lecciones siguen accesibles desde la ruta («Práctica extra: lecciones del Nivel 0») y completarlas todas sigue sacando al alumno del nivel 0 (compatibilidad), igual que aprobar la ruta nueva (`ruta:<idioma>.f0:completa`).

## Verificación

- Prueba unitaria: las 12 claves antiguas → ninguna unidad aprobada; todos los destinos existen en el contenido real y son práctica guiada; claves antiguas intactas.
- `ProgressState.toJson/fromJson` conserva las claves `ruta:*` (viven en `practicas`, que las versiones antiguas no alteran).
