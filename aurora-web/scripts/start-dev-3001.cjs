const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const cwd = path.resolve(__dirname, '..');
const logPath = path.join(cwd, 'vite-dev-3001.log');
const out = fs.openSync(logPath, 'a');

const child = spawn('C:\\Windows\\System32\\cmd.exe', ['/c', 'npm', 'run', 'dev', '--', '--port', '3001'], {
  cwd,
  detached: true,
  stdio: ['ignore', out, out],
  windowsHide: true,
});

child.unref();

process.stdout.write(String(child.pid));
