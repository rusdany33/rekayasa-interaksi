from pathlib import Path
import json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(r'D:\Rekayasa Interaksi')
TMP=ROOT/'tmp'/'worksheet8'
TMP.mkdir(parents=True,exist_ok=True)
STEM='202210370311406_Rusdany_Maestro_Worksheet8_UXRequirements'
doc=Document()
sec=doc.sections[0]
sec.page_width,sec.page_height=Cm(21),Cm(29.7)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2.5)
sec.footer_distance=Cm(1.2)
for s in doc.styles:
    if s.type in (1,2): s.font.name='Times New Roman';s.font.color.rgb=RGBColor(0,0,0)
for name,size in [('Normal',12),('Title',17),('Subtitle',12),('Heading 1',14),('Heading 2',12),('Footer',11)]:
    s=doc.styles[name];s.font.size=Pt(size)
    s.paragraph_format.space_after=Pt(5)
    s.paragraph_format.line_spacing=1.1
    s.paragraph_format.widow_control=True
doc.styles['Normal'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
for n in ('Title','Subtitle'):
    doc.styles[n].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
    doc.styles[n].paragraph_format.space_after=Pt(9)
doc.styles['Title'].font.bold=True
for n in ('Heading 1','Heading 2'):
    s=doc.styles[n];s.font.bold=True;s.paragraph_format.keep_with_next=True
    s.paragraph_format.space_before=Pt(7);s.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT
footer=sec.footer.paragraphs[0]
footer.style=doc.styles['Footer'];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
doc.core_properties.author='Rusdany Maestro'
doc.core_properties.title='Kebutuhan UX Pemeriksaan Pembayaran Transfer pada Fleffy'
doc.core_properties.subject='Worksheet 8 Rekayasa Interaksi'

def p(text,indent=True,size=None):
    a=doc.add_paragraph(text)
    a.paragraph_format.first_line_indent=Cm(.75 if indent else 0)
    if not indent:a.alignment=WD_ALIGN_PARAGRAPH.LEFT
    if size:
        for r in a.runs:r.font.size=Pt(size)
    return a
def h(text,level=1,page=False):
    a=doc.add_paragraph(text,f'Heading {level}')
    a.paragraph_format.page_break_before=page
    return a
def field(label,text,size=11.5):
    a=doc.add_paragraph();a.alignment=WD_ALIGN_PARAGRAPH.LEFT
    a.paragraph_format.line_spacing=1.07
    a.add_run(label+': ').bold=True;a.add_run(text)
    for r in a.runs:r.font.size=Pt(size)
    return a
def table(headers,rows,widths,size=11):
    t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for c,w in zip(t.columns,widths):c.width=Cm(w)
    for c,s in zip(t.rows[0].cells,headers):c.text=s
    for row in rows:
        for c,s in zip(t.add_row().cells,row):c.text=str(s)
    for ri,row in enumerate(t.rows):
        tr=row._tr.get_or_add_trPr();tr.append(OxmlElement('w:cantSplit'))
        if ri==0:tr.append(OxmlElement('w:tblHeader'))
        for ci,c in enumerate(row.cells):
            c.width=Cm(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cp=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
            for edge in ('top','bottom','left','right'):
                el=OxmlElement('w:'+edge)
                for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]:el.set(qn('w:'+k),v)
                b.append(el)
            cp.append(b)
            mar=OxmlElement('w:tcMar')
            for edge,val in [('top',80),('bottom',80),('left',85),('right',85)]:
                el=OxmlElement('w:'+edge);el.set(qn('w:w'),str(val));el.set(qn('w:type'),'dxa');mar.append(el)
            cp.append(mar)
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'F2F2F2' if ri==0 else 'FFFFFF');cp.append(shade)
            for a in c.paragraphs:
                a.alignment=WD_ALIGN_PARAGRAPH.CENTER if ri==0 else WD_ALIGN_PARAGRAPH.LEFT
                a.paragraph_format.line_spacing=1.02;a.paragraph_format.space_after=Pt(2)
                a.paragraph_format.first_line_indent=Cm(0)
                for r in a.runs:r.font.size=Pt(size);r.bold=(ri==0)
    a=doc.add_paragraph();a.paragraph_format.line_spacing=Pt(2);a.paragraph_format.space_after=Pt(3)
    return t

def landscape():
    s=doc.add_section(WD_SECTION_START.NEW_PAGE)
    s.orientation=WD_ORIENT.LANDSCAPE
    s.page_width,s.page_height=Cm(29.7),Cm(21)
    s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Cm(1.5)
    s.footer_distance=Cm(.7)

def portrait():
    s=doc.add_section(WD_SECTION_START.NEW_PAGE)
    s.orientation=WD_ORIENT.PORTRAIT
    s.page_width,s.page_height=Cm(21),Cm(29.7)
    s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Cm(2.5)
    s.footer_distance=Cm(1.2)

