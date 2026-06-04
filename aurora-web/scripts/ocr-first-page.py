from pathlib import Path
import numpy as np
import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR

pdf_path = Path(r"C:\Users\rodri\OneDrive\Pessoal\Desktop\L-G-0000594098-0002399301.pdf")
pdf = pdfium.PdfDocument(str(pdf_path))
page = pdf[0]
bitmap = page.render(scale=2.5)
image = bitmap.to_pil()
engine = RapidOCR()
result, _ = engine(np.array(image))

if not result:
    print("NO_OCR_RESULT")
else:
    for item in result[:40]:
        print(item)
