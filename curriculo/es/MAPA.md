# Español para anglohablantes · mapa de N1–N10

Fuente única para escribir las fichas `curriculo/es/nX.json` (DEC-034). Fija **qué se introduce en cada bloque** y el **hilo de la historia**; el marco común (`curriculo/marco.json`) fija temas, funciones, léxico y situaciones.

## Reglas del idioma

- **Variedad:** español latinoamericano neutro (ustedes, nunca vosotros en lo productivo; tú entre jóvenes y amigos, usted con mayores, clientes y trámites). Notas breves de España desde B1, solo de reconocimiento (claves `vosotros-reconocimiento`, `espana-perfecto-hoy`, `espana-vosotros-imperativo`, `leismo-espana`, `distincion-z-espana`). Lo ecuatoriano o mexicano (¿mande?, chévere, achachay, ñaño, guagua, dame pasando) aparece como nota cultural o en un diálogo con glosa, nunca como respuesta exigida.
- **Apoyo en inglés** (inglés americano): consignas, explicaciones, pistas, feedback y traducciones van en `{"en": …}`. Los ejercicios de traducción dan la frase en inglés. Comparar con el inglés cuando ayuda (ser/estar, género, «I like» → «me gusta»).
- **Tipografía:** ¿…? y ¡…! siempre; tildes correctas; comillas «…» en las explicaciones.
- **Claves:** las de Fundamentos (`previos`) son las de `es.f0` sin el prefijo `es-g-`. Las nuevas están abajo; cada una se introduce una sola vez, en su bloque. Lo ya visto va a `recicla`.
- **Moneda y medidas:** Ecuador usa el dólar (dólares y centavos); en los mercados se pide por libras.

## Reparto canónico

| Personaje | Quién es | Trato |
|---|---|---|
| **Emma García** | estadounidense de Chicago, 25 años en N1 (nació el 12 de abril de 2001). Su abuelo paterno era de Guadalajara (México), pero en casa solo se hablaba inglés. Llega a Quito en septiembre de 2026 a dar clases de inglés en el **Instituto Andino de Idiomas** y estudia español allí mismo. | tú con jóvenes; usted con los Andrade al principio |
| **Rosa Andrade** | 57, la madre de la familia anfitriona; profesora de primaria jubilada; cocina muy bien | Emma le habla de usted («señora Rosa») |
| **Jorge Andrade** | 60, el padre; taxista; hincha del fútbol | usted («don Jorge») |
| **Daniela Andrade** | 22, la hija; estudia Arquitectura en la universidad; se vuelve la mejor amiga de Emma | tú |
| **Mateo Ruiz** | 29, mexicano de Guadalajara, diseñador gráfico, vive en Quito; conoció a Emma en un intercambio de idiomas (f0) | tú |
| **Sofía Herrera** | 35, mexicana, profesora de español de Emma en el instituto | usted al principio; desde N1 B6 tú (ella se lo pide) |
| **Andrés Vaca** | 31, ecuatoriano, coordinador académico del instituto y compañero de trabajo de Emma; jefe directo de Emma mientras ella es coordinadora de cursos (2028–agosto 2029); desde que Emma entra en Andes Vivos, amigo y excolega | tú |
| **Doña Carmen** | 65, dueña de la tienda del barrio (La Floresta) | usted |

Los Andrade viven en una casa en **La Floresta**, un barrio de Quito, con un perro, **Toby**. El instituto está en La Mariscal. Personajes de roles sin nombre: «Mesero», «Mesera», «Vendedora», «Recepcionista», «Taxista», «Doctora», «Policía»… (en español: se muestra igual con la interfaz en inglés).

**Nuevos por nivel (los fija este mapa):** N2 · **Señor Paredes** (casero del departamento de Emma y Daniela, usted), **Dra. Paula Mena** (médica, usted). N4 · **Inés Cárdenas** (directora de la fundación de turismo comunitario **Andes Vivos**, usted). N6 · **Kenji** y **Valentina** (equipo de Andes Vivos). N8 · **Martina** (argentina, compañera del curso del DELE C1, voseo). Ningún personaje nuevo repite nombre ni apellido del reparto (García, Andrade, Ruiz, Herrera, Vaca, Paredes, Mena, Cárdenas).

## Cronología

- **N1** (sep.–dic. 2026): los primeros meses de Emma en Quito con los Andrade.
- **N2** (2027): segundo año; en B3 Emma y Daniela alquilan un departamento juntas en La Mariscal.
- **N3** (2028): Emma ya es coordinadora de cursos de inglés del instituto; Daniela se gradúa (B1).
- **N4** (2029): Daniela se va a hacer una maestría a Madrid (B6; desde aquí trae las notas de España). Emma deja el instituto y entra en **Andes Vivos** (B5).
- **N5–N7** (2030–2032): Emma coordina proyectos de turismo comunitario; residencia ecuatoriana (N5 B1); en N7 B8 visita a Daniela en Madrid.
- **N8** (2033): Emma prepara el DELE C1.
- **N9** (2034): Emma es jefa de proyectos en Andes Vivos.
- **N10** (2035): Emma y Mateo fundan **Puente**, una pequeña agencia de turismo responsable e interpretación. Emma sigue en Andes Vivos hasta lanzar la ruta de abril y lo deja a finales de abril (Inés queda como mentora); Puente se prepara de enero a mayo (pruebas, preventas, pilotos) y se lanza oficialmente el 1 de junio.

---

## N1 · A1 · DELE A1

Historia: Emma llega a Quito, vive con los Andrade, empieza a trabajar en el instituto y a estudiar con Sofía; conoce el barrio, la tienda de Doña Carmen, el transporte y los primeros paseos (Centro Histórico, TelefériQo, Mitad del Mundo).

