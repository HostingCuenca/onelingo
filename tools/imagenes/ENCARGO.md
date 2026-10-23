# Encargo: biblioteca de imágenes de vocabulario (OneLingo)

895 imágenes en 36 lotes de 25. Cada imagen enseña una palabra y la comparten los 10 idiomas de la app (la de «manzana» sirve para *apple*, *pomme*, *Apfel*, *りんご*…). Están ordenadas por prioridad: primero lo que usan más cursos y en niveles más bajos.

## Cómo se pide (lo escribe la persona)

Un mensaje por lote, por ejemplo:

> Lee `tools/imagenes/ENCARGO.md` y haz el **lote 001**.

## Qué hace la IA en cada lote

1. **Lee este archivo** y busca la sección del lote pedido.
2. **Revisa lo ya generado:** abre `work/imagenes-vocab/GENERADAS.md` y salta las imágenes que ya figuren ahí. Mira 3 o 4 de las últimas imágenes de `work/imagenes-vocab/originales/` (y, si aún no hay, 2 o 3 de `assets/img/situaciones/`) como **referencia de estilo**, para que todo el lote se vea de la misma familia.
3. **Genera las 25 imágenes del lote**, una por fila, siguiendo el **Estilo** de abajo y la columna «Qué dibujar».
4. **Guarda cada imagen** en `work/imagenes-vocab/originales/` con el nombre exacto de la columna «Archivo» y extensión `.png` (por ejemplo `fruit-veg-apple.png`). Sin espacios, sin mayúsculas, sin sufijos. Si una imagen sale mal (texto dentro, varios paneles, otra cosa), vuelve a generarla antes de guardarla.
5. **Anota lo hecho** al final de `work/imagenes-vocab/GENERADAS.md`, una línea por imagen: `- [x] lote 001 · 01 · action-buy`.
6. **Responde con la lista** del lote: número, archivo y ✓ o ✗ (y el motivo de cada ✗).

No toques nada fuera de `work/imagenes-vocab/`. No borres ni sobrescribas imágenes ya guardadas salvo que te lo pidan.

## Estilo (igual para todas)

- Ilustración editorial pintada a mano, textura suave de gouache con grano fino de papel, formas redondeadas y naturales, luz cálida de día.
- Paleta: lavanda, índigo profundo, menta y toques de durazno cálido sobre colores naturales.
- Un solo sujeto principal, centrado, completo, ocupando cerca del 70 % del cuadro.
- Fondo liso blanco roto con un halo lavanda muy suave. Solo hay entorno cuando el ítem es un lugar, una acción, un clima o un momento del día.
- Cuadrado 1:1, 1024 × 1024, PNG.
- Personas: adultas, variadas en edad y origen, expresiones amables y naturales; elegante, ni infantil, ni caricatura, ni fotorrealista.
- NUNCA: texto, letras, números, carteles, etiquetas, logos, marcas, marcas de agua, marcos, bordes, collages ni varios paneles. Nunca personas reales.
- La imagen debe hacer obvio el significado de la palabra para un principiante que no sabe leer el idioma.

## Si se usa ChatGPT en la web en lugar de Codex

ChatGPT web no puede poner el nombre del archivo al descargar. Pega la sección del lote, pídele que genere las imágenes **en el orden de la tabla** y descárgalas en ese orden a `work/imagenes-vocab/lote-NNN/`. Claude las renombra por orden de descarga.

## Lotes


### Lote 001

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `action-buy` | comprar | a young Black woman buying red apples from a market stall vendor and putting them in a bag |
| 02 | `action-get-up` | levantarse | an adult Asian man sitting up in bed in the morning, stretching his arms, about to get up |
| 03 | `action-help` | ayudar | an adult man helping an elderly woman carry her shopping bags |
| 04 | `action-pay` | pagar | an adult Latino man paying with a credit card at a shop payment terminal |
| 05 | `action-rest` | descansar | an adult woman resting relaxed in a hammock under trees, eyes closed |
| 06 | `action-study` | estudiar | a young Indian man studying at a desk with open books and a notebook |
| 07 | `action-work` | trabajar | an adult woman working on a laptop at a desk in an office |
| 08 | `adjective-sweet` | dulce | a spoonful of golden honey dripping, next to a pile of colorful candies |
| 09 | `color-blue` | azul | a bright blue ceramic mug beside a bright blue ball on a plain white background |
| 10 | `home-kitchen` | cocina | a bright home kitchen with a stove, a sink, cabinets and a small table |
| 11 | `place-park` | parque | a green city park with trees, a path and a bench on a sunny day |
| 12 | `place-pharmacy` | farmacia | a pharmacy storefront with a green cross sign and shelves of medicine visible through the window |
| 13 | `shopping-bag` | bolsa | a brown paper shopping bag with handles standing on a white table |
| 14 | `sport-team` | equipo | a group of soccer players in matching jerseys posing together on a field |
| 15 | `transport-bus` | autobús | a yellow city bus driving along a sunny street |
| 16 | `transport-train` | tren | a modern passenger train traveling on railway tracks through the countryside |
| 17 | `weather-rain` | lluvia | heavy rain falling from dark clouds onto a street with puddles |
| 18 | `work-office` | oficina | a modern office with several desks, computers and office chairs, nobody in the room |
| 19 | `action-repair` | reparar | an adult man repairing a bicycle wheel with a wrench in a workshop |
| 20 | `health-cough` | tos | an adult man coughing into his fist, looking unwell |
| 21 | `health-medicine` | medicamento | a bottle of syrup with a measuring spoon next to a blister pack of pills |
| 22 | `job-dentist` | dentista | a female dentist in a white coat and mask examining a patient's teeth |
| 23 | `tech-battery` | batería | three cylindrical AA batteries lined up on a white surface |
| 24 | `travel-luggage` | equipaje | a luggage trolley loaded with several suitcases and bags in an airport hall |
| 25 | `action-cook` | cocinar | an adult Black man cooking vegetables in a frying pan on a stove |

### Lote 002

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `action-cut` | cortar | an adult woman cutting a tomato with a knife on a wooden board |
| 02 | `action-drink` | beber | a young woman drinking a glass of water, glass raised to her lips |
| 03 | `action-eat` | comer | an adult woman eating a bowl of soup at a table |
| 04 | `action-open` | abrir | a young woman opening a wooden door wide, the open doorway clearly visible |
| 05 | `action-read` | leer | an elderly man sitting in an armchair reading a book |
| 06 | `action-run` | correr | an adult woman jogging along a park path in sportswear |
| 07 | `action-sleep` | dormir | an adult man sleeping peacefully in bed under a blanket at night |
| 08 | `action-wait` | esperar | an adult Latina woman sitting on a bench at a bus stop, checking her wristwatch |
| 09 | `action-write` | escribir | a young Black man writing in a notebook with a pen at a desk |
| 10 | `body-back` | espalda | an adult woman seen from behind, showing her bare back, hair tied up |
| 11 | `clothing-jacket` | chaqueta | a blue zip-up jacket displayed on a hanger against a white wall |
| 12 | `clothing-shirt` | camisa | a light blue button-up shirt displayed flat on a white background |
| 13 | `color-black` | negro | a solid black cat sitting next to a black ceramic vase on a white background |
| 14 | `color-green` | verde | a bright green leaf and a green apple on a plain white background |
| 15 | `color-red` | rojo | a bright red apple and a red balloon on a plain white background |
| 16 | `color-white` | blanco | a white dove and a white flower on a plain light gray background |
| 17 | `family-family` | familia | a family of four: mother, father, a boy and a girl, standing together smiling |
| 18 | `family-grandfather` | abuelo | an elderly gray-haired man with glasses sitting with his young grandson on a sofa |
| 19 | `family-grandmother` | abuela | an elderly woman with white hair hugging her young granddaughter, both smiling |
| 20 | `food-sugar` | azúcar | a white bowl of sugar with a spoon and a few sugar cubes |
| 21 | `furniture-sofa` | sofá | a comfortable gray three-seat sofa with two cushions in a living room |
| 22 | `furniture-table` | mesa | a wooden dining table with four chairs in a bright room |
| 23 | `home-living-room` | sala | a cozy living room with a sofa, a coffee table, a lamp and a television |
| 24 | `home-window` | ventana | a large open window with curtains and a view of green trees |
| 25 | `leisure-concert` | concierto | a band playing on a lit stage in front of a cheering crowd |

### Lote 003

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `leisure-music` | música | an adult man playing a piano, with musical notes floating above |
| 02 | `object-box` | caja | a closed brown cardboard box on a wooden floor |
| 03 | `object-key` | llave | a single metal key on a ring, shown close up |
| 04 | `place-bank` | banco | a bank building with stone columns and a large coin symbol above the entrance |
| 05 | `place-city` | ciudad | a large city skyline with tall skyscrapers at sunset |
| 06 | `place-gym` | gimnasio | a gym room with treadmills, weights and exercise machines |
| 07 | `place-hospital` | hospital | a large hospital building with an ambulance parked in front and a red cross sign |
| 08 | `place-hotel` | hotel | a multi-story hotel building with many balconies and a palm tree at the entrance |
| 09 | `place-market` | mercado | an outdoor market with stalls of fruits and vegetables and people shopping |
| 10 | `place-platform` | andén | an empty train station platform with a yellow safety line and a train arriving |
| 11 | `shopping-counter` | mostrador | a shop counter with a cash register and a smiling shopkeeper behind it |
| 12 | `transport-subway` | metro | a subway train stopped at an underground station with open doors |
| 13 | `transport-taxi` | taxi | a yellow taxi car with a roof light driving on a city street |
| 14 | `travel-airport` | aeropuerto | an airport terminal building with a large airplane parked outside |
| 15 | `travel-map` | mapa | a large unfolded paper map with roads, rivers and a red pin, no readable text |
| 16 | `travel-passport` | pasaporte | a closed dark blue passport booklet lying next to an airplane ticket, no readable text |
| 17 | `travel-suitcase` | maleta | a large red suitcase with wheels and a handle standing upright |
| 18 | `adjective-salty` | salado | salt being sprinkled onto a plate of french fries, close up |
| 19 | `health-throat` | garganta | an adult woman holding her throat with one hand, looking in discomfort |
| 20 | `tech-screen` | pantalla | a flat computer monitor on a desk showing a simple colorful landscape picture |
| 21 | `job-actor` | actor | an actor in a costume performing on a theater stage under spotlights |
| 22 | `person-thief` | ladrón | a person in a black mask and gloves sneaking at night carrying a sack |
| 23 | `action-close` | cerrar | an adult man closing a wooden door, the door almost shut, hand on the handle |
| 24 | `action-dance` | bailar | a young couple dancing together happily in a living room |
| 25 | `action-swim` | nadar | an adult man swimming in a swimming pool, arms mid-stroke |

### Lote 004

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `action-walk` | paseo | an elderly couple walking together along a tree-lined path in a park |
| 02 | `adjective-big` | grande | a very large dog next to a tiny dog, emphasis on the large one |
| 03 | `adjective-cold` | frío | a man shivering in a winter coat and scarf standing in falling snow |
| 04 | `adjective-long` | largo | a very long pencil next to a very short pencil, emphasis on the long one |
| 05 | `adjective-small` | pequeño | a tiny dog next to a very large dog, emphasis on the tiny one |
| 06 | `adjective-spicy` | picante | a young man with a red face fanning his open mouth after eating a chili pepper |
| 07 | `animal-dog` | perro | a friendly brown dog sitting on grass looking at the camera |
| 08 | `body-head` | cabeza | the head and shoulders of an adult man seen in profile, smiling |
| 09 | `clothing-sweater` | suéter | a warm green knitted sweater folded on a wooden table |
| 10 | `color-yellow` | amarillo | a bright yellow sunflower and a yellow lemon on a plain white background |
| 11 | `drink-milk` | leche | a glass of milk and a milk bottle on a wooden table |
| 12 | `drink-tea` | té | a cup of hot tea with a teapot and steam rising |
| 13 | `food-cake` | pastel | a round chocolate cake with white frosting and strawberries on a cake stand |
| 14 | `food-dessert` | postre | an ice cream sundae with chocolate sauce and a cherry in a glass cup |
| 15 | `food-fish` | pescado | a grilled fish served on a white plate with lemon slices |
| 16 | `food-lunch` | almuerzo | a plate of rice, grilled chicken and salad on a table at midday |
| 17 | `food-rice` | arroz | a white bowl full of steamed white rice with chopsticks |
| 18 | `food-soup` | sopa | a steaming bowl of vegetable soup with a spoon |
| 19 | `furniture-bed` | cama | a double bed with white sheets and two pillows in a bedroom |
| 20 | `home-bathroom` | baño | a bathroom with a sink, a mirror, a toilet and a bathtub |
| 21 | `home-bedroom` | dormitorio | a cozy bedroom with a bed, a nightstand with a lamp and a wardrobe |
| 22 | `home-door` | puerta | a closed wooden front door with a metal handle |
| 23 | `kitchen-pot` | olla | a large metal cooking pot with a lid on a stove |
| 24 | `leisure-birthday` | cumpleaños | a young child about to blow out candles on a birthday cake, friends smiling around |
| 25 | `leisure-party` | fiesta | friends dancing at a party with balloons, confetti and colorful lights |

