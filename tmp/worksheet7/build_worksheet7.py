from pathlib import Path
import json
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION_START,WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(r'D:\Rekayasa Interaksi')
TMP=ROOT/'tmp'/'worksheet7'
DATA=json.loads((TMP/'journey_data.json').read_text(encoding='utf-8'))
PHASES=DATA['phases']
STEM='202210370311406_Rusdany_Maestro_Worksheet7_UserJourney'
OUT=ROOT/(STEM+'.docx')
doc=Document();sec=doc.sections[0]
sec.page_width,sec.page_height=Cm(21),Cm(29.7)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2.5)
sec.footer_distance=Cm(1.2)
for s in doc.styles:
    if s.type in (1,2):s.font.name='Times New Roman';s.font.color.rgb=RGBColor(0,0,0)
for name,size in [('Normal',12),('Title',17),('Subtitle',12),('Heading 1',14),('Heading 2',12),('Footer',11)]:
    s=doc.styles[name];s.font.size=Pt(size)
    s.paragraph_format.space_after=Pt(5);s.paragraph_format.line_spacing=1.15
    s.paragraph_format.widow_control=True
doc.styles['Normal'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
for name in ('Title','Subtitle'):
    doc.styles[name].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
    doc.styles[name].paragraph_format.space_after=Pt(10)
doc.styles['Title'].font.bold=True;doc.styles['Subtitle'].font.italic=False
for name in ('Heading 1','Heading 2'):
    s=doc.styles[name];s.font.bold=True;s.paragraph_format.keep_with_next=True
    s.paragraph_format.space_before=Pt(6);s.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT
doc.styles['Heading 2'].paragraph_format.line_spacing=1
doc.styles['Heading 2'].paragraph_format.space_after=Pt(4)
footer=sec.footer.paragraphs[0];footer.style=doc.styles['Footer'];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
doc.core_properties.author='Rusdany Maestro'
doc.core_properties.title='Worksheet 7 User Journey Pembayaran Transfer pada Fleffy'
doc.core_properties.subject='Rekayasa Interaksi'

def p(text,indent=True,size=None):
    a=doc.add_paragraph(text)
    if indent:a.paragraph_format.first_line_indent=Cm(.75)
    else:a.alignment=WD_ALIGN_PARAGRAPH.LEFT
    if size:
        for r in a.runs:r.font.size=Pt(size)
    return a
def h(text,level=1,new_page=False):
    a=doc.add_paragraph(text,f'Heading {level}')
    a.paragraph_format.page_break_before=new_page
    return a
def field(label,text,size=11.5):
    a=doc.add_paragraph();a.alignment=WD_ALIGN_PARAGRAPH.LEFT
    a.paragraph_format.line_spacing=1.1
    a.add_run(label+': ').bold=True;a.add_run(text)
    for r in a.runs:r.font.size=Pt(size)
    return a
def table(headers,rows,widths,size=11,map_table=False):
    t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for col,w in zip(t.columns,widths):col.width=Cm(w)
    for cell,txt in zip(t.rows[0].cells,headers):cell.text=txt
    for row in rows:
        for cell,txt in zip(t.add_row().cells,row):cell.text=txt
    for ri,row in enumerate(t.rows):
        tr=row._tr.get_or_add_trPr();tr.append(OxmlElement('w:cantSplit'))
        if ri==0:tr.append(OxmlElement('w:tblHeader'))
        for ci,cell in enumerate(row.cells):
            cell.width=Cm(widths[ci]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cp=cell._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
            for edge in ('top','bottom','left','right'):
                el=OxmlElement('w:'+edge)
                for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]:el.set(qn('w:'+k),v)
                b.append(el)
            cp.append(b);mar=OxmlElement('w:tcMar')
            for edge,val in [('top',55 if map_table else 85),('bottom',55 if map_table else 85),('left',85),('right',85)]:
                el=OxmlElement('w:'+edge);el.set(qn('w:w'),str(val));el.set(qn('w:type'),'dxa');mar.append(el)
            cp.append(mar);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'F2F2F2' if ri==0 else 'FFFFFF');cp.append(shade)
            for a in cell.paragraphs:
                a.alignment=WD_ALIGN_PARAGRAPH.CENTER if ri==0 else WD_ALIGN_PARAGRAPH.LEFT
                a.paragraph_format.line_spacing=1.03 if map_table else 1.05
                a.paragraph_format.space_after=Pt(0 if map_table else 2)
                a.paragraph_format.first_line_indent=Cm(0)
                for r in a.runs:r.font.size=Pt(size);r.bold=(ri==0 or (map_table and ci==0))
    a=doc.add_paragraph();a.paragraph_format.line_spacing=Pt(2);a.paragraph_format.space_after=Pt(4)
    return t
