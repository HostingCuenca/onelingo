import '../models/models.dart';
import '../state/providers.dart';
import 'curriculum.dart';

/// Usuarios de prueba para recorrer los flujos sin backend (fase 1).
/// Todos usan la contraseña `1234`. Cada uno arranca en un punto distinto del
/// camino para poder probar desbloqueo, examen, trial agotado y programa completo.
class DemoUser {
  const DemoUser({
    required this.email,
    required this.nombre,
    required this.descripcion,
    required this.estado,
  });
  final String email;
  final String nombre;
  final String descripcion;
  final ProgressState Function() estado;

  static const password = '1234';
}

Set<String> _lecciones(int nivel, int hasta) =>
    leccionesDe(nivel).take(hasta).map((l) => l.id).toSet();

Set<String> _nivelesCompletos(int hastaNivel) => {
      for (var n = 1; n <= hastaNivel; n++) ..._lecciones(n, 100),
    };

List<Mistake> _errores() => [
      Mistake(
        id: 'd1',
        skill: Skill.gramatica,
        original: 'She go to school every day',
        correccion: 'She goes to school every day',
        explicacion: 'En presente simple, la tercera persona singular lleva -s.',
        fecha: DateTime.now().subtract(const Duration(hours: 2)),
        origen: 'L1-017',
      ),
      Mistake(
        id: 'd2',
        skill: Skill.vocabulario,
        original: 'Boock',
        correccion: 'Book',
        explicacion: 'Revisa la ortografía: "book" lleva una sola o doble "o" y una "k".',
        fecha: DateTime.now().subtract(const Duration(days: 1)),
        origen: 'L1-009',
      ),
      Mistake(
        id: 'd3',
        skill: Skill.frases,
        original: 'Yesterday I to the market went',
        correccion: 'Yesterday I went to the market',
        explicacion: 'En inglés el orden es sujeto + verbo + complemento.',
        fecha: DateTime.now().subtract(const Duration(days: 3)),
        origen: 'Conversación libre',
        practicado: true,
      ),
    ];

final demoUsers = <DemoUser>[
  DemoUser(
    email: 'ana@onelingo.demo',
    nombre: 'Ana Torres',
    descripcion: 'Usuaria nueva · Nivel 1 · hora gratis completa',
    estado: () => ProgressState(
      onboardingDone: true,
      nombre: 'Ana Torres',
      idiomaNativo: 'es',
      idiomaMeta: 'en',
      nivelInicial: 1,
      trialInicio: DateTime.now(),
    ),
  ),
  DemoUser(
    email: 'bryan@onelingo.demo',
    nombre: 'Bryan Smith',
    descripcion: 'Nivel 1 en curso · 12 lecciones · 3 errores · racha 3',
    estado: () => ProgressState(
      onboardingDone: true,
      nombre: 'Bryan Smith',
      idiomaNativo: 'es',
      idiomaMeta: 'en',
      nivelInicial: 1,
      completadas: _lecciones(1, 12),
      puntuaciones: {for (final id in _lecciones(1, 12)) id: 80 + (id.hashCode % 21)},
      errores: _errores(),
      xp: 310,
      racha: 3,
      segundosEstudio: 2700,
      trialInicio: DateTime.now().subtract(const Duration(days: 2)),
      trialSegundos: 1500,
      tutorId: 'mia',
    ),
  ),
  DemoUser(
    email: 'carla@onelingo.demo',
    nombre: 'Carla Méndez',
    descripcion: 'Nivel 3 completo · examen final desbloqueado · plan 2 idiomas',
    estado: () => ProgressState(
      onboardingDone: true,
      nombre: 'Carla Méndez',
      idiomaNativo: 'es',
      idiomaMeta: 'en',
      nivelInicial: 1,
      completadas: _nivelesCompletos(3),
      examenes: const {1: 88, 2: 74},
      errores: _errores().take(2).toList(),
      xp: 6800,
      racha: 21,
      segundosEstudio: 3600 * 41,
      trialInicio: DateTime.now().subtract(const Duration(days: 60)),
      trialSegundos: 3600,
      tutorId: 'sofia',
      planId: 'p2',
    ),
  ),
  DemoUser(
    email: 'diego@onelingo.demo',
    nombre: 'Diego Ruiz',
    descripcion: 'Hora gratis agotada · debe elegir plan',
    estado: () => ProgressState(
      onboardingDone: true,
      nombre: 'Diego Ruiz',
      idiomaNativo: 'es',
      idiomaMeta: 'en',
      nivelInicial: 1,
      completadas: _lecciones(1, 5),
      xp: 120,
      racha: 1,
      segundosEstudio: 3600,
      trialInicio: DateTime.now().subtract(const Duration(days: 1)),
      trialSegundos: 3600,
      tutorId: 'leo',
    ),
  ),
  DemoUser(
    email: 'lucia@onelingo.demo',
    nombre: 'Lucía Fernández',
    descripcion: 'Nivel 10 · 100/100 · lista para el examen de Dominio',
    estado: () => ProgressState(
      onboardingDone: true,
      nombre: 'Lucía Fernández',
      idiomaNativo: 'es',
      idiomaMeta: 'en',
      nivelInicial: 1,
      completadas: _nivelesCompletos(10),
      examenes: const {1: 90, 2: 85, 3: 92, 4: 78, 5: 81, 6: 88, 7: 79, 8: 84, 9: 91},
      xp: 24500,
      racha: 120,
      segundosEstudio: 3600 * 380,
      trialInicio: DateTime.now().subtract(const Duration(days: 400)),
      trialSegundos: 3600,
      tutorId: 'max',
      planId: 'p3',
    ),
  ),
];

DemoUser? demoUserPorEmail(String email) {
  final e = email.trim().toLowerCase();
  for (final u in demoUsers) {
    if (u.email == e) return u;
  }
  return null;
}
