# Interfaz OneLingo — septiembre 2026

Se conserva íntegra la paleta OL. Referencia: controles táctiles, tipografía redondeada y animación breve del documento aportado por el usuario; no se importan los colores ni las fuentes propietarias de Duolingo.

- Nunito variable incluida localmente (licencia OFL en assets/fonts).
- Tarjetas con contorno de 2 px y profundidad sólida, sin desenfoque.
- BotonPrincipal: superficie con pedestal, pulsación por estados Material (incluye teclado), deshabilitado nativo y movimiento reducido.
- Banderas locales de Flagcdn: 10 cursos, proporción rectangular y detalles completos, sin emojis dependientes del sistema.
- Bienvenida adaptable y desplazable para pantallas pequeñas o texto ampliado.
- Transiciones cortas de onboarding y progreso animado; respetan disableAnimations.
- Actividades diarias conservan distribución 3 × 2, con contornos de su color existente.

Validación: análisis estático, pruebas de onboarding con tema real, feedback, cuadrícula y botones. La vista local usa build/ui-polish en el puerto 8120. No desplegada a producción en este cambio. Requiere backend local 8091 para registro y actividades conectadas.
