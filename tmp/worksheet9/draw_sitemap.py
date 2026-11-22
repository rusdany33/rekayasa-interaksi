from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math

TMP=Path(r'D:\Rekayasa Interaksi\tmp\worksheet9')
W,H=3200,1800
im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('timesbd.ttf' if bold else 'times.ttf'),n)
def wrap(s,f,width):
    lines=[]
    for line in s.split('\n'):
        words=line.split();cur=''
        for word in words:
            test=(cur+' '+word).strip()
            if cur and d.textlength(test,font=f)>width:lines.append(cur);cur=word
            else:cur=test
        lines.append(cur)
    return lines
def text(s,box,size=50,bold=False,align='center'):
    x1,y1,x2,y2=box;f=font(size,bold);lines=wrap(s,f,x2-x1-28);lh=size*1.13
    y=y1+(y2-y1-lh*len(lines))/2
    for l in lines:
        x=(x1+x2-d.textlength(l,font=f))/2 if align=='center' else x1+12
        d.text((x,y),l,font=f,fill='black');y+=lh
def rect(box,label,size=52,fill='white',bold=True):
    d.rectangle(box,fill=fill,outline='black',width=3);text(label,box,size,bold)
def line(points,fill='black',width=4):d.line(points,fill=fill,width=width,joint='curve')
def dash(a,b,width=4):
    x1,y1=a;x2,y2=b;length=math.hypot(x2-x1,y2-y1)
    for st in range(0,int(length),25):
        en=min(st+14,length)
        d.line((x1+(x2-x1)*st/length,y1+(y2-y1)*st/length,x1+(x2-x1)*en/length,y1+(y2-y1)*en/length),fill='black',width=width)

# Garis induk dan anak ditempatkan di belakang kotak.
line([(1600,200),(1600,290),(500,290),(500,380)])
line([(1600,290),(1600,380)])
line([(1600,290),(2700,290),(2700,380)])
line([(500,620),(500,690),(245,690),(245,770)])
line([(500,690),(770,690),(770,770)])
line([(2700,620),(2700,690),(2220,690),(2220,1500)])
for y in (870,1150,1500):line([(2220,y),(2300,y)])

rect((1260,40,1940,200),'N0 Beranda',58,fill='#F2F2F2')
rect((40,380,960,620),'N1 Pesanan\nDaftar dan pencarian',54,fill='#F2F2F2')
rect((1140,380,2060,620),'N2 Pemeriksaan Pembayaran\nAntrean pemeriksaan',52,fill='#F2F2F2')
rect((2240,380,3160,620),'N3 Bantuan Pemeriksaan\nPanduan dan kontak',52,fill='#F2F2F2')
rect((40,770,450,950),'N1a\nBuat Pesanan',50)
rect((500,770,1040,1430),'',50)
text('N1b\nDetail Pesanan',(510,785,1030,940),52,True)
for i,label in enumerate(['Ringkasan Pesanan','Pembayaran','Pemeriksaan','Tindak Lanjut']):
    y=955+i*112
    d.rectangle((525,y,1015,y+90),fill='#F2F2F2',outline='#808080',width=2)
    text(label,(525,y,1015,y+90),46,False)

rect((2300,785,3140,955),'N3a Arti Status Pembayaran',50)
rect((2300,1065,3140,1235),'N3b Panduan saat Menunggu',50)
rect((2300,1415,3140,1585),'N3c Kontak Pemeriksa',50)

# Tautan silang mengarah ke bagian Pemeriksaan dari halaman yang sama.
target_y=1224
dash((1600,620),(1600,target_y));dash((1600,target_y),(1040,target_y))
d.polygon([(1040,target_y),(1067,target_y-16),(1067,target_y+16)],fill='black')
text('TS1 Pilih pesanan\nBuka Detail Pesanan\nbagian Pemeriksaan',(1630,850,2190,1110),46,False,'left')
text('Empat kotak di dalam Detail Pesanan\nadalah bagian halaman bukan halaman tambahan',(430,1475,1120,1635),40)

line([(90,1710),(270,1710)]);text('Hierarki',(285,1660,560,1760),44,False,'left')
dash((670,1710),(850,1710));text('Tautan silang TS1',(865,1660,1360,1760),44,False,'left')
text('Kotak luar = halaman\nSitemap usulan untuk fokus pembayaran transfer',(1490,1660,3130,1770),44,False,'left')
out=TMP/'sitemap_fleffy.png';im.save(out,dpi=(300,300))
print(out)
