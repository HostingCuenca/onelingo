import 'dart:js_interop';

@JS('URL.revokeObjectURL')
external void _revoke(JSString url);
void liberarBlob(String url) {
  if (url.startsWith('blob:')) _revoke(url.toJS);
}