REQS=[
dict(id='UX01',title='Memahami makna informasi pembayaran',priority='Must',rank=4,problem='M3',goal='G1',u='U1',stage='T2-T3',
need='Ari membutuhkan informasi yang membedakan pembayaran yang telah dicatat dari penerimaan dana yang telah diperiksa agar ia mengetahui kepastian yang sudah tersedia dan yang masih perlu diperoleh.',
basis='R2 membedakan pencatatan dari pemeriksaan rekening pada Q7. R1 masih mempertanyakan jaminan label Lunas, sedangkan R3 tetap memeriksa rekening. Kebutuhan ini memperjelas informasi; tidak menganggap semua pengguna salah memahami status. [S5 R1-R3 Q7; S6 U1; S7 M3]',
criteria=[
'Pada pesanan yang baru dicatat tanpa hasil pemeriksaan, Ari dapat menyebut bahwa pembayaran telah dicatat dan penerimaan dana belum dipastikan.',
'Pada pesanan yang hasil pemeriksaannya tersedia, Ari dapat menjelaskan perbedaan informasi pencatatan dan hasil pemeriksaan dengan benar, tanpa petunjuk moderator.'
],rationale='Makna informasi adalah dasar memahami proses. Prioritas Must karena penafsiran yang tidak tepat dapat melemahkan keputusan, walaupun R2 sudah memahami perbedaannya.',
scope='Berlaku saat membaca catatan dan hasil pemeriksaan. Istilah atau bentuk tampilan dipilih pada tahap rancangan; kebutuhan tidak mewajibkan nama status tertentu.'),
dict(id='UX02',title='Mencocokkan informasi pada pesanan yang sama',priority='Must',rank=3,problem='M2',goal='G1',u='U2',stage='T1-T4',
need='Ari membutuhkan hubungan yang dapat ditelusuri antara pesanan, nominal tagihan, bukti pelanggan, dan hasil pemeriksaan agar ia dapat mencocokkan pembayaran untuk pesanan yang tepat tanpa mengandalkan ingatan semata.',
basis='R2 menghubungkan data Fleffy, bukti pada WhatsApp pelanggan, dan hasil pemeriksaan owner atau finance. R1 dan R3 juga mencocokkan catatan dengan informasi penerimaan. Kejadian salah cocok belum dibuktikan. [S5 R2 Q4-Q8; R1 dan R3 Q4-Q8; S6 U2; S7 M2]',
criteria=[
'Ketika diberi dua pesanan bernominal sama, Ari dapat menunjuk pesanan dan bukti yang sesuai menggunakan identitas pesanan atau konteks pembanding yang tersedia, bukan hanya nominal.',
'Ari dapat membandingkan nominal serta tanggal atau waktu pada informasi pembayaran, dan menghubungkan hasil pemeriksaan dengan pesanan yang sama. Ketidakcocokan pada skenario uji dikenali sebelum tindak lanjut.'
],rationale='Prioritas Must karena konfirmasi hanya berguna jika merujuk pesanan yang benar. Hubungan informasi mendukung koordinasi dan keputusan pada UX03 serta UX05.',
scope='Informasi pembanding mengikuti yang tersedia dan prosedur pemeriksa. Nomor rekening lengkap atau akses bank langsung untuk Ari tidak menjadi syarat.'),
dict(id='UX03',title='Mengetahui penanggung jawab dan perkembangan pemeriksaan',priority='Must',rank=2,problem='M1',goal='G2',u='U3',stage='T4-T5',
need='Ari membutuhkan kejelasan siapa yang bertanggung jawab memeriksa rekening dan sampai di mana permintaan pemeriksaan pesanan ditangani agar ia dapat berkoordinasi dengan pihak yang tepat saat menunggu kepastian.',
basis='R2 meminta owner atau finance memeriksa mutasi dan menunggu balasan. Respons yang lambat dilaporkan dapat menunda pelayanan atau pengerjaan. Worksheet 3 menekankan pembagian tanggung jawab sesuai peran. [S3 profil Kasir Owner Admin; S5 R2 Q1, Q8-Q11; S6 U3; S7 M1]',
criteria=[
'Setelah meminta pemeriksaan, Ari dapat menyebut pesanan yang dimaksud, pihak pemeriksa sesuai prosedur usaha, serta apakah hasil pemeriksaan sudah tersedia atau masih ditunggu.',
'Ketika hasil belum tersedia, Ari tidak menafsirkan pengiriman permintaan sebagai konfirmasi dana masuk; ketika hasil tersedia, ia dapat menemukan hasil untuk permintaan yang sama.'
],rationale='Prioritas Must karena ketergantungan pada pemeriksa merupakan hambatan utama Ari. Kejelasan perkembangan mengurangi ketidakpastian koordinasi; tidak menjamin owner merespons lebih cepat.',
scope='Ari tetap sebagai pencatat dan penerima konfirmasi. Progres hanya menyatakan keadaan yang memiliki dasar; waktu selesai tidak boleh dijanjikan tanpa informasi pemeriksa.'),
dict(id='UX04',title='Menentukan tindak lanjut selama hasil belum tersedia',priority='Should',rank=5,problem='M1',goal='G2',u='U3',stage='T5',
need='Saat hasil pemeriksaan belum tersedia, Ari membutuhkan kejelasan langkah tindak lanjut sesuai prosedur usaha agar ia dapat menghubungi pihak yang tepat dan menjelaskan kondisi pembayaran kepada pelanggan secara akurat.',
basis='R2 melaporkan panggilan telepon saat respons lambat, pelanggan yang diminta menunggu, dan rasa sungkan. Perumusan dukungan tindak lanjut adalah interpretasi atas pola tersebut, bukan prosedur baku yang telah disepakati. [S5 R2 Q9-Q11; S6 U3; S7 T5 dan P5]',
criteria=[
'Pada skenario hasil masih ditunggu, Ari dapat memilih langkah menghubungi kembali atau meminta bantuan sesuai prosedur uji, sambil mempertahankan kondisi pembayaran yang belum dipastikan.',
'Ari dapat menjelaskan kepada pelanggan bahwa pemeriksaan masih berlangsung tanpa menyatakan dana sudah diterima atau menjanjikan waktu selesai yang belum diketahui.'
],rationale='Prioritas Should karena mendukung pelayanan pada kondisi penantian. Penerapannya membutuhkan kesepakatan prosedur dan mengandalkan kejelasan penanggung jawab pada UX03.',
scope='Kontak, batas waktu tindak lanjut, dan pihak pengganti harus disepakati usaha saat pendalaman. Penelitian belum menetapkan berapa menit pengguna harus menunggu.'),
dict(id='UX05',title='Menentukan keputusan berdasarkan hasil pemeriksaan',priority='Must',rank=1,problem='M3 dan M4',goal='G3',u='U4',stage='T6 serta kondisi sebelum konfirmasi',
need='Ari membutuhkan hasil pemeriksaan yang merujuk pesanan yang sama dan berasal dari pihak berwenang agar ia dapat menentukan apakah pesanan boleh diteruskan ke teknisi atau perlu ditahan untuk pemeriksaan lanjutan.',
basis='R2 baru meneruskan pesanan setelah konfirmasi owner atau finance. R3 juga memastikan penerimaan sebelum melanjutkan. Worksheet 3 membedakan tanggung jawab pencatat, pemeriksa, dan teknisi. [S3 hubungan Kasir Owner dan Kasir Teknisi; S5 R2 Q3, Q8; R3 Q8; S6 U4; S7 T6]',
criteria=[
'Pada hasil yang sesuai dari pemeriksa berwenang, Ari dapat menentukan tindak lanjut pesanan dan menjelaskan hasil pemeriksaan yang menjadi dasarnya.',
'Pada hasil yang belum tersedia, tidak cocok, atau tidak jelas rujukan pesanannya, Ari memilih menahan tindak lanjut dan meminta pemeriksaan lanjutan sesuai prosedur uji, tanpa menganggap input pembayaran sebagai kepastian dana.'
],rationale='Prioritas Must dan urutan pertama karena merupakan tujuan akhir tugas: keputusan kerja memiliki dasar yang tepat. Jika kebutuhan ini tidak terpenuhi, kejelasan informasi lain belum cukup menjamin ketepatan tindak lanjut.',
scope='Rincian penanganan ketidaksesuaian adalah kasus uji yang diusulkan, bukan kejadian lapangan yang telah diamati. Kewenangan perubahan status aktual masih perlu diperiksa pada akun terkait.'),
dict(id='UX06',title='Mempertahankan kelancaran pencatatan',priority='Should',rank=6,problem='M2 dan kualitas yang sudah baik',goal='G4',u='U2',stage='T1-T4',
need='Ari membutuhkan proses pencatatan pesanan dan pembayaran yang tetap lancar ketika terhubung dengan pemeriksaan agar ia dapat meneruskan konteks pesanan tanpa memasukkan ulang informasi yang sudah benar hanya untuk meminta pemeriksaan.',
basis='R2 menilai input pesanan serta penerbitan nota sudah lancar, tetapi perlu berpindah sumber saat meminta pemeriksaan. Mencegah pengisian ulang merupakan sasaran menjaga pengalaman baik; bukan hambatan yang telah dilaporkan terjadi. [S5 R2 Q6, Q9, Q12; S6 U2; S7 pengalaman baik dan P2]',
criteria=[
'Setelah mencatat pesanan, Ari dapat melanjutkan permintaan pemeriksaan dengan identitas pesanan dan nominal yang sama tanpa mengetik ulang kedua informasi tersebut dalam alur rancangan.',
'Rincian pelanggan, layanan, dan nominal yang telah benar tetap dapat ditunjuk serta digunakan saat menghubungkan pemeriksaan; tidak ada perubahan data yang tidak disengaja pada skenario uji.'
],rationale='Prioritas Should karena menjaga kelebihan pencatatan yang sudah dinilai baik. Bukti masalah pengisian ulang belum tersedia, sehingga kebutuhan ini ditempatkan setelah kepastian dan koordinasi inti.',
scope='Tidak menetapkan jumlah klik atau waktu input sebelum baseline tersedia. Bentuk pemanfaatan ulang konteks dipilih melalui eksplorasi rancangan.')
]

