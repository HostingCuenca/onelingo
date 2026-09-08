import 'dotenv/config';
type Proveedor = 'openai' | 'gemini' | 'claude';
const proveedorPorDefecto = (): Proveedor =>
  process.env.OPENAI_API_KEY ? 'openai' : process.env.GEMINI_API_KEY ? 'gemini' : 'claude';
export const config = {
  port: Number(process.env.PORT ?? 8090),
  databaseUrl: process.env.DATABASE_URL ?? 'postgres://localhost:5432/onelingo',
  jwtSecret: process.env.JWT_SECRET ?? 'onelingo-dev-secret',
  adminUsuario: process.env.ADMIN_USUARIO ?? 'admin',
  adminPin: process.env.ADMIN_PIN ?? '1234',
  publicUrl: (process.env.PUBLIC_URL ?? 'http://localhost:8091').replace(/\/$/, ''),
  smtp: { host: process.env.SMTP_HOST ?? '', port: Number(process.env.SMTP_PORT ?? 587), user: process.env.SMTP_USER ?? '', pass: process.env.SMTP_PASS ?? '', from: process.env.SMTP_FROM ?? 'OneLingo <no-reply@onelingo.app>' },
  googleClientIds: (process.env.GOOGLE_CLIENT_IDS ?? '').split(',').map((s) => s.trim()).filter(Boolean),
  // Tutor conversacional (conversa, comprende y corrige). Reparto acordado con el cliente:
  // OpenAI → tutor · Gemini → generación de ejercicios (tools/contenido) · ElevenLabs → voz.
  iaProveedor: ((process.env.IA_PROVEEDOR as Proveedor) || proveedorPorDefecto()) as Proveedor,
  openaiApiKey: process.env.OPENAI_API_KEY ?? '',
  openaiModelo: process.env.OPENAI_MODELO ?? 'gpt-4.1-mini',
  // Evaluación de escritura del diagnóstico: modelo más capaz (una llamada por diagnóstico).
  openaiModeloEvaluacion: process.env.OPENAI_MODELO_EVALUACION ?? 'gpt-4.1',
  openaiModeloTranscripcion: process.env.OPENAI_MODELO_TRANSCRIPCION ?? 'gpt-4o-mini-transcribe',
  anthropicApiKey: process.env.ANTHROPIC_API_KEY ?? '',
  iaModelo: process.env.IA_MODELO ?? 'claude-opus-5',
  geminiApiKey: process.env.GEMINI_API_KEY ?? '',
  geminiModelo: process.env.GEMINI_MODELO ?? 'gemini-flash-latest',
  // Voz (ElevenLabs). Los audios se generan una vez y se guardan en AUDIO_DIR + tabla `audios`.
  elevenApiKey: process.env.ELEVENLABS_API_KEY ?? '',
  elevenModelo: process.env.ELEVENLABS_MODELO ?? 'eleven_multilingual_v2',
  audioDir: process.env.AUDIO_DIR ?? './audio',
  // Máximo de caracteres por petición de voz (protege la cuota mensual).
  vozMaxCaracteres: Number(process.env.VOZ_MAX_CARACTERES ?? 600),
};
