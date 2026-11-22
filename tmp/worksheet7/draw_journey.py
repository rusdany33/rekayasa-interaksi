from pathlib import Path
import json, subprocess
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

ROOT=Path(r'D:\Rekayasa Interaksi')
TMP=ROOT/'tmp'/'worksheet7'
data=json.loads((TMP/'journey_data.json').read_text(encoding='utf-8'))
PNG=ROOT/'202210370311406_Rusdany_Maestro_Worksheet7_AlurJourney.png'
PDF=TMP/'journey_overview_vector.pdf'
pdfmetrics.registerFont(TTFont('JRegular',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('JBold',r'C:\Windows\Fonts\arialbd.ttf'))
W,H=1900,820
c=canvas.Canvas(str(PDF),pagesize=(W,H))
c.setTitle('Alur User Journey Ari pada Fleffy')
c.setAuthor('Rusdany Maestro')
c.setFillGray(1);c.rect(0,0,W,H,stroke=0,fill=1)
def txt(x,y,s,size=24,bold=False,center=False,gray=.08):
    c.setFillGray(gray);c.setFont('JBold' if bold else 'JRegular',size)
    (c.drawCentredString if center else c.drawString)(x,y,s)
def para(text,x,top,width,font=24,bold=False,leading=None,max_height=None):
    st=ParagraphStyle('p',fontName='JBold' if bold else 'JRegular',fontSize=font,leading=leading or font*1.15,alignment=TA_CENTER,textColor=(.08,.08,.08))
    p=Paragraph(escape(text),st);_,hh=p.wrap(width,1000)
    if max_height is not None:assert hh<=max_height,(text,hh,max_height)
    p.drawOn(c,x,top-hh);return hh
def arrow(x,y):
    c.setStrokeGray(.58);c.setLineWidth(2.4)
    c.line(x-11,y,x+10,y);c.line(x+10,y,x+3,y+6);c.line(x+10,y,x+3,y-6)
def icon(i,x,y):
    c.saveState();c.translate(x,y);c.setStrokeGray(.12);c.setFillGray(.12);c.setLineWidth(3.3)
    if i==0:
        c.roundRect(-31,-16,62,41,8,stroke=1,fill=0)
        p=c.beginPath();p.moveTo(-16,-16);p.lineTo(-22,-28);p.lineTo(-1,-16);c.drawPath(p)
        c.line(-18,12,18,12);c.line(-18,1,8,1)
    elif i==1:
        c.roundRect(-25,-32,50,66,4,stroke=1,fill=0)
        for yy in (20,7,-6,-19):c.line(-12,yy,13,yy)
    elif i==2:
        c.circle(-5,7,23,stroke=1,fill=0);c.line(11,-10,32,-31)
        c.line(-16,7,-7,-2);c.line(-7,-2,8,14)
    elif i==3:
        p=c.beginPath();p.moveTo(-32,20);p.lineTo(34,31);p.lineTo(10,-32);p.lineTo(-1,-5);p.close();c.drawPath(p)
        c.line(-1,-5,34,31)
    elif i==4:
        c.circle(0,0,32,stroke=1,fill=0);c.line(0,0,0,19);c.line(0,0,17,-9)
        for xx,yy in ((0,25),(25,0),(0,-25),(-25,0)):c.circle(xx,yy,1.2,stroke=0,fill=1)
    else:
        c.circle(0,0,32,stroke=1,fill=0)
        p=c.beginPath();p.moveTo(-17,0);p.lineTo(-4,-13);p.lineTo(20,15);c.drawPath(p)
    c.restoreState()
def face(x,y,kind):
    c.setLineWidth(2.8);c.setStrokeGray(.17);c.setFillGray(1)
    c.circle(x,y,28,stroke=1,fill=1)
    c.setFillGray(.12)
    c.circle(x-9,y+7,2,stroke=0,fill=1);c.circle(x+9,y+7,2,stroke=0,fill=1)
    if kind=='smile':
        p=c.beginPath();p.moveTo(x-12,y-4);p.curveTo(x-6,y-16,x+7,y-16,x+13,y-4);c.drawPath(p)
    elif kind=='sad':
        p=c.beginPath();p.moveTo(x-12,y-14);p.curveTo(x-5,y-2,x+5,y-2,x+12,y-14);c.drawPath(p)
    elif kind=='concern':
        c.line(x-10,y-10,x+10,y-10);c.line(x-15,y+12,x-5,y+16);c.line(x+5,y+16,x+15,y+12)
    else:c.line(x-11,y-10,x+11,y-10)

txt(22,779,'PERJALANAN ARI',34,True)
txt(22,741,'Admin kasir Fleffy  |  Transfer Rp150.000 untuk dua pasang deep cleaning',23)
pad,gap=20,12
card_w=(W-2*pad-5*gap)/6
centers=[]
for i,phase in enumerate(data['phases']):
    x=pad+i*(card_w+gap);cx=x+card_w/2;centers.append(cx)
    c.setFillGray(.95 if i==4 else .985);c.setStrokeGray(.25 if i==4 else .76);c.setLineWidth(2.8 if i==4 else 1.6)
    c.roundRect(x,320,card_w,380,10,stroke=1,fill=1)
    c.setFillGray(.1);c.circle(cx,700,23,stroke=0,fill=1)
    txt(cx,693,phase['id'],21,True,True,gray=1)
    para(phase['tahap'],x+12,665,card_w-24,28,True,31,max_height=96)
    icon(i,cx,526)
    para(phase['short_action'],x+15,473,card_w-30,24,False,28,max_height=90)
    c.setStrokeGray(.83);c.setLineWidth(1);c.line(x+20,376,x+card_w-20,376)
    para(phase['short_touchpoint'],x+13,362,card_w-26,21,False,24,max_height=60)
    if i<5:arrow(x+card_w+gap/2,604)

txt(22,260,'EMOSI PADA TAHAP PERJALANAN',20,True,gray=.35)
for i,(phase,cx) in enumerate(zip(data['phases'],centers)):
    face(cx,195,phase['face'])
    txt(cx,137,phase['short_emotion'],24,True,True)
    if i<5:arrow((cx+centers[i+1])/2,195)
txt(22,73,'D = pola yang dilaporkan R2    I = interpretasi penempatan emosi per tahap',21)
txt(22,37,'Simbol emosi bukan skor atau ukuran intensitas. T5 menyoroti penantian; keterlambatan tidak diklaim terjadi pada setiap transaksi.',19,gray=.35)
c.showPage();c.save()
poppler=r'C:\Users\HP 15\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
r=subprocess.run([poppler,'-singlefile','-r','180','-png',str(PDF),str(PNG.with_suffix(''))],capture_output=True,text=True)
if r.returncode:raise RuntimeError(r.stderr)
print(PNG)