### Lote 005

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `leisure-photo` | foto | an adult woman taking a photo with a camera outdoors |
| 02 | `object-bottle` | botella | a clear plastic water bottle with a blue cap, standing on a table |
| 03 | `object-elevator` | ascensor | an elevator with open metal doors and a button panel inside a building lobby |
| 04 | `object-gift` | regalo | a gift box wrapped in colorful paper with a ribbon and bow |
| 05 | `object-light` | luz | a glowing light bulb hanging from a ceiling in a dark room |
| 06 | `object-umbrella` | paraguas | an open red umbrella shielding a person from rain |
| 07 | `object-wallet` | billetera | a brown leather wallet with a few banknotes sticking out |
| 08 | `place-intersection` | cruce | a city street intersection with crosswalks, cars and traffic lights viewed from above |
| 09 | `place-museum` | museo | a museum building with columns and visitors looking at paintings in a gallery |
| 10 | `place-street` | calle | a quiet city street with buildings, parked cars and a sidewalk |
| 11 | `school-pen` | bolígrafo | a blue ballpoint pen lying on a white notebook |
| 12 | `shopping-store` | tienda | a small clothing store front with a display window and a few mannequins |
| 13 | `sport-yoga` | yoga | an adult woman doing a yoga tree pose on a mat in a calm room |
| 14 | `time-morning` | mañana | sunrise over a house and hills, a person stretching at an open window |
| 15 | `transport-bicycle` | bicicleta | a blue bicycle parked against a wall |
| 16 | `transport-car` | carro | a red passenger car parked on a street |
| 17 | `transport-traffic-light` | semáforo | a traffic light on a pole showing a red light |
| 18 | `adjective-heavy` | pesado | a man straining to lift a huge heavy stone with both arms |
| 19 | `body-leg` | pierna | a person's bare leg from hip to foot, standing on one leg |
| 20 | `home-balcony` | balcón | a small apartment balcony with a railing, potted plants and two chairs |
| 21 | `home-faucet` | grifo | a kitchen faucet with water running into a sink |
| 22 | `home-washing-machine` | lavadora | a front-loading washing machine with clothes visible through the round door |
| 23 | `object-sunscreen` | protector solar | a bottle of sunscreen lotion next to sunglasses on a beach towel |
| 24 | `tech-charger` | cargador | a phone charger plugged into a wall socket with a cable attached to a smartphone |
| 25 | `transport-tire` | llanta | a black car tire mounted on a metal wheel, close up |

### Lote 006

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `action-clean` | limpiar | an adult Latino man mopping a floor with a mop and bucket |
| 02 | `action-give` | dar | an adult man handing a wrapped gift to a smiling woman |
| 03 | `action-turn-off` | apagar | an adult hand switching off a lamp at night, the room turning dark |
| 04 | `action-turn-on` | encender | an adult hand switching on a lamp, the room filled with warm light |
| 05 | `action-wash` | lavar | a young woman washing her hands with soap under a running tap |
| 06 | `adjective-short` | corto | a very short pencil next to a very long pencil, emphasis on the short one |
| 07 | `body-hair` | pelo | a woman's long wavy brown hair seen from the side |
| 08 | `clothing-pants` | pantalón | a pair of dark blue jeans laid flat on a white background |
| 09 | `clothing-skirt` | falda | a red pleated skirt displayed on a hanger |
| 10 | `drink-juice` | jugo | a tall glass of orange juice with two oranges beside it |
| 11 | `family-father` | padre | a smiling father carrying his young daughter on his shoulders in a park |
| 12 | `family-mother` | madre | a smiling mother holding her baby in her arms |
| 13 | `food-bread` | pan | a golden loaf of bread and a few bread rolls on a wooden board |
| 14 | `food-breakfast` | desayuno | a breakfast table with eggs, toast, orange juice and coffee in the morning |
| 15 | `food-dinner` | cena | a family sitting around a dinner table with plates of food in the evening |
| 16 | `food-meat` | carne | a raw red steak on a wooden cutting board with a knife |
| 17 | `food-salt` | sal | a salt shaker spilling a little white salt onto a table |
| 18 | `fruit-veg-fruit` | fruta | a bowl full of mixed fruit: apples, bananas, oranges and grapes |
| 19 | `fruit-veg-tomato` | tomate | three ripe red tomatoes with a green stem on a wooden table |
| 20 | `fruit-veg-vegetables` | verduras | a basket of fresh vegetables: carrots, broccoli, peppers and lettuce |
| 21 | `home-shower` | ducha | a shower with glass walls and water falling from the shower head |
| 22 | `job-driver` | conductor | a bus driver wearing a uniform seated at the steering wheel |
| 23 | `job-teacher` | profesor | a female teacher standing at a whiteboard in a classroom, explaining to students |
| 24 | `kitchen-oil` | aceite | a glass bottle of olive oil next to a small bowl of oil and olives |
| 25 | `kitchen-refrigerator` | refrigerador | a tall silver refrigerator with its door open showing food inside |

### Lote 007

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `leisure-picnic` | picnic | a family picnic on a blanket with a basket and food on green grass |
| 02 | `nature-beach` | playa | a sandy beach with turquoise water, palm trees and a few umbrellas |
| 03 | `nature-lake` | lago | a calm blue lake surrounded by mountains and green trees |
| 04 | `object-backpack` | mochila | a green backpack with two shoulder straps standing on the ground |
| 05 | `object-money` | dinero | a pile of banknotes and coins on a table |
| 06 | `place-bridge` | puente | a long stone bridge crossing a wide river |
| 07 | `place-house` | casa | a single-family house with a red roof, a garden and a front door |
| 08 | `place-library` | biblioteca | a library interior with tall shelves full of books and reading tables |
| 09 | `place-post-office` | correo | a post office building with a mailbox in front and a delivery van |
| 10 | `place-road` | camino | a long winding country road with fields on both sides |
| 11 | `place-square` | plaza | a city square with a fountain in the center, pigeons and people walking |
| 12 | `shopping-supermarket` | supermercado | a supermarket aisle with shelves of products and a shopping cart |
| 13 | `sport-exercise` | ejercicio | a young woman doing push-ups on a gym mat |
| 14 | `tech-computer` | computadora | a desktop computer with a monitor, a keyboard and a mouse on a desk |
| 15 | `transport-airplane` | avión | a white passenger airplane flying in a clear blue sky |
| 16 | `travel-front-desk` | recepción | a hotel receptionist standing behind a reception desk handing a key to a guest |
| 17 | `weather-snow` | nieve | snow falling on a street and rooftops, thick white snow on the ground |
| 18 | `weather-summer` | verano | a hot sunny summer day with a bright sun and people on a beach |
| 19 | `weather-winter` | invierno | a snowy winter landscape with bare trees and a snow-covered house |
| 20 | `action-mix` | mezclar | an adult man mixing batter in a large bowl with a wooden spoon |
| 21 | `adjective-sour` | ácido | a young woman puckering her face while biting into a lemon slice |
| 22 | `body-knee` | rodilla | a close-up of a bent human knee on a person sitting |
| 23 | `health-fever` | fiebre | a woman in bed with a thermometer in her mouth, looking sick and flushed |
| 24 | `health-tablet` | pastilla | a few white round pills in a hand next to a glass of water |
| 25 | `leisure-wedding` | boda | a bride in a white dress and a groom in a suit smiling, holding hands |

### Lote 008

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `transport-breakdown` | avería | a car broken down at the roadside with its hood open and steam rising |
| 02 | `weather-sun` | sol | a bright yellow sun shining in a clear blue sky |
| 03 | `weather-wind` | viento | strong wind bending trees and blowing leaves, a kite flying in the sky |
| 04 | `job-singer` | cantante | a woman singing into a microphone on stage under a spotlight |
| 05 | `place-gas-station` | gasolinera | a gas station with fuel pumps and a car being filled with gasoline |
| 06 | `transport-engine` | motor | a car engine under an open hood, shown close up |
| 07 | `nature-pollution` | contaminación | factory chimneys releasing thick gray smoke over a city under a gray sky |
| 08 | `action-cross` | cruzar | a young man crossing a street at a zebra crosswalk, looking both ways |
| 09 | `action-go-to-bed` | acostarse | an adult man in pajamas getting into bed at night, bedside lamp on |
| 10 | `action-listen` | escuchar | an adult woman with eyes closed wearing headphones, listening attentively |
| 11 | `action-tidy-up` | ordenar | a young woman putting toys into a basket to tidy a messy room |
| 12 | `adjective-hot` | caliente | a sweating man fanning himself under a blazing sun in summer clothes |
| 13 | `adjective-new` | nuevo | a brand-new shiny bicycle with a red ribbon on the handlebar |
| 14 | `adjective-old` | viejo | an old rusty weathered bicycle with peeling paint leaning on a wall |
| 15 | `adjective-tall` | alto | a very tall man standing next to a short boy, emphasis on the tall man |
| 16 | `animal-cat` | gato | an orange tabby cat sitting on a windowsill |
| 17 | `body-tooth` | diente | a single white tooth shown close up, with a toothbrush beside it |
| 18 | `clothing-dress` | vestido | a long yellow summer dress displayed on a hanger |
| 19 | `clothing-shoes` | zapatos | a pair of brown leather shoes standing on the floor |
| 20 | `clothing-t-shirt` | camiseta | a plain white short-sleeved t-shirt displayed flat on a white background |
| 21 | `emotion-shy` | tímido | a young girl blushing and hiding half of her face behind her hands |
| 22 | `emotion-tired` | cansado | a young man's face looking very tired, yawning with heavy eyes |
| 23 | `food-flour` | harina | a paper bag of white flour with a wooden scoop and flour spilled on a table |
| 24 | `food-sandwich` | sándwich | a sandwich with ham, cheese, lettuce and tomato on a plate |
| 25 | `fruit-veg-apple` | manzana | a shiny red apple with a green leaf on a white background |