def landscape():
    s=doc.add_section(WD_SECTION_START.NEW_PAGE);s.orientation=WD_ORIENT.LANDSCAPE
    s.page_width,s.page_height=Cm(29.7),Cm(21)
    s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Cm(1.5);s.footer_distance=Cm(.7)
def portrait():
    s=doc.add_section(WD_SECTION_START.NEW_PAGE);s.orientation=WD_ORIENT.PORTRAIT
    s.page_width,s.page_height=Cm(21),Cm(29.7)
    s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Cm(2.5);s.footer_distance=Cm(1.2)

# Halaman 1
doc.add_paragraph('User Journey Pembayaran Transfer pada Fleffy','Title')
doc.add_paragraph('Worksheet 7 Rekayasa Interaksi','Subtitle')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nMata kuliah: Rekayasa Interaksi\nJenis tugas: Individu\nTanggal penyusunan: 15 Oktober 2026',False)
h('1 Produk dan fokus perjalanan')
p('Fleffy - Kasir Laundry Sepatu mendukung pencatatan pesanan, layanan, dan pembayaran. Journey ini memetakan pengalaman admin ketika mencatat transfer dan memperoleh konfirmasi penerimaan dana sebelum meneruskan pesanan ke teknisi. Fokusnya adalah perjalanan kondisi saat ini menurut laporan pengguna, bukan alur solusi baru. [S1-S4]')
h('2 Persona skenario dan tujuan')
field('Persona','Ari, nama samaran pada Worksheet 6. Admin Operasional yang juga bertugas sebagai kasir, usia 20-22 tahun. Ari memakai Fleffy dan WhatsApp dalam pekerjaan harian; pemeriksaan rekening dilakukan owner atau finance. [S2 Q1-Q2, Q8; S4]')
field('Skenario','Pelanggan memesan deep cleaning dua pasang sepatu melalui WhatsApp dan mengirim bukti transfer Rp150.000. Ari mencatat pesanan, mencocokkan informasi, lalu meminta pemeriksaan penerimaan dana sebelum pesanan diteruskan ke teknisi. [S2 Q4-Q8]')
field('Tujuan utama','Pesanan dan pembayaran tercatat sesuai informasi yang diterima, serta tindak lanjut memiliki dasar konfirmasi dari pihak pemeriksa rekening. [S2 Q3, Q8]')
field('Awal dan akhir','Dimulai ketika pesanan dan bukti diterima; berakhir ketika hasil pemeriksaan yang sesuai menjadi dasar meneruskan pesanan. Pengerjaan cuci hingga pengambilan sepatu berada di luar skenario.')
p('Saya menyusun enam tahap agar hubungan antara pencatatan, pencocokan, koordinasi, dan keputusan tindak lanjut terlihat jelas. Perilaku bersumber dari R2; pikiran, penempatan sebagian emosi, dan peluang perbaikan diberi penanda sesuai jenisnya.')