Cada clase de N1 abre con un **sonido del día** (`sonido`): vocales a e i o u; h muda; r/rr; j y g suave (ge, gi); c/z/s (seseo); ll/y; ñ; b/v; d suave; qu/gu; ch; acento y tilde; diptongos.

- **B1 Saludar y presentarse** — Emma llega a la casa de los Andrade y al instituto.
  - `saludos-hora-del-dia`: buenos días / buenas tardes / buenas noches, hola, ¿qué tal?, ¿cómo está?
  - `despedidas`: chao, hasta luego, hasta mañana, nos vemos
  - `llamarse-presente`: me llamo, te llamas, se llama, nos llamamos, se llaman
  - `nacionalidades-genero`: estadounidense, ecuatoriano/a, mexicano/a, inglés/inglesa
  - `deletrear-como-se-escribe`: ¿Cómo se escribe?, letras dobles (ll, rr), con tilde
  - `presentar-a-otro`: te presento a… / le presento a…; mucho gusto, encantado/a, igualmente
- **B2 Hablar de mí** — Emma habla de su trabajo, sus idiomas y lo que le gusta.
  - `presente-ar`: hablar, trabajar, estudiar (todas las personas)
  - `presente-er-ir`: vivir, aprender, comer, leer, escribir
  - `profesiones-genero`: el profesor / la profesora, el/la estudiante; ¿A qué te dedicas?
  - `idiomas-y-grado`: hablo inglés, un poco de español, muy bien, más o menos
  - `gustar-singular`: me gusta / te gusta / le gusta + sustantivo singular o infinitivo
- **B3 Personas y cosas** — la familia Andrade y la familia de Emma; su cuarto.
  - `articulos-genero`: el/la/los/las, un/una/unos/unas; género del sustantivo
  - `plural`: plural de sustantivos y adjetivos
  - `tener-presente`: tener (todas las personas); edad: ¿Cuántos años tienes?
  - `numeros-0-20`
  - `posesivos-atonos`: mi, tu, su, nuestro/a, sus
  - `hay-y-demostrativos`: hay; este/esta/esto; ¿Qué es esto?
- **B4 Preguntar y negar** — Emma se inscribe en el curso de español y abre una cuenta de teléfono.
  - `interrogativos-completos`: qué, quién, dónde, cuándo, cómo, cuánto/a/os/as, cuál (con tilde)
  - `numeros-21-100`
  - `datos-de-contacto`: teléfono, correo (arroba, punto), dirección; ¿Cuál es tu número?
  - `doble-negacion`: no… nada / nadie / nunca
  - `pedir-repeticion`: ¿Puede repetir, por favor?, más despacio, ¿Cómo dice?, no entiendo
- **B5 Café y compras** — cafetería del instituto, tienda de Doña Carmen, ropa en el centro comercial.
  - `pedir-en-un-cafe`: quisiera…, ¿me da…?, para mí…, ¿me trae la cuenta?
  - `cuanto-cuesta`: ¿Cuánto cuesta/cuestan?, ¿Cuánto es?; dólares y centavos
  - `pagar`: en efectivo, con tarjeta, el vuelto
  - `colores-concordancia`: rojo/roja, verde, azul; colores con el sustantivo
  - `demostrativos-distancia`: este / ese / aquel; ¿Tiene otra talla?
- **B6 Gustos y rutina** — la rutina de Emma y la de los Andrade; el tiempo libre.
  - `la-hora`: ¿Qué hora es?, es la una, son las…, a las…, y media, menos cuarto; días de la semana
  - `reflexivos-rutina`: levantarse, ducharse, acostarse
  - `presente-e-ie`: empezar, querer, preferir, pensar
  - `presente-o-ue`: dormir, volver, poder, almorzar
  - `gustar-plural-encantar`: me gustan, me encanta(n); a mí también / a mí tampoco
  - `frecuencia`: siempre, a veces, nunca, todos los días, los lunes
- **B7 Describir y ubicarse** — Emma describe a la gente y recorre el barrio y el Centro Histórico.
  - `ser-descripcion`: ser + adjetivos de físico y carácter; muy, bastante
  - `tener-llevar-descripcion`: tiene el pelo…, los ojos…; lleva una chaqueta…
  - `preposiciones-lugar`: al lado de, cerca de, lejos de, enfrente de, entre, detrás de
  - `contracciones-al-del`
  - `hay-vs-estar`: hay un banco / el banco está…
  - `venir-presente`: venir; ¿De dónde vienes?
- **B8 Verbos frecuentes y comida** — compras en el mercado con señora Rosa.
  - `querer-poder-infinitivo`: quiero + infinitivo, puedo + infinitivo
  - `tener-que-hay-que`: obligación personal e impersonal
  - `cantidades-envases`: una libra de, medio kilo, una botella de, un paquete de, un poco de, mucho/a
  - `numeros-hasta-1000`: cien/ciento, doscientos/as…
  - `od-lo-la-los-las`: ¿Lo quiere? Sí, lo quiero
  - `verbos-yo-go`: hago, pongo, salgo, traigo
- **B9 Moverse y planes** — bus, Ecovía y taxi con don Jorge; planes con Daniela y Mateo.
  - `ir-presente-transporte`: ir; en bus, en taxi, a pie
  - `imperativo-tu-afirmativo`: sigue, toma, cruza, gira (regulares + indicaciones)
  - `ir-a-infinitivo`: planes próximos
  - `invitar-aceptar-rechazar`: ¿Quieres…?, ¿Te gustaría…?, me encantaría, lo siento, no puedo
  - `fechas-meses`: los meses, ¿Qué fecha es hoy?, el 15 de octubre
