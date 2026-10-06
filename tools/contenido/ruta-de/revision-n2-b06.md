GO

# Revisión de N2 B6 (de.n2.c26–c30)

Validador: `python3 tools/curriculo/validar_bloque.py de 2 6` → 0 errores del bloque (tras las correcciones).

## Cambios por clase

- **c26 (Ein Tisch für vier Personen):** la situación pasa de 66 a 80 palabras (mínimo N2 = 60; con margen del 8 % son ≥ 65). Se añade el par «Kaffee mit/ohne Milch» (usa lo ya enseñado: ohne, Milch, Kaffee). Sin otros cambios: durch y gegen están en la ficha y se enseñan en la tabla antes de evaluarse; la guía de «ü» es correcta (vocal larga).
- **c27 (Mit Reis oder mit Kartoffeln?):**
  - «Hier ist die Karte» se quita de la situación: «Karte» ya se enseñó como tarjeta de pago, y aquí tendría un sentido nuevo («menú») sin enseñar. Se añade un cierre del cliente («Ja, danke. Das ist gut.»). Situación: 72 palabras.
  - Guía de «ß» (explicacion): se mantiene «s sorda» y se añade que la «o» de «Soße» es larga (sin reglas inventadas). Kartoffel, Tomate y Pizza se enseñan en `ejemplos` y `vocabulario` antes de usarse.
- **c28 (Frischer Fisch):**
  - Dos líneas seguidas del mismo hablante fundidas y reordenadas (la pregunta «¿qué desea tomar?» queda justo antes de la respuesta de Anna), más el par «Ist der Fisch salzig?». Situación: 78 palabras.
  - Brot, Kuchen y Milch se enseñan en `vocabulario` y `ejemplos` antes de la situación.
- **c29 (Zwiebeln klein schneiden):**
  - «Rezept» era un hablante del diálogo: rehecho. Frau Becker dice los pasos de la receta; se actualiza el `contexto` y se ajusta «Danach braten Sie» a «Dann braten Sie» para no contradecir la receta. Situación: 76 palabras.
  - **⚠ «Rezept» (decisión):** frente al español no es falso amigo (receta, de cocina o del médico), así que la nota es normal en ES. Frente al inglés sí es real («Rezept» ≠ «receipt»), por lo que el ⚠ queda solo en el campo EN.
  - «Cortar las cebollas finas» → «en trozos pequeños». Guía de «Zwiebel»: ≈ «TSVI-bel» / “TSVEE-bel” (z = ts, w = v, ie larga), igual en nota de vocabulario y en explicación. Wasser y «zum Schluss» están enseñados en esta clase antes de usarse en c30.
- **c30 (Zu salzig, nicht scharf genug):**
  - El ⚠ de «zu + adjetivo» se convierte en nota normal («zu salzig» = demasiado salado): es gramática, no falso amigo.
  - Diálogo rehecho sin relleno ni líneas duplicadas («Gern.» ×2, «Die Portion ist nicht zu klein»); el cierre queda al final («Vielen Dank! Auf Wiedersehen!»). Usa «groß», ya enseñado en la tabla. Situación: 72 palabras.
  - Guía de «heiß»: se avisa de que la «h» es un soplo suave, más débil que la «j» española («jais»); EN «hice».
  - El último ítem de evaluación fija la respuesta única: «usa Das Essen y zu».

## Comprobado sin cambios

- Alemán: dativo tras mit/nach/von/zu y contracciones (zum, zur, vom, beim); sin artículo el adjetivo lleva -er/-e/-es/-em/-en (tabla completa, Nom/Akk/Dat); infinitivo de receta e imperativo con Sie; «zu» delante y «genug» detrás.
- Una sola respuesta por ítem: los `ordenar` fijan el Vorfeld; el `escribir` abierto de c26 acepta los órdenes alternativos que empiezan igual; los `relacionar` tienen una sola pareja.
- Vocabulario añadido fuera de ficha (durch, gegen, nach, Kartoffel, Tomate, Pizza, Brot, Kuchen, Milch, Wasser, zum Schluss, Entschuldigung, groß): todos enseñados antes de usarse y sin adelantar gramática.
- Ecuador y Lumo: ninguno. ES neutro, EN americano.

## Sin resolver

- Voces de-DE: confirmar antes de integrar «ß» (Soße, süß, heiß), «z» (Zwiebel, salzig) y «ü» (für, süß), como pide la calibración.
- Nota de producto: en c29 el ⚠ de «Rezept» existe solo en EN; si la app exige ⚠ en ambos idiomas, quitar el símbolo.