MAPPING=[
('R2 memandang status sebagai catatan; kepastian dana berasal dari pemeriksaan. R1 mempertanyakan jaminan Lunas. [S5 R1-R3 Q7; S6 U1; S7 M3]',
 'Mengetahui informasi yang sudah dicatat dan penerimaan dana yang sudah dipastikan, agar dasar kepastian pembayaran dapat dijelaskan.',
 'FR01 Sistem menyimpan informasi pencatatan pembayaran dan hasil pemeriksaan penerimaan secara terpisah, menghubungkan keduanya ke pesanan, serta menampilkan sumber hasil pemeriksaan.',
 'UX01 Ari dapat membedakan pembayaran tercatat dan penerimaan yang sudah diperiksa dengan benar, tanpa petunjuk moderator. Must; urutan 4.'),
('R2 mencocokkan catatan Fleffy, bukti pada chat pelanggan, dan hasil owner atau finance melalui sumber yang terpisah. [S5 R2 Q4-Q8; S6 U2; S7 M2]',
 'Menghubungkan pesanan, nominal, bukti, dan hasil pemeriksaan untuk pembayaran yang sama tanpa bergantung pada ingatan semata.',
 'FR02 Sistem mengaitkan identitas pesanan, nominal tagihan, rujukan bukti pelanggan, dan hasil pemeriksaan agar dapat ditinjau dalam konteks pesanan yang sama.',
 'UX02 Ari dapat mencocokkan bukti dan hasil dengan pesanan yang tepat, termasuk ketika dua pesanan bernominal sama. Must; urutan 3.'),
('R2 meminta owner atau finance memeriksa rekening. Respons yang lambat dilaporkan dapat menunda pelayanan atau pengerjaan. [S3 hubungan peran; S5 R2 Q8-Q11; S6 U3; S7 M1]',
 'Mengetahui penanggung jawab dan perkembangan permintaan pemeriksaan agar dapat berkoordinasi dengan pihak yang tepat.',
 'FR03 Sistem mencatat permintaan pemeriksaan per pesanan, pihak yang dituju, keadaan permintaan, dan hasil dari pemeriksa sesuai kewenangan yang ditetapkan usaha.',
 'UX03 Ari dapat menyebut pemeriksa serta mengetahui apakah hasil sudah tersedia atau masih ditunggu, tanpa menganggap pengiriman permintaan sebagai penerimaan dana. Must; urutan 2.'),
('R2 kadang menelepon owner ketika respons lambat dan merasa sungkan bila pelanggan menunggu. [S5 R2 Q9-Q11; S6 U3; S7 T5]',
 'Mengetahui langkah berikutnya saat menunggu dan dapat menjelaskan kondisi pembayaran kepada pelanggan tanpa memberikan kepastian yang belum tersedia.',
 'FR04 Sistem menyediakan informasi tindak lanjut dan pihak yang dapat dihubungi ketika hasil pemeriksaan belum tersedia, mengikuti prosedur yang disepakati usaha.',
 'UX04 Ari dapat memilih tindak lanjut sesuai prosedur dan menjelaskan bahwa pemeriksaan masih berlangsung tanpa menjanjikan hasil atau waktu yang belum diketahui. Should; urutan 5.'),
('R2 meneruskan pesanan setelah konfirmasi pemeriksa rekening; R3 juga memastikan penerimaan sebelum melanjutkan. [S3 hubungan Kasir Owner Teknisi; S5 R2 Q3, Q8; R3 Q8; S6 U4; S7 T6]',
 'Memiliki dasar dari pihak berwenang untuk menentukan apakah pesanan dapat diteruskan atau perlu ditahan untuk pemeriksaan lanjutan.',
 'FR05 Sistem mencatat keputusan menahan atau meneruskan pesanan beserta rujukan hasil pemeriksaan dan petugas pengambil keputusan, sesuai kewenangan yang disepakati usaha.',
 'UX05 Ari memilih tindak lanjut berdasarkan hasil yang sesuai untuk pesanan yang sama; tanpa hasil yang memadai, ia menahan tindak lanjut. Must; urutan 1.'),
('R2 menilai input pesanan dan nota sudah lancar, sementara permintaan pemeriksaan melibatkan perpindahan sumber. Pengisian ulang belum dilaporkan sebagai keluhan. [S5 R2 Q6, Q9, Q12; S7 bagian 6]',
 'Mempertahankan kelancaran pencatatan saat menghubungkan pemeriksaan, tanpa mengisi ulang informasi yang sudah benar hanya untuk meminta pemeriksaan.',
 'FR06 Sistem menggunakan kembali identitas pesanan dan nominal yang tersimpan saat membuat permintaan pemeriksaan serta mempertahankan rincian awal yang tidak diubah pengguna.',
 'UX06 Ari dapat meneruskan konteks pesanan ke pemeriksaan tanpa mengetik ulang identitas pesanan dan nominal; rincian yang benar tetap terjaga. Should; urutan 6.')
]
STORIES=[
('US01','As a Fleffy admin handling cashier tasks, I want to distinguish recorded payments from confirmed fund receipts, so that I know which payment information has been verified.','UX01; FR01; G1; V1'),
('US02','As a Fleffy admin handling cashier tasks, I want to match each order with its bill, payment proof, and verification result, so that I can identify the correct payment even when order amounts are the same.','UX02; FR02; G1; V2'),
('US03','As a Fleffy admin handling cashier tasks, I want to know who is checking a payment and whether the result is available, so that I can coordinate with the responsible person while waiting.','UX03; FR03; G2; V1'),
('US04','As a Fleffy admin handling cashier tasks, I want to know the appropriate follow-up when a verification result is unavailable, so that I can explain the situation to the customer without making unsupported promises.','UX04; FR04; G2; V4'),
('US05','As a Fleffy admin handling cashier tasks, I want to base my decision on an authorized verification result for the same order, so that I can decide whether to forward the order to technicians or hold it for further checking.','UX05; FR05; G3; V3-V4'),
('US06','As a Fleffy admin handling cashier tasks, I want to reuse correct order information when requesting payment verification, so that I can continue the process without re-entering the order identity and payment amount.','UX06; FR06; G4; V5')
]

