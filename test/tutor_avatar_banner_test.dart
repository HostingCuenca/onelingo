import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/shared/widgets/tutor_avatar_banner.dart';

void main() {
  testWidgets('banner de tutores es legible y abre Tutor con IA', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(320, 640);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final router = GoRouter(
      routes: [
        GoRoute(
          path: '/',
          builder: (_, _) => const Scaffold(
            body: SingleChildScrollView(child: TutorAvatarBanner()),
          ),
        ),
        GoRoute(
          path: '/tutores',
          builder: (_, _) => const Scaffold(body: Text('Tutor con IA')),
        ),
      ],
    );

    await tester.pumpWidget(
      MaterialApp.router(
        theme: buildTheme(),
        routerConfig: router,
        builder: (context, child) => MediaQuery(
          data: MediaQuery.of(context)
              .copyWith(textScaler: const TextScaler.linear(1.25)),
          child: child!,
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Practica con nuestros avatares'), findsOneWidget);
    expect(find.byType(Image), findsNWidgets(5));
    expect(tester.takeException(), isNull);

    await tester.tap(find.byType(InkWell));
    await tester.pumpAndSettle();
    expect(find.text('Tutor con IA'), findsOneWidget);
  });
}
