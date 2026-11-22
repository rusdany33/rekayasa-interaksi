from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
import hashlib
import ast
from zipfile import ZipFile
from lxml import etree
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
vector_text=PdfReader(TMP/'empathy_map_vector.pdf').pages[0].extract_text()
assert all(label in vector_text for label in ['SAYS','THINKS','DOES','FEELS','PAIN','GAIN'])
assert len(r.pages[2].images)==1,'Empathy Map harus disisipkan sebagai gambar'
assert float(r.pages[2].mediabox.width)>float(r.pages[2].mediabox.height)
assert all(float(page.mediabox.width)<float(page.mediabox.height) for i,page in enumerate(r.pages) if i!=2)
with ZipFile(ROOT/(STEM+'.docx')) as z:
    png=ROOT/'202210370311406_Rusdany_Maestro_Worksheet6_EmpathyMap.png'
    assert hashlib.sha256(png.read_bytes()).digest() in [hashlib.sha256(z.read(n)).digest() for n in z.namelist() if n.startswith('word/media/')]
    tree=etree.fromstring(z.read('word/document.xml'))
    desc=' '.join(tree.xpath('//*[local-name()="docPr"]/@descr'))
    assert all(label in desc for label in ['Says','Thinks','Does','Feels','Pain','Gain'])
def outside_map(path):
    with ZipFile(path) as z:
        tree=etree.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    blocks=[];skip=False
    for child in tree.find('w:body',namespaces=ns):
        txt=' '.join(child.xpath('.//w:t/text()',namespaces=ns))
        if txt.startswith('4 Empathy Map'):skip=True
        if txt.startswith('5 User Persona'):skip=False
        if txt and not skip:blocks.append(txt)
    return blocks
assert outside_map(ROOT/(STEM+'.docx'))==outside_map(TMP/'before_visual_map'/(STEM+'.docx')),'Isi di luar Map berubah'
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
qa={'pages':len(texts),'fonts':fonts,'colors':'hitam putih dan abu-abu netral','empathy_map_domains':6,'persona_fields':14,'map_is_image':True,'map_orientation':'landscape','content_outside_map':'unchanged','pdf_bytes':PDF.stat().st_size,'qa_visual':'Menunggu pemeriksaan gambar halaman'}
(TMP/'qa_render.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
for n,text in enumerate(texts,1):
    lines=[x.strip() for x in text.splitlines() if x.strip()]
    print(n,len(text.split()),' / '.join(lines[:3]))
