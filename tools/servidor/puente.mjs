// Puente temporal en Hetzner durante el cambio de DNS: ocupa el puerto de la API
// vieja (8091, al que apunta el Apache de Hetzner) y reenvía todo al VPS nuevo.
// Así, quien aún resuelva onelingo.org a Hetzner escribe en la base nueva.
import http from 'node:http';
import https from 'node:https';

const NUEVO = process.env.ONELINGO_NUEVO ?? '179.197.89.105';

http.createServer((req, res) => {
  const salida = https.request({
    host: NUEVO, servername: 'onelingo.org', port: 443, method: req.method,
    path: '/api' + req.url, headers: { ...req.headers, host: 'onelingo.org' },
  }, (r) => { res.writeHead(r.statusCode ?? 502, r.headers); r.pipe(res); });
  salida.on('error', () => { if (!res.headersSent) res.writeHead(502); res.end(); });
  res.on('close', () => { if (!res.writableEnded) salida.destroy(); });
  req.pipe(salida);
}).listen(8091, '127.0.0.1');
