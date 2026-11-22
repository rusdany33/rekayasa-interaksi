from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parent
im=Image.new('RGB',(3600,1900),'white')
d=ImageDraw.Draw(im)
BLACK='#202020'; GRAY='#666666'
FONT=r'C:\Windows\Fonts\times.ttf'
BOLD=r'C:\Windows\Fonts\timesbd.ttf'

def font(size=48,bold=False):
    return ImageFont.truetype(BOLD if bold else FONT,size)

def text(box,value,size=48,bold=False,fill=BLACK,gap=10):
    x0,y0,x1,y1=box; f=font(size,bold)
    lines=value.split('\n'); widths=[d.textlength(x,font=f) for x in lines]
    h=len(lines)*(size+gap)-gap
    assert max(widths)<=x1-x0-18,(value,max(widths),x1-x0)
    assert h<=y1-y0-8,(value,h,y1-y0)
    y=y0+(y1-y0-h)/2-4
    for line,w in zip(lines,widths):
        d.text((x0+(x1-x0-w)/2,y),line,font=f,fill=fill)
        y+=size+gap

def box(bounds,value,size=48,terminal=False):
    if terminal:d.rounded_rectangle(bounds,radius=65,fill='white',outline=BLACK,width=5)
    else:d.rectangle(bounds,fill='white',outline=BLACK,width=5)
    text(bounds,value,size)

def diamond(bounds,value):
    x0,y0,x1,y1=bounds; cx=(x0+x1)/2;cy=(y0+y1)/2
    d.polygon([(cx,y0),(x1,cy),(cx,y1),(x0,cy)],fill='white',outline=BLACK,width=5)
    text((cx-220,cy-110,cx+220,cy+110),value,48,True)

def connector(cx,cy):
    r=68
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#f1f1f1',outline=BLACK,width=5)
    text((cx-r,cy-r,cx+r,cy+r),'A',62,True)

def arrow(points,label,label_bounds,size=42):
    d.line(points,fill=BLACK,width=5,joint='curve')
    a,b=points[-2:];theta=atan2(b[1]-a[1],b[0]-a[0]);r=22
    d.polygon([b,(b[0]-r*cos(theta-pi/6),b[1]-r*sin(theta-pi/6)),
              (b[0]-r*cos(theta+pi/6),b[1]-r*sin(theta+pi/6))],fill=BLACK)
    text(label_bounds,label,size)

text((70,20,3530,110),'PROPOSED FLOW — BAGIAN A: MEMINTA PEMERIKSAAN',68,True)
text((70,120,3530,190),
     'Kedua konektor A menuju Bagian B yang sama; tidak membuat pesanan atau permintaan baru.',44,fill=GRAY)

p0=(60,330,590,550)
p1=(730,330,1320,550)
p2=(1470,310,2120,570)
d1=(2260,260,2850,620)
p3=(3000,310,3540,570)
e1=(2150,750,2870,1010)
t1=(1450,760,1990,1000)
d2=(2860,1240,3520,1600)
p4=(2100,1290,2690,1550)
d3=(1400,1240,1950,1600)
p5=(500,1285,1230,1555)
e2=(1420,1660,2440,1810)

box(p0,'P0 • Beranda N0\nSudah login; pesanan\ntransfer telah tercatat',48,True)
box(p1,'P1 • Pesanan N1\nCari dan pilih\npesanan yang tepat')
box(p2,'P2 • Pembayaran N1b\nTinjau ID, nominal,\ndan bukti pelanggan')
diamond(d1,'D1 • Data dan\nbukti cukup\nserta cocok?')
box(p3,'P3 • Pemeriksaan N1b\nTinjau rujukan pesanan\ndan pemeriksa')
box(e1,'E1 • Klarifikasi/perbaiki\ncatatan; pertahankan\nbukti asli')
box(t1,'T1 • DITUNDA\nuntuk klarifikasi\n(bukan Success)',48,True)
diamond(d2,'D2 • Permintaan\npesanan & data ini\nsudah ada?')
box(p4,'P4 • Kirim permintaan\nGunakan ID dan\nnominal tersimpan')
diamond(d3,'D3 • Permintaan\nberhasil\ndicatat?')
box(p5,'P5 • Tampilkan rujukan,\npemeriksa, serta keadaan\nMenunggu hasil')
box(e2,'E2 • Pertahankan data;\nperiksa keberadaan permintaan dan kendala')
connector(250,1420)
connector(3190,1760)

arrow([(590,440),(730,440)],'Pilih',(590,370,730,430),40)
arrow([(1320,440),(1470,440)],'Buka',(1320,370,1470,430),40)
arrow([(2120,440),(2260,440)],'Tinjau',(2120,370,2260,430),40)
arrow([(2850,440),(3000,440)],'Ya',(2850,370,3000,430),48)
arrow([(2555,620),(2555,750)],'Tidak',(2590,645,2790,710),44)
arrow([(2150,880),(1990,880)],'Ditunda',(1985,805,2155,865),40)
arrow([(3270,570),(3270,1120),(3190,1120),(3190,1240)],
      'Lanjut',(3290,1050,3520,1110),44)
arrow([(2860,1420),(2690,1420)],'Tidak',(2690,1345,2860,1405),42)
arrow([(2100,1420),(1950,1420)],'Kirim',(1950,1345,2100,1405),40)
arrow([(1400,1420),(1230,1420)],'Ya',(1230,1345,1400,1405),48)
arrow([(500,1420),(318,1420)],'Lanjut',(320,1345,500,1405),40)
arrow([(3190,1600),(3190,1692)],'Ya',(3240,1615,3410,1675),48)
arrow([(1675,1600),(1675,1660)],'Tidak / belum pasti',(1110,1600,1650,1650),40)
arrow([(2440,1735),(2770,1735),(2770,1510),(3025,1510)],
      'Periksa dahulu',(2450,1745,2760,1805),40)

# Shape legend. The circles marked A are continuations, not success states.
y=1845
d.rounded_rectangle((90,y,185,y+34),radius=17,outline=BLACK,width=3)
d.text((205,y-12),'Mulai / ditunda',font=font(42),fill=BLACK)
d.rectangle((690,y,785,y+34),outline=BLACK,width=3)
d.text((805,y-12),'Proses',font=font(42),fill=BLACK)
d.polygon([(1190,y+17),(1237,y-9),(1284,y+17),(1237,y+43)],fill='white',outline=BLACK,width=3)
d.text((1305,y-12),'Keputusan',font=font(42),fill=BLACK)
d.ellipse((1740,y-9,1792,y+43),outline=BLACK,fill='#f1f1f1',width=3)
d.text((1755,y-11),'A',font=font(36,True),fill=BLACK)
d.text((1815,y-12),'Lanjutan ke Bagian B',font=font(42),fill=BLACK)

im.save(OUT/'proposed_flow_a.png',dpi=(300,300))
print(OUT/'proposed_flow_a.png')
