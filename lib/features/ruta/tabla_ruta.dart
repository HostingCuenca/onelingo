import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/efectos.dart';
import 'item_view.dart';

/// Cuadro de escritura o de conjugación. Cada celda en el idioma meta se
/// escucha al tocarla (kana, hangul, cirílico, pinyin, formas verbales).
class TablaRuta extends StatelessWidget {
  const TablaRuta({
    super.key,
    required this.paso,
    required this.idioma,
    required this.cadena,
  });
  final Paso paso;
  final String idioma;
  final List<String> cadena;

  @override
  Widget build(BuildContext context) {
    final columnas = paso.filas.fold<int>(
      paso.columnas.length,
      (m, f) => f.length > m ? f.length : m,
    );
    final tabla = Table(
      defaultColumnWidth: columnas > 5
          ? const FixedColumnWidth(68)
          : const FlexColumnWidth(),
      defaultVerticalAlignment: TableCellVerticalAlignment.middle,
      border: TableBorder.symmetric(
        inside: const BorderSide(color: OL.moradoClaro, width: 1.2),
      ),
      children: [
        if (paso.columnas.isNotEmpty)
          TableRow(
            decoration: const BoxDecoration(color: OL.moradoClaro),
            children: [
              for (final c in paso.columnas)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 6),
                  child: Text(
                    c.en(cadena),
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      color: OL.morado,
                    ),
                  ),
                ),
            ],
          ),
        for (final fila in paso.filas)
          TableRow(
            children: [
              for (var i = 0; i < columnas; i++)
                i < fila.length
                    ? _CeldaVista(celda: fila[i], idioma: idioma, cadena: cadena)
                    : const SizedBox.shrink(),
            ],
          ),
      ],
    );
    return Container(
      decoration: BoxDecoration(
        color: OL.blanco,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: OL.moradoClaro, width: 2),
      ),
      clipBehavior: Clip.antiAlias,
      child: columnas > 5
          ? SingleChildScrollView(scrollDirection: Axis.horizontal, child: tabla)
          : tabla,
    );
  }
}

class _CeldaVista extends StatelessWidget {
  const _CeldaVista({
    required this.celda,
    required this.idioma,
    required this.cadena,
  });
  final Celda celda;
  final String idioma;
  final List<String> cadena;

  @override
  Widget build(BuildContext context) {
    final texto = celda.texto;
    if (texto == null) {
      return Padding(
        padding: const EdgeInsets.all(8),
        child: Text(
          celda.apoyo?.en(cadena) ?? '',
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 15, color: OL.gris, height: 1.3),
        ),
      );
    }
    final corta = texto.runes.length <= 3;
    return Semantics(
      button: true,
      label: 'Escuchar $texto',
      child: InkWell(
        onTap: () {
          Efectos.toque();
          escucharTexto(context, texto, idioma);
        },
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 6),
          child: Column(
            children: [
              Text(
                texto,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: corta ? 26 : 18,
                  fontWeight: FontWeight.w800,
                  color: OL.texto,
                ),
              ),
              if (celda.rom != null)
                Text(
                  celda.rom!,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: OL.gris, fontSize: 14),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
