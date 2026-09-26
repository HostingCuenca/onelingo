import 'package:flutter/material.dart';

import '../../app/theme.dart';

/// Bundled flags: identical rendering on web, Android and iOS.
class LanguageFlag extends StatelessWidget {
  const LanguageFlag(this.code, {super.key, this.width = 40});
  final String code;
  final double width;

  @override
  Widget build(BuildContext context) => ExcludeSemantics(
    child: Container(
      width: width,
      height: width * .7,
      padding: const EdgeInsets.all(2),
      decoration: BoxDecoration(
        color: OL.blanco,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: OL.grisClaro),
        boxShadow: const [BoxShadow(color: OL.grisClaro, offset: Offset(0, 2))],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(5),
        child: Image.asset(
          'assets/img/flags/$code.png',
          fit: BoxFit.cover,
          filterQuality: FilterQuality.high,
          errorBuilder: (_, _, _) =>
              const Icon(Icons.language, size: 22, color: OL.morado),
        ),
      ),
    ),
  );
}