# Halaman 1
doc.add_paragraph('Kebutuhan UX Pemeriksaan Pembayaran Transfer pada Fleffy','Title')
doc.add_paragraph('Worksheet 8 Rekayasa Interaksi','Subtitle')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nJenis tugas: Praktikum Individu\nTanggal analisis: 15 Oktober 2026',False)
field('Berkas bukti pendukung','Worksheet 3 UserStakeholder; Worksheet 5 UserInterview; Worksheet 6 EmpathyMapPersona; Worksheet 7 UserJourney. Rincian sumber pada bagian 10.',10.5)
h('1 Fokus dan hasil perumusan')
p('Saya merumuskan enam kebutuhan UX untuk membantu admin atau kasir Fleffy mencocokkan pembayaran transfer, memperoleh hasil pemeriksaan, dan menentukan tindak lanjut pesanan. Empat kebutuhan berprioritas Must dan dua kebutuhan berprioritas Should. Kebutuhan paling penting adalah dasar keputusan yang sesuai hasil pemeriksaan dan kewenangan pengguna, yaitu UX05.')
p('Fleffy - Kasir Laundry Sepatu mendukung pencatatan pesanan, layanan, dan pembayaran. Fokus kajian ini dimulai ketika pesanan serta bukti transfer diterima dan berakhir ketika operator menentukan tindak lanjut sebelum pengerjaan oleh teknisi. Proses pencucian, pengantaran, dan pengambilan berada di luar skenario utama. [S3; S5 R2 Q4-Q8; S7]')
h('Pengguna dan konteks utama',2)
p('Persona utama adalah Ari, nama samaran admin operasional yang juga bertugas sebagai kasir, usia 20-22 tahun. Ia mencatat transaksi melalui Fleffy dan meminta owner atau finance memeriksa rekening. R2 menjadi sumber utama Persona dan Journey. R1 serta R3 digunakan sebagai pembanding karena dapat memeriksa rekening sendiri. [S5 bagian 8; S6 bagian 5]')
field('Skenario acuan','Pelanggan memesan deep cleaning dua pasang sepatu melalui WhatsApp dan mengirim bukti transfer Rp150.000. Ari mencatat pesanan, meminta pemeriksaan, lalu menindaklanjuti konfirmasi sebelum menyerahkan pesanan kepada teknisi. [S5 R2 Q4-Q8]')
h('Dasar penyusunan',2)
p('Worksheet 3 memberi batas peran dan tanggung jawab. Worksheet 5 memberi pengalaman, tujuan, hambatan, serta harapan pengguna. Worksheet 6 merangkum kebutuhan Persona menjadi U1-U4. Worksheet 7 menempatkannya pada T1-T6. Bagian 3 dan 4 mengikuti pemetaan serta User Stories pada template Pertemuan 08 dalam workbook.')

