GO

# Revisión de los mapas de claves del italiano N1–N10 (06-10-2026)

Revisor: Claude. Verificación (`verificar.py` en el scratch): 49/48 claves por nivel, clases c01… en orden, 5 por bloque (bloque 10 = c46–c48 [+c49 en N1]), claves kebab-case, 0 duplicados en todo el curso ni con f0 (`previos` + `clavesSalida`), 0 `depende_de` sin resolver ni posteriores.

## Problemas generales encontrados

- **Dependencias rotas (≈190):** N2–N10 se generaron con una versión antigua de N1 y apuntaban a claves que ya no existen (`present-are-regular`, `tu-lei-register`, `ce-ci-sono`, `potere-present`…). Se remapearon a las claves del N1 final o de f0. N10 usaba ids de clase (`c01`) en vez de claves en `depende_de`.
- **Duplicados con N1 final:** presente en -ere/-ire (N2 c02), «fare» (N2 c03), «in» articulada (N2 c11), «quale/qual è» (N2 c34), partitivo (N2 c26).
- **Huecos del curso:** meses y fechas, ordinales, sapere/conoscere, pronombres tónicos, formas adjetivas de quello/bello, superlativo absoluto, piacere en pasado, imperativos irregulares (dimmi, fammi), avere fame/freddo, andare da + persona, futuro de suposición, ce l'ho, volerci, ci si, lasciare + infinito, adverbios en -mente, farcela/andarsene/cavarsela/prendersela, il cui, concordancia del participio con ne, combinados con ne (gliene), periodo hipotético coloquial (reconocimiento).
- **Duplicados entre niveles con otro nombre:** «in caso di» (N3 c17 / N4 c37), «a quanto pare» (N3 c41 / N5 c32), «da un lato… dall'altro» (N4 c47 / N5 c39), «non solo… ma anche» (N5 c38 / N6 c04), gerundio compuesto (N5 c46 / N9 c12).

## Cambios por nivel

### N1 (1)
- c20 depende_de: connectors-e-o-ma (ya no existe) → present-ere-ire-verbs

