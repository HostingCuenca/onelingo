# Plan de clases: cómo se escala cada idioma

Actualizado: 2026-10-01 · DEC-034. **Ninguna clase se escribe si no está antes en el plan.** Un agente que redacta o revisa contenido trabaja solo con lo que su ficha de clase dice.

## 1. Tres capas

| Capa | Archivo | Qué fija | Quién lo cambia |
|---|---|---|---|
| Marco común | `curriculo/marco.json` | 10 niveles × 10 bloques, iguales para todos los idiomas: tema, objetivo (lo que el alumno puede hacer), funciones, campos de léxico y situaciones vinculadas | el coordinador, con una decisión en `DECISIONES.md` |
| Plan del idioma | `curriculo/<idioma>/nX.json` | las 50 clases de cada nivel: título, objetivo, gramática, puntos que introduce y recicla, vocabulario, sonido (N1), situación y tarea de evaluación | el coordinador; un revisor de plan da GO |
| Contenido | `tools/contenido/ruta-<idioma>/` (borrador) → `assets/contenido/<idioma>/ruta/` (publicado) | la clase completa en esquema 2 | autor y revisor por bloque |

`curriculo/` queda fuera de la app: no se empaqueta. Vista legible (generada, no se edita): `python3 tools/curriculo/ver_plan.py fr` → `docs/claude-educacion/plan/marco.md` y `plan/fr.md`.

La escala es la del cliente (`escala-cliente.json`): N1 = A1 completo, N2 = A2, N3–N4 = B1, N5–N7 = B2, N8–N10 = C1. El inglés conserva sus 100 clases por nivel; el marco rige el resto de idiomas (DEC-033), incluido el español para anglohablantes.

## 2. Ficha de clase (`curriculo/<idioma>/nX.json`)

```json
{
  "idioma": "fr", "nivel": 1, "cefr": "A1",
  "previos": ["claves ya vistas en Fundamentos f0"],
  "clases": [{
    "id": "fr.n1.c21", "bloque": 5,
    "titulo": {"es": "…", "en": "…"},
    "objetivo": {"es": "Pedir en un café…", "en": "Order at a café…"},
    "gramatica": ["je voudrais + sustantivo", "un / une en el pedido"],
    "introduce": ["je-voudrais"],
    "recicla": ["un-une-des", "numeros-0-20"],
    "vocabulario": {"campo": {"es": "El café", "en": "At the café"},
                     "palabras": ["un café", "un thé", "…6–12"]},
    "sonido": "é / er / ez",
    "situacion": 2,
    "tarea": {"es": "Pedir dos bebidas y preguntar el precio.", "en": "…"},
    "estado": "planificado"
  }]
}
```

Además, toda ficha `planificado` lleva su **plan de ejercicios**, para que el autor sepa exactamente qué escribir:

```json
"ejercicios": {
  "guiada":        [{"formato": "completar", "clave": "subjonctif-present",
                     "consigna": "Completa con el subjuntivo de venir.",
                     "ejemplo": "Il faut que tu ___ demain. → viennes"}],
  "independiente": [/* 3–4 */],
  "situacion":     {"texto": "Qué pasa, quién habla y en qué formato (diálogo, correo, anuncio)",
                    "preguntas": [/* 1–2 */]},
  "evaluacion":    [/* 4–8, ≥ 3 formatos; evalúa cada punto de introduce y responde a la tarea */]
}
```

- `formato`: elegir, escuchar, ordenar, completar, escribir o relacionar.
- `clave`: el punto que trabaja, de `introduce` o `recicla` de la ficha.
- `consigna` (en español) y `ejemplo`: el ítem tal como se verá, con la respuesta tras «→».
- El autor escribe esos ejercicios; puede pulir la redacción, no cambiar formato, clave ni lo que se evalúa.

Reglas (las comprueba `python3 tools/curriculo/validar_plan.py <idioma>`):
- 50 clases por nivel, 5 por bloque, alineadas con el bloque del marco.
- `introduce`: cada punto se introduce **una sola vez** en todo el idioma. Lo que vuelve a aparecer va en `recicla`, y solo puede reciclarse lo introducido antes. Así dos bloques no enseñan lo mismo (lo que pasó con la edad en B3 y B4).
- Toda clase de un bloque temático introduce algo; el bloque 10 de cada nivel integra y prepara la prueba del nivel.
- N1: cada clase abre con un sonido del Nivel 0.
- Situación: un id del catálogo (1–50), preferiblemente uno de los del bloque en el marco.
- Estado: `planificado` → `escrito` (borrador validado) → `revisado` (GO) → `publicado`. El validador comprueba que la unidad exista cuando el estado lo exige.

## 3. Ciclo de un bloque

1. **Ficha.** El coordinador comprueba que las 5 fichas del bloque están en el plan con GO.
2. **Autor.** Recibe las 5 fichas y `ENCARGO_RUTA_FR.md` (o el encargo del idioma). Escribe exactamente lo que dicen: no introduce gramática que no esté en `introduce` ni en lo ya visto.
3. **Validación.** `validar_ruta.py <idioma> --borrador …` con 0 errores.
4. **Revisor.** Otro agente contrasta el bloque con sus fichas y con las notas de calibración del encargo y deja `revision-bXX.md` con GO.
5. **Reparto.** El revisor lista los «Hechos del reparto confirmados» (`- es / en`); `python3 tools/curriculo/reparto.py <idioma> <nivel>` los copia al plan para el bloque siguiente.
6. **Integración y publicación.** `integrar.py`, suite completa, prueba en el navegador (interfaz es y en), despliegue por tandas y estados del plan en `publicado`.

Los bloques se escriben **en orden**. Dos autores en paralelo solo si sus fichas ya están cerradas, porque cada autor necesita saber qué vocabulario y qué gramática existen antes de su bloque.

## 4. Nuevo idioma

1. Copiar el marco: no cambia.
2. Plan del idioma N1 y N2 con fichas completas; N3–N10 con fichas completas antes de empezar ese nivel.
3. Revisor de plan: progresión de la gramática propia del idioma, examen oficial de referencia (`CURRICULO-IDIOMAS.md`) y que nada se introduzca dos veces.
4. Seguir `PLAN_PRODUCCION.md` §3 (voces, Nivel 0, situaciones, verbos, N1…).
