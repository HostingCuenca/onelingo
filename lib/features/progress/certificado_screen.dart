import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/content/curriculum.dart';
import '../../core/i18n/i18n.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Niveles con certificado: N1–N10 (Fundamentos no lleva).
bool conCertificado(String nivel) => RegExp(r'^n([1-9]|10)$').hasMatch(nivel);

/// Fecha larga en la lengua de la interfaz («22 de octubre de 2026»).
String fechaCertificado(DateTime f, String lengua) {
  const es = [
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
  ];
  const en = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];
  return lengua == 'en'
      ? '${en[f.month - 1]} ${f.day}, ${f.year}'
      : '${f.day} de ${es[f.month - 1]} de ${f.year}';
}

/// Certificado de un nivel superado con el nombre del alumno. El servidor lo
/// emite (comprueba el progreso) y da una dirección pública para verificarlo,
/// descargarlo en PDF y compartirlo. Sin conexión se ve el último guardado.
class CertificadoScreen extends ConsumerStatefulWidget {
  const CertificadoScreen({super.key, required this.nivel});
  final String nivel;

  @override
  ConsumerState<CertificadoScreen> createState() => _CertificadoScreenState();
}

class _CertificadoScreenState extends ConsumerState<CertificadoScreen> {
  Map<String, dynamic>? cert;
  bool cargando = true;
  String? aviso;

  @override
  void initState() {
    super.initState();
    unawaited(_emitir());
  }

  String _clave(String idioma) =>
      'onelingo.certificado.${Sync.instancia.usuarioId ?? 'local'}.$idioma.${widget.nivel}';

  Future<void> _emitir({String? nombre}) async {
    final idioma = ref.read(progressProvider).idiomaMeta;
    final prefs = await SharedPreferences.getInstance();
    if (cert == null) {
      final guardado = prefs.getString(_clave(idioma));
      if (guardado != null && mounted) {
        setState(() => cert = jsonDecode(guardado) as Map<String, dynamic>);
      }
    }
    final sync = Sync.instancia;
    if (!sync.conectado) {
      if (mounted) {
        setState(() {
          cargando = false;
          aviso = tr(
            'Inicia sesión para obtener el enlace y el PDF de tu certificado.',
          );
        });
      }
      return;
    }
    if (mounted) setState(() => cargando = true);
    // Quien terminó el nivel antes de que existiera la marca de «nivel
    // completo» la recibe ahora; el servidor la necesita para emitirlo.
    final ruta = await ref.read(rutaProvider(idioma).future);
    if (ruta != null)
      ref.read(registroRutaProvider).comprobarNivel(ruta, widget.nivel);
    await sync.enviarAhora();
    var r = await sync.certificado(idioma, widget.nivel, nombre: nombre);
    if (r == null && sync.ultimoError == 'nivel_no_superado') {
      await Future<void>.delayed(const Duration(seconds: 2));
      await sync.enviarAhora();
      r = await sync.certificado(idioma, widget.nivel, nombre: nombre);
    }
    if (r != null) await prefs.setString(_clave(idioma), jsonEncode(r));
    if (!mounted) return;
    setState(() {
      cargando = false;
      if (r != null) cert = r;
      aviso = r != null
          ? null
          : tr(
              'No pudimos preparar tu certificado ahora. Revisa tu conexión e inténtalo de nuevo.',
            );
    });
  }