### Lote 009

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `fruit-veg-onion` | cebolla | a whole brown onion and a halved onion on a wooden board |
| 02 | `furniture-chair` | silla | a simple wooden chair on a plain white floor |
| 03 | `home-apartment` | departamento | a small bright apartment interior with a sofa, a kitchen corner and a window |
| 04 | `job-doctor` | médico | a doctor in a white coat with a stethoscope around the neck, smiling |
| 05 | `job-engineer` | ingeniero | an engineer in a hard hat and safety vest looking at blueprints on a construction site |
| 06 | `job-nurse` | enfermera | a female nurse in blue scrubs smiling, holding a clipboard in a hospital |
| 07 | `kitchen-frying-pan` | sartén | a black frying pan with a handle on a stove |
| 08 | `kitchen-knife` | cuchillo | a kitchen knife with a steel blade lying on a wooden board |
| 09 | `leisure-guitar` | guitarra | an acoustic wooden guitar leaning against a chair |
| 10 | `leisure-toy` | juguete | a colorful toy car and a teddy bear on a play mat |
| 11 | `nature-mountain` | montaña | a tall snow-capped mountain above green hills and a lake |
| 12 | `nature-sea` | mar | a wide blue sea with waves under a clear sky |
| 13 | `place-building` | edificio | a tall modern office building with glass windows |
| 14 | `place-restaurant` | restaurante | a restaurant interior with set tables, chairs and a waiter walking |
| 15 | `school-classroom` | aula | a classroom with rows of desks, a whiteboard and a teacher's desk |
| 16 | `school-notebook` | cuaderno | a closed spiral notebook with a blue cover and a pencil on top |
| 17 | `shopping-fitting-room` | probador | a clothing store fitting room with a curtain, a mirror and clothes on a hook |
| 18 | `sport-swimming` | natación | a swimmer competing in a pool lane, mid-stroke with splashing water |
| 19 | `tech-cell-phone` | celular | a smartphone held in a hand, screen glowing with simple colorful icons |
| 20 | `transport-boat` | barco | a small white sailboat on calm blue sea |
| 21 | `transport-bus-stop` | parada de autobús | a bus stop shelter with a bench and a bus approaching |
| 22 | `transport-traffic-jam` | embotellamiento | a long line of cars stuck in traffic on a busy highway |
| 23 | `travel-vacation` | vacaciones | an adult couple relaxing on lounge chairs by a swimming pool with a suitcase nearby |
| 24 | `action-fall` | caer | a man slipping on a banana peel on the pavement, falling backward |
| 25 | `adjective-broken` | roto | a white ceramic cup broken into pieces on a table |

### Lote 010

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `adjective-soft` | suave | a fluffy white pillow being gently pressed by a hand, soft texture |
| 02 | `body-hand` | mano | an open adult hand with five fingers spread, palm up |
| 03 | `body-stomach` | estómago | an adult man holding his stomach with both hands, torso shown |
| 04 | `clothing-sneakers` | tenis | a pair of white athletic sneakers with laces on a plain background |
| 05 | `health-patient` | paciente | a patient lying in a hospital bed while a nurse checks on him |
| 06 | `health-waiting-room` | sala de espera | a clinic waiting room with rows of chairs and a few patients sitting |
| 07 | `home-heating` | calefacción | a white wall radiator beneath a window in a warm room |
| 08 | `job-plumber` | plomero | a plumber in overalls fixing a pipe under a sink with a wrench |
| 09 | `job-technician` | técnico | a technician in uniform repairing an air conditioning unit on a wall |
| 10 | `kitchen-oven` | horno | a kitchen oven with its door open showing a baking tray with bread |
| 11 | `object-trash` | basura | an open trash bin full of garbage bags beside a street curb |
| 12 | `emotion-nervous` | nervioso | a young man biting his nails and sweating, looking nervous |
| 13 | `health-dental-floss` | hilo dental | a box of dental floss and a toothbrush on a bathroom shelf |
| 14 | `health-toothbrush` | cepillo de dientes | a blue toothbrush with toothpaste on its bristles |
| 15 | `job-flight-attendant` | auxiliar de vuelo | a flight attendant in a uniform serving a drink to a passenger on an airplane |
| 16 | `job-police-officer` | policía | a police officer in uniform and cap standing next to a police car |
| 17 | `job-referee` | árbitro | a soccer referee blowing a whistle and holding up a yellow card on a field |
| 18 | `object-blanket` | manta | a thick folded wool blanket with a checkered pattern on a bed |
| 19 | `transport-seat-belt` | cinturón de seguridad | a driver fastening a seat belt across the chest in a car |
| 20 | `transport-tow-truck` | grúa | a tow truck lifting a broken-down car on its flatbed |
| 21 | `work-tool` | herramienta | a toolbox with a hammer, screwdriver and wrench laid on a workbench |
| 22 | `action-get-dressed` | vestirse | an adult man buttoning his shirt in front of a wardrobe at home |
| 23 | `animal-pet` | mascota | a child hugging a dog and a cat at home |
| 24 | `body-eyes` | ojos | a close-up of a person's two open brown eyes |
| 25 | `clothing-coat` | abrigo | a long dark wool coat on a hanger |

### Lote 011

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `clothing-glasses` | lentes | a pair of black-framed eyeglasses folded on a table |
| 02 | `clothing-hat` | sombrero | a straw hat with a wide brim on a table |
| 03 | `clothing-scarf` | bufanda | a long red wool scarf wrapped around a neck stand |
| 04 | `emotion-happy` | feliz | a young woman's face with a big smile and bright joyful eyes |
| 05 | `emotion-sad` | triste | a young woman's face looking very sad with tears running down her cheeks |
| 06 | `food-egg` | huevo | a white egg next to a fried egg on a plate |
| 07 | `food-food` | comida | a table with bread, fruit, cheese, vegetables and a pitcher of water |
| 08 | `fruit-veg-carrot` | zanahoria | three fresh orange carrots with green tops on a wooden table |
| 09 | `fruit-veg-potato` | papa | three brown potatoes, one cut in half, on a wooden board |
| 10 | `home-lamp` | lámpara | a table lamp with a white shade glowing on a nightstand |
| 11 | `job-waiter` | mesero | a waiter in a white shirt and black apron carrying plates in a restaurant |
| 12 | `leisure-fireworks` | fuegos artificiales | colorful fireworks exploding in the night sky above a city |
| 13 | `nature-countryside` | campo | green rolling countryside with fields, a barn and a dirt road |
| 14 | `object-package` | paquete | a brown cardboard parcel tied with string, ready to be mailed |
| 15 | `person-child` | niño | a young boy about six years old playing with building blocks |
| 16 | `person-student` | estudiante | a young woman student with a backpack carrying books across a campus |
| 17 | `place-cafe` | cafetería | a cozy café with small tables, a counter and cups of coffee |
| 18 | `place-movie-theater` | cine | a cinema auditorium with red seats facing a large white screen |
| 19 | `place-parking-lot` | estacionamiento | a parking lot filled with rows of parked cars seen from above |
| 20 | `place-university` | universidad | a large university building with columns, wide stairs and students outside |
| 21 | `school-pencil` | lápiz | a yellow wooden pencil with an eraser, sharpened, on a white surface |
| 22 | `sport-match` | partido | two teams playing a soccer match on a grass field with a crowd in the stands |
| 23 | `sport-tennis` | tenis | an adult man hitting a tennis ball with a racket on a court |
| 24 | `time-afternoon` | tarde | a sunny late afternoon street with golden light and children walking home from school |
| 25 | `time-midnight` | medianoche | a dark night sky with a bright full moon over a sleeping town and a clock at twelve |

### Lote 012

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `time-night` | noche | a dark night sky full of stars over a quiet town with lit windows |
| 02 | `time-noon` | mediodía | a bright sun directly overhead at midday, short shadows beneath a tree |
| 03 | `transport-station` | estación | a train station building with a clock tower and travelers on the platform |
| 04 | `weather-spring` | primavera | a spring garden with blooming trees, flowers and a light blue sky |
| 05 | `action-draw` | dibujar | an adult woman drawing a house on paper with a pencil at a table |
| 06 | `action-fix` | arreglar | an adult man fixing a bicycle wheel with a wrench in a workshop |
| 07 | `action-measure` | medir | an adult man measuring the length of a wooden board with a tape measure |
| 08 | `action-toast` | brindis | two adult friends clinking glasses of sparkling drink in a toast at a table |
| 09 | `adjective-full` | lleno | a tall glass completely full of orange juice, filled to the brim, plain background |
| 10 | `body-arm` | brazo | a person's bare arm bent at the elbow, flexing a muscle |
| 11 | `body-shoulder` | hombro | a man's bare shoulder highlighted from behind, upper back and arm visible, plain background |
| 12 | `clothing-boots` | botas | a pair of brown leather boots standing on the ground |
| 13 | `clothing-sandals` | sandalias | a pair of brown leather summer sandals on a sandy beach |
| 14 | `emotion-relieved` | aliviado | an adult woman exhaling with a relieved smile, eyes closed, hand on her chest |
| 15 | `health-pill` | pastilla | a single white round pill next to a glass of water on a table |
| 16 | `health-syrup` | jarabe | a brown bottle of cough syrup next to a measuring spoon filled with syrup |
| 17 | `health-temperature` | temperatura | a glass thermometer showing a high fever temperature next to a hand |
| 18 | `home-hallway` | pasillo | a long empty indoor hallway with several closed doors and a rug on the floor |
| 19 | `home-stairs` | escalera | an indoor wooden staircase with a railing leading up to the next floor |
| 20 | `home-towel` | toalla | a folded fluffy blue bath towel hanging on a rail in a bathroom |
| 21 | `job-coach` | entrenador | a sports coach with a whistle and a clipboard standing beside a field |
| 22 | `job-pharmacist` | farmacéutico | a smiling adult man in a white coat behind a pharmacy counter handing over a medicine box |
| 23 | `job-trainer` | entrenador | a muscular adult woman fitness trainer with a whistle in a gym |
| 24 | `object-recycling` | reciclaje | three colored recycling bins with bottles, paper and cans beside them |
| 25 | `object-wool` | lana | several colorful balls of wool yarn with knitting needles in a basket |

### Lote 013

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `place-police-station` | comisaría | a small police station building with a police car parked in front, no readable text |
| 02 | `sport-warm-up` | calentamiento | a group of adults doing arm and leg stretching warm-up exercises on a sports field |
| 03 | `tech-cable` | cable | a black electrical cable coiled with a plug at one end |
| 04 | `tech-router` | router | a white wifi router with antennas and small green lights on a shelf |
| 05 | `transport-traffic` | tráfico | a busy city road full of cars stuck in a traffic jam |
| 06 | `weather-cloudy` | nublado | a gray sky completely covered with thick clouds over a quiet field |
| 07 | `action-hug` | abrazo | two adults hugging warmly outdoors, eyes closed, smiling |
| 08 | `job-mechanic` | mecánico | a smiling adult man in overalls repairing a car engine in a garage |
| 09 | `job-police` | policía | a female police officer in uniform standing next to a patrol car |
| 10 | `leisure-band` | banda | a four-piece band with a singer, guitarist, bassist and drummer playing on a stage |
| 11 | `leisure-beach-umbrella` | sombrilla | a striped beach umbrella planted in sand with two beach chairs under it |
| 12 | `person-fan` | hincha | a cheering adult sports fan with painted face and scarf raising arms in a stadium |
| 13 | `sport-volleyball` | voleibol | two players jumping at a net to hit a volleyball on a beach court |
| 14 | `action-boil` | hervir | a pot of water boiling with bubbles and steam on a stove |
| 15 | `action-sell` | vender | a market vendor woman handing a bag of fruit to a customer across a stall |
| 16 | `action-sing` | cantar | a young adult man singing into a microphone with mouth open on a small stage |
| 17 | `action-take-a-shower` | ducharse | an adult man taking a shower under running water in a bathroom, shoulders visible |
| 18 | `action-wake-up` | despertarse | an adult woman waking up in bed, stretching her arms as morning light comes through a window |
| 19 | `body-foot` | pie | a bare human foot seen from the side on a plain light background |
| 20 | `body-teeth` | dientes | a close-up of a smiling mouth showing a row of white teeth |
| 21 | `clothing-clothes` | ropa | a variety of clothes hanging on a rack: shirts, trousers, a dress and a jacket |
| 22 | `clothing-shoe` | zapato | a single black leather lace-up shoe on a plain background |
| 23 | `color-brown` | marrón | a solid brown color swatch next to a brown wooden block and a chocolate bar |
| 24 | `food-butter` | mantequilla | a block of yellow butter with a butter knife on a small plate |
| 25 | `food-cheese` | queso | a wedge of yellow cheese with holes next to a wheel of cheese |