# Halaman 2
h('3 Dasar data dan batas penyusunan',new_page=True)
table(['Sumber','Dasar yang digunakan','Peran dalam Journey'],[
    ('S1 Worksheet 1','Dokumentasi 19 September 2026; B2 menampilkan Lunas dan Bank Transfer Rp57.000.','Konteks layar pembayaran; bukan bukti mutasi atau transaksi Rp150.000.'),
    ('S2 Catatan R2','Wawancara langsung, 15 Oktober 2026, Pesenkopi, 12 menit; Q1-Q13.','Urutan inti Q4-Q8; tujuan Q3; pola usaha, emosi, dampak, dan harapan Q9-Q12.'),
    ('S3 Worksheet 5','Ringkasan jawaban R2 dan perbandingan tiga responden.','Menjaga pembagian kewenangan: Ari tidak mengambil peran owner pemeriksa rekening.'),
    ('S4 Worksheet 6','Persona Ari, Empathy Map, dan kebutuhan UX U1-U4.','Menjaga kesinambungan karakteristik, motivasi, emosi, kebutuhan, dan masalah.')
],[3.1,6.5,6.4])
h('Penanda pada peta',2)
field('D','Data yang dilaporkan R2, termasuk pola umum. Penanda ini tidak berarti peneliti menyaksikan kejadian secara langsung.')
field('I','Interpretasi peneliti untuk membagi tahap, menempatkan pikiran/emosi, atau merumuskan kebutuhan.')
field('P','Peluang perbaikan yang diusulkan untuk dievaluasi; bukan fitur yang sudah ada atau hasil pengujian.')
h('Cara membaca skenario',2)
p('Urutan utama direkonstruksi dari Q4-Q8. Pencatatan dan pencocokan dapat bergantian; pembagian T1-T6 membantu membaca pengalaman, bukan catatan klik atau waktu yang terukur. Q9-Q11 melengkapi pola hambatan dan perasaan pada tahap relevan. Keterlambatan, telepon, atau pelanggan menunggu tidak diklaim semuanya terjadi pada contoh Rp150.000.')
p('Contoh pengambilan sepatu pada Q9 tetap dipisahkan dari pesanan sebelum pengerjaan pada Q4. Peta berakhir pada tindak lanjut setelah konfirmasi. Kasus bukti tidak cocok atau dana belum masuk belum memiliki rincian alur yang cukup untuk dipetakan sebagai cabang lengkap.')
p('Sumber S2 dan S3 merujuk sesi yang sama, bukan dua responden berbeda. Seluruh pernyataan adalah parafrasa. Nama samaran dan kode responden menjaga privasi; tidak ada kontak pelanggan atau informasi rekening pribadi.',False,11)

# Halaman 3
landscape()
h('4 Gambaran visual perjalanan')
p('Urutan dibaca dari T1 menuju T6. Simbol emosi menunjukkan pola yang dilaporkan dan interpretasi per tahap; tidak menyatakan skor, intensitas, atau durasi pengalaman.',False,11)
picp=doc.add_paragraph();picp.alignment=WD_ALIGN_PARAGRAPH.CENTER
picp.paragraph_format.space_after=Pt(3)
picture=picp.add_run().add_picture(str(ROOT/'202210370311406_Rusdany_Maestro_Worksheet7_AlurJourney.png'),width=Cm(26.7))
picture._inline.docPr.set('descr','Alur Journey Ari dari T1 sampai T6. '+' '.join(x['id']+' '+x['tahap']+' '+x['short_action']+' '+x['short_emotion'] for x in PHASES))
h('Bagian yang memerlukan perhatian',2)
p('T3-T5 memperlihatkan usaha menghubungkan informasi dan memperoleh hasil pemeriksaan. T5 ditonjolkan karena R2 melaporkan penantian konfirmasi sebagai hambatan layanan. Penekanan ini merupakan prioritas analisis, tanpa menyatakan lama atau frekuensi keterlambatan pada setiap transaksi. [S2 Q6, Q8-Q11]',False,11)
p('Peta detail berikut melanjutkan alur yang sama dalam dua bagian agar seluruh komponen tetap terbaca. Kolom dan urutan komponen dipertahankan pada kedua halaman.',False,11)

