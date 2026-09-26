# Auditoría e implementación del aprendizaje — 19 septiembre 2026

## Resultado de esta entrega

Tres agentes trabajaron como autores de gramática/lectura/listening, revisor crítico y autores de escenarios de alumno. Son roles simulados de software: no docentes humanos contratados ni alumnos reales. La investigación y enlaces primarios están en AUDITORIA-PEDAGOGIA-2026-09.md, TRAZABILIDAD-LECTURA.md y METODOLOGIA-LISTENING.md.

Se incorporaron 43 guías de gramática (86 preguntas y 43 consignas de producción libre), veinte lecturas (sesenta preguntas, ochenta entradas de vocabulario) y veinte unidades de listening (sesenta preguntas, ochenta entradas de vocabulario). Lectura y listening tienen dos unidades por nivel interno 1–10. Gramática se distribuye por prerrequisitos, no por cuota fija de temas. Vocabulario tiene además ochenta comprobaciones de significado basadas en las palabras de lectura. Las 160 entradas no implican 160 palabras distintas. Las cincuenta situaciones ahora tienen 550 entradas contextuales (531 formas distintas), 400 ejemplos nuevos, 50 patrones y 100 ejemplos bilingües; el backend comparte ese material con el tutor. Los ejercicios nuevos son originales y separados del banco de diagnóstico; no se copiaron exámenes.

Secuencia implementada: objetivo → vocabulario/regla y ejemplos → comprensión/práctica → corrección explicada con evidencia → regreso a explicación. Listening permite repetir y consultar transcripción. Se registra como comprobación guiada, no como prueba de nivel; se excluye de ascensos automáticos incluso sin abrir transcripción. Ver la transcripción queda marcado al cambiar y regresar entre unidades durante la sesión.

El camino mantiene cinco áreas visibles; priorizar una ya no hace desaparecer gramática. Seleccionar nivel manual mantiene ese nivel incluso al agrupar preguntas por texto. El perfil distingue actividad por área de dominio. Calendario de rachas usa fechas registradas, respeta animaciones desactivadas y texto ampliado. Repetir no multiplica XP ni revoca exámenes aprobados. Se conserva primera respuesta para no inventar nueva evidencia con repasos.

La escucha del micrófono en lecciones permite hasta sesenta segundos con tres segundos de silencio en el capturador compatible. La comparación de transcripciones considera orden y negación; no mide pronunciación. El motor nativo alternativo puede seguir imponiendo límites de silencio: no se afirma resuelto sin prueba física Android.

## Autocrítica y prioridades

La aplicación tenía más apariencia de curso que cobertura real: seis palabras y tres frases se repetían en el currículo de respaldo de niveles 3–10. Las cincuenta situaciones tenían tres palabras y tres frases cada una; ahora tienen once entradas cada una, pero aún necesitan más objetivos y tareas de transferencia. Los niveles altos no se demuestran con un condicional difícil. Esta entrega mejora enseñanza y navegación, pero las microlecturas, escucha breve y pocas comprobaciones por tema siguen siendo un piloto, no un curso completo.

| Prioridad | Trabajo siguiente | Criterio de aceptación |
|---|---|---|
| P0 | Auditar autenticación legacy y confianza en progreso/plan enviados por cliente | Pruebas de autorización en entorno aislado; no acceso por correo ajeno; servidor decide derechos |
| P1 | Matriz curricular por competencias y prerrequisitos | Cada objetivo tiene enseñanza, producción, comprensión, prueba nueva y repaso; no títulos duplicados con mismo contenido |
| P1 | Separar completamente banco de práctica y diagnóstico legacy | Ningún ítem visto se usa como evidencia independiente de colocación |
| P1 | Retención y recuperación espaciada | Repasos a intervalos con material nuevo; ayudas y primera respuesta conservadas; no declarar dominio por memorizar opciones |
| P1 | Escritura y conversación por rúbrica | Evaluar cumplimiento, significado, forma y comprensibilidad; ejemplos ancla revisados; no reemplazar todo por nota global |
| P1 | Cincuenta situaciones por nivel | Léxico ampliado, estructuras combinables, varios objetivos, dificultades reales y pruebas de transferencia |
| P1 | Audio real y evaluación de escucha | Verificar TTS, acentos, prosodia, finalización de reproducción; ampliar diálogos y audio espontáneo con derechos claros |
| P1 | Voz en dispositivo Android | Frases con pausas de 1–3 segundos, micrófono manual, ruido, permisos y reconexión; sin truncado ni turno duplicado |
| P2 | Progreso acumulativo y multidispositivo | Modelo por objetivo/idioma, historial de eventos y control de conflictos; no sobrescribir instantáneas silenciosamente |
| P2 | Calibración de diez niveles internos | Pruebas con alumnos y revisión docente; no equivalencia automática MCER ni predicción de aprobar certificación |

No se generaron audios nuevos de pago durante esta entrega. La pantalla de listening usa el servicio de voz existente cuando se solicita reproducir; no se ha validado aquí la calidad acústica de los veinte guiones. El botón habilita respuestas cuando la reproducción se inicia, no certifica escucha completa. Los avatares y APK quedan para después.

## Validación

- 53 pruebas Flutter aprobadas: contenidos, selección de nivel, gramática, borrador propio sin XP, alumno que falla/consulta/vuelve, texto ampliado, vocabulario de 50 situaciones, progreso y voz.
- Cuatro pruebas backend aprobadas: contenido compartido, contexto por situación y memoria que conserva la condición de práctica asistida. TypeScript sin errores.
- Las pruebas de voz comparan transcripciones; no realizan evaluación acústica.
- Análisis estático de pantallas de biblioteca, racha, camino y progreso: sin incidencias.
- Los agentes revisaron 160 ítems; no detectaron claves inequívocamente erróneas. Esto no garantiza ausencia de ambigüedad ni calidad educativa validada.
- Compilación web y revisión local. Sin despliegue de esta entrega a producción.


## Ampliación tras la petición de uso escolar

Ver MATRIZ-GRAMATICA-ESCOLAR.md para el temario amplio y sus brechas, VOCABULARIO-ESCOLAR.md para contextos y variantes y CERTIFICACION-Y-ASCENSO.md para la comparación oficial. Los archivos TEMARIO-GRAMATICA-PROPUESTO.json y COMPETENCIAS-ASCENSO-PROPUESTA.json son especificaciones: no se afirma que sus reglas de dominio o prerrequisitos ya se ejecuten en runtime. El catálogo gramatical sí fue reordenado.

Se descargaron referencias públicas Cambridge (Young Learners, A2 Key y B1 Preliminary) y ETS TOEFL 2026 en work/research/english-curriculum, con fuentes. Están fuera de assets y no se incluyen en la app; su descarga no se interpretó como licencia de redistribución. No se copió un banco comercial de exámenes.

Correcciones de revisión: contexto explícito para la preposición in; excepción de preguntas de sujeto; enseñanza de future continuous antes de contrastarlo; artículos/plurales, capacidad y pronombres añadidos; ejemplos de libreta y traducción de early showing; distinción entre bolso desaparecido y robo; nota de prerrequisito para el patrón médico con present perfect. Las 43 consignas de escritura son borradores de sesión, no evaluadas por IA ni usadas como aciertos.
