import 'package:flutter/material.dart';

class AvatarScreen extends StatelessWidget {
  const AvatarScreen({super.key});
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Tutor con IA')),
    body: const Center(
      child: Text('La prueba de avatares está disponible en la versión web.'),
    ),
  );
}
