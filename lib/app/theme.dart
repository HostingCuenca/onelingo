import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Paleta OneLingo: sacada del logo (globo arcoíris + "Lingo" morado).
class OL {
  static const morado = Color(0xFF4519BB);
  static const moradoOscuro = Color(0xFF2E0F86);
  static const moradoClaro = Color(0xFFE6DEFF);
  static const moradoSuave = Color(0xFFF3F0FF);
  static const naranja = Color(0xFFF7941D);
  static const naranjaSuave = Color(0xFFFFEDD6);
  static const azul = Color(0xFF2E78D1);
  static const azulSuave = Color(0xFFDEEBFC);
  static const rojo = Color(0xFFE03349);
  static const rojoSuave = Color(0xFFFCE6E9);
  static const verde = Color(0xFF40A652);
  static const verdeSuave = Color(0xFFE0F4E3);
  static const amarillo = Color(0xFFFFD23F);
  static const amarilloSuave = Color(0xFFFFF6D6);
  static const fondo = Color(0xFFFCF9F8);
  static const blanco = Color(0xFFFFFFFF);
  static const texto = Color(0xFF1C1B1B);
  static const gris = Color(0xFF79758A);
  static const grisClaro = Color(0xFFEBE8E6);

  static const gradienteMorado = LinearGradient(
    colors: [morado, Color(0xFF7A4AEE)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradienteAzul = LinearGradient(
    colors: [azul, Color(0xFF59A6F2)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradienteRojo = LinearGradient(
    colors: [rojo, Color(0xFFF9736B)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradienteNaranja = LinearGradient(
    colors: [naranja, Color(0xFFFFB85C)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static List<BoxShadow> sombra([double alpha = 0.08]) => [
        BoxShadow(
          color: Colors.black.withValues(alpha: alpha),
          blurRadius: 14,
          offset: const Offset(0, 4),
        ),
      ];
}

ThemeData buildTheme() {
  final base = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: OL.morado,
      primary: OL.morado,
      secondary: OL.naranja,
      surface: OL.blanco,
      error: OL.rojo,
    ),
    scaffoldBackgroundColor: OL.fondo,
  );
  final textTheme = GoogleFonts.plusJakartaSansTextTheme(base.textTheme).apply(
    bodyColor: OL.texto,
    displayColor: OL.texto,
  );
  final titulos = GoogleFonts.beVietnamPro(fontWeight: FontWeight.w700);

  return base.copyWith(
    textTheme: textTheme.copyWith(
      headlineLarge: titulos.copyWith(fontSize: 28, color: OL.texto),
      headlineMedium: titulos.copyWith(fontSize: 22, color: OL.texto),
      headlineSmall: titulos.copyWith(fontSize: 18, color: OL.texto),
      titleLarge: titulos.copyWith(fontSize: 16, color: OL.texto),
      titleMedium: GoogleFonts.beVietnamPro(
          fontSize: 14, fontWeight: FontWeight.w600, color: OL.texto),
    ),
    appBarTheme: AppBarTheme(
      backgroundColor: OL.fondo,
      foregroundColor: OL.texto,
      elevation: 0,
      scrolledUnderElevation: 0,
      centerTitle: false,
      titleTextStyle: titulos.copyWith(fontSize: 18, color: OL.texto),
    ),
    cardTheme: CardThemeData(
      color: OL.blanco,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: OL.morado,
        foregroundColor: OL.blanco,
        elevation: 0,
        minimumSize: const Size.fromHeight(52),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        textStyle: GoogleFonts.plusJakartaSans(
            fontSize: 15, fontWeight: FontWeight.w700, letterSpacing: 0.4),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: OL.texto,
        minimumSize: const Size.fromHeight(52),
        side: const BorderSide(color: OL.grisClaro, width: 1.5),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        textStyle: GoogleFonts.plusJakartaSans(
            fontSize: 15, fontWeight: FontWeight.w700),
      ),
    ),
    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: OL.morado,
        textStyle: GoogleFonts.plusJakartaSans(
            fontSize: 14, fontWeight: FontWeight.w700),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: OL.blanco,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: OL.grisClaro, width: 1.5),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: OL.grisClaro, width: 1.5),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: OL.morado, width: 2),
      ),
      hintStyle: const TextStyle(color: OL.gris),
    ),
    navigationBarTheme: NavigationBarThemeData(
      backgroundColor: OL.blanco,
      indicatorColor: OL.moradoClaro,
      height: 68,
      labelTextStyle: WidgetStateProperty.resolveWith(
        (states) => GoogleFonts.plusJakartaSans(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: states.contains(WidgetState.selected) ? OL.morado : OL.gris,
        ),
      ),
      iconTheme: WidgetStateProperty.resolveWith(
        (states) => IconThemeData(
          color: states.contains(WidgetState.selected) ? OL.morado : OL.gris,
        ),
      ),
    ),
    dividerColor: OL.grisClaro,
  );
}
