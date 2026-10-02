import '../../shared/widgets/mascot_coach.dart';
import '../../shared/widgets/feedback_experience.dart';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/curriculum.dart';
import '../../core/models/models.dart';
import '../../core/i18n/i18n.dart';
import '../../core/lexico/lexico.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Perfil y progreso del estudiante (REQUERIMIENTOS §13).
class ProgressScreen extends ConsumerWidget {
  const ProgressScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final n = s.nivelActual;
    final hab = s.porHabilidad;
    final maxHab = hab.values.fold(1, (a, b) => a > b ? a : b);
    final t = tutor(s.tutorId);
    final plan = planes.where((p) => p.id == s.planId).firstOrNull;

    return Scaffold(
      appBar: AppBar(title: const Text('Mi progreso')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          const MascotCoach(
            message: 'Tu progreso se construye practicando y repasando. Cada habilidad cuenta.',
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
                        '${idioma(s.idiomaNativo).nombre} → ${idioma(s.idiomaMeta).nombre}',
                        style: const TextStyle(color: OL.gris, fontSize: 14),
                      ),
                      const SizedBox(height: 6),
                      Wrap(
                        spacing: 6,
                        runSpacing: 6,
                        children: [
                          Etiqueta('Nivel $n · ${nivel(n).nombre}'),
                          Etiqueta(
                            plan == null ? 'Prueba gratuita' : plan.nombre,
                            color: plan == null
                                ? const Color(0xFF9A6B00)
                                : OL.verde,
                            fondo: plan == null ? OL.amarilloSuave : null,
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
                '${s.rachaVigente} ${s.rachaVigente == 1 ? 'día' : 'días'}',
                'Racha',
                OL.rojo,
              ),
              _Stat(
                Icons.schedule_outlined,
                '${s.segundosEstudio ~/ 60} min',
                'Tiempo de estudio',
                OL.azul,
              ),
              _Stat(
                Icons.menu_book_outlined,
                '${ref.watch(misPalabrasProvider).valueOrNull?.length ?? s.vocabularioAprendido}',
                'Mis palabras',
                OL.verde,
              ),
              _Stat(
                Icons.check_circle_outline,
                '${s.completadas.length}',
                'Lecciones completadas',
                OL.morado,
              ),
              _Stat(
                Icons.flag_outlined,
                'Lección ${s.leccionActual(n)?.numero ?? 100}',
                'Lección actual',
                OL.morado,
              ),
            ],
          ),
          const SizedBox(height: 20),
          if (s.idiomaMeta == 'en') ...[
            const TituloSeccion('Práctica de inglés'),
            const SizedBox(height: 10),
            Tarjeta(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'Tu actividad por área',
                    style: TextStyle(fontWeight: FontWeight.w900),
                  ),
                  const SizedBox(height: 8),
                  for (final entry in const {
                    'vocabulario': 'Vocabulario',
                    'gramatica': 'Gramática',
                    'comprension': 'Lectura',
                    'listening': 'Listening',
                    'escritura': 'Escritura',
                  }.entries)
                    Builder(
                      builder: (context) {
                        final items = s.practicas.values
                            .whereType<Map>()
                            .where(
                              (p) =>
                                  p['skill'] == entry.key &&
                                  (p['idioma'] == 'en' || p['idioma'] == null),
                            )
                            .toList();
                        final review = items
                            .where((p) => p['correcta'] == false)
                            .length;
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 6),
                          child: Text(
                            '${entry.value}: ${items.length} actividades · $review por reforzar',
                          ),
                        );
                      },
                    ),
                  const SizedBox(height: 8),
                  const Text(
                    'Estas cifras muestran práctica, no dominio. Los aciertos con ayuda se guardan por separado de las evaluaciones de nivel.',
                    style: TextStyle(fontSize: 14, color: OL.gris, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
          ],
          const TituloSeccion('Lecciones por habilidad'),
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
          const TituloSeccion('Niveles y exámenes'),
          const SizedBox(height: 10),
          Tarjeta(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Column(
              children: [
                for (final lvl in niveles)
                  ListTile(
                    dense: true,
                    contentPadding: EdgeInsets.zero,
                    leading: Icon(
                      s.examenAprobado(lvl.numero)
                          ? Icons.check_circle
                          : s.nivelDesbloqueado(lvl.numero)
                          ? Icons.radio_button_checked
                          : Icons.lock_outline,
                      color: s.examenAprobado(lvl.numero)
                          ? OL.verde
                          : s.nivelDesbloqueado(lvl.numero)
                          ? OL.morado
                          : OL.gris,
                    ),
                    title: Text(
                      'Nivel ${lvl.numero} · ${lvl.nombre}',
                      style: const TextStyle(
                        fontWeight: FontWeight.w600,
                        fontSize: 14,
                      ),
                    ),
                    trailing: Text(
                      lvl.numero < s.nivelInicial
                          ? 'Convalidado'
                          : s.examenes.containsKey(lvl.numero)
                          ? 'Examen ${s.examenes[lvl.numero]}%'
                          : '${s.completadasEnNivel(lvl.numero)}/100',
                      style: TextStyle(
                        color:
                            s.examenAprobado(lvl.numero) ||
                                lvl.numero < s.nivelInicial
                            ? OL.verde
                            : OL.gris,
                        fontWeight: FontWeight.w700,
                        fontSize: 14,
                      ),
                    ),
                  ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          _Fila(
            Icons.quiz_outlined,
            'Prueba de nivel',
            'Vuelve a medir tu nivel y ajusta tu punto de partida',
            () => context.push('/prueba-nivel'),
          ),
          _Fila(
            Icons.fact_check_outlined,
            'Mis errores',
            '${s.errores.where((e) => !e.practicado).length} por practicar',
            () => context.push('/errores'),
          ),
          _Fila(
            Icons.smart_toy_outlined,
            'Tutor de IA',
            '${t.nombre} · ${nombrePersonalidad(t.personalidad)}',
            () => context.push('/tutores'),
          ),
          _Fila(
            Icons.workspace_premium_outlined,
            'Plan de suscripción',
            plan?.nombre ??
                'Prueba gratuita · ${s.trialRestante ~/ 60} min restantes',
            () => context.push('/planes'),
          ),
          const SizedBox(height: 16),
          const Text(
            'Tu experiencia',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          // Idioma de la app: los nombres van siempre en su propio idioma
          // para que cualquiera encuentre el suyo.
          Text(
            tr('Idioma de la app'),
            style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16),
          ),
          const SizedBox(height: 6),
          Wrap(
            spacing: 8,
            children: [
              for (final e in I18n.disponibles.entries)
                ChoiceChip(
                  label: Text(e.value),
                  selected: s.interfaz == e.key,
                  selectedColor: OL.moradoClaro,
                  onSelected: (_) => ref
                      .read(progressProvider.notifier)
                      .elegirIdiomaInterfaz(e.key),
                ),
            ],
          ),
          const SizedBox(height: 8),
          const EffectsSettings(),
          const SizedBox(height: 10),
          TextButton.icon(
            onPressed: () => showDialog(
              context: context,
              builder: (ctx) => AlertDialog(
                title: const Text('¿Reiniciar la demo?'),
                content: const Text(
                  'Se borra el progreso local y vuelves al registro.',
                ),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(ctx),
                    child: const Text('Cancelar'),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pop(ctx);
                      ref.read(progressProvider.notifier).reiniciar();
                    },
                    child: const Text(
                      'Reiniciar',
                      style: TextStyle(color: OL.rojo),
                    ),
                  ),
                ],
              ),
            ),
            icon: const Icon(Icons.logout, color: OL.rojo, size: 18),
            label: const Text(
              'Cerrar sesión / reiniciar demo',
              style: TextStyle(color: OL.rojo),
            ),
          ),
        ],
      ),
    );
  }

  Color _colorHab(Skill k) => switch (k) {
    Skill.vocabulario => OL.morado,
    Skill.gramatica || Skill.conjugacion => OL.naranja,
    Skill.listening || Skill.pronunciacion => OL.azul,
    Skill.conversacion => OL.rojo,
    _ => OL.verde,
  };
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
