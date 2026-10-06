GO

# Revisión pt N1 B2 (pt.n1.c06–c10)

Validador: `python3 tools/curriculo/validar_bloque.py pt 1 2` → 0 errores (encadenado con n1-b01.json, que ya existe).

## Cambios (13 correcciones + 16 nombres restaurados)

**Palabras de apoyo (5):** B1 existe y f0/B1 ya cubren casi todo. Probado quitando todas las tablas «Palabras de apoyo»: el validador solo exige `hora`, `agora` (c08) y `enfermeiro` (c10).
- c06: tabla de apoyo (no/na/e/não/sim/é/bom/português) → eliminada.
- c07: tabla de apoyo (da/sim/também) → eliminada.
- c08: se mantiene solo `agora`, `a hora` (palabras de la propia ficha).
- c10: `o enfermeiro, a aluna, que` → solo `o enfermeiro` (título y texto en singular).

**Sonido del día (3):**
- c08: la ficha dice «s final em decidir», pero «decidir» no tiene «s» final (la «s» final es el sonido de c10). Se mantiene la lectura del autor («c» = /s/ y «d» → «dyi» en pt-BR, no exigido) y se rotula bien: «la «c» de «decidir»» → ««c» y «d» de «decidir»»; transcripción «dessidjir» → «de-si-dyir».
- c06: «escola suena escóla con final suave» (escola no termina en «e») → eliminado.
- c09: «una «j» suave de «jirafa»» (la j española es /x/, no /ʒ/) → «la «s» de «measure» (más suave que la «j» española)»; «la «o» de «gosto» es abierta» (falso: en «gosto», verbo, es cerrada) → «gosto» suena «gôstu».

**Explicaciones y falsos amigos (3):**
- c06 escritório/oficina: «para «oficina» di «escritório»» (confuso) → «para decir «oficina» (el lugar donde trabajas) usa «escritório»» (es y en).
- c07: «⚠ «como» tiene dos sentidos» (no es falso amigo; en español pasa igual) → nota sin ⚠.
- c08 partir: «Para «dividir» se usa «dividir»» (partir o pão también existe) → «No lo uses para «dividir» una cosa».

**Errores frecuentes (1):** c09 `Me gosto de música.` (no coincidía con la explicación «me gosta») → `Me gosta música.`

**Canon/contexto (1):** c10 «Primera clase en la Escola Capibaribe» (c01–c05 ya fueron con Renata) → «En la Escola Capibaribe».

## Decisiones sobre los puntos del autor
- Ejercicio extra por clase (guiada 4 con `escuchar`, independiente 4): ACEPTADO. El esquema admite guiada 3–5 e independiente 3–4, no cambia formato/clave/lo evaluado de los ítems de la ficha y aporta el formato `escuchar` al bloque. Los ítems cambian de nombre/frase respecto a la ficha pero evalúan la misma clave. `relacionar` no está en el plan de B2 (no se añade).
- Nombres: por aviso del orquestador, `palabrasLibres` ya incluye los de las fichas; se restauraron en ítems Carla, Rita, Marcos, Joana, João, Júlia, Clara, Paulo (16 ítems: p. ej. c08 e5 «Rui abre a porta» → «João abre a porta»). Lia, Rui y Paula quedan solo en ejemplos y errores propios del autor. Sin «Ecuador/Quito».
- Sin sobrantes de gramática: tablas con a gente/vocês/eles (exigido por el encargo), `gostar de` + infinitivo y um pouco/muito solo en c09, `trabalhar como` explicado en c10.

## Hechos del reparto confirmados
- Camila (de Miami) vive en Boa Viagem y trabaja en un «escritório» (c06); estudia português en la Escola Capibaribe y dice «falo espanhol e inglês, e estudo português» (c10).
- Lucas bebe café e come pão en el Café da Bia (c07); gosta muito de música e de ler y um pouco de viajar (c09).
- Camila y Lucas hablan en casa de Dona Marina de un viaje «hoje» (c08): Camila «abre a porta e decide a hora»; «a gente parte hoje». Sin fecha concreta.
- Renata trata a Camila con você; Camila no le habla en la escena de c10 (la senhora hasta c26).
- Bia es la dueña del Café da Bia; Lucas conversa con ella en el café (c07) y con Camila en la Praça de Boa Viagem (c09).
- Nombres secundarios de este bloque (sin hechos): Lia, Rui, Carla, Rita, Marcos, Joana, João, Júlia, Clara, Eva, Marta, Diego, Pedro, Paulo (profesiones ficticias: Lia enfermeira, Rui enfermeiro).

## Sin resolver
- La ficha c08 dice «s final em decidir»: conviene corregir el rótulo del `sonido` en `curriculo/pt/n1.json` (p. ej. «c y d em decidir»).
- En c10 «Moro em Recife e trabalho na cidade» es redundante pero lo fija la ficha; los vocablos «Porto Digital» no están enseñados.

## Pasada de escucha

Se convirtieron a `escuchar` los ítems c06 g3, c07 e3, c08 g3, c09 g3 y c10 g3 (audio pt-BR de la frase, opciones es/en). Cada clase queda con 2 escuchar. Sin otros cambios.
