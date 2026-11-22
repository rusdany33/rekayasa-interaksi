from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, json
from pypdf import PdfReader
from docx import Document
from zipfile import ZipFile

root=Path(r'D:\Rekayasa Interaksi')
stem='202210370311406_Rusdany_Maestro_Worksheet5_UserInterview'
pdf=root/(stem+'.pdf')
docx=root/(stem+'.docx')
out=root/'tmp'/'worksheet5'/'format_akademik_render'
out.mkdir(parents=True,exist_ok=True)
poppler=r'C:\Users\HP 15\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
r=PdfReader(pdf)
texts=[p.extract_text() for p in r.pages]
assert all(len(t)>200 for t in texts),'Halaman kosong atau hampir kosong'
assert not any(s in '\n'.join(texts) for s in ['Draf verifikasi','Nama outlet perlu dikonfirmasi','Perlu dilengkapi'])
assert all(code in '\n'.join(texts) for code in ['R1','R2','R3','10 menit','12 menit','15 menit','Pesenkopi'])
with ZipFile(docx) as z: assert z.testzip() is None
def render(n):
    p=subprocess.run([poppler,'-f',str(n),'-l',str(n),'-singlefile','-png','-r','125',str(pdf),str(out/f'page-{n:02d}')],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr)
    assert (out/f'page-{n:02d}.png').exists()
    return n
with ThreadPoolExecutor(max_workers=3) as pool: list(pool.map(render,range(1,len(r.pages)+1)))
(out/'pdf_text.txt').write_text('\n\n'.join(texts),encoding='utf-8')
print(json.dumps({'pages':len(r.pages),'images':len(list(out.glob('page-*.png'))),'pdf_bytes':pdf.stat().st_size,'docx_bytes':docx.stat().st_size,'checks':'metadata and file integrity passed'},ensure_ascii=False))
