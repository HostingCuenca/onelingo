import 'correccion.dart';
import 'grafo.dart';
import 'modelos.dart';

final _puntuacion = RegExp(r'[.,!?¡¿;:。、！？「」…"“”()«»—–，：；]');

/// Palabras de un texto en el idioma meta (misma regla que tools/validar_ruta.py).
List<String> palabrasMeta(String texto) => texto
    .replaceAll('’', "'")
    .replaceAll('___', ' ')
    .toLowerCase()
    .replaceAll(_puntuacion, ' ')
    .split(RegExp(r'\s+'))
    .where((p) => p.isNotEmpty && p != '-')
    .toList();

/// Problemas pedagógicos y de datos de una ruta. Vacío = íntegra.
List<String> problemasDeContenido(RutaCargada ruta) {
  final errores = [...validarGrafo(ruta.unidades)];
  final apoyos = ruta.curso.idiomasApoyo;
  final libres = {for (final p in ruta.curso.palabrasLibres) ...palabrasMeta(p)};

  void apoyo(TextoApoyo? t, String donde) {
    for (final l in apoyos) {
      if ((t?.porIdioma[l] ?? '').trim().isEmpty) {
        errores.add('$donde: falta texto de apoyo "$l"');
      }
    }
  }

  Set<String> conocidas(UnidadRuta u) => {
    ...libres,
    for (final id in {u.id, ...prerequisitosTransitivos(ruta, u.id)})
      for (final x in [ruta.unidad(id)!]) ...[
        for (final v in x.vocabulario) ...palabrasMeta(v.texto),
        for (final e in x.erroresFrecuentes)
          ...palabrasMeta(e.incorrecto.replaceAll(RegExp(r'\([^)]*\)'), ' ')),
      ],
  };

  for (final u in ruta.unidades) {
    final saber = conocidas(u);
    void meta(String? texto, String donde) {
      if (texto == null) return;
      final faltan = palabrasMeta(texto).where((w) => !saber.contains(w)).toSet();
      if (faltan.isNotEmpty) {
        errores.add('$donde: palabras no enseñadas ${faltan.join(', ')}');
      }
    }

    apoyo(u.titulo, '${u.id}.titulo');
    apoyo(u.objetivo, '${u.id}.objetivo');
    for (final v in u.vocabulario) {
      apoyo(v.traduccion, '${u.id}.${v.id}');
    }
    if (u.pasos.isEmpty || !u.pasos.first.tipo.ensena) {
      errores.add('${u.id}: no empieza enseñando');
    }
    if (u.pasos.isNotEmpty && u.pasos.last.tipo != TipoPaso.evaluacion) {
      errores.add('${u.id}: la evaluación no es el último paso');
    }
    // Enseñar → guiada → independiente → situación → evaluación.
    var rango = -1;
    for (final p in u.pasos) {
      final r = switch (p.tipo) {
        _ when p.tipo.ensena => 0,
        TipoPaso.practicaGuiada => 1,
        TipoPaso.practicaIndependiente => 2,
        TipoPaso.situacion => 3,
        _ => 4,
      };
      if (r < rango) errores.add('${u.id}.${p.id}: paso fuera de orden');
      if (r > rango) rango = r;
      if (p.texto != null || p.tipo == TipoPaso.explicacion) {
        apoyo(p.texto, '${u.id}.${p.id}.texto');
      }
      if (p.tipo == TipoPaso.situacion) apoyo(p.contexto, '${u.id}.${p.id}.contexto');
      for (final f in p.frases) {
        meta(f.texto, '${u.id}.${p.id}');
        apoyo(f.traduccion, '${u.id}.${p.id}.traduccion');
      }
    }
    for (final tipo in [
      TipoPaso.practicaGuiada,
      TipoPaso.situacion,
      TipoPaso.evaluacion,
    ]) {
      if (!u.pasos.any((p) => p.tipo == tipo)) {
        errores.add('${u.id}: falta ${tipo.name}');
      }
    }
    final evaluacion = u.itemsDe(TipoPaso.evaluacion).map((e) => e.$2).toList();
    if (evaluacion.length < 4 ||
        evaluacion.map((i) => i.formato).toSet().length < 2) {
      errores.add('${u.id}: evaluación con < 4 ítems o < 2 formatos');
    }
    for (final p in u.pasos) {
      for (final i in p.items) {
        final donde = '${u.id}.${p.id}.${i.id}';
        apoyo(i.consigna, '$donde.consigna');
        apoyo(i.feedback, '$donde.feedback');
        meta(i.respuesta, donde);
        meta(i.texto, donde);
        meta(i.audio, donde);
        meta(i.pregunta, donde);
        for (final o in i.opciones) {
          o.meta != null ? meta(o.meta, donde) : apoyo(o.apoyo, donde);
        }
        for (final par in i.pares) {
          meta(par.$1, donde);
          apoyo(par.$2, donde);
        }
        // La clave del propio contenido debe corregirse como correcta.
        final clave = switch (i.formato) {
          FormatoItem.elegir || FormatoItem.escuchar => i.indiceRespuesta,
          FormatoItem.relacionar => true,
          _ => i.respuesta,
        };
        if (!corregir(i, clave, u.idioma)) {
          errores.add('$donde: la respuesta del contenido no se acepta');
        }
        if (i.formato == FormatoItem.ordenar &&
            !respuestaEscritaCorrecta(i, i.tokens.join(' '), u.idioma) &&
            !_mismosTokens(i)) {
          errores.add('$donde: las fichas no forman la respuesta');
        }
        if ((i.formato == FormatoItem.elegir ||
                i.formato == FormatoItem.escuchar) &&
            (i.indiceRespuesta == null ||
                i.indiceRespuesta! >= i.opciones.length)) {
          errores.add('$donde: índice de respuesta inválido');
        }
      }
    }
  }
  return errores;
}

bool _mismosTokens(Item i) {
  final a = palabrasMeta(i.tokens.join(' '))..sort();
  final b = palabrasMeta(i.respuesta ?? '')..sort();
  return a.join('|') == b.join('|');
}
