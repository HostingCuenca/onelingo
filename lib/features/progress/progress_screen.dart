import '../../shared/widgets/mascot_coach.dart';
import '../../shared/widgets/feedback_experience.dart';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/content/catalog.dart';
import '../../core/content/curriculum.dart';
import '../../core/models/models.dart';
import '../../core/i18n/i18n.dart';
import '../../core/lexico/lexico.dart';
import '../../core/nivel0/nivel0.dart';
import '../../core/pagos/providers.dart';
import '../plans/idiomas_plan.dart';
import 'codigo_referido.dart';
import 'eliminar_cuenta.dart';
import '../../core/api/sync.dart';
import '../../core/state/providers.dart';
import '../../core/version.dart';
import '../../shared/widgets/enlaces_legales.dart';
import '../../shared/widgets/selector_idioma_app.dart';
import '../../shared/widgets/widgets.dart';

/// Perfil y progreso del estudiante (REQUERIMIENTOS §13).
class ProgressScreen extends ConsumerWidget {
  const ProgressScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    // Sin sesión de servidor (o usuario de prueba) los datos son solo locales.
    final demo = !usaServidorPagos(s.email);
    // Nivel que ve el alumno: el de la ruta, sin superar lo publicado.
    final nAlumno = ref.watch(nivelAlumnoProvider);
    final ruta = ref.watch(rutaProvider(s.idiomaMeta)).valueOrNull;
    final estados = ruta == null ? null : estadosAlumno(ruta, s);
    final pos = ruta == null ? null : posicionEnRuta(ruta, s);
    // Quien empieza de cero pasa antes por el Nivel 0 · Leer y pronunciar.
    final n0Datos = ref.watch(nivel0Provider).valueOrNull;
    final n0 = s.nivel0Pendiente ? n0Datos : null;
    final n0Hechas = n0Datos == null
        ? 0
        : n0Datos.lecciones
              .where(
                (l) => leccionN0Completa(s.practicas, n0Datos.idioma, l.id),
              )
              .length;
    // Nivel y clase actuales con el mismo criterio que Aprender.
    final nivelPos = pos?.nivel == null
        ? null
        : ruta!.curso.niveles.where((x) => x.id == pos!.nivel).firstOrNull;
    final etiquetaNivel = n0 != null
        ? tr('Nivel 0 · Leer y pronunciar')
        : nivelPos != null
        ? _tituloNivel(nivelPos)
        : tr('Nivel {n}', {'n': nAlumno});
    final claseActual = n0 != null && n0.lecciones.isNotEmpty
        ? '${(n0Hechas + 1).clamp(1, n0.lecciones.length)}/${n0.lecciones.length}'
        : pos != null && pos.nivel != null
        ? '${pos.clase}/${pos.total}'
        : '—';
    final hab = s.porHabilidad;
    final maxHab = hab.values.fold(1, (a, b) => a > b ? a : b);
    final t = tutor(s.tutorId);
    final estadoPlan = ref.watch(estadoPlanProvider);
    final nombrePlan = estadoPlan.tienePlan
        ? (ref
                  .watch(catalogoPlanesProvider)
                  .plan(estadoPlan.planId)
                  ?.nombreEn(s.interfaz) ??
              estadoPlan.planId)
        : null;
    // Estado de la suscripción: el del servidor si lo hay; en DEMO, activa.
    final sus = estadoPlan.suscripcion;
    final estadoSuscripcion = sus != null && (sus.acceso || sus.stripeVigente)
        ? (sus.esCortesia ? tr('Cortesía') : sus.estadoTexto)
        : tr('Activa');