- **B10 Mi fin de semana y cierre** — el fin de semana en la Mitad del Mundo; repaso y prueba del nivel.
  - `preterito-ar`: pretérito regular -ar (hablé, visitaste…); ayer, anoche, el sábado pasado
  - `preterito-er-ir`: pretérito regular -er/-ir
  - `preterito-ir-ser-hacer`: fui, fuiste…; hice, hiciste…
  - `hace-desde`: hace dos meses, desde septiembre, ¿desde cuándo?
  - (c49 repaso, c50 prueba del nivel: solo reciclan)

## N2 · A2 · DELE A2

Historia (2027): segundo año. Emma da más clases y prepara el DELE A2; recuerda su vida en Chicago; se muda con Daniela; viaja por Ecuador; se enferma; aprende a cocinar con señora Rosa.

- **B1 Rutinas, trabajo y estudio** — la jornada en el instituto.
  - `presente-e-i`: pedir, servir, repetir, seguir
  - `saber-vs-conocer`: y conocer (conozco), traducir (traduzco)
  - `estar-gerundio`: acción en curso
  - `soler-infinitivo`
  - `adverbios-mente`
- **B2 Contar experiencias pasadas** — la infancia y la universidad de Emma en Chicago; su abuelo.
  - `preterito-irregulares-fuertes`: tener, estar, poder, poner, venir, querer, decir, traer
  - `preterito-cambio-raiz-ir`: pidió, durmió, prefirió
  - `preterito-ortografia`: busqué, llegué, empecé, leyó
  - `marcadores-secuencia`: primero, luego, después, al final, más tarde
  - `imperfecto-intro`: imperfecto regular + ser, ir, ver para describir cómo era algo
- **B3 Casa, barrio y servicios** — Emma y Daniela alquilan un departamento en La Mariscal (casero: señor Paredes).
  - `estar-participio`: la puerta está cerrada, la luz está prendida
  - `objeto-indirecto-le-les`: le escribo al casero, les pago a…
  - `pronombres-preposicion`: para mí, conmigo, contigo
  - `verbos-tipo-gustar`: molestar, importar, faltar, interesar
  - `se-accidental`: se me rompió, se dañó, se nos acabó
- **B4 Planes, citas y predicciones** — agenda de Emma; el clima de Quito (las cuatro estaciones en un día).
  - `futuro-simple-regular`
  - `futuro-irregular`: tendré, haré, podré, saldré, vendré, diré
  - `tiempo-atmosferico`: hace frío, llueve, está nublado, hay sol; la temporada de lluvias
  - `pensar-infinitivo`: intenciones
  - `proponer-y-si`: ¿Y si…?, ¿Qué tal si…?, mejor…
  - `acabar-de-infinitivo`
- **B5 Comparar y elegir productos** — compras para el departamento.
  - `comparativos`: más/menos… que, tan… como, tanto/a… como
  - `comparativos-irregulares`: mejor, peor, mayor, menor
  - `superlativo-isimo`: el más…, -ísimo
  - `quedar-ropa`: me queda grande/pequeño, ¿cómo me queda?
  - `od-oi-se-lo`: pronombres combinados (se lo doy)
  - `imperfecto-cortesia`: quería…, venía a…
- **B6 Restaurante y cocina** — cocina ecuatoriana con señora Rosa (locro de papa, encebollado) y un restaurante.
  - `imperativo-usted-ustedes`: corte, añada, sirvan
  - `imperativo-pronombres`: córtelo, sírvanse, pásamelo
  - `se-impersonal`: se corta, se añade, se sirve caliente
  - `condicional-cortesia`: ¿podría…?, me gustaría…
  - `estar-sabor`: está rico/salado vs es salado
- **B7 Viajes y transporte** — viaje a Cuenca y a Baños.
  - `preterito-perfecto`: he viajado, ¿has estado en…?, nunca he…; nota: en América se usa menos que en España
  - `participios-irregulares`: hecho, visto, puesto, vuelto, escrito, abierto, dicho, roto
  - `ya-todavia-no`
  - `por-para-intro`: para + destino/propósito; por + lugar, tiempo aproximado, precio
  - `avisos-infinitivo`: no fumar, prohibido estacionar, se ruega…
- **B8 Salud y bienestar** — Emma se enferma del estómago; la Dra. Mena.
  - `doler`: me duele la cabeza, me duelen los ojos
  - `sintomas-tener-estar`: tengo fiebre, tos; estoy resfriada
  - `deberias-consejo`: deberías + infinitivo
  - `es-importante-infinitivo`: es mejor / es importante / es necesario + infinitivo
  - `llevar-gerundio`: llevo tres días tosiendo
- **B9 Favores, permisos y normas** — las reglas del edificio y los vecinos.
  - `pedir-favor`: ¿me prestas…?, ¿me puedes…?, ¿te importa…?
  - `ofrecer-ayuda`: ¿te ayudo?, ¿quieres que…? (solo la fórmula)
  - `se-puede-permiso`: ¿se puede…?, no se puede, está prohibido
  - `imperativo-tu-irregular`: pon, ven, haz, di, sal, ten, ve, sé
  - `normas-del-edificio`: hay que / no se permite + infinitivo
- **B10 Repaso y proyecto** — Emma organiza un paseo a Otavalo; repaso y prueba.
  - `preterito-vs-imperfecto-intro`: contexto (imperfecto) + acción (pretérito), primer contraste

## N3 · B1 (entrada) · DELE B1

Historia (2028): Emma, ya coordinadora de cursos; Daniela se gradúa; a Emma le roban el celular en el bus; sus padres visitan Quito; viaje a Galápagos con incidencias; una serie española (primer contacto con el vosotros).

