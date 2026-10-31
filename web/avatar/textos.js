// Textos de interfaz de la videollamada en el idioma de la app (?ui=en|es).
// Como `tr()` en la app: el texto en español es la clave y, si falta la
// traducción, se ve el español (nunca un hueco). Lo que dice el tutor, las
// ideas y la traducción vienen del servidor y no pasan por aquí.
export const ui = new URLSearchParams(location.search).get('ui') === 'en' ? 'en' : 'es';

const EN = {
  // Página (index.html)
  'Tutores IA · OneLingo': 'AI Tutors · OneLingo',
  'ONELINGO · TUTOR CON IA': 'ONELINGO · AI TUTOR',
  'Una conversación, a tu ritmo.': 'A conversation at your own pace.',
  'Elige a tu tutor.': 'Choose your tutor.',
  'Conectando con tu sesión…': 'Connecting to your session…',
  'Volver a los tutores': 'Back to tutors',
  'Preparando…': 'Getting ready…',
  'Ver la conversación': 'View conversation',
  'Cambiar el tema de la conversación': 'Change the conversation topic',
  'Conversación libre': 'Free conversation',
  'Cargando…': 'Loading…',
  'Pedir una pista al tutor': 'Ask the tutor for a hint',
  'Pista': 'Hint',
  '↻ Repetir': '↻ Replay',
  'Ver traducción': 'Show translation',
  'Ocultar traducción': 'Hide translation',
  'Reportar la última respuesta del tutor': "Report the tutor's last reply",
  'Reportar': 'Report',
  'Escribe tu respuesta…': 'Type your answer…',
  'Tu mensaje': 'Your message',
  'Enviar': 'Send',
  'Contestar': 'Answer',
  'Escribir en lugar de hablar': 'Type instead of talking',
  'Mantén pulsado para hablar': 'Press and hold to talk',
  'Colgar la llamada': 'Hang up',
  'Conversación': 'Conversation',
  'Cerrar': 'Close',
  'Cuéntanos qué está mal en esta respuesta del tutor. Nuestro equipo la revisará.': "Tell us what's wrong with this reply from the tutor. Our team will review it.",
  '¿Qué pasó?': 'What happened?',
  'Motivo del reporte': 'Reason for the report',
  'Comentario (opcional)': 'Comment (optional)',
  'Enviar reporte': 'Send report',
  // Idiomas que se practican
  'inglés': 'English', 'español': 'Spanish', 'francés': 'French', 'alemán': 'German', 'portugués': 'Portuguese',
  'italiano': 'Italian', 'chino': 'Chinese', 'japonés': 'Japanese', 'coreano': 'Korean', 'ruso': 'Russian',
  // Galería e inicio
  'Nivel {nivel} · tutores para practicar {idioma}': 'Level {nivel} · tutors to practice {idioma}',
  'Inicia sesión en OneLingo para conversar con los tutores.': 'Sign in to OneLingo to talk with the tutors.',
  'Escribe en {idioma}…': 'Type in {idioma}…',
  'Retrato de {nombre}': 'Portrait of {nombre}',
  'Tu compañero de OneLingo': 'Your OneLingo buddy',
  'Tutor de {idioma} · {estilo}': '{idioma} tutor',
  'Recomendado': 'Recommended',
  'Inicia sesión para conversar': 'Sign in to talk',
  'Inicia sesión en OneLingo para conversar con tu tutor.': 'Sign in to OneLingo to talk with your tutor.',
  'Cargando a {nombre}…': 'Loading {nombre}…',
  'Cargando a {nombre} · {pct} %': 'Loading {nombre} · {pct}%',
  'No se pudo cargar el tutor. Regresa y vuelve a intentarlo.': "Couldn't load the tutor. Go back and try again.",
  'No se pudo cargar a Lumo. Revisa tu conexión.': "Couldn't load Lumo. Check your connection.",
  'El rig del tutor no está disponible.': "The tutor's model isn't available.",
  // Llamada
  'Te está llamando…': 'Calling you…',
  '{nombre} te está llamando…': '{nombre} is calling you…',
  'Conectando…': 'Connecting…',
  'No se pudo conectar': "Couldn't connect",
  'Volver a llamar': 'Call again',
  'El tutor no responde. Revisa tu conexión y vuelve a llamar.': "The tutor isn't responding. Check your connection and call again.",
  'Reconectando con {nombre}…': 'Reconnecting with {nombre}…',
  'En llamada · {tiempo}': 'On call · {tiempo}',
  'Llamada terminada': 'Call ended',
  'Hablando': 'Speaking',
  'Hablando…': 'Speaking…',
  'Pensando…': 'Thinking…',
  'Te escucho': 'Listening',
  'Te escucho…': 'Listening…',
  'Tu turno': 'Your turn',
  'Micrófono en silencio': 'Mic muted',
  'Preparando voz…': 'Preparing voice…',
  'La voz no está disponible ({estado}).': 'Voice is unavailable ({estado}).',
  'Reintentar': 'Try again',
  'Micrófono silenciado: toca 🎙 para hablar.': 'Mic muted: tap 🎙 to talk.',
  'Puedes interrumpir hablando.': 'You can interrupt by talking.',
  'Mantén pulsado 🎙 para interrumpir y responder.': 'Hold 🎙 to interrupt and reply.',
  'Tu turno: habla cuando quieras.': "Your turn: talk whenever you're ready.",
  'Tu turno: mantén pulsado 🎙 para responder.': 'Your turn: hold 🎙 to reply.',
  'Mantén pulsado 🎙 y responde en voz alta.': 'Hold 🎙 and answer out loud.',
  'Corrección': 'Correction',
  'Puedes decir': 'You can say',
  'No se pudo transcribir. Vuelve a intentarlo o escribe con ⌨️.': "Couldn't transcribe that. Try again or type with ⌨️.",
  'No te escuché bien. Mantén pulsado el micrófono mientras hablas.': "I didn't catch that. Hold the mic while you talk.",
  'Tu sesión ha caducado. Vuelve a iniciar sesión.': 'Your session has expired. Please sign in again.',
  'No se pudo conectar con el tutor ({estado}).': "Couldn't reach the tutor ({estado}).",
  'La respuesta quedó incompleta.': 'The reply was cut off.',
  'El tutor tardó demasiado.': 'The tutor took too long.',
  'No se pudo responder.': "Couldn't reply.",
  'No se pudo responder': "Couldn't reply",
  'Tu prueba gratuita terminó. Elige un plan para seguir practicando con el tutor.': 'Your free trial has ended. Choose a plan to keep practicing with the tutor.',
  'El acceso de demostración está cerrado.': 'Demo access is closed.',
  'No hay conexión. Vuelve a intentarlo cuando tengas internet.': "You're offline. Try again when you're connected.",
  // Micrófono
  'OneLingo no tiene permiso del micrófono: actívalo en Ajustes › Apps › OneLingo › Permisos, o escribe con ⌨️.': "OneLingo doesn't have microphone access: turn it on in Settings › Apps › OneLingo › Permissions, or type with ⌨️.",
  'Activa el permiso del micrófono para hablar, o escribe con ⌨️.': 'Allow microphone access to talk, or type with ⌨️.',
  'No encontramos un micrófono en este dispositivo. Puedes escribir con ⌨️.': "We couldn't find a microphone on this device. You can type with ⌨️.",
  'Otra app está usando el micrófono (una llamada o una grabadora). Ciérrala y vuelve a intentarlo, o escribe con ⌨️.': 'Another app is using the microphone (a call or a recorder). Close it and try again, or type with ⌨️.',
  'No se pudo abrir el micrófono. Puedes escribir con ⌨️.': "Couldn't open the microphone. You can type with ⌨️.",
  'Permitir micrófono': 'Allow microphone',
  'Micrófono listo: mantén pulsado 🎙 para hablar.': 'Mic ready: hold 🎙 to talk.',
  'Habla… suelta para enviar · ← desliza para cancelar': 'Talk… release to send · ← slide to cancel',
  '● 0:{s} · suelta para enviar · ← desliza para cancelar': '● 0:{s} · release to send · ← slide to cancel',
  'Mantén pulsado 🎙 mientras hablas.': 'Hold 🎙 while you talk.',
  'Mensaje cancelado.': 'Message canceled.',
  'Mantén pulsado 🎙 mientras hablas y suelta al terminar.': "Hold 🎙 while you talk and release when you're done.",
  'No te escuché. Acércate al micrófono y vuelve a intentarlo.': "I couldn't hear you. Move closer to the mic and try again.",
  'Suelta para cancelar': 'Release to cancel',
  'Silenciado · toca 🎙 para hablar': 'Muted · tap 🎙 to talk',
  'Micrófono abierto · habla cuando quieras': "Mic on · talk whenever you're ready",
  'Reconectando el micrófono…': 'Reconnecting the mic…',
  'Se cortó la escucha en vivo: mantén pulsado 🎙 para hablar.': 'Live listening dropped: hold 🎙 to talk.',
  'La escucha en vivo vuelve en unos minutos: mientras, mantén pulsado 🎙 para hablar.': 'Live listening will be back in a few minutes. In the meantime, hold 🎙 to talk.',
  'Mantén pulsado 🎙 para hablar.': 'Hold 🎙 to talk.',
  // Hoja inferior: temas y reporte
  '¿Qué quieres practicar?': 'What do you want to practice?',
  'Reportar respuesta': 'Report reply',
  'Nuevo tema: {tema}': 'New topic: {tema}',
  'Ofensiva': 'Offensive',
  'Incorrecta': 'Incorrect',
  'Inapropiada': 'Inappropriate',
  'Otro motivo': 'Other reason',
  'Enviando…': 'Sending…',
  'Enviaste muchos reportes. Inténtalo de nuevo más tarde.': "You've sent a lot of reports. Please try again later.",
  'No se pudo enviar el reporte. Inténtalo de nuevo.': "Couldn't send the report. Please try again.",
  'Gracias, lo revisaremos.': "Thanks, we'll take a look.",
  'No se pudo conectar. Revisa tu conexión.': "Couldn't connect. Check your connection.",
  // Resumen al colgar
  'Resumen de la llamada': 'Call summary',
  'No se pudo preparar el resumen.': "Couldn't prepare the summary.",
  'Lo hiciste bien': 'What you did well',
  'Para mejorar': 'To improve',
  'Vocabulario de hoy': "Today's vocabulary",
  '{nombre} recordará esto en tu próxima llamada.': '{nombre} will remember this on your next call.',
};

/** Texto de interfaz: `t('Cargando a {nombre}…', {nombre})`. */
export function t(es, datos = {}) {
  let s = ui === 'en' ? EN[es] ?? es : es;
  for (const [k, v] of Object.entries(datos)) s = s.replaceAll(`{${k}}`, String(v));
  return s;
}

/** Nombre de un tema (topics.json) en el idioma de la interfaz. */
export const nombreTema = u => (ui === 'en' && u.en) || u.nombre;

/** Traduce los textos fijos de index.html (texto, aria-label, placeholder, title). */
export function traducirPagina() {
  document.documentElement.lang = ui;
  if (ui === 'es') return;
  document.title = t(document.title);
  for (const e of document.querySelectorAll('[aria-label],[placeholder],[title]')) {
    for (const a of ['aria-label', 'placeholder', 'title']) if (e.hasAttribute(a)) e.setAttribute(a, t(e.getAttribute(a)));
  }
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const k = n.nodeValue.trim();
    if (k && EN[k]) n.nodeValue = n.nodeValue.replace(k, EN[k]);
  }
}

/** Para pruebas: claves sin traducción en inglés entre las dadas. */
export const sinTraducir = claves => claves.filter(k => !(k in EN));
