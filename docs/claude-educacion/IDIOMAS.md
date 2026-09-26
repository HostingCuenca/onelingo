# Idiomas habilitados

Fuente oficial: `lib/core/content/curriculum.dart:11` (`const idiomas`). Verificado 2026-09-26.
El onboarding permite elegir cualquiera como nativo y cualquiera distinto como meta. La interfaz general está en español; el contenido de las rutas se muestra en el idioma de apoyo del alumno (DEC-004).

Estados: MAPEADO (en el currículo) → DISEÑADO (objetivos y estructura) → IMPLEMENTADO (en la app) → PROBADO (pasa pruebas) → PRODUCCIÓN.

## Tabla maestra

| Idioma | Fundamentos (f0) | A1 | A2 | B1 | B2 | C1 | C2 | Implementación actual |
|---|---|---|---|---|---|---|---|---|
| en Inglés | PROBADO · revisada | DISEÑADO (grafo) + legado | DISEÑADO + legado | DISEÑADO + legado | DISEÑADO + legado | DISEÑADO + legado | MAPEADO (planificado) | Ruta f0 6 u · 69 vocablos · 72 ítems; biblioteca, 43 guías, lectura/listening, 50 situaciones (legado, esquema antiguo) |
| es Español | PROBADO · inicial · apoyo en | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 89 · 91; niveles 0–2 legado (monolingüe, no sirve para no hispanohablantes) |
| fr Francés | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 93 · 89; niveles 1–2 legado; 3–10 banco genérico en inglés |
| de Alemán | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 93 · 93; idem |
| pt Portugués (BR) | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 93 · 91; idem |
| it Italiano | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 91 · 90; idem |
| zh Chino | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 78 · 81; idem |
| ja Japonés | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 86 · 80; idem |
| ko Coreano | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 92 · 81; idem |
| ru Ruso | PROBADO · inicial | DISEÑADO (A1 inicial) | MAPEADO | MAPEADO | MAPEADO | MAPEADO | MAPEADO | Ruta f0 6 u · 75 · 92; idem |

«Legado» = contenido del esquema antiguo (`assets/contenido/<idioma>/nivel-N.json`, `curriculum.dart`), no migrado al esquema 2 ni conectado al modelo de dominio. Ningún idioma está completo: solo sus fundamentos.

## Rutas de fundamentos por idioma

| Idioma | Unidades (orden 0 → 5) | Particularidad |
|---|---|---|
| en | primer-contacto · pronombres · be-afirmativo · be-negativo · be-preguntas · presentarse | referencia; migra foundations-v1 |
| es | sonidos-saludos · yo-tu-usted · ser · estar · negacion-preguntas · presentarse | para no hispanohablantes; textos de apoyo en inglés; ustedes |
| fr | premier-contact · sons · pronoms · etre · negation-questions · se-presenter | sujeto obligatorio, tu/vous, nasales |
| de | laute-gruesse · pronomen-du-sie · sein-heissen · der-die-das · nicht-kein-fragen · vorstellen | género y artículos, V2 |
| pt | primeiro-contato · sons · pronomes · ser-estar · negacao-perguntas · apresentar-se | pt-BR, você + 3.ª persona, falsos amigos |
| it | primo-contatto · suoni · pronomi · essere-stare · negazione-domande · presentarsi | consonantes dobles, tu/Lei |
| zh | tonos-saludos · pinyin · caracteres · pronombres · shi-bushi-ma · presentarse | tonos antes de gramática; frases con espacios |
| ja | vocales-saludos · hiragana-1 · hiragana-2 · katakana · desu · jikoshoukai | kana en 3 unidades; sin kanji en f0 |
| ko | vocales-saludos · consonantes-bloques · batchim · personas · ieyo-yeyo · presentarse | hangul antes de gramática; 해요체 |
| ru | bukvy-druzya · bukvy-novye · mestoimeniya · eto · ne-voprosy · predstavlenie | cirílico, acento marcado en `rom`, presente sin «ser» |

Revisión nativa pendiente en los 9 idiomas marcados «inicial»: lista de puntos en DECISIONES.md (DEC-010).

## Actualización 2026-09-26 (release edu-3)

| Idioma | Fundamentos (f0) | A1 (esquema 2) | Escritura / sonidos en f0 |
|---|---:|---:|---|
| en | 7 u. | 29 u. | alfabeto + sonidos |
| es | 8 u. | 9 u. | alfabeto, vocales y consonantes (para angloparlantes) |
| fr | 8 u. | 9 u. | alfabeto, vocales, nasales, liaison |
| de | 8 u. | 9 u. | alfabeto, Umlaute, vocales y consonantes |
| pt | 8 u. | 9 u. | alfabeto, vocales abiertas/nasales, consonantes |
| it | 8 u. | 9 u. | alfabeto, c/g, dobles, vocales |
| zh | 13 u. | 9 u. | 4 tonos + neutro, 21 iniciales, finales, sandhi, trazos, radicales |
| ja | 16 u. | 8 u. | hiragana y katakana completos (+ dakuten, yōon, っ, vocales largas, préstamos) |
| ko | 9 u. | 9 u. | hangul completo: 21 vocales, 19 consonantes, 받침, reglas de lectura |
| ru | 10 u. | 9 u. | 33 letras, vocales duras/blandas, ь ъ, acento y reducción |

Todas las rutas: PROBADO (validador y pruebas); 9 idiomas «inicial» (revisión nativa pendiente, DEC-010). A1 de otros idiomas = módulo «Primeras frases» (nivel `a1-1`); `a1-2` pendiente salvo inglés.