# Halaman 4 dan 5 merupakan satu matriks yang berlanjut.
fields=[('Tujuan pengguna','tujuan'),('Aktivitas pengguna','aktivitas'),('Tindakan pengguna','tindakan'),('Touchpoint atau media','touchpoint'),('Pemikiran pengguna','pikiran'),('Perasaan atau emosi','emosi'),('Masalah atau hambatan','hambatan'),('Kebutuhan pengguna','kebutuhan'),('Peluang perbaikan UX','peluang'),('Dasar data','sumber')]
for start,title in [(0,'5 User Journey Map Tahap 1 sampai 3'),(3,'User Journey Map Tahap 4 sampai 6')]:
    h(title,new_page=True)
    p('D = laporan R2; I = interpretasi; P = peluang perbaikan. Tahapan berikut adalah bagian dari skenario dan Persona yang sama.',False,10.5)
    selected=PHASES[start:start+3]
    headers=['Komponen']+[x['id']+' '+x['tahap'] for x in selected]
    rows=[tuple([label]+[x[key] for x in selected]) for label,key in fields]
    table(headers,rows,[3.0,7.9,7.9,7.9],size=11,map_table=True)

# Halaman 6
portrait()
h('6 Ringkasan masalah UX utama')
h('M1 Penantian hasil pemeriksaan',2)
p('Pada T4-T5, Ari mengandalkan respons owner atau finance yang memegang akses rekening. R2 melaporkan bahwa konfirmasi yang lambat dapat membuat layanan tersendat atau pengerjaan tertunda. Rasa cemas saat menunggu turut muncul pada Q10. Karena berkaitan dengan keputusan sebelum pesanan dilanjutkan, bagian ini menjadi prioritas utama dalam analisis. [S2 Q8-Q11]')
p('Keterlambatan merupakan pengalaman umum yang dilaporkan, bukan pengukuran khusus contoh Rp150.000. Data belum cukup untuk menetapkan rata-rata waktu tunggu atau persentase transaksi yang terdampak.')
h('M2 Pencocokan informasi terpisah',2)
p('Pada T3-T4, rincian pesanan berada di Fleffy, bukti pada chat pelanggan, dan hasil pemeriksaan diperoleh melalui chat owner. R2 menjelaskan perpindahan sumber secara berulang. Kebutuhan utamanya adalah menjaga kecocokan informasi dan konteks pesanan saat berkoordinasi. Potensi salah menghubungkan informasi merupakan risiko interpretatif; kejadian salah cocok belum dibuktikan. [S2 Q5-Q8]')
h('M3 Perbedaan pencatatan dan kepastian dana',2)
p('Pada T2-T3, catatan pembayaran tidak menjadi satu-satunya dasar kepastian penerimaan. B2 pada observasi awal menunjukkan informasi di layar; R2 sendiri sudah membedakannya dari hasil pemeriksaan rekening. Karena itu, Journey tidak menyatakan bahwa Ari salah memahami Lunas. Peluangnya adalah memperjelas makna informasi serta dasar keputusan, terutama menuju T6. [S1 B2; S2 Q3, Q7-Q8]')
h('Pengalaman baik yang perlu dipertahankan',2)
p('R2 menilai input pesanan dan penerbitan nota berjalan lancar. Sesudah konfirmasi, ia merasa lega. Perbaikan pada koordinasi perlu mempertahankan kemudahan pencatatan dan ketelitian keputusan; menghapus pemeriksaan tanpa dasar penerimaan tidak menjadi kesimpulan Journey ini. [S2 Q9-Q10; S4 U1-U4]')

