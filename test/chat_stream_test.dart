import 'dart:async';
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/api/sync.dart';

class StreamingClient extends http.BaseClient {
  final StreamController<List<int>> events = StreamController();
  final Completer<void> requested = Completer();
  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    expect(request.headers['accept'], 'text/event-stream');
    final body = jsonDecode(await request.finalize().bytesToString());
    expect((body['historial'] as List).length, 30);
    requested.complete();
    return http.StreamedResponse(events.stream, 200, headers: {'content-type': 'text/event-stream'});
  }
}
void main() {
  test('el cliente entrega reply antes de final y no necesita otro POST', () async {
    SharedPreferences.setMockInitialValues({'onelingo.api.token': 'test-token', 'onelingo.api.usuarioId': 'test-user'});
    Sync.instancia.inicializar(await SharedPreferences.getInstance());
    final client = StreamingClient();
    final early = Completer<String>();
    var finished = false;
    final result = Sync.instancia.chat(idiomaMeta: 'en', idiomaNativo: 'es', nivel: 1, tutorId: 'mia',
      historial: List.generate(40, (_) => {'rol': 'alumno', 'texto': 'Hi'}), client: client, onReply: early.complete).then((r) { finished = true; return r; });
    await client.requested.future;
    client.events.add(utf8.encode('data: {"tipo":"reply","data":"Hello!"}\n'));
    expect(await early.future, 'Hello!'); expect(finished, false);
    client.events.add(utf8.encode('\ndata: {"tipo":"final","data":{"reply":"Hello!","corrections":[]}}\n\n'));
    expect((await result)?['reply'], 'Hello!');
    await client.events.close();
  });
}
