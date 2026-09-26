import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import 'widgets.dart';

class LearningPrimer extends StatelessWidget {
  const LearningPrimer({super.key, required this.skill, required this.nivel});
  final String skill;
  final int nivel;
  @override
  Widget build(BuildContext context) {
    final (title, steps, example) = switch (skill) {
      'comprension' => (
        'Antes de leer',
        '1. Mira el título y anticipa el tema.\n2. Lee una vez para entender la idea general.\n3. Busca evidencia en el texto para cada respuesta. No necesitas traducir todas las palabras.',
        '“Maya takes the bus because it is raining.”\n¿Quién? Maya. ¿Qué hace? Toma el autobús. ¿Por qué? Porque llueve.',
      ),
      'listening' => (
        'Aprende a escuchar',
        '1. Identifica qué debes buscar: persona, lugar, motivo o detalle.\n2. Escucha una vez para captar el sentido.\n3. Repite para comprobar el detalle. Después de responder podrás revisar la transcripción.',
        'En “The train leaves at half past nine”, la información clave es la hora: 9:30. No hace falta reconocer cada sonido a la primera.',
      ),
      'gramatica' => (
        'Entiende antes de responder',
        'Lee la regla, compara ejemplos y construye una frase. Luego comprueba si puedes usarla con palabras diferentes.',
        'I work every day. / She works every day.\nEn presente simple afirmativo, he/she/it añade -s al verbo regular. En preguntas: Does she work?',
      ),
      'vocabulario' => (
        'Aprende palabras en contexto',
        'Relaciona significado, sonido y uso. Piensa en una frase propia; vuelve a recordar la palabra más tarde sin mirar la traducción.',
        'order = pedir (en un restaurante).\n“I would like to order a salad.”\nCambia “a salad” por otro plato: aprende la combinación, no solo la traducción.',
      ),
      _ => (
        'Prepara tu escritura',
        'Decide qué quieres comunicar. Organiza una idea por frase. Revisa sujeto, verbo y tiempo verbal. Usa la corrección para reescribir, no solo para ver una nota.',
        'Idea: posponer algo.\n“We need to postpone the meeting because the report is not ready.”\nEstructura: decisión + because + motivo.',
      ),
    };
    return Tarjeta(
      color: OL.moradoSuave,
      sombra: false,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            title,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 10),
          Text(steps, style: const TextStyle(height: 1.5)),
          const SizedBox(height: 12),
          const Text(
            'EJEMPLO DE ESTRATEGIA',
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w900,
              color: OL.morado,
            ),
          ),
          const SizedBox(height: 6),
          Text(example, style: const TextStyle(height: 1.45)),
          if (skill == 'gramatica') ...[
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () => context.push('/gramatica?nivel=$nivel'),
              icon: const Icon(Icons.menu_book_rounded),
              label: const Text('Aprender gramática de este nivel'),
            ),
          ],
        ],
      ),
    );
  }
}
