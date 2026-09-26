import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../core/content/catalog.dart';

/// Seis acciones en 3 × 2, sin columnas vacías y con texto multilínea.
class DailyActivities extends StatelessWidget {
  const DailyActivities({super.key});
  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, box) {
      final width = (box.maxWidth - 16) / 3;
      return Wrap(
        spacing: 8,
        runSpacing: 8,
        children: [
          for (var i = 0; i < actividadesDiarias.length; i++)
            SizedBox(
              width: width,
              child: Material(
                color: actividadesDiarias[i].$4.withValues(alpha: .10),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(18),
                  side: BorderSide(
                    color: actividadesDiarias[i].$4.withValues(alpha: .28),
                    width: 2,
                  ),
                ),
                child: InkWell(
                  borderRadius: BorderRadius.circular(18),
                  onTap: () => context.push(
                    '/chat?situacion=${[48, 50, 21, 37, 34, 49][i % 6]}',
                  ),
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(minHeight: 104),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 14,
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            actividadesDiarias[i].$3,
                            color: actividadesDiarias[i].$4,
                            size: 27,
                          ),
                          const SizedBox(height: 9),
                          Text(
                            actividadesDiarias[i].$1,
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              fontWeight: FontWeight.w700,
                              fontSize: 12,
                              height: 1.3,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
        ],
      );
    },
  );
}
