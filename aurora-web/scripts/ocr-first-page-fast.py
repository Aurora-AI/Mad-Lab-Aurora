from pathlib import Path
import time
import numpy as np
import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR

pdf_path = Path(r"C:\Users\rodri\OneDrive\Pessoal\Desktop\L-G-0000594098-0002399301.pdf")
t0 = time.time()
engine = RapidOCR()
doc = pdfium.PdfDocument(str(pdf_path))
page = doc[0]
bitmap = page.render(scale=1.8)
image = bitmap.to_pil()
result, _ = engine(np.array(image))
print(f"elapsed={time.time()-t0:.2f}s")
print("items=", 0 if not result else len(result))
if result:
    for item in result[:12]:
        print(item[1])
