# OneLingo · Flujos (diagramas)

Los diagramas siguen el orden del viaje del usuario. Están en Mermaid: se
renderizan en GitHub, VS Code y en la página compartible generada para el cliente.

## 1. Primera experiencia y registro

```mermaid
flowchart TD
  A([Abrir OneLingo]) --> B[Bienvenida]
  B -->|COMENZAR| P1[Paso 1 · Crea tu cuenta<br/>nombre · email · contraseña · Google/Apple]
  B -->|Ya tengo cuenta| L[Iniciar sesión<br/>demo: 5 usuarios con datos visibles]
  L --> H
  P1 --> P2[Paso 2 · Idioma nativo<br/>10 idiomas del contrato]
  P2 --> P3[Paso 3 · Idioma a aprender<br/>los 9 restantes]
  P3 --> P4{Paso 4 · Nivel}
  P4 -->|Prueba de nivel · fase 2| P4a[20 preguntas adaptativas]
  P4 -->|Elegir manualmente| P4b[Nivel 1-10]
  P4a --> P5
  P4b --> P5[Paso 5 · Tu prueba gratuita<br/>1 hora de uso real]
  P5 -->|COMENZAR MI HORA GRATIS| H([Inicio · trial en marcha])
```

## 2. El bucle de aprendizaje (estructura general del contrato)

```mermaid
flowchart LR
  A[APRENDER<br/>lección del curso] --> B[PRACTICAR<br/>ejercicios · actividades diarias]
  B --> C[CONVERSAR CON IA<br/>tutor adaptado al nivel]
  C --> D[RECIBIR CORRECCIONES<br/>error · forma correcta · explicación]
  D --> E[REPASAR<br/>sección Mis errores]
  E --> A
  A -->|100 lecciones completas| F{EXAMEN FINAL}
  F -->|65 % o más| G([Siguiente nivel desbloqueado])
  F -->|64 % o menos| E
  G --> A
```

## 3. Estructura del curso por idioma

```mermaid
flowchart TD
  I[1 idioma] --> N[10 niveles<br/>N1-N2 Básico · N3 Básico Av. · N4-N5 Intermedio<br/>N6 Interm. Av. · N7-N8 Avanzado · N9 Av. Superior · N10 Dominio]
  N --> U[20 unidades por nivel<br/>temario CEFR / Oxford]
  U --> LE[5 lecciones por unidad<br/>Vocabulario · Frases · Escucha · Práctica · Repaso]
  LE --> PA[5-6 pasos por lección]
  PA --> T1[flashcard]
  PA --> T2[opción múltiple]
  PA --> T3[completar hueco]
  PA --> T4[ordenar palabras]
  PA --> T5[escucha y escribe]
  PA --> T6[unir parejas]
  PA --> T7[elige la imagen]
  PA --> T8[repite en voz alta]
  N -. "10 × 100 = 1 000 lecciones · ~3 meses por nivel" .-> LE
```

## 4. Desbloqueo progresivo y examen final

```mermaid
stateDiagram-v2
  direction LR
  state "Lección n" as Lec {
    [*] --> Bloqueada
    Bloqueada --> Desbloqueada : lección n-1 completada
    Desbloqueada --> EnCurso : abrir
    EnCurso --> Completada : todos los pasos
    Completada --> [*]
  }
  state "Nivel k" as Niv {
    [*] --> Activo
    Activo --> ExamenDisponible : 100/100 lecciones
    ExamenDisponible --> Aprobado : nota ≥ 65 %
    ExamenDisponible --> NoAprobado : nota ≤ 64 %
    NoAprobado --> ExamenDisponible : repasar errores y reintentar
    Aprobado --> [*] : desbloquea nivel k+1
  }
```

Al aprobar el Nivel 10 se muestra la pantalla **Programa completado**.

## 5. Dentro de una lección

```mermaid
flowchart TD
  S([Abrir lección]) --> P[Mostrar paso i]
  P --> R[/Respuesta del estudiante/]
  R --> Q{¿Correcta?}
  Q -->|Sí| X[+XP · aciertos+1]
  Q -->|No| E[Corazón −1<br/>registrar error con explicación]
  X --> M{¿Más pasos?}
  E --> M
  M -->|Sí| P
  M -->|No| RS[Resultados<br/>puntuación · XP · racha]
  RS --> D[Marcar completada<br/>desbloquear lección i+1]
  D --> H([Volver a la unidad])
```

## 6. Práctica libre con IA (50 situaciones + conversación libre)

```mermaid
sequenceDiagram
  actor U as Estudiante
  participant A as App OneLingo
  participant P as Perfil de nivel
  participant IA as Tutor IA
  participant ER as Mis errores
  U->>A: Elige situación (1-50) o conversación libre
  A->>P: Lee nivel actual (1-10) y tutor elegido
  P-->>A: vocabulario máx · tiempos · velocidad · tipo de corrección
  A->>IA: system prompt = tutor + perfil + situación + idioma nativo
  IA-->>A: reply · corrections[] · suggestions[]
  A-->>U: Mensaje del tutor + chips de respuesta + traducción
  U->>A: Responde por voz o texto
  A->>IA: turno del estudiante
  IA-->>A: reply + corrección (si hay error)
  A->>ER: Guarda error (❌ ✅ 📚 🗣️)
  A-->>U: Muestra corrección y continúa
```

La misma situación cambia con el nivel: **Restaurante N1** = frases cortas y lentas;
**N5** = pedir recomendaciones y modificar la orden; **N10** = imprevistos, opiniones
y conversación espontánea. Solo cambia el perfil inyectado, no la situación.

## 7. Prueba gratuita y planes

```mermaid
flowchart TD
  R([Registro completo]) --> T[Trial · 60 min de uso real<br/>latido cada 30 s mientras la app está abierta]
  T --> C{¿Minutos restantes?}
  C -->|Sí| USO[Todas las funciones disponibles]
  USO --> T
  C -->|No| PL[Planes]
  PL --> P1[1 idioma · $20/mes]
  PL --> P2[2 idiomas · $30/mes]
  PL --> P3[3 idiomas · $40/mes]
  P1 --> SEL[Elegir idioma(s) del plan]
  P2 --> SEL
  P3 --> SEL
  SEL --> H([Progreso independiente por idioma])
```

## 8. Mapa de navegación de la app

```mermaid
flowchart LR
  subgraph Tabs
    I[Inicio]
    AP[Aprender]
    PR[Practicar]
    PE[Perfil]
  end
  I --> LEC[Lección del día]
  I --> SIT[Situaciones destacadas]
  I --> ACT[Actividades diarias]
  AP --> NIV[Nivel k · 20 unidades]
  NIV --> UNI[Unidad · 5 lecciones]
  UNI --> LEC
  NIV --> EX[Examen final]
  EX --> FIN[Programa completado]
  PR --> CH[Chat con IA]
  PR --> TU[Elegir tutor]
  PE --> ERR[Mis errores]
  PE --> PLA[Planes]
  PE --> STATS[Progreso · habilidades · niveles]
```

## 9. Arquitectura (fase 2)

```mermaid
flowchart LR
  APP[App Flutter<br/>Android · iOS · Web] -->|REST + JWT| API[Backend Fastify]
  API --> DB[(Postgres<br/>usuarios · progreso · errores · exámenes · contenido)]
  API -->|prompt con perfil de nivel| CL[Claude API]
  API --> PAY[Pagos<br/>App Store · Play · Stripe]
  GEN[Pipeline de contenido<br/>CURRICULO.md → Claude → JSON validado] --> DB
```