### Lote 014

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `food-salad` | ensalada | a bowl of fresh green salad with tomato, cucumber and lettuce |
| 02 | `fruit-veg-banana` | banana | a bunch of ripe yellow bananas on a white table |
| 03 | `home-air-conditioner` | aire acondicionado | a white wall-mounted air conditioner unit blowing cool air in a living room |
| 04 | `home-alarm-clock` | despertador | a classic round alarm clock with two bells ringing on a bedside table |
| 05 | `kitchen-cup` | taza | a white ceramic cup of hot coffee on a saucer with steam rising |
| 06 | `kitchen-spoon` | cuchara | a silver soup spoon lying on a wooden table |
| 07 | `leisure-piano` | piano | an upright brown piano with open keys in a bright room |
| 08 | `nature-river` | río | a wide river flowing through green hills under a blue sky |
| 09 | `object-clock` | reloj | a round wall clock with hour and minute hands on a plain wall |
| 10 | `person-friends` | amigos | a group of diverse adult friends laughing together on a sofa |
| 11 | `person-tourist` | turista | an adult tourist with a camera, sun hat and backpack looking at a map in front of a monument |
| 12 | `place-factory` | fábrica | a large industrial factory building with tall chimneys releasing white steam |
| 13 | `place-sidewalk` | acera | an empty city sidewalk beside a street with a curb and a lamp post |
| 14 | `place-stadium` | estadio | a large sports stadium seen from outside with a packed oval grandstand and a green pitch |
| 15 | `place-train-station` | estación de tren | a train station platform with a train waiting and travelers walking, no readable text |
| 16 | `place-village` | pueblo | a small village of a few houses with red roofs among green fields |
| 17 | `school-board` | pizarra | a green school blackboard on a classroom wall with chalk and an eraser, no writing |
| 18 | `shopping-cash` | efectivo | a hand holding a few banknotes and coins, no readable numbers |
| 19 | `shopping-shop` | tienda | a small neighborhood shop with an open door and goods displayed in the window, no readable text |
| 20 | `sport-basketball` | básquetbol | a player jumping to shoot an orange basketball toward a hoop on an indoor court |
| 21 | `sport-hike` | hacer senderismo | two adult hikers with backpacks and walking sticks on a mountain trail |
| 22 | `tech-atm` | cajero automático | a street ATM machine with screen and keypad set into a building wall, no readable text |
| 23 | `action-hang` | colgar | an adult woman hanging a framed picture on a wall |
| 24 | `action-stretch` | estirar | an adult woman stretching her arms high above her head in a park |
| 25 | `adjective-strong` | fuerte | a very muscular man lifting a heavy barbell overhead, emphasis on strength |

### Lote 015

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `body-muscle` | músculo | a man flexing his arm to show a strong biceps muscle |
| 02 | `clothing-heel` | tacón | a single red high-heeled shoe seen from the side |
| 03 | `food-barbecue` | barbacoa | a charcoal barbecue grill with sausages and meat cooking over flames |
| 04 | `food-main-course` | plato fuerte | a plate with grilled chicken, rice and vegetables served as a main course |
| 05 | `food-sauce` | salsa | a bowl of red tomato sauce with a spoon beside a plate of pasta |
| 06 | `health-bandage` | curita | an adhesive bandage applied on a child's knee |
| 07 | `health-headache` | dolor de cabeza | an adult woman with her hands on her forehead, eyes closed in pain, suffering a headache |
| 08 | `health-ointment` | pomada | a small tube of ointment with a bit of cream squeezed out beside it |
| 09 | `health-painkiller` | analgésico | a blister pack of white painkiller tablets with a glass of water |
| 10 | `home-garage` | garaje | a home garage with an open door and a car parked inside |
| 11 | `home-hot-water` | agua caliente | a bathroom tap pouring steaming hot water into a sink |
| 12 | `home-toilet` | inodoro | a clean white toilet in a bathroom with tiled wall |
| 13 | `home-wall` | pared | a plain white interior wall with a wooden floor and a small plant at its base |
| 14 | `home-water-heater` | calentador de agua | a white cylindrical water heater tank mounted on a wall with pipes |
| 15 | `home-yard` | patio | a house backyard with grass lawn, a tree and a wooden fence |
| 16 | `job-guide` | guía | an adult tour guide with a flag leading a small group of tourists in a city square |
| 17 | `job-secretary` | secretario | an adult man secretary at an office desk answering a phone call and typing |
| 18 | `kitchen-plate` | plato | an empty white round dinner plate on a wooden table |
| 19 | `nature-island` | isla | a small tropical island with palm trees surrounded by turquoise sea |
| 20 | `nature-landscape` | paisaje | a wide landscape of mountains, a lake and green meadows at sunset |
| 21 | `object-balloon` | globo | a bunch of colorful inflated party balloons tied with strings |
| 22 | `object-plug` | enchufe | an electric plug with two prongs next to a wall socket |
| 23 | `shopping-credit-card` | tarjeta de crédito | a blue plastic credit card with a chip, no readable text, held in a hand |
| 24 | `sport-treadmill` | caminadora | a person running on a treadmill in a gym |
| 25 | `tech-headphones` | audífonos | a pair of black over-ear headphones on a plain background |

### Lote 016

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `travel-ticket-window` | taquilla | a ticket booth window with a clerk behind glass and a person buying a ticket, no readable text |
| 02 | `weather-cloud` | nube | a fluffy white cloud floating in a blue sky |
| 03 | `action-press` | presionar | a finger pressing a round red button on a panel |
| 04 | `action-slip` | resbalar | an adult man slipping on a wet floor with arms flung up near a yellow wet-floor sign without text |
| 05 | `emotion-cheerful` | alegre | a young woman's face with a very cheerful bright smile and sparkling eyes |
| 06 | `emotion-disappointed` | decepcionado | a young man's face looking disappointed, frowning with his head tilted down |
| 07 | `emotion-get-angry` | enojarse | an adult man's face looking very angry, red, frowning and clenching teeth |
| 08 | `emotion-worried` | preocupado | a middle-aged woman's face looking worried, eyebrows raised and biting her lip |
| 09 | `family-grandparents` | abuelos | an elderly man and an elderly woman with gray hair sitting together with a young grandchild |
| 10 | `health-toothpaste` | pasta de dientes | a tube of toothpaste squeezed onto a toothbrush |
| 11 | `health-x-ray` | radiografía | an x-ray image of a human chest and ribs on a light box |
| 12 | `home-pipe` | tubería | a set of metal water pipes with a valve under a sink |
| 13 | `object-parcel` | paquete | a brown cardboard parcel tied with string on a doorstep |
| 14 | `object-screwdriver` | destornillador | a screwdriver with a red handle lying on a wooden workbench |
| 15 | `person-crowd` | multitud | a large crowd of many people gathered together in a city square |
| 16 | `person-pedestrian` | peatón | an adult pedestrian crossing a street at a zebra crossing while cars wait |
| 17 | `sport-marathon` | maratón | a group of runners in sportswear running along a city street in a marathon |
| 18 | `sport-player` | jugador | a soccer player in a jersey kicking a ball on a grass field |
| 19 | `tech-remote-control` | control remoto | a black TV remote control with buttons held in a hand in front of a television |
| 20 | `weather-flood` | inundación | a flooded street with brown water covering the road up to the car doors |
| 21 | `action-recycle` | reciclar | an adult woman putting a plastic bottle into a green recycling bin |
| 22 | `job-lifeguard` | salvavidas | an adult lifeguard sitting on a tall lifeguard tower watching the beach, with a red float |
| 23 | `nature-wave` | ola | a large blue ocean wave curling and breaking with white foam |
| 24 | `object-lock` | cerradura | a metal door lock with a key inserted in a wooden door |
| 25 | `sport-medal` | medalla | a gold medal with a ribbon hanging on a podium |

### Lote 017

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `weather-drought` | sequía | a dry cracked brown earth field under a hot sun with a dead tree |
| 02 | `action-bake` | hornear | an adult man taking a tray of freshly baked bread out of an oven |
| 03 | `action-go-up` | subir | an adult woman walking up a flight of stairs carrying a bag |
| 04 | `action-have-breakfast` | desayunar | a young adult man having breakfast at a table with coffee, bread and eggs |
| 05 | `action-photograph` | fotografiar | an adult woman taking a photo with a camera of a mountain view |
| 06 | `action-sit-down` | sentarse | an adult man sitting down onto a wooden chair at a table |
| 07 | `action-stir-fry` | saltear | an adult man stir-frying vegetables in a wok over a flame |
| 08 | `adjective-closed` | cerrado | a shop door firmly closed and locked with shutters pulled down, no text |
| 09 | `adjective-fast` | rápido | a cheetah sprinting at full speed beside a tiny slow turtle, emphasis on the fast cheetah |
| 10 | `adjective-wide` | ancho | a very wide door next to a narrow door, emphasis on the wide one |
| 11 | `body-eye` | ojo | a close-up of a human open eye with eyelashes and a brown iris |
| 12 | `color-gray` | gris | a solid gray color swatch next to a gray stone and a gray elephant |
| 13 | `food-chocolate` | chocolate | a bar of dark chocolate partly unwrapped with a few squares broken off |
| 14 | `food-jam` | mermelada | a glass jar of strawberry jam with a spoon and a slice of toast |
| 15 | `food-pizza` | pizza | a whole round pizza with melted cheese and tomato slices |
| 16 | `food-yogurt` | yogur | a glass cup of white yogurt topped with berries and a spoon |
| 17 | `fruit-veg-orange` | naranja | a whole orange next to a cut half orange showing the segments |
| 18 | `home-candle` | vela | a lit white candle with a small flame on a holder |
| 19 | `home-picture` | cuadro | a framed painting of a landscape hanging on a living room wall |
| 20 | `home-tap` | grifo | a chrome kitchen tap with water running into a sink |
| 21 | `kitchen-bowl` | tazón | a deep white ceramic bowl filled with cereal and milk |
| 22 | `kitchen-chopsticks` | palillos | a pair of wooden chopsticks resting on a bowl of rice |
| 23 | `person-baby` | bebé | a smiling baby sitting on a blanket and holding a toy |
| 24 | `person-girl` | chica | a smiling teenage girl with long dark hair standing outdoors |
| 25 | `person-man` | hombre | an adult man with short hair and a beard smiling, upper body portrait |

### Lote 018

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `person-woman` | mujer | an adult woman with curly hair smiling, upper body portrait |
| 02 | `place-bakery` | panadería | a bakery storefront with shelves of bread and pastries in the window, no readable text |
| 03 | `place-church` | iglesia | a stone church with a bell tower and arched wooden doors |
| 04 | `place-crosswalk` | paso de peatones | a zebra crosswalk painted on an empty road with a traffic light nearby |
| 05 | `place-downtown` | centro | a downtown city center with tall office buildings and busy streets |
| 06 | `place-garden` | jardín | a home garden with flower beds, green lawn and a small path |
| 07 | `place-town-hall` | alcaldía | a stately town hall building with columns, a clock tower and a flag |
| 08 | `plant-flower` | flor | a single red flower with green stem and leaves in a field |
| 09 | `school-diploma` | diploma | a rolled diploma tied with a red ribbon next to a graduation cap |
| 10 | `school-textbook` | libro de texto | a thick closed textbook with a blue cover on a school desk with a pencil |
| 11 | `shopping-checkout` | caja | a supermarket checkout counter with a cashier scanning groceries for a customer |
| 12 | `shopping-shopping` | compras | an adult woman walking down a street carrying several colorful shopping bags |
| 13 | `sport-ball` | pelota | a round red rubber ball on a grass lawn |
| 14 | `transport-bike` | bicicleta | a city bicycle with two wheels and handlebars parked against a wall |
| 15 | `weather-sunny` | soleado | a bright sunny day with a blue sky and a shining sun over a green park |
| 16 | `action-camp` | acampar | two adults setting up a tent in a forest clearing |
| 17 | `action-go-down` | bajar | an adult man walking down a flight of stairs holding the railing |
| 18 | `action-graduate` | graduarse | a young adult in a cap and gown throwing the cap in the air at graduation |
| 19 | `action-lift` | levantar | an adult man lifting a heavy cardboard box off the floor |
| 20 | `action-serve` | servir | a waiter placing a plate of pasta on a restaurant table in front of a customer |
| 21 | `action-sweat` | sudar | a young man jogging outdoors with sweat dripping from his forehead, wiping his brow |
| 22 | `action-waiting` | esperando | a woman standing at a bus stop looking at her wristwatch while waiting |
| 23 | `action-walking` | caminando | an elderly man walking along a park path with trees, side view |
| 24 | `body-ear` | oído | a close-up side view of a human ear on a plain background |
| 25 | `body-waist` | cintura | an adult's torso from chest to hips with a hand resting on the waist, plain background |

