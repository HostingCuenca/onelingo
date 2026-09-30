# Respaldos educativos locales

`education-pre-client-scale-20260927T193146-clean.tar.gz` conserva el estado educativo inmediatamente anterior a DEC-020 y es la copia recomendada para restaurar.

- SHA-256: `6ed6a436e33f9078dac0ae36ba85da5f6851811a93e058d080eb5fdbbf7b75c8`
- Entradas: 107
- Archivos regulares: 88
- Incluye rutas inglesas, modelos de aprendizaje, diagnóstico/progreso, documentación, pruebas y herramientas curriculares.
- Excluye `.git`, `.codex`, `.agents`, cachés Python, `.env`, credenciales, builds, APK y activos de avatar.

La primera captura, `education-pre-client-scale-20260927T193146.tar.gz`, se conserva como evidencia histórica, pero queda reemplazada para restauración porque incluía entradas vacías `.git`, `.codex` y `.agents`. Su SHA-256 original es `0423dc65ef300343569793c4c287875145ed082b24c1d4125ae439d15c7cbf44`.

Para inspeccionarlo sin sobrescribir el proyecto:

```bash
mkdir -p /tmp/onelingo-education-restore
tar -xzf backups/education-pre-client-scale-20260927T193146-clean.tar.gz -C /tmp/onelingo-education-restore
```

No extraer directamente sobre el repositorio sin comparar primero el contenido.
