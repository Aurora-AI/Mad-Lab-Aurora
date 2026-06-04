import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE = r"C:\Program Files\nodejs\node.exe"
SCRIPT = ROOT / "scripts" / "pdf_to_md.cjs"

pdf_path = sys.argv[1]
start_page = sys.argv[2] if len(sys.argv) > 2 else "1"

subprocess.run([NODE, str(SCRIPT), pdf_path, start_page], cwd=str(ROOT), check=False)