- **B1 Novedades, cambios y logros** — Daniela se gradúa; Emma, nueva coordinadora.
  - `subjuntivo-presente-formas`: regulares
  - `subjuntivo-irregulares`: tenga, haga, vaya, sea, esté, sepa, pueda
  - `reaccionar-que-bueno-que`: ¡Qué bueno que…! + subjuntivo
  - `deseos-que-subjuntivo`: ¡Que te vaya bien!, ¡Que tengas suerte!
  - `dar-novedades`: ¿Sabes que…?, resulta que…, ¿te conté que…?
- **B2 Incidentes y anécdotas** — el celular robado en el bus; la denuncia.
  - `preterito-vs-imperfecto`: contraste completo
  - `estaba-gerundio-cuando`: estaba esperando cuando…
  - `cuando-mientras`
  - `impersonal-tercera-plural`: me robaron, me llamaron
  - `exclamaciones-que-tan`: ¡Qué susto!, ¡qué mala suerte!, ¡no me digas!
- **B3 Historias de familia** — los padres de Emma en Quito; la historia del abuelo de Guadalajara.
  - `relativos-que-donde-quien`
  - `llevarse-parecerse`: llevarse bien/mal, parecerse a
  - `ponerse-volverse`: verbos de cambio
  - `sentimientos-subjuntivo`: me alegra que…, me da pena que…
  - `soler-imperfecto`: solíamos…, tradiciones
- **B4 Planes con condiciones** — un fin de semana que cambia por la lluvia.
  - `si-presente`: si + presente, futuro/presente/imperativo
  - `cuando-subjuntivo-futuro`: cuando llegues, llámame
  - `imperativo-negativo`: no llegues tarde, no se olvide
  - `hasta-que-antes-de-que`
  - `te-parece`: ¿te parece si…?, ¿te parece bien que…?
- **B5 Viajes e incidencias** — Galápagos: vuelo retrasado, control, maleta dañada.
  - `querer-que-subjuntivo`: quiero que me devuelvan…
  - `necesario-que-subjuntivo`: es necesario que…
  - `condicional-simple`: todas las formas
  - `posicion-pronombres-perifrasis`: me lo pueden cambiar / pueden cambiármelo
  - `reclamar-cortesia`: lamento decirle, quisiera hablar con…
- **B6 Salud, hábitos y consejos** — Emma empieza a correr; consejos de la Dra. Mena.
  - `recomendar-que-subjuntivo`: te recomiendo / te aconsejo que…
  - `es-bueno-que-subjuntivo`
  - `yo-que-tu`: yo que tú / yo en tu lugar + condicional
  - `dejar-de-seguir-volver-a`: perífrasis
  - `para-que-subjuntivo`
- **B7 Explicar cómo funciona algo** — el carro de don Jorge en el taller; la lavadora del departamento.
  - `relativos-preposicion`: con el que, en la que
  - `lo-que`
  - `servir-para`: sirve para, funciona con
  - `pasiva-ser-reconocimiento`
  - `averias`: no prende, hace un ruido, se calienta
- **B8 Transmitir mensajes** — recados en el instituto.
  - `estilo-indirecto-presente`: dice que…
  - `estilo-indirecto-pasado`: dijo que + imperfecto / condicional
  - `preguntas-indirectas`: me preguntó si…, quiere saber dónde…
  - `peticiones-indirectas`: me pide que + subjuntivo presente
  - `verbos-de-comunicacion`: comentar, contar, explicar, avisar
- **B9 Medios, cine y música** — una serie española, la radio y la música de Quito.
  - `creer-que-indicativo-subjuntivo`: creo que… / no creo que…
  - `es-verdad-que`: es verdad que… / no es verdad que + subjuntivo
  - `opinar-me-parece`: me parece que…, me parece bien/mal que…
  - `segun-al-parecer`
  - `vosotros-reconocimiento`: nota de España: vosotros en presente (habláis, tenéis), solo para entender
- **B10 Repaso y proyecto** — Emma propone un club de conversación; repaso y prueba.
  - `conectores-causa-consecuencia`: porque, como, por eso, así que
  - `aunque-indicativo`

## N4 · B1 · DELE B1

Historia (2029): Emma busca un trabajo nuevo y entra en Andes Vivos (B5, directora Inés Cárdenas); Daniela se va a Madrid (B6) y en las videollamadas trae el español de España; Emma alquila sola en Guápulo (B3); fiestas y páramo (B9).

- **B1 Recuerdos y experiencias de vida** — Emma recuerda sus tres años en Quito.
  - `pluscuamperfecto`
  - `ya-no-todavia`: ya no vivo con…, todavía…
  - `acordarse-recordar`
  - `hacia-tiempo-que`
  - `acostumbrarse-a`
- **B2 Deseos, lamentos y deducciones**
  - `ojala-subjuntivo`: ojalá + presente de subjuntivo
  - `futuro-probabilidad`: estará en casa
  - `quizas-a-lo-mejor`: a lo mejor + indicativo, quizás/tal vez + subjuntivo
  - `deberia-haber`: debería haber + participio
  - `certeza-duda`: estoy seguro de que… / no estoy seguro de que + subjuntivo
- **B3 Vivienda y convivencia** — el departamento de Guápulo; el contrato y los vecinos.
  - `relativo-subjuntivo`: busco un departamento que tenga…
  - `mandar-a-hacer`: mandar a arreglar (uso americano)
  - `estar-dispuesto-a`
  - `quedar-en-acuerdos`: quedamos en que…
  - `reciprocos-se`: nos ayudamos, se saludan
- **B4 Servicios, bancos y reclamaciones**
  - `correo-formal`: Estimado/a…, Le escribo para…, Atentamente
  - `condicional-peticion-formal`: le agradecería…, ¿sería posible…?
  - `por-para-ampliacion`: por error, por correo, para el lunes
  - `numeros-grandes-decimales`: mil, millón de, 1.250,50
  - `expresiones-de-plazo`: a partir de, dentro de, en un plazo de