# Halaman 7
h('7 Kebutuhan dan peluang perbaikan UX',new_page=True)
p('P1-P6 pada peta diturunkan dari kebutuhan berikut. Hubungannya dengan U1-U4 pada Worksheet 6 mempertahankan dasar Persona Ari. Kriteria di bawah digunakan untuk pemeriksaan rancangan berikutnya; belum merupakan hasil uji atau janji peningkatan kinerja.')
h('Kejelasan makna status dan dasar keputusan',2)
p('T2-T3 memerlukan makna informasi pembayaran yang dapat dijelaskan. P2 mendukung perbedaan antara catatan pembayaran dan hasil pemeriksaan penerimaan, sambil mempertahankan kemudahan input. Dasarnya adalah penafsiran R2 pada Q7 dan kebutuhan U1 pada Worksheet 6.')
p('Kriteria pemeriksaan: operator dapat menjelaskan informasi yang telah dicatat dan apakah hasil pemeriksaan penerimaan sudah tersedia.')
h('Kecocokan informasi dengan pesanan',2)
p('T1-T3 memerlukan hubungan yang jelas antara pelanggan, layanan, nominal, dan bukti. P1 serta P3 mendukung ringkasan data awal dan rujukan bukti yang sesuai. Dasarnya adalah aktivitas Q4-Q6 dan kebutuhan U2 pada Worksheet 6.')
p('Kriteria pemeriksaan: operator dapat menunjuk pesanan, bukti, serta rincian pembanding yang digunakan dalam permintaan pemeriksaan.')
h('Kejelasan koordinasi dan perkembangan pemeriksaan',2)
p('T4-T5 memerlukan penanggung jawab dan tindak lanjut yang jelas. P4 serta P5 menghubungkan permintaan, pemeriksa, dan hasilnya dengan pesanan. Dasarnya adalah Q8-Q11 dan kebutuhan U3 pada Worksheet 6.')
p('Kriteria pemeriksaan: ketika hasil belum tersedia, operator dapat menjelaskan siapa yang memeriksa dan langkah berikutnya sesuai prosedur usaha.')
h('Kepastian tindak lanjut setelah konfirmasi',2)
p('T6 memerlukan dasar untuk meneruskan pesanan sesuai kewenangan. P6 mendukung hasil pemeriksaan yang terkait dengan pesanan dan informasi tindak lanjut. Dasarnya adalah Q3, Q8, Q10 dan kebutuhan U4 pada Worksheet 6.')
p('Kriteria pemeriksaan: operator dapat menentukan tindak lanjut dari hasil pemeriksa yang sesuai, tanpa mengganti konfirmasi penerimaan dengan sekadar input nominal.')

# Halaman 8
h('8 Keterbatasan dan asumsi',new_page=True)
p('Journey bertumpu pada satu anggota kelompok yang menjadi dasar Persona, yaitu R2. R1 dan R3 tidak digabungkan ke alur Ari karena akses rekening dan pembagian tugas mereka berbeda. Urutan T1-T6 merupakan rekonstruksi untuk membaca satu skenario; belum divalidasi melalui observasi lapangan dari awal sampai akhir.')
p('Q10 memberikan pola tenang sebelum proses, cemas selama pemeriksaan, dan lega sesudah konfirmasi. Penempatan tenang di T2, waspada di T3, serta awal cemas di T4 merupakan interpretasi, bukan perasaan yang diukur pada tiap tahap. Pikiran pada peta juga berupa interpretasi, bukan kutipan langsung.')
p('Pada T1 dan T6, hambatan khusus belum dirinci. Peta menyatakan batas tersebut dan tetap merumuskan kebutuhan yang relevan. Tidak ada asumsi bahwa pelanggan hadir secara fisik pada contoh WhatsApp atau bahwa telepon serta penundaan beberapa jam pasti terjadi pada transaksi Rp150.000.')
p('Data belum menjelaskan alur lengkap ketika bukti tidak cocok, dana belum masuk, atau konfirmasi tidak diperoleh. Pendalaman berikutnya perlu mengamati kasus tersebut, mencatat perpindahan informasi dan waktu tunggu bila diizinkan, serta memeriksa urutan dengan operator dan owner. Mutasi dan data pelanggan pribadi tetap tidak direproduksi.')
h('9 Kesimpulan')
p('Perjalanan Ari bergerak dari penerimaan pesanan dan bukti, pencatatan, pencocokan, permintaan pemeriksaan, penantian hasil, hingga tindak lanjut setelah konfirmasi. Tujuan di seluruh alur adalah memperoleh catatan yang benar dan dasar penerimaan dana yang dapat dipertanggungjawabkan sebelum pesanan diteruskan.')
p('Usaha utama muncul ketika informasi berpindah sumber dan pemeriksaan membutuhkan respons pihak lain. Peluang UX berfokus pada kecocokan informasi, kejelasan koordinasi, dan dasar keputusan yang sesuai kewenangan. Validasi otomatis atau integrasi bank yang diharapkan R2 tetap merupakan alternatif untuk dievaluasi, bukan solusi yang sudah terbukti. [S2 Q12-Q13]')
h('Sumber data',2)
p('S1. Rusdany Maestro. Worksheet 1 UX Detective, dokumentasi 19 September 2026, terutama bukti B2 dan batas observasi.\nS2. Catatan wawancara R2 Admin Operasional, 15 Oktober 2026, Q1-Q13 beserta pendalaman.\nS3. Rusdany Maestro. Worksheet 5 User Interview, terutama ringkasan R2 dan perbandingan responden.\nS4. Rusdany Maestro. Worksheet 6 Empathy Map dan Persona, Persona Ari, enam bagian Empathy Map, dan kebutuhan UX U1-U4.\nAcuan tugas. Worksheet 7 User Journey, mata kuliah Rekayasa Interaksi.',False,11)

