import unittest
import os
import sys
import json
import shutil
from pathlib import Path

# Add project root/SES directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import pipeline functions
from ki_pipeline import CANDIDATES_DIR, APPROVED_DIR, MANIFEST_PATH, run_ki_pipeline, validate_ki, parse_ki

class TestKIPipeline(unittest.TestCase):

    def setUp(self):
        # Create backups of candidates/approved directories and manifest if they exist
        self.temp_candidates = []
        self.temp_approved = []
        
        # Ensure directories exist
        CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
        APPROVED_DIR.mkdir(parents=True, exist_ok=True)
        
        # Backup existing manifest
        self.manifest_backup = None
        if MANIFEST_PATH.exists():
            self.manifest_backup = MANIFEST_PATH.read_text(encoding='utf-8')

        # Define valid/invalid test contents
        self.valid_ki_content = """---
title: "Evitar animação imediata em preloaders"
domain: web-gl
evidence_type: "Tratamento de latência em Next.js"
applicable_to: ["ceo-effects", "ceo-web"]
---

# Evitar animação imediata em preloaders

## O Aprendizado
Nunca iniciar animações complexas antes do hidratamento completo da página Next.js.

## Por Que Isso É Um KI
Animações imediatas causam quebra de layout durante a reidratação do React.

## Aplicação Prática
```javascript
// Aguardar sinal de hidratação
window.addEventListener('load', () => { ... });
```

## Evidência de Origem
Bug report no log de console da OS-MADLAB-002.
"""

        self.invalid_ki_content = """---
title: "KI Mal Formado"
# Falta domain, evidence_type e applicable_to
---

# KI Mal Formado

## O Aprendizado
Conteúdo sem seções obrigatórias.
"""

    def tearDown(self):
        # Remove any temp test files we created
        for p in self.temp_candidates:
            if p.exists():
                p.unlink()
        for p in self.temp_approved:
            if p.exists():
                p.unlink()
                
        # Restore manifest backup
        if self.manifest_backup is not None:
            with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
                f.write(self.manifest_backup)

    def test_ki_validation(self):
        # Test valid KI
        metadata, body = parse_ki(self.valid_ki_content)
        valid, errors = validate_ki(metadata, body)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

        # Test invalid KI
        metadata_inv, body_inv = parse_ki(self.invalid_ki_content)
        valid_inv, errors_inv = validate_ki(metadata_inv, body_inv)
        self.assertFalse(valid_inv)
        self.assertGreater(len(errors_inv), 0)

    def test_run_ki_pipeline(self):
        # Create temp candidate files
        valid_path = CANDIDATES_DIR / "temp_valid_ki.md"
        invalid_path = CANDIDATES_DIR / "temp_invalid_ki.md"
        
        valid_path.write_text(self.valid_ki_content, encoding='utf-8')
        invalid_path.write_text(self.invalid_ki_content, encoding='utf-8')
        
        self.temp_candidates.extend([valid_path, invalid_path])

        # Run pipeline
        promoted = run_ki_pipeline()
        
        # Valid should be promoted, invalid should remain in candidates
        self.assertEqual(len(promoted), 1)
        self.assertTrue(any("evitar-animação-imediata" in f for f in promoted))
        
        # Track promoted path for cleanup
        for f in promoted:
            self.temp_approved.append(APPROVED_DIR / f)
            
        # Check files
        self.assertFalse(valid_path.exists()) # Promoted files are deleted from candidates
        self.assertTrue(invalid_path.exists()) # Rejected files remain

        # Check manifest update
        if MANIFEST_PATH.exists():
            with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            ki_section = next((s for s in manifest if s.get("vault_section") == "KIs"), None)
            self.assertIsNotNone(ki_section)
            self.assertGreater(ki_section["sub_sections"]["approved"]["count"], 0)
            self.assertTrue(any(f in ki_section["sub_sections"]["approved"]["items"] for f in promoted))

if __name__ == "__main__":
    unittest.main()