- **B5 Buscar trabajo** — la entrevista en Andes Vivos.
  - `perfecto-vs-indefinido`: he trabajado / trabajé (nota de uso americano y español)
  - `ser-bueno-para`: soy bueno/a para…, se me da bien (nota de España)
  - `en-cuanto-subjuntivo`: en cuanto, apenas + subjuntivo
  - `verbos-con-preposicion`: encargarse de, dedicarse a, consistir en, contar con
  - `derivacion-sustantivos`: -ción, -dad, -miento
- **B6 Tono formal e informal** — Daniela en Madrid; el primer correo formal de Emma.
  - `tutear`: ¿nos tuteamos?, pasar del usted al tú
  - `discrepar-que-subjuntivo`: no estoy de acuerdo con que…
  - `que-subjuntivo-encargo`: que lo haga Andrés
  - `diminutivos`: un ratito, un cafecito, ahorita
  - `espana-perfecto-hoy`: nota de España: «hoy he comido» vs «hoy comí»
- **B7 Deporte, ocio y personalidad**
  - `ser-estar-cambio-significado`: es aburrido / está aburrido, es listo / está listo
  - `imperativo-nosotros`: ¡vamos!, hagámoslo
  - `lo-adjetivo`: lo bueno, lo mejor de…
  - `indefinidos`: alguno, ninguno, cualquier(a)
  - `gerundio-modo`: aprendí jugando
- **B8 Viajar por tu cuenta** — Emma alquila un carro para la Ruta de las Cascadas.
  - `imperativo-negativo-pronombres`: no te olvides, no lo dejes
  - `hace-falta`: hace falta + infinitivo / que + subjuntivo
  - `en-caso-de-que`
  - `por-si`: por si acaso, por si llueve
  - `a-pesar-de`
- **B9 Tradiciones y medio ambiente** — Día de los Difuntos (colada morada y guaguas de pan), Inti Raymi; el páramo.
  - `mientras-que-contraste`
  - `conectores-causa-formales`: debido a, a causa de, ya que
  - `habria-que`: habría que + infinitivo, se debería
  - `coletillas`: ¿verdad?, ¿no?, ¿cierto?
  - `cada-vez-mas`
- **B10 Repaso y proyecto**
  - `aunque-subjuntivo`: aunque + subjuntivo vs indicativo
  - `organizadores-discurso`: en primer lugar, por un lado / por otro, en conclusión

## N5 · B2 (entrada) · DELE B2

Historia (2030): Emma coordina proyectos de turismo comunitario en Andes Vivos; tramita la residencia (B1); viaja a la Amazonía (B3); lidera un proyecto en una comunidad cerca del Cotopaxi (B9).

- **B1 Cambios de vida y adaptación**
  - `imperfecto-subjuntivo-formas`
  - `verbos-cambio-ampliacion`: hacerse, convertirse en, llegar a ser, quedarse
  - `pasiva-ser`: la visa fue aprobada
  - `estar-a-punto-de`
  - `infinitivo-compuesto`: después de haber vivido…
- **B2 Especular y valorar el pasado**
  - `condicional-compuesto`
  - `futuro-perfecto-probabilidad`: habrá llegado
  - `condicional-probabilidad-pasado`: serían las ocho
  - `si-imperfecto-subjuntivo`: si tuviera…, + condicional
  - `ojala-imperfecto`: ojalá estuvieras aquí
- **B3 Viajes con detalle** — la Amazonía.
  - `relativos-el-cual`: el cual, la cual, lo cual (explicativas)
  - `cuyo`
  - `vale-la-pena`
  - `correlacion-tiempos-subjuntivo`: exigí que me devolvieran…
  - `uno-de-los-mas`
- **B4 Gastronomía y cultura**
  - `ir-gerundio`: ir añadiendo poco a poco
  - `lo-adjetivo-que`: lo rico que está
  - `no-solo-sino`
  - `sino-vs-pero`
  - `posicion-adjetivo`: un gran plato / un plato grande
- **B5 Salud, ciencia y prevención**
  - `de-ahi-que`
  - `se-ha-demostrado`
  - `a-medida-que`
  - `con-tal-de-que`: con tal de que, a no ser que, siempre que + subjuntivo
  - `cuanto-mas`
- **B6 Lo que dijeron otros**
  - `estilo-indirecto-cambios-tiempo`: dijo que vendría, que había llegado
  - `estilo-indirecto-subjuntivo-pasado`: me pidió que fuera
  - `verbos-de-reporte`: afirmar, negar, admitir, advertir, sugerir
  - `dequeismo`: pienso que (no «pienso de que»), me acuerdo de que
  - `resumir-acta`: según lo conversado, se acordó…
- **B7 Medios con criterio**
  - `matizadores`: en cierto modo, hasta cierto punto
  - `que-yo-sepa`
  - `en-cambio-por-el-contrario`
  - `distancia-supuestamente`: supuestamente, al parecer (ampliación)
  - `condicional-rumor`: el ministro habría dicho
- **B8 Acuerdos, desacuerdos y ética**
  - `por-mucho-que`
  - `si-bien`
  - `no-es-que`: no es que + subjuntivo, sino que…
  - `valoracion-subjuntivo`: es lógico/normal/injusto que…
  - `a-cambio-de-que`
- **B9 Liderar un proyecto pequeño** — el proyecto cerca del Cotopaxi.
  - `porcentajes-fracciones`
  - `verbos-de-variacion`: aumentar, disminuir, duplicar
  - `encargarse-de-que`
  - `el-hecho-de-que`
  - `imperativo-ustedes-pronombres`: siéntense, organícense
