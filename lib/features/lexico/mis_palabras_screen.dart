import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/lexico/lexico.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/widgets.dart';
import '../../core/i18n/i18n.dart';

/// «Mis palabras»: todo el vocabulario que el alumno ya vio en clases,
/// situaciones y Nivel 0, agrupado por nivel o por situación, con su repaso
/// espaciado por palabra.
class MisPalabrasScreen extends ConsumerStatefulWidget {
  const MisPalabrasScreen({super.key});

  @override
  ConsumerState<MisPalabrasScreen> createState() => _MisPalabrasScreenState();
}

enum _Agrupar { nivel, situacion }

class _MisPalabrasScreenState extends ConsumerState<MisPalabrasScreen> {
  _Agrupar agrupar = _Agrupar.nivel;
  String busqueda = '';

  @override
  void dispose() {
    VozNube.instancia.parar();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final mias = ref.watch(misPalabrasProvider);
    return Scaffold(
      appBar: AppBar(title: Text(tr('Mis palabras'))),
      body: Movil(
        child: mias.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (_, _) => Center(
            child: TextButton(
              onPressed: () => ref.invalidate(lexicoProvider),
              child: Text(tr('No se pudo cargar. Reintentar')),
            ),
          ),
          data: (palabras) {
            final estado = repasoLexico(s.practicas, s.idiomaMeta);
            final hoy = DateTime.now();
            final paraHoy = vencidasHoy(palabras, estado, hoy);
            final nuevas = palabras
                .where((e) => !estado.containsKey(e.clave))
                .length;
            final dominadas = palabras
                .where((e) => estado[e.clave]?.dominada ?? false)
                .length;
            if (palabras.isEmpty) return const _Vacio();
            final filas = _filas(palabras);
            return Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
                    itemCount: filas.length + 1,
                    itemBuilder: (context, i) {
                      if (i == 0) {
                        return _Cabecera(
                          total: palabras.length,
                          paraHoy: paraHoy,
                          dominadas: dominadas,
                          agrupar: agrupar,
                          onAgrupar: (a) => setState(() => agrupar = a),
                          onBuscar: (v) => setState(() => busqueda = v),
                        );
                      }
                      final f = filas[i - 1];
                      return f is String
                          ? Padding(
                              padding: const EdgeInsets.fromLTRB(0, 14, 0, 6),
                              child: Text(
                                f,
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w900,
                                ),
                              ),
                            )
                          : _FilaPalabra(
                              entrada: f as EntradaLexico,
                              caja: estado[f.clave]?.caja,
                              onOir: () => VozNube.instancia.reproducir(
                                f.texto,
                                s.idiomaMeta,
                              ),
                            );
                    },
                  ),
                ),
                DecoratedBox(
                  decoration: const BoxDecoration(
                    color: OL.fondo,
                    border: Border(top: BorderSide(color: OL.grisClaro)),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(20, 4, 20, 12),
                    child: BotonPrincipal(
                      onPressed: paraHoy + nuevas == 0
                          ? null
                          : () => context.push('/palabras/repaso'),
                      child: Text(
                        paraHoy > 0
                            ? (paraHoy == 1
                                  ? tr('REPASAR {n} PALABRA', {'n': paraHoy})
                                  : tr('REPASAR {n} PALABRAS', {'n': paraHoy}))
                            : nuevas > 0
                            ? tr('PRACTICAR PALABRAS NUEVAS')
                            : tr('TODO AL DÍA'),
                      ),
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  /// Encabezados (String) y palabras, ya filtradas y agrupadas.
  List<Object> _filas(List<EntradaLexico> palabras) {
    final q = busqueda.trim().toLowerCase();
    final visibles = q.isEmpty
        ? palabras
        : [
            for (final e in palabras)
              if (e.texto.toLowerCase().contains(q) ||
                  e.traduccion.toLowerCase().contains(q))
                e,
          ];
    final grupos = <String, List<EntradaLexico>>{};
    final deClases = tr('De las clases');
    for (final e in visibles) {
      if (agrupar == _Agrupar.nivel) {
        grupos
            .putIfAbsent(
              e.nivel == 0 ? tr('Desde cero') : tr('Nivel {n}', {'n': e.nivel}),
              () => [],
            )
            .add(e);
      } else {
        final ids = e.situaciones.toList()..sort();
        if (ids.isEmpty) {
          grupos.putIfAbsent(deClases, () => []).add(e);
        }
        for (final id in ids) {
          grupos.putIfAbsent(trDato(situacion(id).nombre), () => []).add(e);
        }
      }
    }
    final claves = grupos.keys.toList();
    if (agrupar == _Agrupar.situacion) {
      claves.sort((a, b) {
        if (a == deClases) return 1;
        if (b == deClases) return -1;
        return a.compareTo(b);
      });
    }
    return [
      for (final k in claves) ...[k, ...grupos[k]!],
    ];
  }
}

class _Vacio extends StatelessWidget {
  const _Vacio();

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(24),
    children: [
      const Icon(Icons.menu_book_rounded, size: 64, color: OL.morado),
      const SizedBox(height: 12),
      Text(
        tr(
          'Aquí aparecerán las palabras que aprendas en tus clases y situaciones, listas para repasar.',
        ),
        textAlign: TextAlign.center,
        style: const TextStyle(fontSize: 17, height: 1.4),
      ),
      const SizedBox(height: 20),
      BotonPrincipal(
        onPressed: () => context.go('/aprender'),
        child: Text(tr('IR A APRENDER')),
      ),
    ],
  );
}

class _Cabecera extends StatelessWidget {
  const _Cabecera({
    required this.total,
    required this.paraHoy,
    required this.dominadas,
    required this.agrupar,
    required this.onAgrupar,
    required this.onBuscar,
  });
  final int total, paraHoy, dominadas;
  final _Agrupar agrupar;
  final ValueChanged<_Agrupar> onAgrupar;
  final ValueChanged<String> onBuscar;

  Widget _dato(String valor, String nombre, Color color) => Expanded(
    child: Column(
      children: [
        Text(
          valor,
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.w900,
            color: color,
          ),
        ),
        Text(
          nombre,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 13, color: OL.gris),
        ),
      ],
    ),
  );

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Tarjeta(
        sombra: false,
        child: Row(
          children: [
            _dato('$total', tr('palabras'), OL.morado),
            _dato('$paraHoy', tr('para hoy'), OL.naranja),
            _dato('$dominadas', tr('dominadas'), OL.verde),
          ],
        ),
      ),
      const SizedBox(height: 12),
      TextField(
        onChanged: onBuscar,
        decoration: InputDecoration(
          hintText: tr('Buscar palabra…'),
          prefixIcon: const Icon(Icons.search),
        ),
      ),
      const SizedBox(height: 10),
      Wrap(
        spacing: 8,
        children: [
          for (final (a, nombre) in [
            (_Agrupar.nivel, tr('Por nivel')),
            (_Agrupar.situacion, tr('Por situación')),
          ])
            ChoiceChip(
              label: Text(nombre),
              selected: agrupar == a,
              onSelected: (_) => onAgrupar(a),
              selectedColor: OL.moradoClaro,
            ),
        ],
      ),
    ],
  );
}

class _FilaPalabra extends StatelessWidget {
  const _FilaPalabra({
    required this.entrada,
    required this.caja,
    required this.onOir,
  });
  final EntradaLexico entrada;
  final int? caja;
  final VoidCallback onOir;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 6),
    child: Tarjeta(
      sombra: false,
      onTap: onOir,
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      child: Row(
        children: [
          const Icon(Icons.volume_up_rounded, color: OL.morado, size: 20),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  entrada.texto,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                Text(
                  entrada.traduccion,
                  style: const TextStyle(color: OL.gris, fontSize: 14),
                ),
              ],
            ),
          ),
          // Fuerza de la memoria: un punto por repaso superado.
          Semantics(
            label: caja == null
                ? tr('Sin repasar')
                : tr('Repasada {n} veces', {'n': caja}),
            child: Row(
              children: [
                for (var i = 0; i < 5; i++)
                  Container(
                    width: 7,
                    height: 7,
                    margin: const EdgeInsets.only(left: 3),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: (caja ?? 0) > i ? OL.verde : OL.grisClaro,
                    ),
                  ),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}
