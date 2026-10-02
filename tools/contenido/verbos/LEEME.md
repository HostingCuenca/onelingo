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

## Francés: `verbos-fr.json` (y otros idiomas nuevos)

Cada verbo trae explícitas sus **tablas**, sin deducirlas:

```json
{"infinitivo": "aller", "traduccion": {"es": "ir", "en": "to go"}, "tipo": "irregular", "nivel": 1,
 "tablas": {
   "presente":      ["vais", "vas", "va", "allons", "allez", "vont"],
   "passe_compose": ["suis allé(e)", "es allé(e)", "est allé(e)", "sommes allé(e)s", "êtes allé(e)(s)", "sont allé(e)s"],
   "imperfecto":    ["allais", "allais", "allait", "allions", "alliez", "allaient"],
   "futur_proche":  ["vais aller", "vas aller", "va aller", "allons aller", "allez aller", "vont aller"],
   "futuro":        ["irai", "iras", "ira", "irons", "irez", "iront"]
 },
 "ejemplo": {"meta": "Je vais au marché.", "traduccion": {"es": "Voy al mercado.", "en": "I'm going to the market."}}}
```

- **Personas, en orden:** je, tu, il/elle/on, nous, vous, ils/elles. La forma va sin pronombre; la app escribe j’ ante vocal o h muda.
- **Tipo:** `regular` solo para los -er regulares y los -ir del tipo finir; los demás son `irregular`.