- **B10 Repaso y proyecto**
  - `reformuladores`: es decir, o sea, dicho de otro modo, en definitiva
  - `tilde-diacritica`: tú/tu, más/mas, sé/se, aún/aun

## N6 · B2 · DELE B2

Historia (2031): Emma negocia con proveedores y comunidades; da su primera charla en una feria de turismo (B8); Mateo abre su estudio de diseño (B5); equipo nuevo: Kenji y Valentina.

Calendario fijado al escribir N6: B1 abril–mayo (Emma cumple 30 el sábado 12-abr-2031) · B2 sin mes (hacia mayo–junio) · B3 mayo–junio · B4 julio · B5 agosto (estudio de Mateo) · B6 octubre · B7 primera mitad de noviembre · B8 ensayos del 17 al 28 de noviembre · B9 sin mes salvo la encuesta (finales de noviembre) · B10: debate el lunes 1-dic, montaje y feria el sábado 13-dic-2031, cierre el lunes 22-dic.

- **B1 Familias y relaciones hoy**
  - `como-si`
  - `a-diferencia-de`
  - `lo-que-pasa-es-que`
  - `articulo-generico`
  - `verbos-pronominales-relacion`: casarse con, separarse de, enamorarse de
- **B2 Condiciones, contratos y garantías**
  - `a-menos-que`
  - `supuesto-de-que`: en el supuesto de que
  - `futuro-normativo`: el arrendatario deberá…
  - `participio-absoluto`: firmado el contrato…
  - `quien-generico`: quien firme…
- **B3 Valorar decisiones y dar retroalimentación**
  - `subjuntivo-perfecto`: siento que no hayas podido…
  - `si-pluscuamperfecto`: si hubiera sabido…, habría…
  - `estaria-bien-que`
  - `tener-razon-en`
  - `de-infinitivo-condicional`: de haberlo sabido…
- **B4 Decir las cosas con tacto**
  - `condicional-atenuador`: yo diría que…
  - `no-se-si`
  - `te-importaria-que`
  - `me-temo-que`
  - `cuantificadores-atenuadores`: un poco, algo, medio cansado
- **B5 Recursos para convencer** — el estudio de Mateo y su publicidad.
  - `escindidas`: fue Emma quien…, es ahí donde…
  - `preguntas-retoricas`
  - `prefijos-intensificadores`: súper, re-, -ísimo
  - `lo-atributo`: lo es, lo está
  - `dislocacion-duplicado`: a mi hermana la vi ayer
- **B6 Reuniones y plazos**
  - `para-cuando`: para cuando llegues, ya habremos terminado
  - `a-mas-tardar`
  - `se-acordo`: se acordó que, quedó en que
  - `lo-cual`
  - `nominalizacion`: la entrega, el envío
- **B7 Negociar en la vida diaria** — el mercado de artesanías de Otavalo; el técnico.
  - `que-conste-que`
  - `en-vez-de`
  - `como-condicional`: como no me lo rebaje, no lo compro
  - `regateo`: ¿me hace una rebajita?, ¿cuánto es lo menos?
  - `lo-de`: lo del precio
- **B8 Hablar en público** — la charla en la feria.
  - `marcadores-orales`: bueno, pues, a ver
  - `como-decia`
  - `deixis-discursiva`: lo anterior, esto que acabo de mostrar
  - `no-sabria-decir`
  - `entonacion-enfasis`
- **B9 Tecnología, datos y sociedad**
  - `hacer-que-subjuntivo`: hace que la gente lea menos
  - `probable-que-subjuntivo`
  - `negacion-parcial`: no necesariamente, no siempre
  - `anglicismos-tecnologia`: hacer clic, el enlace, descargar
  - `se-impersonal-a`: se contrató a…
- **B10 Repaso y proyecto**
  - `aun-asi`: aun así, de todas formas
  - `ensayo-estructura`: tesis, argumentos, conclusión

## N7 · B2 (alto)

Historia (2032): Emma redacta mensajes delicados para la fundación; investiga la historia de Quito para una ruta guiada (B4); visita a Daniela en Madrid (B8); lee novelas latinoamericanas (B9).

Calendario fijado al escribir N7 (2032): B1 4–17 feb (derrumbe; recorrido del sáb 14 pasa al sáb 21) · B2 24 feb–5 mar · B3 9–19 mar (golpe al taxi el mar 16) · B4 23 mar–1 abr · B5 3–24 abr (aniversario de Andes Vivos el sáb 10; Emma cumple 31 el lun 12) · B6 26–30 abr (reunión de tarifas) · B7 3–12 may (negociación del viaje) · viaje de 24 estudiantes del vie 14 al lun 17 may · B8 Madrid del lun 24 al lun 31 may (cumpleaños de Daniela el sáb 29) · B9 club de lectura 3–24 jun (Sofía propone el DELE C1 el jue 24) · B10 7–26 jun (informe y quejas del viaje; Emma acepta preparar el DELE).

- **B1 Registro y matices**
  - `registros-lexico`
  - `formulas-mensajes-delicados`: lamentamos informarle que…
  - `eufemismos`
  - `tratamientos`: don, doña, licenciado/a, ingeniero/a
  - `impersonalizar-responsabilidad`: se tomó la decisión de…
- **B2 Cronologías complejas**
  - `preterito-anterior-reconocimiento`
  - `nada-mas-infinitivo`: nada más llegar, una vez que, apenas
  - `de-aqui-a`
  - `presente-historico`
  - `llevar-participio`: llevo hechas tres
- **B3 Lo que pudo ser y lo que sabemos**
  - `condicionales-mixtas`: si hubiera estudiado, ahora sería…
  - `igual-probabilidad`: igual llueve
  - `deber-de-haber`
  - `percepcion-infinitivo`: vi salir a un hombre, oí gritar
  - `por-poco`