for tree in (doc.element,doc.styles.element,sec.footer._element):
    for fonts in tree.iter(qn('w:rFonts')):
        fonts.attrib.clear()
        for attr in ('ascii','hAnsi','eastAsia','cs'):fonts.set(qn('w:'+attr),'Times New Roman')
    for border in list(tree.iter(qn('w:pBdr'))):border.getparent().remove(border)
    for rp in tree.iter(qn('w:rPr')):
        spacing=rp.find(qn('w:spacing'))
        if spacing is not None:rp.remove(spacing)
    for color in tree.iter(qn('w:color')):color.attrib.clear();color.set(qn('w:val'),'000000')
doc.save(OUT)
plain=[]
for child in doc.element.body:
    txt=' '.join(child.xpath('.//w:t/text()'))
    if txt:plain.append(txt)
(TMP/'report_content.txt').write_text('\n\n'.join(plain),encoding='utf-8')
audit={
    'persona':'Ari','scenario':DATA['skenario'],'phases':len(PHASES),
    'required_components':['Tahapan perjalanan pengguna','Tujuan pengguna','Aktivitas pengguna','Tindakan pengguna','Touchpoint atau media interaksi','Pemikiran pengguna','Perasaan atau emosi pengguna','Masalah atau hambatan','Kebutuhan pengguna','Peluang perbaikan UX'],
    'rubrik':[
        {'aspek':'Kesesuaian dengan Persona dan skenario','bobot':20,'halaman_rencana':[1,2,3,4,5]},
        {'aspek':'Kelengkapan tahapan perjalanan','bobot':20,'halaman_rencana':[3,4,5]},
        {'aspek':'Aktivitas touchpoint pikiran dan emosi','bobot':20,'halaman_rencana':[3,4,5]},
        {'aspek':'Identifikasi masalah dan hambatan UX','bobot':15,'halaman_rencana':[4,5,6]},
        {'aspek':'Kejelasan kebutuhan dan peluang UX','bobot':15,'halaman_rencana':[4,5,7]},
        {'aspek':'Visualisasi dan kerapian','bobot':10,'halaman_rencana':list(range(1,9))}
    ],
    'pemisahan_bukti':{'D':'laporan R2','I':'interpretasi','P':'peluang belum diuji'},
    'qa_visual':'Menunggu render','deadline':None
}
(TMP/'audit_kelengkapan.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(OUT)
print('Kata:',sum(len(x.split()) for x in plain))
