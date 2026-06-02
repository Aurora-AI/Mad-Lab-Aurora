const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const pdfPath = 'C:\\Users\\rodri\\OneDrive\\Pessoal\\Desktop\\L-G-0000594098-0002399301.pdf';
const mdPath = pdfPath.replace(/\.pdf$/i, '.md');
let startPage = 1;

if (fs.existsSync(mdPath)) {
  const content = fs.readFileSync(mdPath, 'utf8');
  const sections = content.split('## Página ').slice(1);
  if (sections.length) {
    const lastHeader = sections[sections.length - 1].split(/\s+/)[0];
    const lastPage = Number(lastHeader);
    if (Number.isFinite(lastPage) && lastPage > 0) {
      startPage = lastPage + 1;
    }
  }
}

const cwd = path.resolve(__dirname, '..');
const logPath = path.join(cwd, 'pdf-ocr.log');
const out = fs.openSync(logPath, 'a');

const PYTHON = 'C:\\Users\\rodri\\AppData\\Local\\Programs\\Python\\Python311\\python.exe';

const child = spawn(PYTHON, [
  path.join(cwd, 'scripts', 'run-pdf-ocr.py'),
  pdfPath,
  String(startPage),
], {
  cwd,
  detached: true,
  stdio: ['ignore', out, out],
  windowsHide: true,
});

child.unref();

process.stdout.write(`pid=${child.pid} start_page=${startPage}`);
