const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const cwd = path.resolve(__dirname, '..');
const logPath = path.join(cwd, 'vite-dev.log');
const out = fs.openSync(logPath, 'a');

const child = spawn('npm.cmd', ['run', 'dev'], {
  cwd,
  detached: true,
  stdio: ['ignore', out, out],
  windowsHide: true,
});

child.unref();

process.stdout.write(String(child.pid));