### Lote 019

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `clothing-gloves` | guantes | a pair of warm knitted winter gloves on a table |
| 02 | `clothing-pocket` | bolsillo | close-up of blue jeans with a front pocket and a hand sliding into it |
| 03 | `clothing-swimsuit` | traje de baño | a blue one-piece swimsuit and swim trunks laid out on a beach towel |
| 04 | `food-snack` | refrigerio | a small plate with crackers, cheese slices and apple wedges, simple light snack |
| 05 | `furniture-shelf` | estante | a wooden wall shelf holding a few books and a small potted plant |
| 06 | `furniture-wardrobe` | armario | a tall wooden wardrobe with doors open showing clothes on hangers |
| 07 | `health-blood-pressure` | presión arterial | a doctor measuring a patient's blood pressure with an arm cuff |
| 08 | `health-checkup` | revisión | a doctor with a stethoscope examining a seated middle-aged male patient |
| 09 | `home-doorbell` | timbre | a finger pressing a doorbell button beside a front door |
| 10 | `home-light-bulb` | foco | a lit glowing light bulb hanging from a ceiling cord |
| 11 | `home-mirror` | espejo | a young woman looking at her reflection in a large wall mirror |
| 12 | `home-vacuum-cleaner` | aspiradora | a middle-aged woman vacuuming a living room carpet with an upright vacuum cleaner |
| 13 | `job-receptionist` | recepcionista | a smiling Black woman receptionist at a hotel front desk with a telephone and computer |
| 14 | `kitchen-microwave` | microondas | a microwave oven with a plate of food inside, glowing, on a kitchen counter |
| 15 | `nature-scenery` | paisaje | a wide landscape of green mountains, a calm lake and a blue sky with clouds |
| 16 | `object-flashlight` | linterna | a black flashlight shining a bright beam in a dark room |
| 17 | `object-locker` | casillero | a row of metal lockers with one door open in a gym corridor |
| 18 | `object-postcard` | postal | a postcard showing a tropical beach scene lying on a wooden table, no readable text |
| 19 | `object-scratch` | rayón | a silver car door with a long visible scratch along its side |
| 20 | `object-stain` | mancha | a white shirt laid flat with a large red wine stain on the front |
| 21 | `place-bench` | banca del parque | a wooden park bench under a tree on a path |
| 22 | `place-campsite` | camping | a campsite with several tents, a campfire and trees |
| 23 | `place-clinic` | clínica | a small modern medical clinic building with glass doors and a green cross symbol without text |
| 24 | `place-elementary-school` | escuela primaria | a small colorful elementary school building with a playground and children playing |
| 25 | `place-hair-salon` | peluquería | an adult woman getting her hair cut by a hairdresser in a salon with mirrors |

### Lote 020

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `place-laundromat` | lavandería | a laundromat with a row of washing machines and a woman loading clothes |
| 02 | `place-playground` | patio de recreo | a colorful children's playground with a slide, swings and climbing frame, no people, sunny day |
| 03 | `place-real-estate-agency` | inmobiliaria | storefront of a real estate agency with photos of houses in the window, no readable text |
| 04 | `place-ticket-office` | boletería | a ticket booth window at a train station with a clerk behind the glass, no readable text |
| 05 | `shopping-cart` | carrito | an empty metal supermarket shopping cart |
| 06 | `sport-helmet` | casco | a bicycle helmet with straps on a plain table |
| 07 | `sport-workout` | entrenamiento | a muscular man lifting dumbbells in a gym during a workout |
| 08 | `tech-app` | aplicación | a smartphone screen showing a grid of colorful app icons, no readable text |
| 09 | `tech-radio` | radio | a vintage tabletop radio with a round dial and an extended antenna on a wooden shelf |
| 10 | `travel-double-room` | habitación doble | a hotel double room with a large double bed, two night tables and a window |
| 11 | `travel-tent` | tienda de campaña | an orange camping tent pitched on green grass among pine trees |
| 12 | `weather-fog` | niebla | a road and trees disappearing into thick white fog |
| 13 | `weather-heat` | calor | a very hot sunny day with a man sweating and fanning himself under a blazing sun |
| 14 | `weather-storm` | tormenta | dark storm clouds with lightning and heavy rain over an open field |
| 15 | `emotion-angry` | rabia | an adult man's face looking very angry, red face, shouting |
| 16 | `emotion-impatient` | impaciente | a man tapping his foot and looking at his watch with an impatient face |
| 17 | `emotion-joy` | alegría | a young woman jumping with arms raised and a huge joyful smile |
| 18 | `emotion-upset` | molesto | a middle-aged woman's face looking upset and irritated, frowning |
| 19 | `food-popcorn` | palomitas de maíz | a striped paper bucket full of fresh popcorn |
| 20 | `food-sweets` | dulces | a bowl of colorful wrapped candies and gummy sweets |
| 21 | `home-drain` | desagüe | a bathroom sink drain with water swirling down it |
| 22 | `home-pillow` | almohada | a white fluffy pillow on a made bed |
| 23 | `job-journalist` | periodista | a young journalist holding a microphone and notepad while reporting outdoors |
| 24 | `leisure-classical-music` | música clásica | a string orchestra with violins and cellos playing in a concert hall |
| 25 | `object-drill` | taladro | a handheld electric drill with a drill bit lying on a workbench |

### Lote 021

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `object-nail` | clavo | a hammer hitting a nail into a wooden board, close-up |
| 02 | `object-wall-outlet` | enchufe | a white wall electrical outlet with a plug inserted |
| 03 | `place-repair-shop` | taller | a car mechanic's garage with a car lifted on a hoist and tools on the wall |
| 04 | `sport-push-up` | flexión de brazos | a young woman doing a push-up on a gym mat, side view |
| 05 | `sport-score-a-goal` | meter un gol | a soccer player kicking the ball into the net past the goalkeeper |
| 06 | `tech-dashcam` | cámara del carro | a small camera mounted on a car windshield near the rear-view mirror |
| 07 | `tech-gps` | gps | a small GPS navigation device on a car dashboard showing a route map, no readable text |
| 08 | `transport-brakes` | frenos | close-up of a car wheel showing the metal brake disc and red brake caliper |
| 09 | `transport-clutch` | embrague | a driver's foot pressing the clutch pedal in a manual car, footwell view |
| 10 | `transport-expressway` | autopista | a wide multi-lane highway with cars driving in both directions, aerial view |
| 11 | `transport-flat-tire` | pinchazo | a car on the roadside with a completely flat rear tire |
| 12 | `transport-hood` | cofre | a car with its hood open showing the engine, parked |
| 13 | `transport-motorcycle` | moto | a red motorcycle parked on a street, side view |
| 14 | `transport-steering-wheel` | volante | a car steering wheel with a driver's hands on it, interior view |
| 15 | `transport-wheel` | rueda | a single car wheel with a black tire and silver rim, side view |
| 16 | `work-job-interview` | entrevista de trabajo | a woman candidate being interviewed by a man across an office desk |
| 17 | `home-ceiling` | techo | a living room ceiling with a hanging lamp, viewed from below |
| 18 | `job-traffic-officer` | agente de tráfico | a female traffic officer in uniform directing cars with raised hand at an intersection |
| 19 | `leisure-carnival` | carnaval | dancers in colorful feathered costumes at a carnival parade |
| 20 | `leisure-parade` | desfile | a street parade with a marching band and people lining the street |
| 21 | `nature-field` | campo | a wide green farm field with crop rows and a barn in the distance |
| 22 | `nature-fire` | incendio | a house on fire with large flames and smoke while firefighters spray water |
| 23 | `nature-sand` | arena | a close-up of golden beach sand with a small pile and a hand scooping it |
| 24 | `nature-trail` | sendero | a narrow dirt trail winding through a green forest |
| 25 | `place-city-hall` | alcaldía | a grand city hall building with columns and a flag on the front |

### Lote 022

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `shopping-debit-card` | tarjeta de débito | a blank plastic bank card with a chip, held in a hand, no readable text |
| 02 | `shopping-tag` | etiqueta | a price tag hanging by a string from a folded shirt, no readable text |
| 03 | `shopping-withdrawal` | retiro de dinero | a young man taking banknotes from an ATM machine |
| 04 | `transport-warning-triangle` | triángulo de emergencia | a red reflective warning triangle placed on the road behind a broken-down car |
| 05 | `action-brush-teeth` | cepillado de dientes | an adult woman brushing her teeth with a toothbrush in front of a bathroom mirror |
| 06 | `action-do-the-laundry` | lavar la ropa | a man loading clothes into a front-loading washing machine |
| 07 | `action-go-home` | volver a casa | a tired woman with a bag walking to the front door of her house at dusk |
| 08 | `action-go-to-work` | ir a trabajar | a man in a suit with a briefcase walking into an office building in the morning |
| 09 | `action-have-dinner` | cenar | a family of four having dinner together at a table in the evening |
| 10 | `action-line-up` | hacer fila | a line of people standing one behind another waiting at a counter |
| 11 | `action-listen-to-music` | escuchar música | a young man with headphones on, eyes closed, listening to music |
| 12 | `action-nap` | siesta | a man napping on a sofa with a book resting on his chest |
| 13 | `action-oversleeping` | quedarse dormido | a man fast asleep in bed while an alarm clock rings and sunlight shines in |
| 14 | `action-peel` | pelar | an adult woman peeling an apple with a small knife in a kitchen |
| 15 | `action-take-a-walk` | pasear | a couple strolling together along a tree-lined park path |
| 16 | `action-take-photo` | tomar fotos | an adult woman holding up a camera to take a photo of a landscape |
| 17 | `action-teach` | enseñar | a teacher standing at a whiteboard explaining to a class of students |
| 18 | `action-try-on` | probarse | a woman trying on a jacket in front of a mirror in a clothing store |
| 19 | `action-wash-up` | lavarse | a boy washing his hands with soap at a bathroom sink |
| 20 | `action-watch-tv` | ver la tele | a family sitting on a sofa watching television together |
| 21 | `adjective-blond` | rubio | a young man with bright blond hair smiling, portrait |
| 22 | `adjective-dark` | oscuro | a room almost completely dark with only a single candle lit |
| 23 | `adjective-large` | grande | a very large dog next to a small cat, emphasis on the large dog |
| 24 | `adjective-narrow` | estrecho | a very narrow alley between two buildings, emphasis on the tight width |
| 25 | `adjective-slim` | delgado | a tall slim young man standing, full body view |

### Lote 023

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `adjective-spacious` | amplio | a very large bright empty living room with high ceiling and lots of open space |
| 02 | `body-nose` | nariz | a close-up of a person's face showing the nose in profile |
| 03 | `clothing-cap` | gorra | a red baseball cap with a curved brim on a plain surface |
| 04 | `drink-coffee-with-milk` | café con leche | a glass cup of coffee with milk on a saucer, steam rising |
| 05 | `drink-green-tea` | té verde | a clear glass cup of green tea with loose green tea leaves beside it |
| 06 | `drink-latte` | latte | a latte in a white cup with heart-shaped milk foam art |
| 07 | `drink-wine` | vino | a glass of red wine next to a bottle on a table |
| 08 | `emotion-hungry` | con hambre | a young man holding his stomach looking hungrily at a plate of food |
| 09 | `family-dad` | papá | a smiling father carrying his young daughter on his shoulders |
| 10 | `food-bread-roll` | panecillo | two golden crusty bread rolls on a wooden board |
| 11 | `food-cereal` | cereal | a bowl of breakfast cereal with milk and a spoon |
| 12 | `food-cooked-rice` | arroz cocido | a white bowl of steaming cooked white rice |
| 13 | `food-cookie` | galleta | three round chocolate chip cookies on a plate |
| 14 | `food-croissant` | cruasán | a golden flaky croissant on a small plate |
| 15 | `food-ham` | jamón | several thin slices of pink ham on a plate |
| 16 | `food-ice-cream` | helado | a hand holding an ice cream cone with two scoops, strawberry and vanilla |
| 17 | `food-soy-sauce` | salsa de soja | a small bowl of dark soy sauce next to a glass bottle |
| 18 | `food-tofu` | tofu | white tofu cubes on a plate with chopsticks |
| 19 | `fruit-veg-garlic` | ajo | a whole garlic bulb with a few loose cloves on a wooden table |
| 20 | `fruit-veg-strawberry` | fresa | three ripe red strawberries with green leaves |
| 21 | `health-sick` | enfermo | a man lying in bed with a thermometer, tissues and a sick pale face |
| 22 | `home-laundry` | ropa para lavar | a wicker laundry basket full of colorful clothes |
| 23 | `home-restroom` | baño | a clean bathroom with a toilet, a sink and a mirror |
| 24 | `job-cashier` | cajera | a smiling cashier woman at a supermarket register scanning groceries |
| 25 | `job-designer` | diseñador | a young woman graphic designer working at a desk with a drawing tablet and color swatches |