# Halaman 2
h('2 Masalah tujuan kebutuhan dan harapan pengguna',page=True)
p('Ringkasan berikut menghubungkan pengalaman pengguna dengan hasil yang dibutuhkan. M1-M4 adalah kode analisis pada worksheet ini; G1-G4 adalah tujuan yang menjadi dasar rumusan kebutuhan.',False,11)
table(['Masalah dan dasar riset','Tujuan dan kebutuhan pengguna','Harapan hasil pengalaman'],[
('M1 Penantian konfirmasi pihak lain. R2 melaporkan respons lambat, rasa cemas, dan kemungkinan layanan atau pengerjaan tertunda. [S5 R2 Q8-Q11; S7 M1]','G2 Menangani koordinasi dengan jelas saat menunggu. Ari perlu mengetahui pemeriksa, perkembangan permintaan, dan langkah berikutnya.','Kepastian lebih mudah diperoleh; operator dapat menjelaskan keadaan pembayaran selama menunggu. [R2 Q10, Q12]'),
('M2 Informasi pembayaran tersebar. Ari berpindah antara Fleffy, bukti pelanggan, dan chat pemeriksa. [S5 R2 Q4-Q8; S7 M2]','G1 Mencocokkan catatan dengan pembayaran yang tepat. Ari perlu hubungan yang jelas antara pesanan, nominal, bukti, dan hasil pemeriksaan.','Pengecekan lebih praktis dengan konteks pesanan tetap terjaga. [R1 Q12; R2 Q12; R3 Q12]'),
('M3 Pencatatan belum menjadi satu-satunya dasar kepastian penerimaan. R2 dan R3 memahami perbedaannya; R1 masih mempertanyakan cakupan Lunas. [S5 R1-R3 Q7; S7 M3]','G1 Memahami informasi yang sudah dipastikan. Ari perlu membedakan catatan pembayaran dan hasil pemeriksaan penerimaan.','Status yang akurat dan dasar kepastian yang jelas. [S5 R1-R3 Q3, Q12]'),
('M4 Keputusan bergantung pada konfirmasi berwenang. Bukan keluhan terpisah, melainkan kebutuhan keputusan dari Q3 dan Q8. [S3 hubungan peran; S5 R2 Q3, Q8]','G3 Menentukan kapan pesanan dapat diteruskan. Ari perlu hasil pemeriksaan untuk pesanan yang sama sesuai tanggung jawabnya.','Dapat melanjutkan pesanan dengan yakin setelah hasil pemeriksaan sesuai. [R2 Q3, Q8, Q10]')
],[5.5,5.5,5.0])
h('Pengalaman baik yang menjadi kebutuhan pemeliharaan',2)
p('G4 adalah mempertahankan kelancaran pencatatan. R2 menilai input pesanan dan nota sudah membantu. Karena itu, hubungan dengan pemeriksaan perlu menjaga konteks data yang telah benar dan menghindari tambahan pengisian yang tidak diperlukan. Bagian ini menjadi dasar UX06, bukan klaim bahwa pengisian ulang sudah menjadi keluhan. [S5 R2 Q6, Q9, Q12; S7 bagian 6]')
p('R1-R3 mengusulkan integrasi bank; R2 juga menyebut validasi otomatis, QRIS dinamis, dan payment gateway. Harapan teknologi ini tidak dijadikan kebutuhan wajib. Kebutuhan UX berfokus pada kepastian dan kemudahan memperoleh hasil; pilihan integrasi masih perlu dinilai. [S5 Q12-Q13]',False,11)