### N2 (22)
- c02 present-ere-ire-and-isc duplicaba N1 c19 → stare-gerundio-present
- c03 quitado «fare» (ya en N1 c26); ahora uscire, dire, bere, rimanere
- c05 depende_de incluye stare-gerundio-present
- c05 gramática integra stare+gerundio
- c06 + modales en passato prossimo
- c11 preposizioni-articolate-in-su → su-articulated-and-ordinals: «in» articulada duplicaba N1 c33; ahora «su» + ordinales
- c11 gramática nueva
- c14 + sapere/conoscere (faltaba)
- c16 weather-impersonals-and-seasons → dates-months-seasons-weather: faltaban meses y fechas en todo el curso
- c16 gramática nueva
- c18 + futuro de suposición
- c22 + superlativo absoluto -issimo e irregulares
- c23 + formas adjetivas de quello/bello (faltaban)
- c26 partitivo ya en N1 c22: se reformula como ampliación (un po' di, qualche) y se quita la referencia al francés
- c28 + piacere en passato prossimo y a me/a te
- c29 + imperativos irregulares y dimmi/fammi
- c34 quale-selection-and-travel-issues → succedere-and-travel-problems: «quale/qual è» duplicaba N1 c16
- c34 gramática nueva
- c36 + avere fame/freddo (calco frecuente)
- c38 + andare da + persona
- c41 + pronombres tónicos (faltaban)
- depende_de: 36 clases apuntaban a claves de la versión antigua de N1 o renombradas; remapeadas

### N3 (7)
- c02 + concordancia con ne
- c04 + ce l'ho
- c06 se centra en el pasado; el presente pasa a N2 c02
- c23 + volerci vs metterci
- c33 + ci si
- depende_de: 13 clases apuntaban a claves de la versión antigua de N1 o renombradas; remapeadas
- c34 + combinados con ne (gliene)

### N4 (8)
- c13 + lasciare + infinito
- c32 + formación de adverbios en -mente
- c33 indefinite-place-adverbs-for-outings → pronominal-verbs-farcela-andarsene: faltaban los verbos pronominales farcela/andarsene/cavarsela
- c33 gramática nueva
- c35 gramática integra farcela/andarsene
- c37 in-caso-di-and-salvo-imprevisti → salvo-imprevisti-and-contingency-instructions: «in caso di» ya en N3 c17
- c37 gramática
- depende_de: 16 clases apuntaban a claves de la versión antigua de N1 o renombradas; remapeadas

### N5 (4)
- c32 «a quanto pare» ya en N3 c41
- c39 «da un lato… dall'altro» ya en N4 c47
- c12 + relativo posesivo il cui
- depende_de: 5 clases apuntaban a claves de la versión antigua de N1 o renombradas; remapeadas

### N6 (3)
- c04 non-solo-ma-anche-and-sia-sia → correlatives-sia-sia-ne-ne: «non solo… ma anche» ya en N5 c38
- c04 gramática
- depende_de: 5 clases apuntaban a claves de la versión antigua de N1 o renombradas; remapeadas

### N7 (1)
- depende_de: 4 clases apuntaban a claves de la versión antigua de N1 o renombradas; remapeadas

### N8 (2)
- c01 + ipotetico colloquiale (reconocimiento)
- depende_de: 2 clases apuntaban a claves de la versión antigua de N1 o renombradas; remapeadas

### N9 (1)
- c12 gerundio compuesto ya presentado en N5 c46: aquí se recicla con valor causal

### N10 (1)
- depende_de: 37 clases usaban ids de clase (c01…) en vez de claves; convertidas

## Lista de control de gramática (dónde queda cada punto)

Artículos y lo/gli N1 c07 · preposiciones articuladas a/di N1 c22, in/da N1 c33, su N2 c11 · partitivo N1 c22, N2 c26 · ci locativo N2 c13 · ne partitivo N2 c24 · ci/ne preposicionales N3 c04 · directos N2 c14 · indirectos N2 c33, N2 c41 · tónicos N2 c41 · con infinitivo N2 c42 · combinados N3 c34 · reflexivos N1 c27, N2 c07, recíprocos N3 c12 · imperativo tu/Lei (fórmulas) N1 c42, con pronombres N2 c29, Lei N4 c27, dos clíticos N5 c42 · comparativos N2 c21, superlativos N2 c22, adverbios N4 c32 · relativos che/dove N2 c12, cui N3 c11, quello che/ciò che N3 c13, chi N4 c23, il quale/il cui N5 c12 · passato prossimo N1 c46–c47, participios N2 c06, concordancia con pronombres N3 c02 · imperfetto N2 c08–c09 · futuro N2 c17–c18, anteriore N5 c09/N6 c27 · condizionale N2 c39 (cortesía), N3 c16, passato N4 c08 · trapassato prossimo N3 c07 · congiuntivo presente N3 c26–c27, passato N4 c07, imperfetto N3 c18, trapassato N5 c06 · periodo hipotético I N2 c19, II N3 c19, III y mixto N5 c07–c08 · pasiva essere N3 c21, agente N4 c11, venire/andare N5 c04 · si passivante/impersonale N3 c32–c33, pasado N6 c09 · gerundio N3 c24, stare + gerundio N2 c02/N3 c06, stare per N4 c04 · infinito pasado N5 c01 · participio absoluto N5 c18, presente N6 c13 · passato remoto reconocimiento N5 c11, producción N8 c31 · trapassato remoto N7 c41/N10 c09 · discurso indirecto N2 c32, N3 b8, N4 c46, N5 b6 · fare/lasciare + infinito N4 c13, N5 c41 · farcela/andarsene N4 c33, metterci/volerci N3 c23 · conectores N2 c47, N3 c44/c46, N5 b8, N6 b10, N7 c26 · nominalización y registro N5 c03, N7 b1, N10 c21/c43.

## Sin resolver

- **Periodo hipotético II en N3 (B1, bloque 4) antes del congiuntivo presente (bloque 6):** se mantiene. El Profilo della lingua italiana sitúa «se + congiuntivo imperfetto» en B1, y el tema del bloque («Planes con condiciones») lo pide. N3 c18 enseña solo las formas que hacen falta en la hipótesis. Moverlo a N4–N5 obligaría a rehacer dos bloques. Si se prefiere el orden del encargo (II en B2), hay que replanificar N3 b4 y N4 b2.
- El congiuntivo presente queda en N3 (B1) y no en N4: ambos son B1 y N4 lo usa desde el bloque 2.
- Los textos de `gramatica` que no se tocaron conservan la redacción del modelo; algunos ejemplos se apoyan en léxico que el esqueleto (outline) tendrá que introducir.