- **B4 Historias de ciudades y objetos** — la ruta por el Quito colonial.
  - `atribucion-se-dice`: según cuenta la leyenda, se dice que
  - `participio-adjetivo`: construida en…
  - `siglos-epocas`: el siglo XVI, en los años veinte
  - `a-principios-de`: a principios / mediados / finales de
  - `articulo-toponimos`: el Ecuador, el Perú, La Paz
- **B5 Humor, metáforas y modismos**
  - `metaforas-cotidianas`
  - `modismos`: meter la pata, tomar el pelo, estar en las nubes
  - `doble-sentido`
  - `aumentativos`: -azo, -ote
  - `comparaciones-fijas`: más terco que una mula
- **B6 Argumentar y debatir**
  - `ahora-bien`
  - `perdone-que`: perdone que lo interrumpa
  - `el-que-subjuntivo`: el que hayan subido los precios…
  - `de-modo-que`
  - `aun-cuando`
- **B7 Negociaciones con varias partes**
  - `a-condicion-de-que`
  - `tal-como`: tal como acordamos, según lo conversado
  - `tanto-como-correlativo`
  - `salvo-excepto`
  - `en-cuanto-a`
- **B8 Culturas en contacto** — Emma en Madrid.
  - `generalizar-tender-a`
  - `por-lo-general`
  - `me-choco-que`: me chocó que + imperfecto de subjuntivo
  - `espana-vosotros-imperativo`: nota de España: vosotros en imperativo y pasado (reconocimiento)
  - `leismo-espana`: nota de España: le vi = lo vi
- **B9 Relatos, personajes y narradores**
  - `estilo-indirecto-libre`
  - `raya-dialogo`: la raya del diálogo y los verbos de habla (susurró, exclamó)
  - `presente-sinopsis`
  - `ambos-sendos`
  - `no-hay-nadie-que`
- **B10 Repaso y proyecto**
  - `cohesion-referencia`
  - `puntuacion`

## N8 · C1 (entrada) · DELE C1

Historia (2033): Emma prepara el DELE C1 en un curso donde conoce a Martina (argentina, voseo); habla rápida y radio; variedades del español; reclamación por escrito; presenta un estudio en un curso universitario (B9).

Calendario fijado al escribir N8 (2033): B1 10–31 ene (empieza el curso del DELE C1, los jueves; Emma conoce a Martina el primer día; vuelo a Guayaquil) · B2 1–28 feb (informe para Inés, cena en casa de Mateo el sáb 12, Andrés desaparece del lun 21 al vie 25, departamento de Mateo) · B3 1–14 mar (compras; zapatos para la hermana de Emma, que vive en EE. UU.) · B4 17 mar–2 abr (módulo de variedades desde el jue 17; excursión a la sierra el sáb 19; hotel de Madrid para unas vacaciones de julio) · B5 3–17 abr (Emma cumple 32 el mar 12; se inscribe en el DELE C1 de noviembre) · B6 18–26 abr · B7 28 abr–4 may (módulo de literatura con sesiones extra) · B8 5–31 may (reclamación de internet el jue 5; nueva Administradora del edificio) · B9 3–28 oct (3.100 visitantes = proyección de todo 2033) · B10 31 oct–18 nov (feriado del jue 3 de noviembre; simulacro y nota provisional antes del examen).

- **B1 Escucha rápida y habla conectada**
  - `formas-reducidas-oral`: pa’, ’ta, ’toy
  - `muletillas`: este…, o sea, tipo, nomás
  - `aclaraciones-precisas`: ¿te refieres a…?, ¿o sea que…?
  - `lenguaje-megafonia`: se informa, se ruega
  - `elision-d`: cansao, terminao (reconocimiento)
- **B2 Leer entre líneas**
  - `no-digo-que`
  - `ironia-antifrasis`
  - `convendria`
  - `inferencias-o-sea-que`
  - `futuro-concesivo`: será caro, pero…
- **B3 Cómo persuade un mensaje**
  - `paralelismo`
  - `recursos-retoricos`: anáfora, tríada
  - `superlativos-cultos`: óptimo, pésimo, máximo
  - `verbos-influencia`: convencer de que, persuadir para que
  - `elipsis`
- **B4 Variedades de la lengua** — Martina y el voseo; el Caribe, México, los Andes y España.
  - `voseo`: vos sos, tenés, vení (reconocimiento)
  - `andino-dar-gerundio`: dame pasando, ¿mande?, ¡achachay! (reconocimiento)
  - `distincion-z-espana`: nota de España: z/ce/ci frente al seseo
  - `lexico-variedades`: carro/coche, celular/móvil, computadora/ordenador
  - `negociar-significado`: ¿cómo se dice aquí…?
- **B5 Expresiones idiomáticas**
  - `refranes`
  - `modismos-deporte`: tirar la toalla, en la recta final
  - `parafrasear`
  - `locuciones-verbales`: echar de menos / extrañar, dar la lata
  - `colocaciones`: tomar una decisión, cometer un error
- **B6 Cine, series y pódcasts**
  - `perifrasis-c1`: acabar + gerundio, terminar por, llegar a + infinitivo
  - `valoracion-matizada`: no está mal, deja que desear
  - `resumen-nominal`
  - `superlativo-subjuntivo`: la mejor serie que haya visto
  - `referencias-temporales-relativas`: al día siguiente, la víspera
- **B7 Literatura y memoria**
  - `lenguaje-evocador`
  - `futuro-subjuntivo-reconocimiento`: sea cual fuere
  - `formas-en-se`: hubiese, fuese
  - `hiperbaton`
  - `verbos-precisos`
- **B8 Reclamar y dar seguimiento por escrito**
  - `correspondencia-formal-c1`: por medio de la presente, sin otro particular
  - `me-vere-obligado`
  - `reiterar`
  - `dar-por-participio`: dar por resuelto
  - `gerundio-incorrecto`