# Bagian A pada template workbook
landscape()
for start in (0,3):
    h('3 Bagian A Pemetaan Insight Need dan Requirement' if start==0 else 'Pemetaan Insight Need dan Requirement lanjutan',page=start>0)
    p('Empat kolom mengikuti template Pertemuan 08. Insight bersumber dari riset; User Need menyatakan kebutuhan pengguna; FR01-FR06 adalah usulan fungsi; UX01-UX06 menetapkan hasil pengalaman yang dapat diperiksa. Rumusan lengkap dan kriterianya tersedia pada bagian 5.',False,11)
    table(['Research Insight','User Need','Functional Requirement','UX Requirement'],MAPPING[start:start+3],[6.2,6.3,7.1,7.1],size=11.5)
    p('Functional Requirement menjelaskan perilaku sistem yang diusulkan, sedangkan UX Requirement menjelaskan apa yang harus dapat dipahami atau dilakukan pengguna. Fungsi belum diimplementasikan atau diuji. Pemetaan tidak mewajibkan integrasi bank maupun memberi Ari akses rekening langsung.',False,11)

# Bagian B pada template workbook
portrait()
h('4 Bagian B User Stories')
p('Enam User Stories berikut menggunakan format As a [user], I want to [action], so that [benefit]. Seluruhnya mengikuti peran Ari sebagai admin yang menjalankan tugas kasir. Kode FR dan UX merujuk pemetaan bagian A; V1-V5 adalah kasus uji pada bagian 8.',False,11)
for sid,story,links in STORIES:
    h(sid,2)
    p(story,False,11.5)
    field('Keterkaitan',links,10.5)
p('Kriteria penerimaan setiap cerita mengikuti kriteria keterpenuhan UX yang bersesuaian pada bagian 5. Cerita menggambarkan kebutuhan rancangan, bukan bukti bahwa fitur tersebut sudah ada pada Fleffy.',False,11)

# Halaman 3 sampai 5
for start,heading in [(0,'5 Daftar kebutuhan UX'),(2,'Daftar kebutuhan UX lanjutan'),(4,'Daftar kebutuhan UX lanjutan')]:
    h(heading,page=True)
    if start==0:
        p('Rumusan berfokus pada hasil yang perlu dipahami atau dilakukan pengguna. Kriteria keterpenuhan adalah sasaran uji rancangan berikutnya, belum merupakan hasil pengujian. Must berarti wajib untuk skenario inti; Should berarti penting setelah kebutuhan inti.',False,11)
    for r in REQS[start:start+2]:
        h(r['id']+' '+r['title'],2)
        field('Prioritas',r['priority']+' | Urutan '+str(r['rank'])+' | Tujuan '+r['goal']+' | Journey '+r['stage'],11)
        p(r['need'])
        field('Dasar riset',r['basis'],11)
        field('Kriteria keterpenuhan','1. '+r['criteria'][0]+'\n2. '+r['criteria'][1],11)
        field('Alasan prioritas',r['rationale'],11)
        field('Batas penerapan',r['scope'],11)