### Lote 024

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `job-lawyer` | abogado | a lawyer in a dark suit holding legal files beside a desk with law books |
| 02 | `job-salesperson` | vendedor | a smiling male salesperson in a shirt showing a product to a customer in a store |
| 03 | `job-server` | mesero | a waiter in a black apron carrying a tray with drinks in a restaurant |
| 04 | `job-shop-assistant` | empleado de tienda | a young woman store employee folding clothes on a shop counter |
| 05 | `kitchen-dishes` | platos | a neat stack of clean white plates on a kitchen counter |
| 06 | `kitchen-stove` | estufa | a kitchen stove with four gas burners and a pot with steam on top |
| 07 | `leisure-hiking` | subir montañas | two adults with backpacks and walking sticks hiking up a mountain trail |
| 08 | `nature-autumn` | otoño | an autumn park with orange and yellow leaves falling from trees |
| 09 | `object-novel` | novela | a thick paperback novel with a plain cover on a table |
| 10 | `object-painting` | cuadro | a framed landscape painting hanging on a living room wall |
| 11 | `person-boy` | chico | a young boy about eight years old smiling, standing in a park |
| 12 | `person-gentleman` | señor | an elderly man in a suit and tie with gray hair, portrait |
| 13 | `person-lady` | señora | an elderly woman with gray hair in a cardigan smiling, portrait |
| 14 | `person-university-student` | estudiante universitario | a young Asian man university student with a backpack and books on campus |
| 15 | `place-cathedral` | catedral | a large stone cathedral with two tall towers and a rose window |
| 16 | `place-convenience-store` | tienda de conveniencia | a small corner convenience store with glass front and shelves of goods, evening |
| 17 | `place-historic-center` | centro histórico | an old colonial town square with cobblestones, a church and balconied houses |
| 18 | `place-monument` | monumento | a tall stone monument with a statue on top in a city plaza |
| 19 | `place-shopping-mall` | centro comercial | the interior of a large shopping mall with several floors, escalators and shops |
| 20 | `place-swimming-pool` | piscina | an outdoor swimming pool with blue water and lounge chairs |
| 21 | `place-theater` | teatro | a theater stage with red curtains and an audience seated in rows |
| 22 | `place-viewpoint` | mirador | a scenic lookout platform with a railing overlooking a valley |
| 23 | `school-books` | libros | a neat stack of colorful hardcover books on a table |
| 24 | `school-paper` | papel | a single blank white sheet of paper on a desk |
| 25 | `shopping-checkout-counter` | caja | a supermarket checkout counter with a conveyor belt and cash register |

### Lote 025

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `sport-baseball` | béisbol | a baseball batter swinging at a pitch on a ball field |
| 02 | `sport-cycling` | ciclismo | a cyclist in helmet riding a road bike along a country road |
| 03 | `sport-jogging` | trote | a woman jogging along a riverside path in sportswear |
| 04 | `tech-telephone` | teléfono | a classic desk telephone with a handset and a keypad |
| 05 | `tech-television` | televisor | a flat-screen television on a stand in a living room |
| 06 | `transport-roundabout` | rotonda | a traffic roundabout with cars circling a central green island, aerial view |
| 07 | `transport-tram` | tranvía | a modern tram running on rails along a city street |
| 08 | `action-applause` | aplauso | an audience of adults clapping their hands enthusiastically in a theater |
| 09 | `action-climb` | trepar | a young man climbing up a rocky wall using his hands and feet |
| 10 | `action-fry` | freír | an adult man frying eggs in a pan on a stove |
| 11 | `action-grill` | asar | a woman grilling meat and vegetables on a barbecue grill outdoors |
| 12 | `action-iron` | planchar | a man ironing a shirt on an ironing board |
| 13 | `action-pour` | verter | a young Black woman pouring water from a glass jug into a glass |
| 14 | `action-set-the-table` | poner la mesa | an adult man placing plates and forks on a dining table |
| 15 | `action-stir` | mover | an older Asian man stirring a pot of soup on a stove with a wooden spoon |
| 16 | `action-sunbathe` | tomar el sol | an adult woman lying on a beach towel on the sand, sunbathing with sunglasses |
| 17 | `action-throw-away` | tirar | an adult man throwing an empty plastic bottle into a trash bin |
| 18 | `action-vacuum` | pasar la aspiradora | an adult Latino man vacuuming the carpet of a living room |
| 19 | `action-wrap` | envolver | an older woman wrapping a gift box with colorful paper and a ribbon at a table |
| 20 | `action-write-down` | anotar | a young woman writing notes with a pen in a notebook at a desk |
| 21 | `adjective-empty` | vacío | an empty glass next to a full glass, emphasis on the empty one |
| 22 | `adjective-wet` | mojado | a man standing in heavy rain with soaked clothes and dripping hair, holding no umbrella |
| 23 | `body-ankle` | tobillo | a close-up of a person's bare foot and ankle, side view |
| 24 | `body-belly` | barriga | a person's bare belly in close-up with a hand resting on it |
| 25 | `body-fingerprint` | huella | a close-up of a finger pressed on ink pad leaving a clear fingerprint on white paper |

### Lote 026

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `clothing-belt` | cinturón | a brown leather belt with a metal buckle, coiled on a surface |
| 02 | `clothing-dress-shoes` | zapatos | a pair of polished black leather dress shoes |
| 03 | `clothing-uniform` | uniforme | a school uniform with white shirt, navy blazer, tie and grey trousers on a hanger |
| 04 | `drink-herbal-tea` | infusión | a clear cup of herbal tea with a tea bag and fresh mint leaves |
| 05 | `emotion-dizzy` | mareado | a woman holding her head with a dizzy expression and swirling stars around her |
| 06 | `emotion-stressed` | estresado | a young man at a desk with papers, hands on his head, looking very stressed |
| 07 | `food-chewing-gum` | chicle | a girl blowing a large pink bubble with chewing gum |
| 08 | `food-pepper` | pimienta | a wooden pepper grinder beside a small pile of whole black peppercorns on a white table |
| 09 | `furniture-cabinet` | armario | a wooden kitchen cabinet with doors open showing plates inside |
| 10 | `furniture-furniture` | muebles | a living room with a sofa, a coffee table and an armchair |
| 11 | `health-adhesive-bandage` | curita | an adhesive bandage applied on a finger, close-up |
| 12 | `health-have-a-fever` | tener fiebre | a sick man in bed with flushed face looking at a thermometer |
| 13 | `health-having-a-cold` | resfriado | a woman sneezing into a tissue with a red nose, wrapped in a blanket |
| 14 | `health-stomachache` | dolor de barriga | an adult woman holding her stomach with a pained expression, bent slightly forward |
| 15 | `home-bath` | bañera | a white bathtub filled with water and bubbles in a bathroom |
| 16 | `home-courtyard` | patio | a sunny courtyard with potted plants, a tiled floor and a central fountain |
| 17 | `home-curtain` | cortina | a window with long blue curtains partly open showing daylight |
| 18 | `home-rug` | alfombra | a patterned rectangular rug on a wooden living room floor, seen from above at an angle |
| 19 | `job-accountant` | contador | a middle-aged accountant with glasses using a calculator at a desk with papers |
| 20 | `job-chef` | chef | a chef in a white uniform and tall hat cooking in a professional kitchen |
| 21 | `job-hairdresser` | peluquero | a male hairdresser cutting a woman's hair in a salon |
| 22 | `job-porter` | maletero del hotel | a hotel porter in uniform pushing a luggage cart full of suitcases through a lobby |
| 23 | `job-repairman` | técnico | a repairman with a toolbox kneeling to fix a washing machine |
| 24 | `job-tour-guide` | guía de turistas | a smiling female tour guide pointing at a monument while leading a small group of tourists |
| 25 | `kitchen-coffee-maker` | cafetera | an electric drip coffee maker with a glass pot full of coffee |

### Lote 027

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `kitchen-cutting-board` | tabla de cortar | a wooden cutting board with a knife and sliced vegetables |
| 02 | `kitchen-dishwasher` | lavavajillas | an open dishwasher loaded with clean plates and glasses |
| 03 | `leisure-camping` | camping | a family sitting around a small campfire next to a tent at dusk |
| 04 | `leisure-graduation` | graduación | young graduates in gowns throwing their caps in the air |
| 05 | `leisure-reading-books` | lectura | a teenage boy reading a book on a sofa with a stack of books beside him |
| 06 | `nature-path` | camino | a narrow dirt path winding through green fields toward distant hills under a blue sky |
| 07 | `nature-seaside` | orilla del mar | gentle waves reaching a sandy shore at the seaside with a clear sky |
| 08 | `nature-waterfall` | cascada | a tall waterfall pouring over rocks into a pool surrounded by green forest |
| 09 | `nature-wood` | madera | a neat stack of cut wooden logs with visible bark and rings |
| 10 | `object-fabric` | tela | a roll of colorful striped fabric with scissors and measuring tape |
| 11 | `object-stroller` | cochecito de bebé | an empty baby stroller standing on a sidewalk in a park |
| 12 | `object-vending-machine` | máquina expendedora | a vending machine filled with snacks and drinks standing in a hallway, no text |
| 13 | `person-bride` | novia | a bride in a white dress holding a bouquet, smiling |
| 14 | `person-groom` | novio | a groom in a dark suit with a boutonniere, smiling |
| 15 | `person-queue` | fila | a line of five adults waiting one behind another in front of a counter |
| 16 | `place-cafeteria` | comedor | a school cafeteria with long tables and students holding food trays |
| 17 | `place-doctor-s-office` | consulta | a doctor's consulting room with a desk, an examination bed and a stethoscope |
| 18 | `place-hot-spring` | baño termal | people relaxing in a steaming natural hot spring pool among rocks and trees |
| 19 | `place-locker-room` | vestuario | a locker room with a wooden bench and rows of metal lockers |
| 20 | `place-town` | pueblo | a small town with a few houses, a church and a main street seen from a hill |
| 21 | `sport-skiing` | esquí | a skier in a jacket and helmet skiing down a snowy mountain slope |
| 22 | `sport-weights` | pesas | a pair of black dumbbells and a barbell with weight plates on a gym floor |
| 23 | `tech-keyboard` | teclado | a black computer keyboard on a desk |
| 24 | `tech-phone-call` | llamada telefónica | a young woman talking on a smartphone held to her ear, smiling |
| 25 | `tech-video-call` | videollamada | a woman at a desk talking to a laptop screen showing three smiling faces in a video call |

