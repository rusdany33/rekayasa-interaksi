from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
import json,subprocess,hashlib
from lxml import etree
from pypdf import PdfReader
import pdfplumber

ROOT=Path(r'D:\Rekayasa Interaksi')
TMP=ROOT/'tmp'/'worksheet7'
STEM='202210370311406_Rusdany_Maestro_Worksheet7_UserJourney'
PDF=ROOT/(STEM+'.pdf')
DOCX=ROOT/(STEM+'.docx')
OUT=TMP/'render';OUT.mkdir(parents=True,exist_ok=True)
POPPLER=r'C:\Users\HP 15\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
data=json.loads((TMP/'journey_data.json').read_text(encoding='utf-8'))
audit=json.loads((TMP/'audit_kelengkapan.json').read_text(encoding='utf-8'))
assert sum(x['bobot'] for x in audit['rubrik'])==100
assert len(data['phases'])>=5
keys=['tahap','tujuan','aktivitas','tindakan','touchpoint','pikiran','emosi','hambatan','kebutuhan','peluang']
assert all(all(p.get(k) for k in keys) for p in data['phases'])
r=PdfReader(PDF)
texts=[page.extract_text() for page in r.pages]
for n,t in enumerate(texts,1):
    lines=[x.strip() for x in t.splitlines() if x.strip()]
    print(n,len(t.split()),' / '.join(lines[:3]))
assert len(texts)==8, f'Jumlah halaman {len(texts)}, periksa halaman yang melimpah'
assert all(len(t)>300 for t in texts),'Halaman kosong atau terlalu sedikit isi'
assert '202210370311406' in texts[0] and 'Ari' in texts[0] and 'Rp150.000' in texts[0]
assert len(r.pages[2].images)==1
labels=['Tujuan pengguna','Aktivitas pengguna','Tindakan pengguna','Touchpoint atau media','Pemikiran pengguna','Perasaan atau emosi','Masalah atau hambatan','Kebutuhan pengguna','Peluang perbaikan UX']
for i,ids in [(3,['T1','T2','T3']),(4,['T4','T5','T6'])]:
    flat=' '.join(texts[i].split())
    assert all(x in flat for x in labels),(i+1,flat)
    assert all(x in texts[i] for x in ids)
for i,page in enumerate(r.pages):
    assert (float(page.mediabox.width)>float(page.mediabox.height))==(i in (2,3,4)),i+1
with ZipFile(DOCX) as z:
    assert z.testzip() is None
    png=ROOT/'202210370311406_Rusdany_Maestro_Worksheet7_AlurJourney.png'
    assert hashlib.sha256(png.read_bytes()).digest() in [hashlib.sha256(z.read(n)).digest() for n in z.namelist() if n.startswith('word/media/')]
    tree=etree.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    assert not tree.xpath('//w:pBdr',namespaces=ns)

def neutral(color):
    if color is None or isinstance(color,(int,float)):return True
    if len(color)==1:return True
    if len(color)==3:return max(color)-min(color)<.0001
    if len(color)==4:return max(color[:3])<.0001
    return False
with pdfplumber.open(PDF) as p:
    fonts=sorted({c['fontname'] for page in p.pages for c in page.chars})
    assert all('TimesNewRoman' in f for f in fonts),fonts
    for n,page in enumerate(p.pages,1):
        for obj in page.chars+page.lines+page.rects+page.curves:
            assert neutral(obj.get('stroking_color')) and neutral(obj.get('non_stroking_color')),(n,obj)
        assert all(-1<=c['x0'] and c['x1']<=page.width+1 for c in page.chars),n
def render(n):
    s=subprocess.run([POPPLER,'-f',str(n),'-l',str(n),'-singlefile','-r','140','-png',str(PDF),str(OUT/f'page-{n:02d}')],capture_output=True,text=True)
    if s.returncode:raise RuntimeError(s.stderr)
    return n
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,range(1,len(texts)+1)))
(TMP/'pdf_text.txt').write_text('\n\n'.join(f'HALAMAN {n}\n{t}' for n,t in enumerate(texts,1)),encoding='utf-8')
qa={'pages':len(texts),'phase_count':len(data['phases']),'components_per_phase':len(keys),'fonts':fonts,'colors':'hitam putih dan abu-abu netral','pdf_bytes':PDF.stat().st_size,'qa_visual':'Menunggu pemeriksaan gambar seluruh halaman'}
(TMP/'qa_render.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