# Halaman 6
h('6 Prioritas kebutuhan dan alasan penetapannya',page=True)
p('Saya menggunakan kategori Must dan Should. Must diperlukan agar skenario utama menghasilkan pemahaman, kecocokan informasi, koordinasi, dan keputusan yang tepat. Should meningkatkan penanganan kondisi penantian atau menjaga kelancaran yang sudah baik. Tidak ada kategori Could yang diisi hanya untuk menambah daftar.')
p('Urutan ditetapkan dari dampak terhadap tujuan pengguna, konsekuensi bila kebutuhan tidak terpenuhi, ketergantungan antarkebutuhan, serta kekuatan bukti. Penilaian ini bersifat kualitatif. Frekuensi hambatan, biaya implementasi, dan durasi tunggu belum diukur, sehingga tidak digunakan sebagai skor prioritas.')
table(['Urutan dan kategori','Kebutuhan','Alasan dan ketergantungan'],[
('1 Must','UX05 Dasar keputusan','Langsung memenuhi G3. Tanpa dasar yang sesuai, pesanan dapat ditindaklanjuti tanpa kepastian yang dibutuhkan. Memakai informasi UX01-UX03.'),
('2 Must','UX03 Koordinasi pemeriksaan','Menangani M1, hambatan yang paling menonjol pada pola Ari. Memerlukan pesanan yang jelas dari UX02; mendukung keputusan UX05.'),
('3 Must','UX02 Kecocokan informasi','Memastikan permintaan dan hasil pemeriksaan merujuk pesanan yang benar. Menjadi prasyarat isi bagi UX03 dan UX05.'),
('4 Must','UX01 Makna informasi','Membedakan pencatatan dan hasil pemeriksaan. Memperkuat pemahaman sebelum keputusan; tidak menyatakan R2 terbukti salah memahami status.'),
('5 Should','UX04 Tindak lanjut penantian','Mendukung pelayanan saat hasil belum tersedia. Bergantung pada UX03 serta prosedur tindak lanjut yang perlu disepakati usaha.'),
('6 Should','UX06 Kelancaran pencatatan','Menjaga bagian yang sudah dinilai baik. Larangan pengisian ulang adalah sasaran perbaikan yang perlu diuji, dengan bukti keluhan lebih terbatas.')
],[2.7,4.2,9.1])
h('7 Kebutuhan terpenting dan fokus pengembangan',2)
p('UX05 menjadi hasil utama yang harus dicapai. Empat kebutuhan Must dikembangkan dan diuji sebagai satu alur inti: informasi pesanan cocok melalui UX02, maknanya dipahami melalui UX01, pemeriksaan ditelusuri melalui UX03, lalu keputusan ditentukan melalui UX05. Urutan kepentingan pada tabel bukan urutan pengerjaan teknis.')
p('UX03 menjadi fokus perbaikan pengalaman pada titik menunggu karena R2 secara langsung melaporkan dampaknya. Kejelasan koordinasi tidak sendirinya mempersingkat pemeriksaan bank; kecepatan aktual tetap perlu diukur. UX04 dan UX06 ditambahkan setelah alur inti terbukti dapat dipahami dan keputusan tidak keliru.')

# Halaman 7
h('8 Rencana pemeriksaan keterpenuhan kebutuhan',page=True)
p('Pengujian yang direncanakan menggunakan prototipe dan data pesanan fiktif. Peserta utama adalah admin atau kasir dengan pembagian tugas seperti Ari. Sebelum uji, pemilik usaha perlu memastikan siapa pemeriksa berwenang dan prosedur tindak lanjut yang berlaku. Pemeriksaan rekening nyata tidak diperlukan.')
table(['Kasus uji yang diusulkan','Kebutuhan','Bukti keterpenuhan yang dicatat'],[
('V1 Catatan pembayaran sudah ada, hasil pemeriksaan belum tersedia.','UX01, UX03','Peserta menjelaskan perbedaan pencatatan dan kepastian dana, serta menunjuk pemeriksa dan keadaan permintaan dengan benar.'),
('V2 Dua pesanan bernominal sama dengan bukti dan konteks pembanding berbeda.','UX02','Peserta menghubungkan pesanan dengan bukti dan hasil yang tepat, serta mengenali ketidakcocokan yang disiapkan dalam uji.'),
('V3 Hasil pemeriksaan sesuai dari pihak berwenang.','UX05','Peserta menentukan tindak lanjut dan menunjuk hasil pemeriksaan untuk pesanan yang sama sebagai alasannya.'),
('V4 Hasil belum tersedia, hasil tidak cocok, atau rujukan pesanan belum jelas.','UX04, UX05','Peserta menahan tindak lanjut, memilih langkah sesuai prosedur, dan tidak memberi kepastian dana atau waktu yang belum diketahui.'),
('V5 Pencatatan dilanjutkan menjadi permintaan pemeriksaan.','UX06','Peserta menggunakan identitas pesanan serta nominal yang sudah benar tanpa mengetik ulang keduanya; rincian awal tetap sesuai.')
],[6.4,2.3,7.3])
h('Cara menilai',2)
p('Setiap kriteria pada bagian 5 diberi catatan terpenuhi atau belum terpenuhi, disertai tindakan, penjelasan peserta, serta bantuan yang diperlukan. Kriteria dianggap terpenuhi pada satu sesi bila peserta menyelesaikannya dengan benar tanpa arahan moderator. Semua kriteria Must harus terpenuhi untuk menerima alur inti pada sesi tersebut; hasil antarpeserta tetap dilaporkan terpisah.')
p('Keputusan meneruskan pesanan ketika belum ada hasil yang sesuai dicatat sebagai kesalahan kritis pada uji UX05 dan menjadi alasan revisi. Targetnya tidak ada keputusan kritis yang keliru pada skenario uji yang disiapkan. Ini adalah target rancangan, bukan bukti bahwa risiko pembayaran telah hilang di penggunaan nyata.')
p('Durasi tugas, perpindahan sumber, serta kebutuhan bantuan dapat dicatat sebagai baseline pengujian berikutnya. Target menit, jumlah klik, persentase keberhasilan populasi, atau janji penghematan waktu belum ditetapkan karena data pembanding belum tersedia.',False,11)
h('Keterbatasan yang memengaruhi pemeriksaan',2)
p('Persona Ari terutama bertumpu pada R2. Cabang ketidaksesuaian dan prosedur eskalasi masih memerlukan pendalaman, sehingga V2 dan V4 merupakan skenario rancangan yang diusulkan. Hasil uji harus diperiksa kembali pada pengguna dengan tugas serupa sebelum kebutuhan diperluas ke seluruh pengguna Fleffy.',False,11)

