import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/diagnostico.dart';
import 'package:onelingo/core/state/providers.dart';

void main() {
  test(
    'perfil compatible con cuentas anteriores y persiste múltiples selecciones',
    () {
      expect(ProgressState.fromJson({}).sectores, isEmpty);
      final state = const ProgressState().copyWith(
        sectores: ['tecnologia', 'estudiante'],
        objetivos: ['escuchar', 'trabajar'],
      );
      final restored = ProgressState.fromJson(state.toJson());
      expect(restored.sectores, ['tecnologia', 'estudiante']);
      expect(restored.objetivos, ['escuchar', 'trabajar']);
    },
  );
  test(
    'diez actividades cubren listening y escritura sin doble ponderación',
    () async {
      final d = Diagnostico(
        declarado: 6,
        banco: [],
        personalizado: true,
        generador: (p) async => PreguntaDiag(
          nivel: p.nivel,
          skill: p.skill,
          tipo: p.tipo,
          tema: p.skill,
          instruccion: 'Pregunta',
          texto: 'Texto ${p.evitar.length}',
          aceptadas: ['ok'],
          explicacion: 'Explicación',
        ),
      );
      for (var i = 0; i < 10; i++) {
        final q = (await d.siguienteAsync())!;
        if (q.esEscritura) {
          final antes = d.estimacion;
          d.registrarEscritura(
            'I can explain my ideas.',
            const EvaluacionEscritura(puntuacion: 4),
          );
          expect(
            d.estimacion,
            antes,
            reason: 'Escritura no modifica también la estimación objetiva',
          );
        } else {
          d.responder(i.isEven ? 'ok' : 'wrong');
        }
      }
      expect(await d.siguienteAsync(), isNull);
      expect(d.respuestas.where((r) => r.pregunta.esAuditiva).length, 3);
      expect(d.respuestas.where((r) => r.pregunta.esEscritura).length, 2);
      expect(
        d.respuestas.any((r) => r.pregunta.tipo == TipoDiag.ordenar),
        isTrue,
      );
      expect(
        d.resultado().skills.keys,
        containsAll([
          'listening',
          'gramatica',
          'comprension',
          'escritura',
          'vocabulario',
        ]),
      );
      expect(d.nivelFinal, ((d.estimacion * .65 + 4 * .35) * 2).round() / 2);
    },
  );
  test(
    'fallo del generador no consume pregunta ni modifica estimación',
    () async {
      final d = Diagnostico(
        declarado: 6,
        banco: [],
        personalizado: true,
        generador: (_) async => null,
      );
      await expectLater(d.siguienteAsync(), throwsStateError);
      expect(d.n, 0);
      expect(d.estimacion, 6);
      expect(d.terminado, isFalse);
    },
  );  test('ordenar acepta las variantes válidas y rechaza palabras faltantes', () {
    final d = Diagnostico(declarado: 6, banco: []);
    d.actual = const PreguntaDiag(nivel: 6, skill: 'gramatica', tipo: TipoDiag.ordenar,
      tema: 'condicional', instruccion: 'Ordena', texto: 'Una situación hipotética',
      aceptadas: ['If I knew, I would help.', 'I would help if I knew.']);
    expect(d.responder('I would help if I knew'), isTrue);
    expect(d.responder('I help if I knew'), isFalse);
  });
  test('el perfil conserva errores de ambas muestras escritas', () {
    final d = Diagnostico(declarado: 6, banco: []);
    d.actual = const PreguntaDiag(nivel: 6, skill: 'escritura', tipo: TipoDiag.escritura,
      tema: 'escribir', instruccion: 'Escribe', texto: 'Describe una experiencia');
    d.registrarEscritura('First text', const EvaluacionEscritura(puntuacion: 5, errores: ['pasado perfecto']));
    d.registrarEscritura('Second text', const EvaluacionEscritura(puntuacion: 7, errores: ['artículos']));
    expect(d.resultado().refuerzo, containsAll(['pasado perfecto', 'artículos']));
    expect(d.mediaEscritura, 6);
  });

}
