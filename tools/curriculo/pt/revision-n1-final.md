# Auditoría longitudinal final · pt-BR N1

## Veredicto: GO

Audité `curriculo/pt/n1.json` ya consolidado frente a `tools/curriculo/pt/n1-outline.json`, con revisión específica de las fronteras C05→06, C10→11, C15→16, C20→21, C25→26, C30→31, C35→36, C40→41 y C45→46.

## Pruebas ejecutadas

* `python3 tools/curriculo/validar_outline_n1.py pt` → **0 errores · 50 clases · 49 claves nuevas · 40 previos**.
* `python3 tools/curriculo/validar_plan_detallado.py pt` → **0 errores · 50 clases · 652 ejercicios · 650 consignas únicas · 652 ejemplos únicos**.
* Comparación programática de raíz y metadatos (`bloque`, título, objetivo, gramática, claves, vocabulario, sonido, situación y tarea) contra el outline → **0 diferencias**; las 50 clases tienen `estado: planificado`.
* Secuencia de IDs → exactamente `pt.n1.c01`…`pt.n1.c50`, en orden.
* Conteo por clase → C01–C49 tienen 3 guiadas + 3 independientes + 2 situación + 5 evaluación; C50 tiene 7 evaluaciones de cierre.
* Cronología de claves, sembrada con los 40 `previos` del marco → **0 claves recicladas antes de estar disponibles, 0 duplicados de introducción y 49/49 introducciones únicas**.

## Continuidad en fronteras

Cada frontera solicitada recicla explícitamente la clave introducida en la clase anterior: `nationalities-expanded`, `regular-present-transfer`, `possessives-basic`, `confirmation-repair`, `demonstratives-basic`, `routine-preferences`, `location-description-transfer`, `shopping-modal-transfer` y `dates-calendar`, respectivamente. La secuencia no deja huecos ni introduce una clave futura.

Las revisiones de lotes C06–C45 están en GO y son coherentes con el consolidado; los pilotos C01–C05 y C46–C50 también constan como GO. C50 no introduce clave nueva y consolida las claves tardías (`desde-faz`, los tres grupos de perfeito y el resto de funciones N1).

## Límites y metadatos

No se detectan saltos de progresión en las claves ni discrepancias entre metadatos del outline y el plan. La pronunciación permanece como práctica no bloqueante. El consolidado conserva los 40 previos y los límites declarados para imperativo, `tem/há`, `ir + infinitivo`, fechas y pretérito inicial.

**Conclusión:** el N1 consolidado puede pasar a la siguiente etapa sin reescritura longitudinal.