# Halaman 8
h('9 Penelusuran kebutuhan ke sumber dan tujuan',page=True)
table(['ID UX','Masalah dan tujuan','Persona dan Journey','Bukti wawancara pada S5'],[
(r['id'],('M2' if r['id']=='UX06' else r['problem'])+'; '+r['goal'], 'S6 '+r['u']+'; S7 '+('T6; sebelum hasil' if r['id']=='UX05' else r['stage']),src)
for r,src in zip(REQS,[
'R1-R3 Q7; R2 Q3, Q12',
'R2 Q4-Q8; R1 dan R3 Q4-Q8',
'R2 Q1, Q8-Q11',
'R2 Q9-Q11',
'R2 Q3, Q8; R3 Q8',
'R2 Q6, Q9, Q12'
])],[2.0,3.2,4.1,6.7])
p('Worksheet 3 mendukung UX03 dan UX05 melalui batas tugas Kasir, Admin, Owner, dan Teknisi. Wawancara memperjelas pembagian pemeriksaan: R2 meminta owner atau finance, sedangkan R1 dan R3 dapat memeriksa sendiri. Perbedaan akses ini tetap dipertahankan.',False,11)
h('10 Sumber dan batas kesimpulan',2)
p('S3. Worksheet 3 User and Stakeholder, revisi 28 September 2026.\nS5. Worksheet 5 User Interview, 15 Oktober 2026; R1-R3 dan Q1-Q13.\nS6. Worksheet 6 Empathy Map dan Persona, 15 Oktober 2026; Ari dan U1-U4.\nS7. Worksheet 7 User Journey, 15 Oktober 2026; T1-T6, M1-M3, dan P1-P6.\nPenulis S3-S7: Rusdany Maestro.\nAcuan utama. UX Design Hands-on Workbook, Pertemuan 08 From Insight to Requirement, bagian 2 dan 5, tabel A serta User Stories B.\nAcuan penilaian. Instruksi Worksheet 8 UX Requirements, Rekayasa Interaksi.',False,11)
p('Jawaban wawancara merupakan parafrasa. Pesenkopi adalah tempat wawancara. Kebutuhan dan prioritas adalah sintesis peneliti; belum tersedia hasil uji prototipe, pengukuran rata-rata penantian, atau bukti kejadian penipuan. [S5; S6; S7]',False,10.5)
h('Kelengkapan hasil',2)
p('Ringkasan masalah, tujuan, kebutuhan, dan harapan tersedia pada bagian 1-2. Tabel A memisahkan insight, kebutuhan pengguna, fungsi, dan kriteria UX. Bagian B memuat enam User Stories. Bagian 5 memberi kriteria keterpenuhan, bagian 6-7 menjelaskan prioritas, dan bagian 9 menelusuri hubungan ke riset serta tujuan.',False,11)

for tree in (doc.element,doc.styles.element,sec.footer._element):
    for fonts in tree.iter(qn('w:rFonts')):
        fonts.attrib.clear()
        for attr in ('ascii','hAnsi','eastAsia','cs'):fonts.set(qn('w:'+attr),'Times New Roman')
    for border in list(tree.iter(qn('w:pBdr'))):border.getparent().remove(border)
    for rp in tree.iter(qn('w:rPr')):
        tracking=rp.find(qn('w:spacing'))
        if tracking is not None:rp.remove(tracking)
    for color in tree.iter(qn('w:color')):
        color.attrib.clear();color.set(qn('w:val'),'000000')
out=TMP/(STEM+'_sebelum_sanitasi.docx')
doc.save(out)
(TMP/'requirements_data.json').write_text(json.dumps(REQS,ensure_ascii=False,indent=2),encoding='utf-8')
(TMP/'mapping_and_stories.json').write_text(json.dumps({'mapping':MAPPING,'stories':STORIES},ensure_ascii=False,indent=2),encoding='utf-8')
content=[]
for x in doc.element.body:
    if x.tag==qn('w:p'):
        from docx.text.paragraph import Paragraph
        content.append(Paragraph(x,doc).text)
    elif x.tag==qn('w:tbl'):
        from docx.table import Table
        for row in Table(x,doc).rows:content.append(' | '.join(c.text for c in row.cells))
(TMP/'report_content.txt').write_text('\n\n'.join(content),encoding='utf-8')
print(str(out))
