import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PORT = process.env.PORT || 3000;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8'
};

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;
  const acceptHeader = req.headers['accept'] || '';

  // Content-Signal Headers
  res.setHeader('Content-Signal', 'ai-train=yes, search=yes, ai-input=yes');
  res.setHeader('Link', '</llms.txt>; rel="llms-txt"');

  // 1. API: Ingestão de Diagnóstico
  if (req.method === 'POST' && pathname === '/api/v1/ingest-diagnostic') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      let data = {};
      try {
        if (req.headers['content-type']?.includes('application/json')) {
          data = JSON.parse(body);
        } else {
          const params = new URLSearchParams(body);
          data = Object.fromEntries(params.entries());
        }
      } catch {
        data = { raw: body };
      }

      const protocolId = 'OS-ELYSIAN-' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + '-' + Math.floor(1000 + Math.random() * 9000);
      const responsePayload = {
        status: 'PROTOCOL_CREATED',
        protocol: protocolId,
        company: data.empresa || data.company_name || 'Empresa Registrada',
        vertical: data.vertical || data.business_vertical || 'B2C_Medio_Porte',
        timestamp: new Date().toISOString(),
        next_step: 'Auditoria Forense de 7 dias iniciada no motor Ozzmosis. O dossie preliminar sera enviado em ate 24h uteis.'
      };

      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(responsePayload, null, 2));
    });
    return;
  }

  // 2. Content Negotiation: Accept: text/markdown na rota raiz
  if ((pathname === '/' || pathname === '/index.html') && acceptHeader.includes('text/markdown')) {
    const mdPath = path.join(__dirname, 'index.md');
    if (fs.existsSync(mdPath)) {
      res.writeHead(200, { 'Content-Type': 'text/markdown; charset=utf-8' });
      fs.createReadStream(mdPath).pipe(res);
      return;
    }
  }

  // 3. Roteamento de Arquivos Estáticos
  let filePath = '';
  if (pathname === '/' || pathname === '/index.html') {
    filePath = path.join(__dirname, 'index.html');
  } else if (pathname === '/index.md') {
    filePath = path.join(__dirname, 'index.md');
  } else if (pathname === '/llms.txt') {
    filePath = path.join(__dirname, 'public', 'llms.txt');
  } else if (pathname === '/robots.txt') {
    filePath = path.join(__dirname, 'public', 'robots.txt');
  } else if (pathname === '/.well-known/agent-card.json') {
    filePath = path.join(__dirname, 'public', '.well-known', 'agent-card.json');
  } else {
    filePath = path.join(__dirname, pathname);
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath);
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ error: 'NOT_FOUND', path: pathname }));
  }
});

server.listen(PORT, () => {
  console.log(`[Elysian Turnkey Server] Ativo em http://localhost:${PORT}`);
});