  Future<void> _corregirNombre(String actual) async {
    final c = TextEditingController(text: actual);
    final nuevo = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(tr('Nombre en el certificado')),
        content: TextField(
          controller: c,
          autofocus: true,
          textCapitalization: TextCapitalization.words,
          maxLength: 80,
          decoration: InputDecoration(hintText: tr('Tu nombre completo')),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(tr('Cancelar')),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, c.text.trim()),
            child: Text(tr('Guardar')),
          ),
        ],
      ),
    );
    if (nuevo != null && nuevo.isNotEmpty && nuevo != actual) {
      await _emitir(nombre: nuevo);
    }
  }

  Future<void> _abrir(String url) async {
    try {
      await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final ruta = ref.watch(rutaProvider(s.idiomaMeta)).valueOrNull;
    final superado =
        ruta != null &&
        nivelSuperado(
          ruta,
          estadosRuta(ruta, s.practicas),
          s.practicas,
          widget.nivel,
        );
    final lengua = I18n.idioma.value == 'en' ? 'en' : 'es';
    final url = cert?['url'] as String?;
    final nombre = cert?['nombre'] as String? ?? nombreLimpio(s.nombre);
    final prueba =
        cert?['via'] == 'prueba' ||
        (cert == null &&
            s.practicas[ClaveRuta.nivelCompleto(s.idiomaMeta, widget.nivel)] ==
                null &&
            pruebaNivelAprobada(s.practicas, s.idiomaMeta, widget.nivel));
    final local =
        (s.practicas[ClaveRuta.nivelCompleto(s.idiomaMeta, widget.nivel)] ??
                s.practicas[ClaveRuta.pruebaNivel(s.idiomaMeta, widget.nivel)])
            as Map?;
    final fecha = DateTime.tryParse(
      (cert?['logradoEn'] ??
              cert?['emitidoEn'] ??
              local?['primeraFecha'] ??
              local?['aprobadaEn'] ??
              local?['fecha'] ??
              '')
          as String,
    )?.toLocal();
    final nombreIdioma = trDato(idioma(s.idiomaMeta).nombre);
    return Scaffold(
      appBar: AppBar(title: Text(tr('Tu certificado'))),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
          children: [
            if (!conCertificado(widget.nivel) ||
                (ruta != null && !superado && cert == null))
              Padding(
                padding: const EdgeInsets.only(top: 40),
                child: Text(
                  tr('Supera este nivel para recibir su certificado.'),
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              )
            else ...[
              _Certificado(
                nombre: nombre,
                nivel: int.parse(widget.nivel.substring(1)),
                motivo: (prueba
                    ? tr(
                        'por aprobar la prueba del Nivel {n} del curso de {idioma} de OneLingo.',
                        {
                          'n': widget.nivel.substring(1),
                          'idioma': lengua == 'es'
                              ? nombreIdioma.toLowerCase()
                              : nombreIdioma,
                        },
                      )
                    : tr(
                        'por completar el Nivel {n} del curso de {idioma} de OneLingo.',
                        {
                          'n': widget.nivel.substring(1),
                          'idioma': lengua == 'es'
                              ? nombreIdioma.toLowerCase()
                              : nombreIdioma,
                        },
                      )),
                fecha: fecha == null ? null : fechaCertificado(fecha, lengua),
                codigo: cert?['codigo'] as String?,
              ),
              const SizedBox(height: 16),
              if (cargando && url == null)
                const Center(
                  child: Padding(
                    padding: EdgeInsets.all(12),
                    child: CircularProgressIndicator(),
                  ),
                )
              else if (aviso != null)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: Text(
                    aviso!,
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: OL.gris, height: 1.4),
                  ),
                ),
              if (url != null) ...[
                BotonPrincipal(
                  onPressed: () => _abrir(url),
                  child: Text(tr('DESCARGAR PDF')),
                ),
                const SizedBox(height: 10),
                OutlinedButton.icon(
                  onPressed: () async {
                    await Clipboard.setData(ClipboardData(text: url));
                    if (!context.mounted) return;
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(
                          tr(
                            'Enlace copiado. Pégalo donde quieras compartirlo.',
                          ),
                        ),
                      ),
                    );
                  },
                  icon: const Icon(Icons.public_rounded),
                  label: Padding(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    child: Text(tr('COPIAR ENLACE')),
                  ),
                ),
                const SizedBox(height: 6),
                TextButton(
                  onPressed: cargando ? null : () => _corregirNombre(nombre),
                  child: Text(tr('¿Tu nombre no está bien escrito? Corrígelo')),
                ),
                const SizedBox(height: 4),
                Text(
                  tr(
                    'El PDF se abre en el navegador. Quien reciba el enlace puede comprobar que el certificado es auténtico.',
                  ),
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 13,
                    color: OL.gris,
                    height: 1.4,
                  ),
                ),
              ] else if (!cargando && Sync.instancia.conectado)
                OutlinedButton(
                  onPressed: () => _emitir(),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    child: Text(tr('REINTENTAR')),
                  ),
                ),
            ],
          ],
        ),
      ),
    );
  }
}

/// El certificado en pantalla, con el mismo diseño que la página pública.
class _Certificado extends StatelessWidget {
  const _Certificado({
    required this.nombre,
    required this.nivel,
    required this.motivo,
    required this.fecha,
    required this.codigo,
  });
  final String nombre, motivo;
  final int nivel;
  final String? fecha, codigo;

  @override
  Widget build(BuildContext context) {
    const etiqueta = TextStyle(
      fontSize: 10.5,
      letterSpacing: 1.4,
      fontWeight: FontWeight.w800,
      color: OL.gris,
    );
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Container(
        padding: const EdgeInsets.fromLTRB(18, 18, 18, 16),
        decoration: BoxDecoration(
          border: Border.all(color: OL.morado, width: 2),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Row(
              children: [
                Text.rich(
                  const TextSpan(
                    text: 'One',
                    children: [
                      TextSpan(
                        text: 'Lingo',
                        style: TextStyle(color: OL.morado),
                      ),
                    ],
                  ),
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w900,
                    color: Color(0xFF1C1B1B),
                  ),
                ),
                const Spacer(),
                Flexible(
                  child: Text(
                    tr('Certificado de nivel').toUpperCase(),
                    textAlign: TextAlign.right,
                    style: const TextStyle(
                      fontSize: 10.5,
                      letterSpacing: 1.6,
                      fontWeight: FontWeight.w800,
                      color: OL.morado,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 22),
            Container(
              width: 74,
              height: 74,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: OL.amarillo,
                shape: BoxShape.circle,
                border: Border.all(color: Colors.white, width: 4),
                boxShadow: const [
                  BoxShadow(color: OL.amarillo, spreadRadius: 2),
                ],
              ),
              child: Text(
                'N$nivel',
                style: const TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.w900,
                  color: OL.morado,
                ),
              ),
            ),
            const SizedBox(height: 14),
            Text(
              tr('Se otorga a').toUpperCase(),
              style: etiqueta.copyWith(fontSize: 12, letterSpacing: 2),
            ),
            const SizedBox(height: 6),
            FittedBox(
              fit: BoxFit.scaleDown,
              child: Text(
                nombre,
                style: const TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.w900,
                  height: 1.15,
                  color: Color(0xFF1C1B1B),
                ),
              ),
            ),
            Container(
              margin: const EdgeInsets.only(top: 8, bottom: 12),
              height: 2,
              width: 180,
              color: OL.amarillo,
            ),
            Text(
              motivo,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 15.5,
                height: 1.45,
                color: Color(0xFF1C1B1B),
              ),
            ),
            const SizedBox(height: 18),
            const Divider(height: 1),
            const SizedBox(height: 12),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(tr('Fecha').toUpperCase(), style: etiqueta),
                      const SizedBox(height: 2),
                      Text(
                        fecha ?? '—',
                        style: const TextStyle(
                          fontSize: 13.5,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ],
                  ),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(tr('Código').toUpperCase(), style: etiqueta),
                    const SizedBox(height: 2),
                    Text(
                      codigo ?? '—',
                      style: const TextStyle(
                        fontSize: 13.5,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'monospace',
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
