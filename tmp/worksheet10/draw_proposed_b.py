from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 3600, 1900
im = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(im)
BLACK = '#202020'
GRAY = '#666666'
FONT = r'C:\Windows\Fonts\times.ttf'
BOLD = r'C:\Windows\Fonts\timesbd.ttf'

def font(size=50, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def text_center(box, text, size=50, bold=False, fill=BLACK, gap=9):
    x0,y0,x1,y1 = box
    f = font(size, bold)
    lines = text.split('\n')
    lh = size + gap
    total = len(lines)*lh-gap
    widths = [d.textlength(s,font=f) for s in lines]
    assert max(widths) <= x1-x0-20, (text, max(widths), x1-x0)
    assert total <= y1-y0-10, (text, total, y1-y0)
    yy = y0+(y1-y0-total)/2-4
    for s,sw in zip(lines,widths):
        d.text((x0+(x1-x0-sw)/2,yy),s,font=f,fill=fill)
        yy += lh

def process(box, text, size=50):
    d.rectangle(box,fill='white',outline=BLACK,width=5)
    text_center(box,text,size)

def end(box, text, size=48, success=False):
    d.rounded_rectangle(box,radius=65,fill='#eeeeee' if success else 'white',outline=BLACK,width=5)
    text_center(box,text,size,bold=success)

def decision(box, text):
    x0,y0,x1,y1=box
    cx,cy=(x0+x1)/2,(y0+y1)/2
    d.polygon([(cx,y0),(x1,cy),(cx,y1),(x0,cy)],fill='white',outline=BLACK,width=5)
    text_center((cx-260,cy-95,cx+260,cy+95),text,48,True)

def arrow(points, label=None, label_box=None, size=48):
    d.line(points,fill=BLACK,width=5,joint='curve')
    a,b=points[-2:]
    ang=atan2(b[1]-a[1],b[0]-a[0]); z=24
    d.polygon([b,(b[0]-z*cos(ang-pi/6),b[1]-z*sin(ang-pi/6)),
               (b[0]-z*cos(ang+pi/6),b[1]-z*sin(ang+pi/6))],fill=BLACK)
    if label:
        assert label_box
        text_center(label_box,label,size)

text_center((70,20,3530,115),'PROPOSED FLOW B — MEMBACA HASIL DAN MENENTUKAN TINDAK LANJUT',64,True)
text_center((80,125,3520,195),
    'Rancangan usulan. A melanjutkan Bagian A; pemeriksaan rekening tetap dilakukan owner/finance.',44,fill=GRAY)

# Row 1: the principal path runs left to right.
conn=(65,320,215,470)
d.ellipse(conn,fill='white',outline=BLACK,width=5)
text_center(conn,'A',62,True)
d4=(300,220,1000,570)
p7=(1150,270,1800,520)
d5=(1900,220,2480,570)
p9=(2750,260,3500,530)
d6=(2750,850,3500,1210)
s=(2750,1390,3500,1650)
p6=(300,870,1000,1160)
t2=(300,1380,1000,1650)
p8=(1150,870,1800,1160)
t3=(1150,1380,1800,1650)
e3=(1900,885,2480,1165)

decision(d4,'D4 • Hasil\ntersedia?')
process(p7,'P7 • Baca hasil\nSumber pemeriksa dan\nrujukan pesanan')
decision(d5,'D5 • Hasil\nmemadai?')
process(p9,'P9 • N1b Tindak Lanjut\nTinjau dasar; catat\nkeputusan Teruskan')
decision(d6,'D6 • Keputusan\ntersimpan?')
end(s,'S • BERHASIL\nKeputusan lanjut tercatat;\npesanan siap diteruskan\nke teknisi',48,success=True)
process(p6,'P6 • Menunggu hasil\nBuka panduan/kontak\nbila diperlukan')
end(t2,'T2 • DITUNDA SEMENTARA\nHasil masih ditunggu\nLanjut melalui N2, TS1,\ndan N1b Pemeriksaan',48)
process(p8,'P8 • Tahan pesanan\nMinta klarifikasi atau\npemeriksaan lanjutan')
end(t3,'T3 • DITAHAN\nBelum boleh diteruskan\nLanjut setelah klarifikasi\natau hasil diperbarui',48)
process(e3,'E3 • Pertahankan\nkonteks pesanan\nPeriksa catatan;\nulangi secara aman',48)

arrow([(215,395),(300,395)])
arrow([(1000,395),(1150,395)],'Ya',(1000,320,1150,380))
arrow([(1800,395),(1900,395)])
arrow([(2480,395),(2750,395)],'Ya',(2510,320,2690,380))
arrow([(650,570),(650,870)],'Belum',(685,650,965,725))
arrow([(650,1160),(650,1380)])
arrow([(2190,570),(2190,650),(1475,650),(1475,870)],
      'Tidak',(1760,575,2110,635))
arrow([(1475,1160),(1475,1380)])
arrow([(3125,530),(3125,850)])
arrow([(3125,1210),(3125,1390)],'Ya',(3165,1260,3370,1330))
arrow([(2750,1030),(2480,1030)],'Tidak /\nbelum pasti',(2485,875,2745,1015),44)
# Retry joins the original P9 entry rather than implying a second decision/handoff.
arrow([(2190,885),(2190,760),(2650,760),(2650,395),(2750,395)])
d.ellipse((2642,387,2658,403),fill=BLACK)
text_center((2230,675,2620,745),'Periksa / ulangi',44)

# All return states are explicitly different from success. These notes are design rules.
text_center((80,1680,3520,1795),
    'Memadai: sumber berwenang, pesanan/data terbaru sama, perbandingan cocok, dan dana diterima.\n'
    'T2 dan T3 belum berhasil. Penyerahan fisik kepada teknisi berada di luar alur ini.',44,fill=GRAY,gap=8)

# Compact symbol legend; the external activity is stated in the subtitle, not an Ari process.
y=1843
d.rounded_rectangle((120,y,215,y+36),radius=18,outline=BLACK,width=3)
d.text((235,y-10),'Mulai / akhir',font=font(44),fill=BLACK)
d.rectangle((850,y,945,y+36),outline=BLACK,width=3)
d.text((965,y-10),'Proses Ari',font=font(44),fill=BLACK)
d.polygon([(1530,y+18),(1577,y-8),(1624,y+18),(1577,y+44)],outline=BLACK,fill='white',width=3)
d.text((1645,y-10),'Keputusan',font=font(44),fill=BLACK)
d.ellipse((2260,y-10,2316,y+46),outline=BLACK,width=3)
d.text((2335,y-10),'Penghubung antarbagian',font=font(44),fill=BLACK)

im.save(OUT/'proposed_flow_b.png',dpi=(300,300))
print(OUT/'proposed_flow_b.png')
