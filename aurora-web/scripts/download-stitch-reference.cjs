const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const targets = [
  {
    url: 'https://lh3.googleusercontent.com/aida/ADBb0ujQ5-akkth_0_T1DDgX57aH7UIfBpAJZLdJZrwNigxS7UDdx9kZza9f0qUI11Y1bbuRc-Z344pYq0LO1Ak0aBJ4MndYZljTakLB6ta6iIIk9DX4vGQf4xsCtMoStaUhfgdeeiCNXi7pQmYVtTWas-1Q9_ZyfzLsqqSigBB4B-03-uwdasnbTauI67q-N-Q8hWZRYnL6l6gcUkFBlHUXz_JdjxVyJdezayiQuG7WdJPhEXpkF324DO8XYpM',
    filename: 'elysian-obsidian-monolith.png',
  },
  {
    url: 'https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzQyYjEzMDczYTgzMzRmY2VhMDM1NmM3Y2Q0MmI5NDU0EgsSBxCW2M6I7xQYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDYxMTcxNjU5ODY2MzE0MTUxMg&filename=&opi=89354086',
    filename: 'elysian-obsidian-monolith.html',
  },
];

const outDir = path.resolve(__dirname, '..', 'stitch-reference');
fs.mkdirSync(outDir, { recursive: true });

function download(url, destination, redirects = 0) {
  const client = url.startsWith('https:') ? https : http;

  return new Promise((resolve, reject) => {
    client
      .get(url, (response) => {
        if (
          response.statusCode &&
          response.statusCode >= 300 &&
          response.statusCode < 400 &&
          response.headers.location
        ) {
          if (redirects > 10) {
            reject(new Error(`Too many redirects for ${url}`));
            return;
          }
          const redirectedUrl = new URL(response.headers.location, url).toString();
          resolve(download(redirectedUrl, destination, redirects + 1));
          return;
        }

        if (response.statusCode !== 200) {
          reject(new Error(`Request failed for ${url}: ${response.statusCode}`));
          return;
        }

        const file = fs.createWriteStream(destination);
        response.pipe(file);
        file.on('finish', () => {
          file.close(() => resolve(destination));
        });
        file.on('error', reject);
      })
      .on('error', reject);
  });
}

async function main() {
  for (const target of targets) {
    const outputPath = path.join(outDir, target.filename);
    await download(target.url, outputPath);
    process.stdout.write(`${outputPath}\n`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