    return Scaffold(
      appBar: AppBar(title: Text(tr('Mi progreso'))),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          MascotCoach(
            message: tr(
              'Tu progreso se construye practicando y repasando. Cada habilidad cuenta.',
            ),
          ),
          Tarjeta(
            child: Row(
              children: [
                CircleAvatar(
                  radius: 30,
                  backgroundColor: OL.moradoClaro,
                  child: Text(
                    s.nombre.isEmpty ? 'B' : s.nombre[0].toUpperCase(),
                    style: const TextStyle(
                      color: OL.morado,
                      fontSize: 24,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        s.nombre,
                        style: Theme.of(context).textTheme.headlineSmall,
                      ),
                      Text(
                        '${trDato(idioma(s.idiomaNativo).nombre)} → ${trDato(idioma(s.idiomaMeta).nombre)}',
                        style: const TextStyle(color: OL.gris, fontSize: 14),
                      ),
                      const SizedBox(height: 6),
                      Wrap(
                        spacing: 6,
                        runSpacing: 6,
                        children: [
                          Etiqueta(etiquetaNivel),
                          Etiqueta(
                            nombrePlan ?? tr('Prueba gratuita'),
                            color: nombrePlan == null
                                ? const Color(0xFF9A6B00)
                                : OL.verde,
                            fondo: nombrePlan == null ? OL.amarilloSuave : null,
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          GridView.count(
            crossAxisCount: 2,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            childAspectRatio: 1.7,
            children: [
              _Stat(Icons.bolt_outlined, '${s.xp}', 'XP', OL.naranja),
              _Stat(
                Icons.local_fire_department_outlined,
                s.rachaVigente == 1
                    ? tr('{n} día', {'n': s.rachaVigente})
                    : tr('{n} días', {'n': s.rachaVigente}),
                tr('Racha'),
                OL.rojo,
              ),
              _Stat(
                Icons.schedule_outlined,
                '${s.segundosEstudio ~/ 60} min',
                tr('Tiempo de estudio'),
                OL.azul,
              ),
              _Stat(
                Icons.menu_book_outlined,
                '${ref.watch(misPalabrasProvider).valueOrNull?.length ?? s.vocabularioAprendido}',
                tr('Mis palabras'),
                OL.verde,
              ),
              _Stat(
                Icons.check_circle_outline,
                // Las lecciones del Nivel 0 también cuentan: antes salía 0
                // con varias terminadas.
                pos == null && n0Hechas == 0
                    ? '—'
                    : '${(pos?.aprobadas ?? 0) + n0Hechas}',
                tr('Lecciones completadas'),
                OL.morado,
              ),
              _Stat(
                Icons.flag_outlined,
                claseActual,
                tr('Clase actual'),
                OL.morado,
              ),
            ],
          ),
          const SizedBox(height: 20),
          // En todos los idiomas: antes solo salía en inglés y el resto
          // veía ceros en «Lecciones por habilidad».
          TituloSeccion(
            s.idiomaMeta == 'en' ? tr('Práctica de inglés') : tr('Tu práctica'),
          ),
          const SizedBox(height: 10),
          Tarjeta(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  tr('Tu actividad por área'),
                  style: const TextStyle(fontWeight: FontWeight.w900),
                ),
                const SizedBox(height: 8),
                for (final entry in {
                  'vocabulario': tr('Vocabulario'),
                  'gramatica': tr('Gramática'),
                  'comprension': tr('Lectura'),
                  'listening': tr('Escucha'),
                  'escritura': tr('Escritura'),
                }.entries)
                  Builder(
                    builder: (context) {
                      final items = s.practicas.values
                          .whereType<Map>()
                          .where(
                            (p) =>
                                _area(p) == entry.key &&
                                (p['idioma'] == s.idiomaMeta ||
                                    (p['idioma'] == null &&
                                        s.idiomaMeta == 'en')),
                          )
                          .toList();
                      final review = items
                          .where((p) => p['correcta'] == false)
                          .length;
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 6),
                        child: Text(
                          items.length == 1
                              ? tr(
                                  '{area}: 1 actividad · {review} por reforzar',
                                  {'area': entry.value, 'review': review},
                                )
                              : tr(
                                  '{area}: {n} actividades · {review} por reforzar',
                                  {
                                    'area': entry.value,
                                    'n': items.length,
                                    'review': review,
                                  },
                                ),
                        ),
                      );
                    },
                  ),
                const SizedBox(height: 8),
                Text(
                  tr(
                    'Estas cifras muestran práctica, no dominio. Los aciertos con ayuda se guardan por separado de las evaluaciones de nivel.',
                  ),
                  style: const TextStyle(
                    fontSize: 14,
                    color: OL.gris,
                    height: 1.4,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          // Cuenta solo las lecciones antiguas: sin ellas, todo en cero.
          if (hab.values.any((n) => n > 0)) ...[
            TituloSeccion(tr('Lecciones por habilidad')),
            const SizedBox(height: 10),
            Tarjeta(
              child: Column(
                children: [
                  for (final k in [
                    Skill.vocabulario,
                    Skill.gramatica,
                    Skill.frases,
                    Skill.listening,
                    Skill.pronunciacion,
                    Skill.conversacion,
                  ])
                    Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: Row(
                        children: [
                          SizedBox(
                            width: 110,
                            child: Text(
                              k.nombre,
                              style: const TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                          Expanded(
                            child: BarraProgreso(
                              (hab[k] ?? 0) / maxHab,
                              color: _colorHab(k),
                            ),
                          ),
                          const SizedBox(width: 8),
                          SizedBox(
                            width: 28,
                            child: Text(
                              '${hab[k] ?? 0}',
                              textAlign: TextAlign.right,
                              style: const TextStyle(
                                fontSize: 14,
                                color: OL.gris,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 20),
          ],
          if (ruta != null && estados != null) ...[
            TituloSeccion(tr('Tus diez niveles')),
            const SizedBox(height: 10),
            Tarjeta(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Column(
                children: [
                  for (final nv in ruta.curso.niveles)
                    if ((nv.nivelInterno ?? 0) >= 1)
                      _FilaNivel(ruta: ruta, estados: estados, s: s, nivel: nv),
                ],
              ),
            ),
            const SizedBox(height: 20),
          ],
          _Fila(
            Icons.quiz_outlined,
            tr('Prueba de nivel'),
            tr('Vuelve a medir tu nivel y ajusta tu punto de partida'),
            () => context.push('/prueba-nivel'),
          ),
          _Fila(
            Icons.fact_check_outlined,
            tr('Mis errores'),
            tr('{n} por practicar', {
              'n': s.errores.where((e) => !e.practicado).length,
            }),
            () => context.push('/errores'),
          ),
          _Fila(
            Icons.translate_rounded,
            tr('Idioma que estudias'),
            trDato(idioma(s.idiomaMeta).nombre),
            () => elegirIdiomaQueEstudias(context, ref),
          ),
          _Fila(
            Icons.smart_toy_outlined,
            tr('Tutor de IA'),
            '${t.nombre} · ${nombrePersonalidad(t.personalidad)}',
            () => context.push('/tutores'),
          ),
          _Fila(
            Icons.workspace_premium_outlined,
            tr('Suscripción'),
            nombrePlan != null
                ? '$nombrePlan · $estadoSuscripcion'
                : estadoPlan.trialAgotado
                ? tr('Prueba gratuita terminada · elige un plan')
                : tr('Prueba gratuita · {min} min restantes', {
                    'min': estadoPlan.trialRestante ~/ 60,
                  }),
            () => context.push('/planes'),
          ),
          const SizedBox(height: 16),
          Text(
            tr('Tu experiencia'),
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          // Idioma de la app: los nombres van siempre en su propio idioma
          // para que cualquiera encuentre el suyo.
          Text(
            tr('Idioma de la app'),
            style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16),
          ),
          const SizedBox(height: 6),
          const SelectorIdiomaApp(),
          const SizedBox(height: 8),
          const EffectsSettings(),
          const SizedBox(height: 10),
          if (Sync.instancia.conectado && !demo)
            TextButton.icon(
              onPressed: () => abrirCodigoReferido(context),
              icon: const Icon(
                Icons.handshake_outlined,
                color: OL.gris,
                size: 18,
              ),
              label: Text(
                tr('Código de referido'),
                style: const TextStyle(color: OL.gris),
              ),
            ),
          TextButton.icon(
            onPressed: () => showDialog(
              context: context,
              builder: (ctx) => AlertDialog(
                // Con cuenta real no se pierde nada: el progreso está en el
                // servidor. El aviso de borrado es solo para la demo.
                title: Text(
                  demo ? tr('¿Reiniciar la demo?') : tr('¿Cerrar sesión?'),
                ),
                content: Text(
                  demo
                      ? tr('Se borra el progreso local y vuelves al registro.')
                      : tr(
                          'Tu progreso queda guardado en tu cuenta. Para seguir, inicia sesión otra vez.',
                        ),
                ),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(ctx),
                    child: Text(tr('Cancelar')),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pop(ctx);
                      ref.read(progressProvider.notifier).reiniciar();
                    },
                    child: Text(
                      demo ? tr('Reiniciar') : tr('Cerrar sesión'),
                      style: const TextStyle(color: OL.rojo),
                    ),
                  ),
                ],
              ),
            ),
            icon: const Icon(Icons.logout, color: OL.rojo, size: 18),
            label: Text(
              demo ? tr('Cerrar sesión / reiniciar demo') : tr('Cerrar sesión'),
              style: const TextStyle(color: OL.rojo),
            ),
          ),
          // Con cuenta en el servidor (las demo las rechaza el servidor).
          if (Sync.instancia.conectado)
            TextButton.icon(
              onPressed: () => confirmarEliminarCuenta(context, ref),
              icon: const Icon(
                Icons.delete_forever_outlined,
                color: OL.gris,
                size: 18,
              ),
              label: Text(
                tr('Eliminar cuenta'),
                style: const TextStyle(color: OL.gris),
              ),
            ),
          const SizedBox(height: 4),
          const EnlacesLegales(),
          const SizedBox(height: 4),
          Center(
            child: Text(
              tr('OneLingo · versión {v} ({n})', {
                'v': versionApp,
                'n': compilacionApp,
              }),
              style: const TextStyle(color: OL.gris, fontSize: 12),
            ),
          ),
        ],
      ),
    );
  }

  /// Nombre del nivel como en Aprender: «Fundamentos» o «Nivel 2 · A2».
  static String _tituloNivel(NivelCurso nv) => (nv.nivelInterno ?? 0) < 1
      ? tr('Fundamentos')
      : tr('Nivel {n} · {cefr}', {'n': nv.nivelInterno, 'cefr': nv.cefr});

  Color _colorHab(Skill k) => switch (k) {
    Skill.vocabulario => OL.morado,
    Skill.gramatica || Skill.conjugacion => OL.naranja,
    Skill.listening || Skill.pronunciacion => OL.azul,
    Skill.conversacion => OL.rojo,
    _ => OL.verde,
  };
}

/// Un nivel N1–N10 de la ruta: superado (por sus clases o su prueba),
/// convalidado por la prueba de ubicación, en curso o bloqueado.
class _FilaNivel extends StatelessWidget {
  const _FilaNivel({
    required this.ruta,
    required this.estados,
    required this.s,
    required this.nivel,
  });
  final RutaCargada ruta;
  final Map<String, InfoUnidad> estados;
  final ProgressState s;
  final NivelCurso nivel;

  @override
  Widget build(BuildContext context) {
    final unidades = ruta.delNivel(nivel.id);
    final primera = unidades.isEmpty ? null : estados[unidades.first.id];
    final superado =
        primera != null && nivelSuperado(ruta, estados, s.practicas, nivel.id);
    final convalidado = !superado && (primera?.omitible ?? false);
    final abierto = primera != null && primera.estado != EstadoUnidad.bloqueada;
    final aprobadas = unidades
        .where((u) => estados[u.id]!.estado.alMenos(EstadoUnidad.aprobada))
        .length;
    final hecho = superado || convalidado;
    return ListTile(
      dense: true,
      contentPadding: EdgeInsets.zero,
      // Cada nivel superado tiene su certificado con el nombre del alumno.
      onTap: superado ? () => context.push('/certificado/${nivel.id}') : null,
      leading: Icon(
        primera == null
            ? Icons.schedule_rounded
            : hecho
            ? Icons.check_circle
            : abierto
            ? Icons.radio_button_checked
            : Icons.lock_outline,
        color: hecho
            ? OL.verde
            : abierto
            ? OL.morado
            : OL.gris,
      ),
      title: Text(
        ProgressScreen._tituloNivel(nivel),
        style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
      ),
      trailing: superado
          ? Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  tr('Certificado'),
                  style: const TextStyle(
                    color: OL.morado,
                    fontWeight: FontWeight.w800,
                    fontSize: 14,
                  ),
                ),
                const SizedBox(width: 4),
                const Icon(
                  Icons.workspace_premium_rounded,
                  color: OL.morado,
                  size: 20,
                ),
              ],
            )
          : Text(
              primera == null
                  ? tr('Próximamente')
                  : superado
                  ? tr('Superado')
                  : convalidado
                  ? tr('Convalidado')
                  : '$aprobadas/${unidades.length}',
              style: TextStyle(
                color: hecho ? OL.verde : OL.gris,
                fontWeight: FontWeight.w700,
                fontSize: 14,
              ),
            ),
    );
  }
}

class _Stat extends StatelessWidget {
  const _Stat(this.icono, this.v, this.l, this.c);
  final IconData icono;
  final String v, l;
  final Color c;

  @override
  Widget build(BuildContext context) => Tarjeta(
    padding: const EdgeInsets.all(12),
    child: Row(
      children: [
        IconoCuadro(icono, color: c, tamano: 38),
        const SizedBox(width: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                v,
                style: const TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.w800,
                ),
              ),
              Text(
                l,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: OL.gris, fontSize: 14),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}

class _Fila extends StatelessWidget {
  const _Fila(this.icono, this.titulo, this.sub, this.onTap);
  final IconData icono;
  final String titulo, sub;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Tarjeta(
      onTap: onTap,
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      child: Row(
        children: [
          IconoCuadro(
            icono,
            tamano: 38,
            color: onTap == null ? OL.gris : OL.morado,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  titulo,
                  style: const TextStyle(
                    fontWeight: FontWeight.w700,
                    fontSize: 14,
                  ),
                ),
                Text(sub, style: const TextStyle(color: OL.gris, fontSize: 14)),
              ],
            ),
          ),
          if (onTap != null) const Icon(Icons.chevron_right, color: OL.gris),
        ],
      ),
    ),
  );
}

/// Área de una práctica para «Tu actividad por área». La biblioteca guarda
/// comprension/listening; la ruta guarda la habilidad de la unidad, a veces
/// con tilde («gramática»), así que casi nada contaba. En la ruta manda el
/// formato del ejercicio: un audio es escucha aunque la clase sea de gramática.
String? _area(Map p) {
  if (p['area'] is String) return p['area'] as String;
  switch (p['formato']) {
    case 'escuchar':
      return 'listening';
    case 'escribir':
      return 'escritura';
  }
  final h = '${p['skill'] ?? ''}'
      .toLowerCase()
      .replaceAll('á', 'a')
      .replaceAll('é', 'e')
      .replaceAll('í', 'i')
      .replaceAll('ó', 'o')
      .replaceAll('ú', 'u');
  return switch (h) {
    'escucha' || 'listening' => 'listening',
    'lectura' || 'comprension' => 'comprension',
    'gramatica' || 'vocabulario' || 'escritura' => h,
    _ => null,
  };
}
