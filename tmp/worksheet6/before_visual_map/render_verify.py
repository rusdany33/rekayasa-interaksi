from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
from pypdf import PdfReader
import pdfplumber

ROOT=Path(r'D:\Rekayasa Interaksi')
TMP=ROOT/'tmp'/'worksheet6'
STEM='202210370311406_Rusdany_Maestro_Worksheet6_EmpathyMapPersona'
PDF=ROOT/(STEM+'.pdf')
OUT=TMP/'render'
OUT.mkdir(parents=True,exist_ok=True)
POPPLER=r'C:\Users\HP 15\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
r=PdfReader(PDF)
texts=[page.extract_text() for page in r.pages]
assert len(texts)==8, f'Periksa pergantian halaman: {len(texts)}'
assert all(len(text)>400 for text in texts), 'Halaman kosong atau terlalu sedikit isi'
assert all(label in texts[2] for label in ['Says','Thinks','Does','Feels','Pain','Gain'])
assert all(label in texts[3] for label in ['Nama Persona','Representasi singkat','Latar belakang','Usia atau rentang usia','Pekerjaan atau status','Tujuan pengguna','Kebutuhan pengguna','Motivasi pengguna','Masalah utama','Perilaku dan kebiasaan','Konteks penggunaan','Kemampuan menggunakan teknologi','Kutipan pengguna','Kebutuhan UX utama'])
assert '20-22' in texts[3]
assert '202210370311406' in texts[0]
assert 'Catatan verbatim tidak tersedia' in texts[3]
assert not any(s in '\n'.join(texts) for s in ['Perlu dilengkapi','Draf verifikasi'])

def neutral(color):
    if color is None or isinstance(color,(int,float)):return True
    if len(color)==1:return True
    if len(color)==3:return max(color)-min(color)<.0001
    if len(color)==4:return max(color[:3])<.0001
    return False

with pdfplumber.open(PDF) as p:
    fonts=sorted({c['fontname'] for page in p.pages for c in page.chars})
    assert all('TimesNewRoman' in f for f in fonts), fonts
    for n,page in enumerate(p.pages,1):
        for obj in page.chars+page.lines+page.rects+page.curves:
            assert neutral(obj.get('stroking_color')) and neutral(obj.get('non_stroking_color')),(n,obj)
        assert all(-1<=c['x0'] and c['x1']<=page.width+1 for c in page.chars),n

def render(n):
    s=subprocess.run([POPPLER,'-f',str(n),'-l',str(n),'-singlefile','-r','135','-png',str(PDF),str(OUT/f'page-{n:02d}')],capture_output=True,text=True)
    if s.returncode:raise RuntimeError(s.stderr)
    return n

with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(render,range(1,len(texts)+1)))
(TMP/'pdf_text.txt').write_text('\n\n'.join(f'HALAMAN {n}\n{text}' for n,text in enumerate(texts,1)),encoding='utf-8')
qa={'pages':len(texts),'fonts':fonts,'colors':'hitam putih dan abu-abu netral','empathy_map_domains':6,'persona_fields':14,'pdf_bytes':PDF.stat().st_size,'qa_visual':'Menunggu pemeriksaan gambar halaman'}
(TMP/'qa_render.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
for n,text in enumerate(texts,1):
    lines=[x.strip() for x in text.splitlines() if x.strip()]
    print(n,len(text.split()),' / '.join(lines[:3]))
