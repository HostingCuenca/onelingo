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

## Español: `verbos-es.json` (curso para anglohablantes)

Como el francés, con tablas explícitas, pero el apoyo es **solo inglés** y el participio va aparte:

```json
{"infinitivo": "ir", "traduccion": {"en": "to go"}, "tipo": "irregular", "nivel": 1, "participio": "ido",
 "tablas": {
   "presente":    ["voy", "vas", "va", "vamos", "van", "van"],
   "preterito":   ["fui", "fuiste", "fue", "fuimos", "fueron", "fueron"],
   "imperfecto":  ["iba", "ibas", "iba", "íbamos", "iban", "iban"],
   "futuro":      ["iré", "irás", "irá", "iremos", "irán", "irán"],
   "condicional": ["iría", "irías", "iría", "iríamos", "irían", "irían"],
   "perfecto":    ["he ido", "has ido", "ha ido", "hemos ido", "han ido", "han ido"],
   "subjuntivo":  ["vaya", "vayas", "vaya", "vayamos", "vayan", "vayan"]
 },
 "ejemplo": {"meta": "Voy al mercado los sábados.", "traduccion": {"en": "I go to the market on Saturdays."}}}
```

- **Personas, en orden:** yo, tú, él/ella/usted, nosotros/nosotras, ustedes, ellos/ellas (sin vosotros: la quinta persona es «ustedes» y coincide con la sexta). La forma va sin pronombre; los reflexivos llevan el pronombre en la forma («me levanto», «te levantas», «se levanta», «nos levantamos», «se levantan», «se levantan»; «me he levantado»).
- **Tipo:** `regular` solo si las siete tablas siguen el modelo -ar/-er/-ir sin cambios de raíz ni de ortografía; los de cambio vocálico (pensar, poder, pedir), ortográficos (buscar, llegar, coger) e irregulares son `irregular`. `reflexivo` no es tipo: lo marca el infinitivo en -se.