### Lote 028

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `tech-wifi` | wifi | a white wireless router with antennas and curved wifi signal waves radiating from it |
| 02 | `time-sunrise` | amanecer | the sun rising over a calm sea horizon with orange and pink morning sky |
| 03 | `travel-guided-tour` | visita guiada | a tour guide with a flag leading a small group of tourists in front of a monument |
| 04 | `travel-hotel-reception` | recepción | a hotel reception desk with a smiling receptionist, a bell and key hooks behind her |
| 05 | `travel-passport-control` | control de pasaportes | an airport officer in a booth checking a traveler's open passport |
| 06 | `travel-single-room` | habitación individual | a small hotel room with one single bed, a nightstand and a window |
| 07 | `weather-thunderstorm` | tormenta | dark storm clouds with a bright lightning bolt striking over a field and heavy rain |
| 08 | `work-meeting-room` | sala de reuniones | a meeting room with a long table, chairs and a presentation screen |
| 09 | `work-planning-meeting` | reunión breve de planificación | four colleagues standing around a table with sticky notes on a whiteboard, discussing a plan |
| 10 | `work-working-from-home` | trabajo en casa | a woman working on a laptop at a desk in her home living room with a coffee cup |
| 11 | `action-catch` | atrapar | a boy catching a ball with both hands in a park |
| 12 | `action-drink-water` | beber agua | an adult woman drinking water from a glass, head slightly tilted back |
| 13 | `action-plant` | plantar | an adult man planting a small tree seedling in the soil with a shovel |
| 14 | `action-plug-in` | enchufar | a hand plugging a power cable into a wall outlet |
| 15 | `clothing-handbag` | bolso | a brown leather handbag with two handles on a white background |
| 16 | `emotion-afraid` | tener miedo | a young woman's face looking afraid, wide eyes, hands covering her mouth |
| 17 | `emotion-embarrassed` | avergonzado | a young man with a blushing face covering part of it with his hand, looking embarrassed |
| 18 | `emotion-exhausted` | rendido | a young woman lying exhausted on a sofa after a long day, eyes closed, arm hanging |
| 19 | `emotion-furious` | furioso | a man's face red with rage, shouting furiously with veins visible on the forehead |
| 20 | `emotion-lonely` | sentirse solo | an elderly man sitting alone on a park bench looking sad and lonely |
| 21 | `emotion-surprised` | sorprenderse | a young man's face looking very surprised, wide open eyes and open mouth |
| 22 | `family-family-dinner` | cena familiar | a family of grandparents, parents and children sharing dinner around a table |
| 23 | `family-grandchild` | nieto | a young boy hugging his smiling grandfather on a sofa |
| 24 | `family-great-grandfather` | bisabuelo | a very old man with white hair and a cane sitting with a small child on his lap |
| 25 | `family-married-couple` | matrimonio | a smiling married couple in their forties holding hands and showing wedding rings |

### Lote 029

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `food-feast` | comida especial | a large table covered with many dishes of roast meat, vegetables, bread and fruit |
| 02 | `health-bleed` | sangrar | a finger with a small cut and a drop of blood, held over a white tissue |
| 03 | `health-braces` | aparato dental | a teenage girl smiling wide showing metal braces on her teeth |
| 04 | `health-swelling` | hinchazón | a swollen ankle, red and puffy, with an ice pack on it |
| 05 | `health-toothache` | dolor de muelas | a middle-aged woman holding her cheek with a pained face because of a toothache |
| 06 | `home-electrical-outlet` | enchufe | a white wall electrical outlet with one plug inserted, close view |
| 07 | `home-roof` | techo | a house with a red tiled roof seen from the front garden |
| 08 | `job-actress` | actriz | an actress in an elegant dress performing on a theater stage under a spotlight |
| 09 | `job-author` | autor | a writer sitting at a desk with a typewriter, a pile of paper and a book |
| 10 | `job-captain` | capitán | an airplane captain in uniform with four stripes and a cap, smiling in the cockpit |
| 11 | `job-courier` | mensajero | a delivery courier in a cap carrying a cardboard package to a front door |
| 12 | `job-customs-officer` | agente | a customs officer in uniform inspecting an open suitcase on a table at an airport |
| 13 | `job-film-director` | director de cine | a film director sitting on a chair on a set, holding a megaphone beside a camera |
| 14 | `job-locksmith` | cerrajero | a locksmith kneeling at a front door and opening the lock with tools |
| 15 | `kitchen-tray` | bandeja | a wooden tray holding a teapot and two cups, seen from the side |
| 16 | `leisure-christmas` | navidad | a decorated Christmas tree with lights, ornaments and wrapped gifts underneath in a living room |
| 17 | `leisure-news-broadcast` | noticiero | a news anchor sitting at a studio desk in front of a camera, with a city backdrop |
| 18 | `object-candles` | velas | three lit white candles of different heights on a table in the dark |
| 19 | `object-hammer` | martillo | a hammer with a wooden handle lying next to nails on a workbench |
| 20 | `object-hose` | manguera | a green garden hose spraying water onto flowers in a garden |
| 21 | `object-jack` | gato | a car jack lifting the corner of a car beside a wheel |
| 22 | `object-screw` | tornillo | a metal screw next to a screwdriver on a wooden board |
| 23 | `object-wrench` | llave inglesa | a metal adjustable wrench on a workbench |
| 24 | `person-adult` | adulto | a standing adult man in a casual shirt next to a small child, emphasis on the adult |
| 25 | `person-teenager` | adolescente | a teenage boy with a backpack and headphones standing on a street |

### Lote 030

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `place-bus-station` | terminal | a bus station with several buses parked and passengers waiting on platforms |
| 02 | `place-guesthouse` | posada | a small cozy countryside guesthouse with a wooden door and flowers by the windows |
| 03 | `place-workshop` | taller | a car repair workshop with a car lifted on a hoist and tools on the wall |
| 04 | `plant-tree` | árbol | a big tree with a thick trunk and green leafy crown in a meadow |
| 05 | `sport-cardio` | cardio | a young woman running on a treadmill in a gym, sweating |
| 06 | `sport-squat` | sentadilla | a woman doing a squat with a barbell on her shoulders in a gym |
| 07 | `sport-weight-training` | entrenamiento de fuerza | a muscular man lifting a barbell with plates in a gym |
| 08 | `transport-bumper` | parachoques | the rear bumper of a silver car, close view from behind |
| 09 | `transport-car-trunk` | maletero | an open car trunk with suitcases inside, seen from behind the car |
| 10 | `transport-engine-oil` | aceite de motor | a bottle of motor oil being poured into a car engine under the open hood |
| 11 | `transport-gasoline` | gasolina | a person filling a car with fuel using a pump nozzle at a gas station |
| 12 | `transport-headlight` | faro | the front of a car with one bright headlight turned on at dusk |
| 13 | `transport-road-sign` | señal de tránsito | a red-bordered triangular warning road sign with a pedestrian symbol on a pole, no text |
| 14 | `transport-rush-hour` | hora pico | a busy road full of cars in a traffic jam at sunset, with commuters |
| 15 | `transport-shuttle-bus` | autobús de enlace | a small white airport shuttle bus parked in front of a terminal with passengers boarding |
| 16 | `transport-windshield` | parabrisas | a car windshield with wiper blades, seen from inside the car on a clear day |
| 17 | `travel-baggage-carousel` | banda | suitcases moving on a baggage carousel belt in an airport hall |
| 18 | `travel-plane-landing` | aterrizar | a passenger airplane landing on a runway with wheels touching the ground |
| 19 | `travel-plane-takeoff` | despegue | a passenger airplane taking off from a runway, nose lifted into the sky |
| 20 | `weather-heavy-rain` | lluvia fuerte | very heavy rain pouring on a city street with puddles and grey sky |
| 21 | `weather-typhoon` | tifón | a violent typhoon storm with swirling dark clouds over the sea, palm trees bending in the wind |
| 22 | `action-freeze` | congelar | a woman putting a bag of vegetables inside an open freezer drawer with ice |
| 23 | `action-renovate` | renovar | a worker painting a wall with a roller in a room being renovated |
| 24 | `clothing-costume` | disfraz | an adult dressed in a pirate costume with hat and eye patch at a party |
| 25 | `emotion-annoyed` | molesto | a young woman's face looking annoyed, rolling her eyes with a frown |

### Lote 031

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `food-afternoon-snack` | merienda | a cup of tea and a small plate with a sandwich and a pastry on a table |
| 02 | `home-dampness` | humedad | a wall in a room with damp stains and mold patches near the ceiling |
| 03 | `home-home-appliances` | electrodomésticos | a kitchen with a refrigerator, a washing machine, a microwave and a stove |
| 04 | `home-light-switch` | interruptor | a white wall light switch with a hand about to press it |
| 05 | `home-water-pipe` | tubería de agua | metal water pipes with a valve under a sink, with a drip of water |
| 06 | `job-baker` | panadero | a baker in an apron and white hat holding a tray of fresh bread loaves |
| 07 | `job-bank-teller` | cajero | a bank teller behind a counter handing money to a customer through a glass window |
| 08 | `job-electrician` | electricista | an electrician in a helmet fixing wires inside an electrical panel |
| 09 | `kitchen-straw` | popote | a tall glass of orange juice with a striped drinking straw |
| 10 | `kitchen-tableware` | vajilla y cubiertos | white plates, bowls, glasses, forks, knives and spoons arranged on a table |
| 11 | `leisure-hide-and-seek` | escondidas | a child hiding behind a tree trunk while another child covers eyes and counts |
| 12 | `nature-bonfire` | hoguera | a large bonfire burning at night with people sitting around it |
| 13 | `nature-coast` | costa | a rocky coast with cliffs and sea waves under a bright sky |
| 14 | `nature-compost` | compost | a compost bin full of fruit peels, leaves and dark soil in a garden |
| 15 | `nature-sandy-beach` | playa de arena | a wide sandy beach with turquoise sea and a few palm trees |
| 16 | `nature-seashell` | concha | a spiral seashell lying on wet sand at the beach |
| 17 | `nature-shade` | sombra | a person resting in the shade of a big tree on a sunny day |
| 18 | `object-diary` | diario | a closed diary notebook with a pen and a small lock on its cover |
| 19 | `object-paper-lantern` | farolito | a red paper lantern hanging and glowing against a dark night sky |
| 20 | `object-recycling-bins` | recolección separada de residuos | three colored recycling bins, blue, green and yellow, in a row |
| 21 | `object-reusable-water-bottle` | botella reutilizable | a stainless steel reusable water bottle with a cap standing on a table |
| 22 | `person-best-friends` | mejor amigo | two young men laughing with their arms around each other's shoulders |
| 23 | `place-landfill` | basurero | a large landfill with piles of garbage and birds flying above |
| 24 | `school-school-bag` | mochila escolar | a blue school backpack with books and a pencil case sticking out |
| 25 | `sport-climbing` | escalada | a climber with a helmet and rope scaling a steep rock wall |

### Lote 032

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `sport-dive` | bucear | a scuba diver in a wetsuit swimming underwater near colorful fish and coral |
| 02 | `sport-surfing` | surf | a surfer riding a big blue wave on a surfboard |
| 03 | `time-sunset` | atardecer | the sun setting over the sea with orange and purple sky and silhouettes of palm trees |
| 04 | `transport-bike-lane` | ciclovía | a cyclist riding along a green painted bike lane separated from cars on a city street |
| 05 | `transport-highway` | autopista | a multi-lane highway with cars driving and green road lanes |
| 06 | `transport-spare-tire` | rueda de repuesto | a spare tire lying on the ground next to a car with a flat tire |
| 07 | `transport-toll-booth` | caseta de peaje | a toll booth on a highway with a car stopped and a driver paying |
| 08 | `weather-heat-wave` | ola de calor | a scorching sun over a city with a sweating man fanning himself and a thermometer showing a very high temperature |
| 09 | `action-have-lunch` | almorzar | a young man eating lunch at a table with a plate of rice and chicken at midday |
| 10 | `action-kick` | patear | a young Black man kicking a soccer ball on a grass field |
| 11 | `action-play-piano` | tocar el piano | an adult man sitting at an upright piano, hands on the keys, playing |
| 12 | `action-take-bus` | tomar el bus | an adult man in line stepping onto a city bus through the open door |
| 13 | `action-wash-dishes` | lavar los platos | an adult woman washing plates at a kitchen sink with soap suds |
| 14 | `action-wash-face` | lavarse la cara | a young man leaning over a bathroom sink splashing water on his face |
| 15 | `adjective-ancient` | antiguo | weathered ancient stone temple ruins with broken columns standing in dry grass under a clear sky |
| 16 | `adjective-clean` | ser limpio | a spotless shiny clean kitchen counter with sparkling surface and a fresh cloth beside it |
| 17 | `body-beard` | barba | close-up of a middle-aged man with a full thick dark beard smiling |
| 18 | `body-face` | cara | front view of a smiling middle-aged Asian man's face, neutral background |
| 19 | `body-feet` | pies | a pair of bare human feet standing side by side on a wooden floor |
| 20 | `body-mouth` | boca | a close-up of a smiling woman's mouth with lips and teeth visible |
| 21 | `clothing-anorak` | anorak | a bright red hooded anorak jacket displayed on a plain background |
| 22 | `clothing-jeans` | jeans | a pair of blue denim jeans folded on a plain background |
| 23 | `color-light-blue` | celeste | a large flat swatch of pale sky light blue color filling the frame, with a few light blue objects |
| 24 | `drink-black-tea` | té negro | a white cup of hot black tea on a saucer with steam rising |
| 25 | `drink-cappuccino` | capuchino | a cup of cappuccino with foam art on a saucer with a small spoon |

