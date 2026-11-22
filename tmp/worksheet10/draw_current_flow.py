from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 3600, 1900
im = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(im)
BLACK = '#202020'
GRAY = '#666666'
LIGHT = '#eeeeee'
FONT = r'C:\Windows\Fonts\times.ttf'
BOLD = r'C:\Windows\Fonts\timesbd.ttf'

def font(size=50, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def text_center(box, text, size=50, bold=False, fill=BLACK, line_gap=10):
    x0, y0, x1, y1 = box
    f = font(size, bold)
    lines = text.split('\n')
    line_h = size + line_gap
    total = len(lines)*line_h-line_gap
    widths = [d.textlength(line, font=f) for line in lines]
    assert max(widths) <= x1-x0-24, (text, max(widths), x1-x0)
    assert total <= y1-y0-12, (text, total, y1-y0)
    yy = y0+(y1-y0-total)/2-4
    for line, width in zip(lines, widths):
        d.text((x0+(x1-x0-width)/2, yy), line, font=f, fill=fill)
        yy += line_h

def process(box, text, size=50):
    d.rectangle(box, fill='white', outline=BLACK, width=5)
    text_center(box, text, size)

def terminator(box, text, size=50):
    d.rounded_rectangle(box, radius=75, fill='white', outline=BLACK, width=5)
    text_center(box, text, size)

def dashed_line(a, b, fill=GRAY, width=5, dash=20, gap=14):
    x0,y0=a; x1,y1=b
    length=((x1-x0)**2+(y1-y0)**2)**.5
    if not length: return
    p=0
    while p<length:
        q=min(p+dash,length)
        d.line((x0+(x1-x0)*p/length,y0+(y1-y0)*p/length,
                x0+(x1-x0)*q/length,y0+(y1-y0)*q/length),fill=fill,width=width)
        p+=dash+gap

def external(box, text):
    x0,y0,x1,y1=box
    d.rectangle(box, fill='#f7f7f7')
    for a,b in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),
                ((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]:
        dashed_line(a,b)
    text_center(box,text,50)

def decision(box, text):
    x0,y0,x1,y1=box
    cx=(x0+x1)/2; cy=(y0+y1)/2
    d.polygon([(cx,y0),(x1,cy),(cx,y1),(x0,cy)],fill='white',outline=BLACK,width=5)
    text_center((cx-300,cy-115,cx+300,cy+115),text,50,bold=True)

def arrow(points, label=None, label_box=None, label_size=44):
    d.line(points,fill=BLACK,width=5,joint='curve')
    a,b=points[-2:]
    ang=atan2(b[1]-a[1],b[0]-a[0])
    size=22
    p1=(b[0]-size*cos(ang-pi/6),b[1]-size*sin(ang-pi/6))
    p2=(b[0]-size*cos(ang+pi/6),b[1]-size*sin(ang+pi/6))
    d.polygon([b,p1,p2],fill=BLACK)
    if label:
        assert label_box
        text_center(label_box,label,label_size)

def note(box,text):
    d.rounded_rectangle(box,radius=14,fill=LIGHT,outline='#b5b5b5',width=2)
    text_center(box,text,48,fill=GRAY,line_gap=6)

text_center((80,25,3520,115),'CURRENT FLOW — PEMERIKSAAN PEMBAYARAN TRANSFER',68,True)
text_center((90,125,3510,195),
            'Rekonstruksi R2 Q6–Q8; tindak lanjut telepon pada Q9 bersifat kondisional.',44,fill=GRAY)

note((1630,220,3500,345),
     'P1 • Perpindahan sumber: Fleffy, WhatsApp pelanggan,\ndan WhatsApp owner/finance.')

start=(70,410,770,660)
c1=(920,420,1470,650)
c2=(1620,390,2400,680)
c3=(2580,380,3500,690)
ext=(2640,850,3470,1110)
dec=(1800,1280,2700,1710)
c4=(2820,1360,3510,1640)
c5=(900,1365,1600,1625)
end=(70,1365,750,1625)

terminator(start,'MULAI\nPesanan transfer sudah tercatat;\nAri perlu memastikan\npenerimaan',48)
process(c1,'C1 • Fleffy\nBuka pesanan yang\nsudah tercatat')
process(c2,'C2 • WhatsApp pelanggan\nBuka bukti; cocokkan\nnominal dan waktu')
process(c3,'C3 • WhatsApp owner/finance\nKirim rujukan pesanan\ndan bukti kepada pemeriksa')
external(ext,'Owner/finance\nmemeriksa mutasi rekening\n(di luar aktivitas Ari)')
decision(dec,'D1 • Konfirmasi\ndana masuk\nditerima?')
process(c4,'C4 • Menunggu hasil\nHubungi kembali bila perlu\n(telepon: pola Q9)',48)
process(c5,'C5 • Ari\nKonfirmasi pembayaran\ndan teruskan pesanan')
terminator(end,'SELESAI\nPesanan diteruskan\nsetelah konfirmasi')
note((2820,1205,3510,1335),'P2 • Penantian\nkonfirmasi')

arrow([(770,535),(920,535)],'Lanjut',(770,460,920,520),40)
arrow([(1470,535),(1620,535)],'Lanjut',(1470,460,1620,520),40)
arrow([(2400,535),(2580,535)],'Lanjut',(2400,460,2580,520),40)
arrow([(3055,690),(3055,850)],'Permintaan\npemeriksaan',(3090,700,3490,835),44)
arrow([(3055,1110),(3055,1180),(2250,1180),(2250,1280)],
      'Koordinasi hasil via WhatsApp',(2300,1115,3030,1170),42)
arrow([(1800,1495),(1600,1495)],'Ya',(1615,1420,1785,1480),48)
arrow([(900,1495),(750,1495)],'Lanjut',(750,1420,900,1480),40)
arrow([(2700,1495),(2820,1495)],'Belum',(2690,1420,2830,1480),40)
arrow([(3165,1640),(3165,1780),(2250,1780),(2250,1710)],
      'Periksa kembali',(2480,1710,3070,1770),44)

# A separate, compact legend explains shape meaning without interrupting the flow.
y=1843
d.rounded_rectangle((90,y,185,y+36),radius=18,outline=BLACK,width=3)
d.text((205,y-10),'Mulai / selesai',font=font(44),fill=BLACK)
d.rectangle((680,y,775,y+36),outline=BLACK,width=3)
d.text((795,y-10),'Proses Ari',font=font(44),fill=BLACK)
d.polygon([(1280,y+18),(1327,y-8),(1374,y+18),(1327,y+44)],outline=BLACK,fill='white',width=3)
d.text((1395,y-10),'Keputusan',font=font(44),fill=BLACK)
for a,b in [((1870,y),(1965,y)),((1965,y),(1965,y+36)),((1965,y+36),(1870,y+36)),((1870,y+36),(1870,y))]:
    dashed_line(a,b,width=3,dash=12,gap=8)
d.text((1985,y-10),'Aktivitas pemeriksa eksternal',font=font(44),fill=BLACK)

im.save(OUT/'current_flow.png',dpi=(300,300))
print(OUT/'current_flow.png')
