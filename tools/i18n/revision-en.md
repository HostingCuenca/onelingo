# Revisión independiente de en.json

**Veredicto: GO** (tras 44 correcciones aplicadas; `extraer.py --comprobar` sale con 0: 935 textos, 0 errores).

## Correcciones por tipo
- Mala traducción / ambigüedad: 17
- Consistencia de términos de producto: 18
- Naturalidad / tono: 9

## Ejemplos antes → después
1. "Toca repasar": Tap review → Time to review
2. "inicio" (Nivel 0 en la lista de niveles): home → start
3. "Hogar" (categoría de situaciones): Home → Housing (evita choque con la pestaña Home)
4. "Convalidado": Credited → Placed out
5. "PARTICIPAR": JOIN → JOIN IN
6. "Mínimo" (65 % en examen): Minimum → Pass mark
7. "No se entendió bien…": That wasn't clear. → We couldn't make that out. …
8. "Ya tengo una cuenta · Iniciar sesión": Sign in → Log in (y "Couldn't sign in." → "Couldn't log in.")
9. "Esta clase está temporalmente fuera de servicio": This lesson → This class (clase = class, lección = lesson)
10. "{n} días de constancia": {n} days of consistency → {n}-day streak

## Verificado sin cambios
Prefijo L{n} ya consistente; botones en MAYÚSCULAS, placeholders, emoji y saltos de línea intactos; "inglés" literal donde es el idioma aprendido; placement test (Prueba de nivel) vs "{nivel} test" (subir de nivel) coherentes.

## Observaciones fuera de alcance
Las etiquetas de la barra inferior (Inicio/Aprender/Practicar/Perfil en lib/app/router.dart) son `const` sin `tr()`, por lo que no se traducen a inglés.
