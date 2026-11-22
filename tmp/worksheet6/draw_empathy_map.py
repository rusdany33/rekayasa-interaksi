from pathlib import Path
import ast
import json
import subprocess
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER

ROOT=Path(r'D:\Rekayasa Interaksi')
TMP=ROOT/'tmp'/'worksheet6'
PNG=ROOT/'202210370311406_Rusdany_Maestro_Worksheet6_EmpathyMap.png'
VECTOR=TMP/'empathy_map_vector.pdf'
builder=ast.parse((TMP/'build_worksheet6.py').read_text(encoding='utf-8'))
for node in builder.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='map_cells' for t in node.targets):
        cells=ast.literal_eval(node.value)
        break
assert [c[0] for c in cells]==['Says','Thinks','Does','Feels','Pain','Gain']
assert len(cells)==6 and sum(len(c[2]) for c in cells)==18

pdfmetrics.registerFont(TTFont('MapRegular',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('MapBold',r'C:\Windows\Fonts\arialbd.ttf'))
W,H=1600,860
c=canvas.Canvas(str(VECTOR),pagesize=(W,H))
c.setTitle('Empathy Map Ari Admin Kasir Fleffy')
c.setAuthor('Rusdany Maestro')
c.setFillGray(1)
c.rect(0,0,W,H,stroke=0,fill=1)

def text(x,y,txt,size=22,bold=False,center=False,gray=0.08):
    c.setFillGray(gray)
    c.setFont('MapBold' if bold else 'MapRegular',size)
    (c.drawCentredString if center else c.drawString)(x,y,txt)

def path(points,width=2,gray=.7):
    c.setStrokeGray(gray);c.setLineWidth(width)
    p=c.beginPath();p.moveTo(*points[0])
    for point in points[1:]:p.lineTo(*point)
    c.drawPath(p)

def icon(kind,x,y):
    c.saveState();c.translate(x,y);c.setStrokeGray(.12);c.setFillGray(.12)
    c.setLineWidth(2.8);c.setLineJoin(1);c.setLineCap(1)
    if kind=='Says':
        c.roundRect(1,5,34,25,6,stroke=1,fill=0)
        path([(8,5),(7,-1),(16,5)],2.8,.12)
        for yy in (22,15):c.line(9,yy,27,yy)
    elif kind=='Thinks':
        c.circle(19,22,13,stroke=1,fill=0)
        c.circle(6,7,4,stroke=1,fill=0);c.circle(0,0,1.8,stroke=0,fill=1)
        for xx in (12,19,26):c.circle(xx,22,1.3,stroke=0,fill=1)
    elif kind=='Does':
        p=c.beginPath();p.moveTo(7,33);p.lineTo(7,0);p.lineTo(15,8)
        p.lineTo(22,-1);p.lineTo(28,3);p.lineTo(21,13);p.lineTo(33,16);p.close()
        c.drawPath(p,stroke=1,fill=0)
    elif kind=='Feels':
        p=c.beginPath();p.moveTo(18,0);p.curveTo(8,8,-1,15,2,24)
        p.curveTo(5,34,14,32,18,26);p.curveTo(24,34,35,33,36,24)
        p.curveTo(38,14,28,7,18,0);c.drawPath(p,stroke=1,fill=0)
    elif kind=='Pain':
        p=c.beginPath();p.moveTo(18,34);p.lineTo(0,1);p.lineTo(36,1);p.close()
        c.drawPath(p,stroke=1,fill=0)
        c.line(18,24,18,12);c.circle(18,7,1.4,stroke=0,fill=1)
    elif kind=='Gain':
        for r in (17,10,3):c.circle(18,17,r,stroke=1,fill=0)
        c.line(20,19,38,36);path([(30,36),(38,36),(38,28)],2.8,.12)
    c.restoreState()

# Penghubung tanpa arah memusatkan keenam area pada pengguna.
card_h=(H-28-24)/3
ys=[H-14-card_h,H-14-2*card_h-12,14]
anchors=[y+card_h/2 for y in ys]
path([(634,anchors[0]),(657,anchors[0]),(657,anchors[2]),(634,anchors[2])],2,.72)
path([(634,anchors[1]),(688,anchors[1])],2,.72)
path([(966,anchors[0]),(943,anchors[0]),(943,anchors[2]),(966,anchors[2])],2,.72)
path([(966,anchors[1]),(912,anchors[1])],2,.72)
path([(657,anchors[1]),(688,485)],2,.72)
path([(943,anchors[1]),(912,485)],2,.72)

measurements=[]
short_subtitles={
    'Says':'Pernyataan pengguna dalam parafrasa',
    'Thinks':'Pemikiran hasil interpretasi',
    'Does':'Tindakan yang dilaporkan',
    'Feels':'Perasaan yang dilaporkan',
    'Pain':'Hambatan dan kekhawatiran',
    'Gain':'Manfaat yang diinginkan'
}
for i,(domain,subtitle,items) in enumerate(cells):
    x=14 if i%2==0 else 966
    y=ys[i//2];w=620;top=y+card_h
    c.setLineWidth(1.7);c.setStrokeGray(.76);c.setFillGray(.985)
    c.roundRect(x,y,w,card_h,12,stroke=1,fill=1)
    c.setFillGray(.93);c.circle(x+37,top-36,23,stroke=0,fill=1)
    icon(domain,x+19,top-54)
    text(x+76,top-32,domain.upper(),28,True)
    text(x+76,top-57,short_subtitles[domain],18,gray=.35)
    yy=top-76
    style=ParagraphStyle('item',fontName='MapRegular',fontSize=22,leading=24.5,textColor=(.08,.08,.08))
    heights=[]
    for item in items:
        para=Paragraph(escape(item),style)
        _,hh=para.wrap(w-62,1000)
        c.setFillGray(.2);c.circle(x+25,yy-10,2.6,stroke=0,fill=1)
        para.drawOn(c,x+39,yy-hh)
        yy-=hh+4
        heights.append(hh)
    assert yy>=y+10,(domain,yy,y,heights)
    measurements.append({'domain':domain,'bottom_clearance':round(yy-y,1),'points':len(items),'items':items})

# Ilustrasi simbolis tidak menyerupai atau mengidentifikasi responden.
text(800,720,'ARI',34,True,True)
text(800,684,'Admin kasir Fleffy',21,center=True)
text(800,653,'20-22 tahun',20,center=True,gray=.35)
c.setFillGray(.95);c.setStrokeGray(.35);c.setLineWidth(2.5)
c.circle(800,485,112,stroke=1,fill=1)
c.setStrokeGray(.1);c.setLineWidth(4);c.setFillGray(1)
c.circle(800,531,29,stroke=1,fill=1)
c.line(786,506,786,492);c.line(814,506,814,492)
p=c.beginPath();p.moveTo(743,418);p.lineTo(747,458)
p.curveTo(749,482,769,493,786,493)
p.curveTo(792,480,808,480,814,493)
p.curveTo(836,493,850,477,853,456)
p.lineTo(857,418);c.drawPath(p,stroke=1,fill=0)
c.line(761,453,765,416);c.line(838,449,834,416)
c.roundRect(809,437,35,58,5,stroke=1,fill=1)
c.line(816,488,836,488);c.circle(826,444,1.8,stroke=0,fill=1)
c.setLineWidth(5)
p=c.beginPath();p.moveTo(761,446);p.curveTo(782,435,796,440,812,456)
c.drawPath(p,stroke=1,fill=0)
c.line(844,454,849,449)

text(800,330,'FOKUS PEKERJAAN',18,True,True,gray=.35)
center_style=ParagraphStyle('center',fontName='MapRegular',fontSize=21,leading=27,alignment=TA_CENTER,textColor=(.08,.08,.08))
para=Paragraph('Menentukan tindak lanjut pembayaran transfer',center_style)
_,hh=para.wrap(250,200);para.drawOn(c,675,306-hh)
text(800,195,'Pemeriksa rekening',18,center=True,gray=.35)
text(800,167,'Owner atau finance',20,True,True)
text(800,130,'Dasar profil E1 E2 C1',15,center=True,gray=.4)
text(800,86,'Ilustrasi persona',15,center=True,gray=.4)
c.showPage();c.save()

poppler=r'C:\Users\HP 15\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
out=subprocess.run([poppler,'-singlefile','-f','1','-l','1','-r','200','-png',str(VECTOR),str(PNG.with_suffix(''))],capture_output=True,text=True)
if out.returncode:raise RuntimeError(out.stderr)
(TMP/'map_visual_data.json').write_text(json.dumps({'domains':cells,'layout':measurements,'png':str(PNG),'vector':str(VECTOR),'persona':'Ari','uses_real_photo':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(PNG)
print(json.dumps(measurements,ensure_ascii=False))
