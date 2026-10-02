# Verbos (fuente de «Mis verbos»)

`verbos-<idioma>.json` es la **fuente** escrita a mano y revisada. `generar_verbos.py` la expande a `assets/contenido/<idioma>/verbos.json`, con las tablas de conjugación. No se edita el generado.

## Inglés: `verbos-en.json`

Lista de objetos:

```json
{"infinitivo": "go", "es": "ir", "tipo": "irregular",
 "tercera": "goes", "pasado": "went", "participio": "gone", "gerundio": "going",
 "ejemplo": {"en": "I go to work by bus.", "es": "Voy al trabajo en autobús."}}
```

- **Variedad:** inglés general americano (gotten, learned, burned, dreamed).
- **Tipo:** `regular` (pasado = participio = -ed) o `irregular`.
- **Formas:** las cinco formas se escriben explícitas (no se deducen): la tercera persona (goes, watches, studies, has) y el gerundio (making, running, lying).
- **Ejemplo:** una frase natural y corta (≤ 10 palabras) que usa el verbo, con su traducción al español neutro.
- **Exclusiones:** sin verbos modales (can, must…) ni phrasal verbs.
- **Formas especiales:** `be` y `have` llevan sus formas especiales en el generador.
