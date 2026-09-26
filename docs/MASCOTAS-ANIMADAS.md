# Mascotas del recorrido inicial

Lumo saluda en `/fundamentos`; Nara acompaña las comprobaciones guiadas. El resto de módulos y los tutores de voz siguen sin cambios.

Los clips originales de cinco segundos fueron generados con Higgsfield / Seedance 2.5, usando las láminas originales de OneLingo:

- Lumo: `3a4137cb-346b-45aa-8124-8a182b962a61`.
- Nara: `41ebd594-4531-4836-b321-1c6ecfae6c1f`.

Recursos distribuidos: WebP animado de 320 × 320, 12 fps, sin audio, más PNG de reposo. Aproximadamente 770 KiB en total. Se empaquetan en `assets/img/mascotas/`; no se generan por usuario y no requieren contactar Higgsfield en ejecución.

`MascotCoach` limita cada gesto a cinco segundos desde el primer fotograma y vuelve a la imagen estática. Usa el PNG durante carga o error, respeta movimiento reducido del sistema, el ajuste Efectos.animaciones y TickerMode de la ruta. Los personajes son decorativos para el lector de pantalla; su nombre y mensaje se leen como texto. No indican evaluación de micrófono ni pronunciación.

Para siguientes gestos: generar acierto y ánimo específicos, evitando celebrar respuestas incorrectas; reproducir al evento y dejar reposo entre eventos. Las variantes `-alpha` tienen transparencia real. Higgsfield video_background_remover devolvió H.264 sobre negro; se convirtió a RGBA con colorkey (0.025/0.02) antes de escalar y codificar WebP. Se comprobaron muestras de alfa a lo largo de ambos clips y los PNG sobre el fondo violeta claro. Los originales con fondo se conservan. Trabajos de recorte: Lumo 5fca86f6-c2c5-4068-9588-0a250accb484; Nara 186cad06-3dd4-40fd-bfa4-be274ae77479.
