import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/api/sync.dart';

void main() {
  test('un fallo HTTP conserva el perfil hasta confirmar el reintento', () async {
    SharedPreferences.setMockInitialValues({'onelingo.api.token': 'test-token', 'onelingo.api.usuarioId': 'test-user'});
    final prefs = await SharedPreferences.getInstance();
    var llamadas = 0;
    await http.runWithClient(() async {
      Sync.instancia.inicializar(prefs);
      Sync.instancia.subir({'sectores': ['estudiante'], 'objetivos': ['escuchar']});
      await Future<void>.delayed(const Duration(milliseconds: 2200));
      expect(llamadas, 1);
      expect(prefs.containsKey('onelingo.pending.test-user'), isTrue);
      await Future<void>.delayed(const Duration(milliseconds: 5200));
      expect(llamadas, 2);
      expect(prefs.containsKey('onelingo.pending.test-user'), isFalse);
      await Sync.instancia.cerrarSesion();
    }, () => MockClient((req) async {
      llamadas++;
      expect(jsonDecode(req.body)['objetivos'], ['escuchar']);
      return http.Response('{}', llamadas == 1 ? 503 : 200);
    }));
  });
}
