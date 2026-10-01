# Tutor con avatar v2 — análisis y plan

Fecha: 2026-09-30. Responsable: Claude. Base: auditoría del código (avatar web, chat, backend) e investigación de cómo lo resolvió Duolingo.

## Diagnóstico: por qué se siente lento

El retraso viene de la cadena de esperas, no del dibujo del avatar:

| # | Cuello de botella | Impacto |
|---|---|---|
| 1 | Fin de turno por **3 s de silencio** + grabación completa + transcripción sin streaming | ~4–5 s antes de que la IA empiece |
| 2 | Modelos 3D de **22–28 MB** (texturas PNG de hasta 4096²) y la conversación esperaba a que terminaran de descargarse | 7–17 s en móvil al abrir |
| 3 | La IA escribe la respuesta completa antes de que empiece la voz (sin frases en streaming) | 2,6–5 s medidos por turno |
| 4 | JS del visor y `main.dart.js` servidos **sin gzip**; ~0,6 s de primer byte por petición | segundos en la carga inicial |
| 5 | Safari/iOS descarga el MP3 completo antes de reproducir | +1–2 s en iPhone |
| 6 | Boca por volumen (2 de 32 formas) | calidad percibida, no latencia |

Pedagogía: el avatar no recibía la unidad, el vocabulario enseñado ni los errores recientes del alumno; las 10 personalidades comparten el mismo prompt.

## Cómo lo hizo Duolingo (Video Call con Lily)

- **2D con Rive** (máquina de estados, < 1 MB), más de 20 bocas (visemas) sincronizadas con el audio y decenas de variantes de reposo. Nada de vídeo generado por frase.
- **Ocultar la latencia con estados**: si hay espera, Lily «piensa» con un gesto en lugar de una pausa muerta.
- **GPT-4o** con prompt en tres capas (diseñadores de aprendizaje · personaje · alumno), nivel MCER, estructura de llamada (apertura, primera pregunta preparada, conversación, cierre) y memoria de «hechos del alumno» tras cada llamada.
- Fuentes: blog de Rive y de Duolingo, heise, whitepaper de Duolingo (ver informe de investigación).

## Fase 1 — hecha (releases edu-16 a edu-19)

- Modelos 3D optimizados (texturas 1024 px WebP + geometría meshopt, visemas intactos): **22–28 MB → 1,5–2,1 MB** por tutor (~3 s en producción).
- El saludo (texto y voz) se pide **en paralelo** a la descarga del modelo.
- Fin de turno de voz: **1,2 s** de silencio (avatar web y chat), con botón Terminar.
- Boca por bandas de frecuencia (A, O/U, E/I, S, labios cerrados) en lugar de solo abrir/cerrar.
- Integración: pantalla nativa única «Tutores con IA» (videollamada 3D + chat de voz/texto), visor en tema claro dentro de la app con cabecera y pestañas, brazos con caída natural, retratos regenerados.
- Estados tipo Duolingo: **pensando** (cabeza inclinada, mirada arriba, cejas) mientras llega la respuesta o la voz, y **escuchando** (leve asentimiento) mientras el alumno habla.

## Fase 2 — propuesta (requiere decisiones)

1. **Servidor** (cambio de configuración, requiere autorización): gzip para JS/WASM y `Cache-Control` largo para modelos e imágenes. Reduce la carga inicial de ~5 MB a ~1,5 MB.
2. **Backend** (requiere reiniciar `onelingo-api`): la IA emite la respuesta **frase a frase** y la voz arranca con la primera frase → ~1–1,5 s hasta oír al tutor.
3. **Pedagogía**: pasar al tutor la unidad actual, el vocabulario y los errores recientes; prompt en tres capas; tarjeta de corrección en pantalla (el tutor la dice breve); resumen de «hechos del alumno» al terminar.
4. **Lumo como tutor que habla** (recomendado, al estilo Duolingo): personaje 2D con 6–8 bocas y estados (escucha, piensa, habla, corrige, celebra).
   - Activo necesario: un archivo **Rive** de Lumo, o un juego de imágenes de su boca (cerrada, A, O, E, U, M/B/P) con el mismo encuadre.
   - Voz: mantener la cadena actual en streaming (barata) o pasar a voz a voz en tiempo real (Gemini Live ≈ $0,012/min; gpt-realtime mini ≈ $0,02–0,05/min) con la boca por amplitud.
5. **HeyGen**: LiveAvatar no admite personajes de dibujos (no sirve para Lumo en tiempo real) y cuesta ≈ $0,08/min. Usarlo para **vídeos pre-renderizados** (intros de nivel, explicaciones), no para la conversación.