### Lote 033

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `drink-cola` | refresco de cola | a glass of dark cola with ice cubes and bubbles next to a closed unlabeled bottle |
| 02 | `drink-mineral-water` | agua mineral | a clear glass bottle of sparkling mineral water next to a glass with bubbles, no label text |
| 03 | `drink-orange-juice` | jugo de naranja | a tall glass of fresh orange juice with two halved oranges beside it |
| 04 | `emotion-bored` | estar aburrido | a young woman slumped on a sofa with her chin on her hand, looking very bored |
| 05 | `emotion-thirsty` | tener sed | a tired adult woman looking longingly at a tall glass of cold water, hand on her throat |
| 06 | `family-brother` | hermano | two boys, a teenager and a younger boy, laughing together as brothers |
| 07 | `family-daughter` | hija | a smiling mother hugging her little girl of about six years old |
| 08 | `family-husband` | esposo | a married couple, a smiling man holding hands with his wife, wedding rings visible, the man emphasized |
| 09 | `family-older-brother` | hermano mayor | a tall teenage boy standing next to his much smaller younger brother, older one emphasized |
| 10 | `family-older-sister` | hermana mayor | a tall teenage girl standing next to her much smaller younger sister, older one emphasized |
| 11 | `family-sister` | hermana | two girls, a teenager and a younger girl, smiling and hugging as sisters |
| 12 | `family-son` | hijo | a father hugging his smiling young boy of about seven years old |
| 13 | `family-wife` | esposa | a married couple, a smiling woman holding hands with her husband, wedding rings visible, the woman emphasized |
| 14 | `family-younger-brother` | hermano menor | a small young boy standing next to his much taller teenage brother, younger one emphasized |
| 15 | `family-younger-sister` | hermana menor | a small young girl standing next to her much taller teenage sister, younger one emphasized |
| 16 | `food-baguette` | baguette | a long golden French baguette lying on a wooden board |
| 17 | `food-baozi` | bao | three white steamed baozi buns in a bamboo steamer basket |
| 18 | `food-bibimbap` | bibimbap | a Korean bibimbap rice bowl topped with colorful vegetables, beef and a fried egg |
| 19 | `food-bulgogi` | bulgogi | a plate of Korean bulgogi marinated grilled beef slices with green onion and sesame |
| 20 | `food-cookies` | galletas | a plate of round chocolate chip cookies |
| 21 | `food-crepe` | crepa | a folded thin crepe on a plate topped with strawberries and powdered sugar |
| 22 | `food-curry` | curry | a bowl of yellow curry with chicken and vegetables served with white rice |
| 23 | `food-dumplings` | dumplings | a plate of steamed dumplings with a small dish of dipping sauce |
| 24 | `food-empanada` | empanada | a golden baked empanada pastry turnover on a plate |
| 25 | `food-honey` | miel | a glass jar of golden honey with a wooden honey dipper |

### Lote 034

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `food-instant-noodles` | ramyeon | a pot of steaming Korean-style instant noodles with egg and green onions, chopsticks in hand |
| 02 | `food-kimchi` | kimchi | a small bowl of red Korean kimchi fermented cabbage |
| 03 | `food-korean-stew` | guiso o estofado coreano | a bubbling red Korean stew in a black stone pot with tofu and vegetables |
| 04 | `food-noodles` | fideos | a white bowl of plain cooked noodles with chopsticks resting on the bowl |
| 05 | `food-pasta` | pasta | a plate of spaghetti pasta with tomato sauce and a fork |
| 06 | `food-ramen` | ramen | a bowl of ramen noodle soup with egg, pork slices and green onions, chopsticks beside it |
| 07 | `food-sushi` | sushi | a wooden plate with assorted sushi rolls and nigiri, with soy sauce dish and chopsticks |
| 08 | `food-tempura` | tempura | a plate of golden fried tempura shrimp and vegetables with a small dipping sauce |
| 09 | `food-tteokbokki` | tteokbokki | a bowl of Korean tteokbokki, cylindrical rice cakes in red spicy sauce with fish cakes |
| 10 | `food-uncooked-rice` | arroz crudo | a wooden bowl full of dry uncooked white rice grains with a scoop |
| 11 | `fruit-veg-apples` | manzanas | three fresh red apples arranged together on a wooden table |
| 12 | `fruit-veg-avocado` | aguacate | a ripe avocado cut in half showing the green flesh and large brown pit |
| 13 | `fruit-veg-beans` | frijol | a bowl of cooked brown beans on a table with a wooden spoon |
| 14 | `fruit-veg-cucumber` | pepino | a whole green cucumber next to several round cucumber slices |
| 15 | `fruit-veg-lemon` | limón | a single bright yellow whole lemon next to a halved lemon on a white surface |
| 16 | `fruit-veg-lettuce` | lechuga | a fresh green head of lettuce with crisp leaves on a wooden board |
| 17 | `fruit-veg-papaya` | papaya | a whole papaya next to a halved papaya showing orange flesh and black seeds |
| 18 | `fruit-veg-pineapple` | piña | a whole ripe pineapple with a green leafy crown next to a few cut slices |
| 19 | `fruit-veg-watermelon` | sandía | a whole green striped watermelon next to a cut wedge showing red flesh and seeds |
| 20 | `home-small-apartment` | departamento pequeño | a cozy small studio apartment with a bed, tiny kitchen and one sofa in a single room |
| 21 | `job-artist` | artista | a middle-aged woman artist painting on a canvas at an easel in a studio |
| 22 | `job-bank-employee` | empleado de banco | a smiling young Black man in a shirt and tie working as a bank teller behind a counter |
| 23 | `job-delivery-person` | entrega a domicilio | a smiling delivery woman handing a cardboard package to a person at a front door |
| 24 | `job-programmer` | programador | a young Black woman programmer working at a desk with a laptop and two monitors showing abstract code shapes |
| 25 | `job-salesman` | vendedor | a friendly adult man in a shirt and tie standing behind a store counter showing a product to a customer |

### Lote 035

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `job-taxi-driver` | taxista | a middle-aged Latino man driving a yellow taxi, smiling, hands on the steering wheel |
| 02 | `job-waitress` | mesera | a smiling Asian woman waitress in an apron carrying a tray with plates in a restaurant |
| 03 | `kitchen-pantry` | despensa | a small pantry closet with shelves full of jars, boxes of food and bags of rice |
| 04 | `kitchen-scale` | balanza | a digital kitchen scale with a bowl of flour on top |
| 05 | `leisure-chess` | ajedrez | a chessboard with black and white chess pieces in the middle of a game |
| 06 | `object-basket` | canasta | a woven wicker basket with a handle on a plain light background |
| 07 | `object-cologne` | colonia | an elegant glass perfume bottle with a spray top on a plain surface, no label text |
| 08 | `object-magazine` | revista | an open glossy magazine with colorful photographs lying on a coffee table, no readable text |
| 09 | `object-plastic-bag` | bolsa de plástico | a transparent plastic bag with handles holding some groceries, on a white surface |
| 10 | `object-small-bag` | bolsa pequeña | a small leather handbag standing next to a much larger travel bag, emphasis on the small one |
| 11 | `object-transit-card` | tarjeta de transporte | a plastic public transport card being tapped on a card reader at a turnstile, no text |
| 12 | `person-men` | hombres | a group of three adult men of different ages and ethnicities standing together, smiling |
| 13 | `person-neighbor` | vecino | a smiling middle-aged man waving over a garden fence from his house yard |
| 14 | `person-women` | mujeres | a group of three adult women of different ages and ethnicities standing together, smiling |
| 15 | `person-young-people` | jóvenes | a group of four teenagers and young adults of different ethnicities laughing together outdoors |
| 16 | `place-apartment-building` | departamento | a modern apartment building of concrete and glass with balconies on several floors |
| 17 | `place-avenue` | avenida | a wide city avenue lined with trees and tall buildings with cars driving |
| 18 | `place-bar` | bar | a cozy bar interior with a wooden counter, tall stools and bottles on shelves behind |
| 19 | `place-castle` | castillo | a large stone medieval castle with towers on a green hill under a blue sky |
| 20 | `place-cinema` | cine | a cinema movie theater interior with rows of red seats facing a large blank screen |
| 21 | `place-city-center` | centro de la ciudad | a busy city center square with tall buildings, pedestrians and a fountain |
| 22 | `place-country-house` | casa de campo | a small wooden country house with a garden and a fence among trees |
| 23 | `place-high-rise-building` | edificio alto de departamentos | a tall high-rise apartment building with many windows rising above a city street |
| 24 | `place-lobby` | lobby | a spacious hotel lobby with a reception desk, sofas and a potted plant, no signs |
| 25 | `place-main-gate` | puerta principal | a large wide entrance gate of a building complex, open, with a paved path leading through |

### Lote 036

| # | Archivo | Palabra | Qué dibujar |
|---|---|---|---|
| 01 | `place-multi-story-building` | edificio de varios pisos | a tall apartment building with many floors and rows of windows seen from the street |
| 02 | `place-primary-school` | escuela primaria | a small colorful school building with children playing in the yard in front |
| 03 | `place-subway-station` | estación de metro | an underground subway station platform with a train arriving and passengers waiting, no readable signs |
| 04 | `place-tower` | torre | a tall stone tower rising against a blue sky with a few clouds |
| 05 | `school-eraser` | borrador | a white rubber pencil eraser lying next to a yellow pencil |
| 06 | `school-go-to-school` | ir a la escuela | a young schoolchild with a backpack walking toward a school building |
| 07 | `school-ruler` | regla | a straight transparent plastic ruler with marks lying on a notebook, no numbers visible |
| 08 | `shopping-cash-register` | caja registradora | a store cash register on a counter with an open drawer and a few coins, no readable text |
| 09 | `shopping-go-shopping` | ir de compras | a young woman carrying several colorful shopping bags walking in a shopping mall |
| 10 | `shopping-groceries` | compra de comida | a brown paper bag full of groceries including bread, vegetables and milk |
| 11 | `shopping-grocery` | hacer las compras de comida | an adult man pushing a shopping cart with vegetables and bread in a supermarket aisle |
| 12 | `shopping-parcel-delivery` | paquetería | a delivery man in uniform handing a cardboard parcel to a smiling woman at her door |
| 13 | `shopping-shopping-bag` | bolsa | a woman's hand holding a paper shopping bag with rope handles, no logo or text |
| 14 | `shopping-shopping-cart` | carrito de compras | a metal supermarket shopping cart filled with groceries in a store aisle |
| 15 | `sport-soccer` | jugar fútbol | two boys playing soccer on a grass field, one kicking the ball |
| 16 | `time-daytime` | día | a bright sunny sky at midday over a green park, sun high above |
| 17 | `time-early-morning` | mañana temprano | sunrise over a quiet village with soft orange light and mist at dawn |
| 18 | `time-evening` | por la noche | a city street at dusk with an orange and purple sky and lit windows |
| 19 | `weather-cold` | hacer frío | a man in a winter coat and scarf shivering outdoors in falling snow |
| 20 | `weather-hot` | hacer calor | a sweating man wiping his forehead under a blazing sun in a hot sunny street |