- **B9 Estudiar y presentar con cautela**
  - `cabria`: cabría pensar, parece indicar
  - `describir-graficos`
  - `cabe-senalar`
  - `evidencia-sugieren`: los datos sugieren que
  - `nosotros-de-autor`
- **B10 Repaso y proyecto**
  - `sintesis-de-textos`
  - `mediacion-resumen`

## N9 · C1 · DELE C1

Historia (2034): Emma es jefa de proyectos en Andes Vivos: contactos en una feria en Lima (B1), reuniones, selección de personal (B5), informes para donantes (B6), seguridad en las rutas (B7), trámites públicos (B8) y un conflicto con un proveedor (B9).

- **B1 Crear contactos**
  - `charla-trivial`
  - `coincidir-en`
  - `estar-al-frente-de`
  - `quedar-en-contacto`
  - `tuteo-profesional`
- **B2 Historias con propósito**
  - `marcadores-tension`: de repente, justo cuando
  - `extraer-leccion`
  - `captar-atencion`: imagínense…, ¿saben qué…?
  - `estilo-directo-dramatizado`
  - `flashback`
- **B3 Mensajes claros y breves**
  - `sintetizar`: en resumen, en pocas palabras
  - `priorizar`: ante todo, lo primero es
  - `correo-ejecutivo`
  - `voz-activa-claridad`
  - `economia-lenguaje`
- **B4 Dirigir reuniones**
  - `dar-la-palabra`
  - `lenguaje-de-actas`
  - `reconducir`: volviendo al tema
  - `pasemos-a`
  - `consenso-votacion`
- **B5 Entrevistas y procesos de selección**
  - `respuesta-estructurada`
  - `contar-con-avalar`
  - `preguntas-de-seguimiento`
  - `debilidades-reformular`
  - `verbos-de-logro`: lograr, conseguir, alcanzar
- **B6 Informes y datos**
  - `informe-estructura`
  - `matizar-conclusiones`: en principio, a priori
  - `tendencias-lexico`: repunte, estancamiento
  - `finanzas-basicas`
  - `aproximacion-cifras`: alrededor de, rondar
- **B7 Riesgo, seguridad y prevención**
  - `no-vaya-a-ser-que`
  - `riesgo-de-que`
  - `a-fin-de-que`
  - `de-producirse`
  - `seguros-coberturas`
- **B8 Normas y trámites públicos**
  - `lenguaje-normativo`: deberá, queda prohibido, el/la solicitante
  - `tramites-lexico`
  - `solicitar-que`
  - `conforme-a`: en virtud de, conforme a
  - `siglas`: IVA, SRI, RUC, IESS; DNI en España
- **B9 Negociar y resolver conflictos**
  - `mensajes-yo`: me preocupa que…, siento que…
  - `entiendo-que`
  - `en-la-medida-en-que`
  - `asumir-responsabilidad`
  - `intereses-posiciones`
- **B10 Repaso y proyecto**
  - `propuesta-presupuesto`
  - `responder-objeciones`

## N10 · C1 (dominio)

Historia (2035): Emma y Mateo fundan Puente, una agencia de turismo responsable e interpretación; conversación natural, humor, debate, escritura extensa, crítica cultural, vida de barrio y mediación (Emma interpreta para turistas en un hospital y en un trámite, B9).

- **B1 Conversación natural**
  - `marcadores-conversacionales`: pues nada, total que, bueno pues
  - `por-cierto`
  - `reacciones-coloquiales`
  - `coloquialismos-regionales`: chévere, bacán, padre
  - `enunciados-suspendidos`: es que…, si yo te contara…
- **B2 Contar historias con maestría**
  - `y-va-y-dice`
  - `cierre-narrativo`
  - `hiperbole`
  - `interjecciones-onomatopeyas`
  - `verbos-expresivos`: se coló, salió disparado
- **B3 Humor, ironía y cultura**
  - `sarcasmo-atenuacion`
  - `juegos-de-palabras`
  - `referencias-culturales`: Mafalda, el Chavo, Gabo
  - `exageracion-coloquial`: un montón, una barbaridad
  - `humor-intercultural`
- **B4 Debate complejo y diplomacia**
  - `no-es-tanto-que`
  - `asi-concesivo`: así me lo pidas…
  - `cortesia-imagen`
  - `es-mas-encima`: es más, encima, para colmo
  - `ni-que`
- **B5 Escritura académica y extensa**
  - `nominalizacion-academica`
  - `integrar-fuentes`
  - `discusion-resultados`
  - `claridad-revision`
  - `conectores-academicos`
- **B6 Proyectos y negocios propios** — el plan de negocio de Puente.
  - `plan-de-negocio`
  - `supondria`
  - `de-no-infinitivo`
  - `de-cara-a`
  - `acuerdos-de-socios`
- **B7 Crítica cultural: cine y literatura**
  - `critica-adjetivacion`
  - `a-la-luz-de`
  - `interpretacion-modal`: podría leerse como…
  - `intertextualidad`
  - `canon-latinoamericano`
- **B8 Vivir en la lengua**
  - `no-queda-otra`
  - `reparar-malentendidos`
  - `vida-de-barrio-andina`: la minga, la junta de vecinos
  - `tramites-complejos`
  - `me-toca`
- **B9 Mediar entre personas y textos** — Emma interpreta para turistas.
  - `mediacion-oral`
  - `resumir-para-terceros`
  - `adaptar-texto`
  - `falsos-amigos`: embarazada, constipado, actualmente
  - `lexico-sanitario-legal`
- **B10 Repaso y proyecto final**
  - `proyecto-final`
  - `autoevaluacion`
