const http = require('http');

const port = process.argv[2] || '3000';

function requestOnce() {
  return new Promise((resolve, reject) => {
    const req = http.get(`http://127.0.0.1:${port}`, (res) => {
      let data = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        resolve({ statusCode: res.statusCode, data });
      });
    });

    req.on('error', reject);
    req.setTimeout(5000, () => {
      req.destroy(new Error('timeout'));
    });
  });
}

async function main() {
  const startedAt = Date.now();

  while (Date.now() - startedAt < 20000) {
    try {
      const result = await requestOnce();
      process.stdout.write(`${result.statusCode}\n${result.data.slice(0, 200)}`);
      return;
    } catch (error) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }

  process.stderr.write(`localhost:${port} did not respond within 20 seconds`);
  process.exitCode = 1;
}

main();
