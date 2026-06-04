const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const PYTHON = 'C:\\Users\\rodri\\AppData\\Local\\Programs\\Python\\Python311\\python.exe';

const inputPath = process.argv[2];
const startPageArg = Number(process.argv[3] || '1');

function findFileByName(rootDir, targetName) {
  const pending = [rootDir];
  while (pending.length) {
    const current = pending.pop();
    let entries = [];
    try {
      entries = fs.readdirSync(current, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        pending.push(fullPath);
      } else if (entry.isFile() && entry.name.toLowerCase() === targetName.toLowerCase()) {
        return fullPath;
      }
    }
  }
  return null;
}

let absoluteInput = inputPath ? path.resolve(inputPath) : '';
if (!absoluteInput || !fs.existsSync(absoluteInput)) {
  const targetName = inputPath ? path.basename(inputPath) : 'L-G-0000594098-0002399301.pdf';
  const roots = ['C:\\Users\\rodri', 'C:\\Users', 'C:\\'];
  let found = null;
  for (const root of roots) {
    found = findFileByName(root, targetName);
    if (found) break;
  }
  if (!found) {
    console.error(`PDF not found: ${targetName}`);
    process.exit(1);
  }
  absoluteInput = found;
}

const outputPath = absoluteInput.replace(/\.pdf$/i, '.md');

const py = `
from pathlib import Path
from pypdf import PdfReader
import numpy as np
import sys
import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR

pdf_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
start_page = int(sys.argv[3])
ocr_engine = RapidOCR()
pdfium_doc = pdfium.PdfDocument(str(pdf_path))

def normalize_text(raw):
    raw = raw.replace("\\r\\n", "\\n").replace("\\r", "\\n")
    lines = [line.rstrip() for line in raw.split("\\n")]
    cleaned = []
    prev_blank = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_blank:
                cleaned.append("")
            prev_blank = True
            continue
        cleaned.append(stripped)
        prev_blank = False
    return "\\n".join(cleaned).strip()

def ocr_page(pdf_path, page_index):
    page = pdfium_doc[page_index]
    bitmap = page.render(scale=1.3)
    image = bitmap.to_pil()
    result, _ = ocr_engine(np.array(image))
    if not result:
        return ""

    lines = []
    for item in result:
        if len(item) >= 2 and item[1]:
            lines.append(str(item[1]).strip())
    return normalize_text("\\n".join(lines))

reader = PdfReader(str(pdf_path))
mode = "a" if start_page > 1 and out_path.exists() else "w"
with out_path.open(mode, encoding="utf-8") as out_file:
    for i, page in enumerate(reader.pages, start=1):
        if i < start_page:
            continue
        text = page.extract_text() or ""
        cleaned = normalize_text(text)
        if not cleaned:
            cleaned = ocr_page(pdf_path, i - 1)
        if i > 1:
            out_file.write("\\n\\n")
        out_file.write(f"## Página {i}\\n\\n")
        out_file.write(cleaned)
        out_file.flush()
        print(f"page {i} done", file=sys.stderr)

print(out_path)
`;

const result = spawnSync(PYTHON, ['-c', py, absoluteInput, outputPath, String(startPageArg)], {
  encoding: 'utf8',
});

if (result.error) {
  process.stderr.write(String(result.error.message));
  process.exit(1);
}

if (result.status !== 0) {
  process.stderr.write(result.stderr || result.stdout || `Conversion failed for ${absoluteInput}`);
  process.exit(result.status || 1);
}

process.stdout.write(result.stdout);
