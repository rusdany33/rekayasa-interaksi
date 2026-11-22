from pathlib import Path
import json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(r'D:\Rekayasa Interaksi')
TMP = ROOT / 'tmp' / 'worksheet6'
TMP.mkdir(parents=True, exist_ok=True)
STEM = '202210370311406_Rusdany_Maestro_Worksheet6_EmpathyMapPersona'
OUT = ROOT / (STEM + '.docx')
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Cm(2.5)
sec.footer_distance = Cm(1.2)
for style in doc.styles:
    if style.type in (1, 2):
        style.font.name = 'Times New Roman'
        style.font.color.rgb = RGBColor(0, 0, 0)
for name, size in [('Normal', 12), ('Title', 17), ('Subtitle', 12), ('Heading 1', 14), ('Heading 2', 12), ('Footer', 11)]:
    s = doc.styles[name]
    s.font.size = Pt(size)
    s.paragraph_format.space_after = Pt(5)
    s.paragraph_format.line_spacing = 1.15
    s.paragraph_format.widow_control = True
doc.styles['Normal'].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
for name in ('Title', 'Subtitle'):
    doc.styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.styles[name].paragraph_format.space_after = Pt(10)
doc.styles['Title'].font.bold = True
doc.styles['Subtitle'].font.italic = False
for name in ('Heading 1', 'Heading 2'):
    s = doc.styles[name]
    s.font.bold = True
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    s.paragraph_format.keep_with_next = True
    s.paragraph_format.space_before = Pt(6)
doc.styles['Heading 2'].paragraph_format.line_spacing = 1.0
doc.styles['Heading 2'].paragraph_format.space_after = Pt(4)
footer = sec.footer.paragraphs[0]
footer.style = doc.styles['Footer']
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld = OxmlElement('w:fldSimple')
fld.set(qn('w:instr'), 'PAGE')
footer._p.append(fld)
doc.core_properties.author = 'Rusdany Maestro'
doc.core_properties.title = 'Worksheet 6 Empathy Map dan Persona Pengguna Fleffy'
doc.core_properties.subject = 'Rekayasa Interaksi'

def p(text, indent=True, size=None):
    para = doc.add_paragraph(text)
    if indent:
        para.paragraph_format.first_line_indent = Cm(.75)
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if size:
        for run in para.runs:
            run.font.size = Pt(size)
    return para

def h(text, level=1, new_page=False):
    para = doc.add_paragraph(text, f'Heading {level}')
    if new_page:
        para.paragraph_format.page_break_before = True
    return para

def field(label, text, size=11.5):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para.paragraph_format.line_spacing = 1.1
    para.paragraph_format.space_after = Pt(5)
    para.add_run(label + ': ').bold = True
    para.add_run(text)
    for run in para.runs:
        run.font.size = Pt(size)
    return para

def cell_format(cell, header=False, top=False, padding=85):
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP if top else WD_CELL_VERTICAL_ALIGNMENT.CENTER
    cp = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'bottom', 'left', 'right'):
        b = OxmlElement('w:' + edge)
        for attr, val in [('val', 'single'), ('sz', '4'), ('color', 'D9D9D9')]:
            b.set(qn('w:' + attr), val)
        borders.append(b)
    cp.append(borders)
    mar = OxmlElement('w:tcMar')
    for edge, val in [('top', padding), ('bottom', padding), ('left', 110), ('right', 110)]:
        el = OxmlElement('w:' + edge)
        el.set(qn('w:w'), str(val))
        el.set(qn('w:type'), 'dxa')
        mar.append(el)
    cp.append(mar)
    shade = OxmlElement('w:shd')
    shade.set(qn('w:fill'), 'F2F2F2' if header else 'FFFFFF')
    cp.append(shade)

def table(headers, rows, widths, size=11):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for col, width in zip(t.columns, widths):
        col.width = Cm(width)
    for cell, text in zip(t.rows[0].cells, headers):
        cell.text = text
    for row in rows:
        for cell, text in zip(t.add_row().cells, row):
            cell.text = text
    for ri, row in enumerate(t.rows):
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        if ri == 0:
            row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
        for ci, cell in enumerate(row.cells):
            cell.width = Cm(widths[ci])
            cell_format(cell, ri == 0)
            for para in cell.paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER if ri == 0 else WD_ALIGN_PARAGRAPH.LEFT
                para.paragraph_format.first_line_indent = Cm(0)
                para.paragraph_format.line_spacing = 1.05
                para.paragraph_format.space_after = Pt(2)
                for run in para.runs:
                    run.font.size = Pt(size)
                    run.bold = ri == 0
    spacer = doc.add_paragraph()
    spacer.paragraph_format.line_spacing = Pt(2)
    spacer.paragraph_format.space_after = Pt(4)
    return t

# Halaman 1
doc.add_paragraph('Empathy Map dan Persona Pengguna Fleffy', 'Title')
doc.add_paragraph('Worksheet 6 Rekayasa Interaksi', 'Subtitle')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nMata kuliah: Rekayasa Interaksi\nJenis tugas: Individu\nTanggal penyusunan: 15 Oktober 2026', indent=False)
h('1 Produk dan tujuan kajian')
p('Fleffy - Kasir Laundry Sepatu digunakan untuk mencatat pesanan, layanan, dan pembayaran. Kajian ini berfokus pada pengalaman memastikan penerimaan Bank Transfer setelah pembayaran tercatat di aplikasi. Empathy Map dan Persona disusun untuk memahami dasar keputusan operator sebelum menindaklanjuti pesanan. [S1; S2 Q3-Q8]')
h('2 Kelompok pengguna yang dipilih')
p('Saya memilih admin atau kasir laundry sepatu yang mencatat pembayaran melalui Fleffy, tetapi mengandalkan owner atau finance untuk memeriksa rekening. Kelompok ini dikenali dari pembagian tugas pemeriksaan, bukan hanya jabatan. R2 menjadi sumber utama karena menjalankan pola kerja tersebut secara langsung. [E1, E4]')
p('R1 dan R3 tetap digunakan sebagai pembanding. Keduanya dapat memeriksa rekening sendiri, sehingga kewenangan tersebut tidak dimasukkan ke Persona admin yang menunggu konfirmasi. Persona yang disusun merupakan gambaran awal dari pola R2 dan belum mewakili seluruh pengguna Fleffy. [S3, bagian 8]')
h('Ringkasan kebutuhan pengguna', 2)
p('Admin membutuhkan kecocokan antara catatan pesanan dan hasil pemeriksaan penerimaan dana. Hambatan yang dilaporkan mencakup perpindahan sumber informasi serta penantian respons pemeriksa rekening. Perbaikan UX perlu membantu operator mengetahui hasil pemeriksaan dan tindak lanjut yang sesuai kewenangannya, sambil menjaga ketelitian pembayaran. [E3-E8]')

# Halaman 2
h('3 Sumber data dan penyusunan', new_page=True)
table(['Sumber', 'Cakupan data', 'Penggunaan dalam analisis'], [
    ('S1 Worksheet 1', 'Dokumentasi layar dan catatan pengguna, 19 September 2026; satu alur transaksi contoh.', 'Konteks pencatatan Bank Transfer dan batas makna bukti layar.'),
    ('S2 Catatan R2', 'Wawancara langsung, 15 Oktober 2026 di Pesenkopi; 12 menit; 13 jawaban dan pendalaman.', 'Sumber utama pekerjaan, perilaku, perasaan, tujuan, hambatan, dan harapan.'),
    ('S3 Worksheet 5', 'Tiga pengguna: R1 kasir, R2 admin operasional, dan R3 owner.', 'Ringkasan serta pembandingan akses dan tanggung jawab pemeriksaan.'),
    ('C1 Klarifikasi', 'Rentang usia R2 20-22 tahun; semua jawaban merupakan parafrasa.', 'Mengisi usia dan menetapkan batas penggunaan kutipan.')
], [3.0, 6.5, 6.5])
h('Dasar observasi', 2)
p('Pada S1, bukti B2 memperlihatkan status Lunas dan Bank Transfer Rp57.000. Bukti ini menunjukkan catatan pada layar, tanpa memperlihatkan mutasi bank. Nominal tersebut adalah transaksi contoh pada observasi, berbeda dari contoh Rp150.000 yang diceritakan R2. [O1; E4]')
h('Batas kelompok pengguna', 2)
table(['Responden', 'Cara memperoleh kepastian', 'Kedudukan terhadap Persona'], [
    ('R1 Kasir', 'Memeriksa sendiri; dapat meminta bantuan.', 'Pembanding; bukan dasar ketergantungan pemeriksaan.'),
    ('R2 Admin', 'Meminta owner atau finance memeriksa rekening.', 'Anggota kelompok yang menjadi dasar Persona.'),
    ('R3 Owner', 'Memeriksa rekening sendiri.', 'Pembanding yang memiliki akses berbeda.')
], [2.6, 6.8, 6.6])
p('Saya mengelompokkan jawaban R2 ke enam bagian Empathy Map, lalu menurunkan karakteristik Persona dari pola tersebut. Kode E1-E8 menelusuri jawaban asal; O1 merujuk observasi dan C1 klarifikasi. Pernyataan pengguna, interpretasi, dan kebutuhan UX dibedakan. Rincian kode tersedia pada bagian 8.')
p('Pesenkopi adalah tempat wawancara, bukan nama usaha laundry. Penggunaan kode responden mengikuti persetujuan pada Worksheet 5; nama usaha, kontak, dan informasi rekening pribadi tidak dicantumkan.', size=11)

# Halaman 3
map_section=doc.add_section(WD_SECTION_START.NEW_PAGE)
map_section.orientation=WD_ORIENT.LANDSCAPE
map_section.page_width,map_section.page_height=Cm(29.7),Cm(21)
map_section.top_margin=map_section.bottom_margin=map_section.left_margin=map_section.right_margin=Cm(1.5)
map_section.footer_distance=Cm(.7)
h('4 Empathy Map')
map_intro=p('Kelompok yang dipetakan adalah admin/kasir pencatat pembayaran yang meminta konfirmasi owner atau finance. Isi berasal dari pola R2. Pernyataan dan tindakan merupakan laporan responden; bagian Thinks merupakan interpretasi peneliti.', indent=False, size=11)
map_intro.paragraph_format.line_spacing=1.05
map_intro.paragraph_format.space_after=Pt(4)
map_cells = [
    ('Says', 'Pernyataan pengguna dalam parafrasa', [
        'R2 menilai input pesanan dan penerbitan nota membantu pekerjaan. [E6]',
        'Status pada layar dipahami sebagai pencatatan, sementara dana tetap perlu diperiksa. [E5]',
        'R2 mengharapkan validasi pembayaran yang lebih praktis. [E8]'
    ]),
    ('Thinks', 'Pemikiran hasil interpretasi', [
        'Catatan pembayaran perlu cocok dengan informasi dana yang diterima. [E3, E5]',
        'Tindak lanjut membutuhkan hasil pemeriksaan pihak yang memegang akses rekening. [E1, E4]',
        'Penantian perlu ditangani tanpa mengurangi ketelitian keputusan. [E6, E7]'
    ]),
    ('Does', 'Tindakan dan kebiasaan yang dilaporkan', [
        'Mencatat pelanggan, layanan, nominal, dan pembayaran di Fleffy. [E1, E4]',
        'Mencocokkan bukti, lalu mengirim permintaan cek mutasi melalui WhatsApp. [E4]',
        'Menunggu konfirmasi dan dapat menelepon owner ketika respons lambat. [E1, E6]'
    ]),
    ('Feels', 'Perasaan yang dilaporkan', [
        'Tenang dan siap melayani sebelum proses pemeriksaan. [E7]',
        'Cemas saat menunggu kepastian dan sungkan ketika pelanggan menunggu. [E7]',
        'Lega setelah menerima konfirmasi mutasi dari owner. [E7]'
    ]),
    ('Pain', 'Hambatan dan kekhawatiran', [
        'Informasi harus dihubungkan antara Fleffy dan percakapan WhatsApp. [E4]',
        'Respons pemeriksa dapat terlambat; layanan atau pengerjaan ikut tertunda. [E6]',
        'Ada kekhawatiran terhadap bukti transfer yang tidak sah; kejadian penipuan tidak terbukti. [E3, E7]'
    ]),
    ('Gain', 'Hasil dan manfaat yang diinginkan', [
        'Mendapatkan kepastian bahwa catatan sesuai penerimaan dana. [E3, E8]',
        'Memperoleh hasil pemeriksaan lebih mudah tanpa komunikasi berulang. [E8]',
        'Melayani pelanggan lebih lancar sambil menjaga ketelitian pembayaran. [E6, E8]'
    ])
]
map_image=ROOT/'202210370311406_Rusdany_Maestro_Worksheet6_EmpathyMap.png'
assert map_image.exists(),'Buat gambar Empathy Map terlebih dahulu.'
map_para=doc.add_paragraph()
map_para.alignment=WD_ALIGN_PARAGRAPH.CENTER
map_para.paragraph_format.line_spacing=1.0
map_para.paragraph_format.space_after=Pt(0)
picture=map_para.add_run().add_picture(str(map_image),width=Cm(26.7))
picture._inline.docPr.set('name','Empathy Map Ari enam area')
picture._inline.docPr.set('descr','Empathy Map dengan ilustrasi persona Ari di tengah. '+' '.join(domain+' '+subtitle+' '+' '.join(items) for domain,subtitle,items in map_cells))
map_note=p('Says tidak memakai kutipan langsung karena catatan yang tersedia berupa parafrasa. Thinks tidak diperlakukan sebagai ucapan atau isi pikiran yang diamati. Does bersumber dari cerita aktivitas R2; observasi S1 mendukung konteks layar pembayaran, tanpa membuktikan semua tindakan R2.', indent=False, size=10.5)
map_note.paragraph_format.space_before=Pt(4)
map_note.paragraph_format.space_after=Pt(0)
map_note.paragraph_format.line_spacing=1.05

# Halaman 4
body_section=doc.add_section(WD_SECTION_START.NEW_PAGE)
body_section.orientation=WD_ORIENT.PORTRAIT
body_section.page_width,body_section.page_height=Cm(21),Cm(29.7)
body_section.top_margin=body_section.bottom_margin=body_section.left_margin=body_section.right_margin=Cm(2.5)
body_section.footer_distance=Cm(1.2)
h('5 User Persona')
p('Persona eksploratif berdasarkan pola kerja R2 pada Empathy Map. Nama digunakan sebagai samaran representasi, tanpa menyatakan identitas responden.', indent=False, size=11)
persona = [
    ('Nama Persona', 'Ari, nama samaran untuk representasi admin/kasir.'),
    ('Representasi singkat', 'Operator pencatat pembayaran yang menunggu hasil pemeriksaan rekening dari owner atau finance. [E1]'),
    ('Latar belakang', 'Menangani layanan awal usaha laundry sepatu: menerima pesanan, mencatat layanan, menerbitkan nota, dan berkoordinasi dengan pemeriksa pembayaran serta teknisi. [E1]'),
    ('Usia atau rentang usia', '20-22 tahun, berdasarkan klarifikasi lanjutan. Rentang usia tidak digunakan untuk menyimpulkan kemampuan atau perilaku. [C1]'),
    ('Pekerjaan atau status', 'Admin Operasional yang juga menjalankan tugas kasir. [E1]'),
    ('Tujuan pengguna', 'Mencatat pembayaran sesuai dana yang diterima dan menentukan kapan pesanan dapat ditindaklanjuti dengan yakin. [E3, E4]'),
    ('Kebutuhan pengguna', 'Kecocokan data pesanan, bukti transfer, dan hasil pemeriksaan; informasi yang jelas dari pihak berwenang. [E1, E4, E8]'),
    ('Motivasi pengguna', 'Mengurangi risiko salah menentukan pembayaran dan menghindari penantian pelanggan yang tidak perlu. [E3, E6-E8]'),
    ('Masalah utama', 'Informasi tersebar dan konfirmasi bergantung pada respons owner/finance. Penantian dapat menghambat layanan serta pengerjaan dalam pengalaman R2. [E4, E6]'),
    ('Perilaku dan kebiasaan', 'Memakai Fleffy setiap hari kerja, memeriksa rincian bukti di WhatsApp, meneruskan permintaan cek, lalu menindaklanjuti hasilnya. Dapat menelepon saat respons lambat. [E2, E4, E6]'),
    ('Konteks penggunaan', 'Penerimaan pesanan dan pembayaran, pelunasan saat pengambilan, serta rekap harian. Pelanggan dapat menunggu ketika konfirmasi belum diperoleh. [E2, E6]'),
    ('Kemampuan menggunakan teknologi', 'Terbiasa menjalankan tugas operasional melalui Fleffy dan WhatsApp; melaporkan penggunaan tablet Android, smartphone, serta sesekali browser laptop. Tingkat kemahiran belum diuji. [E2]'),
    ('Kutipan pengguna', 'Catatan verbatim tidak tersedia. Parafrasa pernyataan R2: ia merasa lega setelah menerima konfirmasi mutasi dari owner. [E7; C1]'),
    ('Kebutuhan UX utama', 'Kejelasan makna status, kecocokan pesanan dengan hasil pemeriksaan, dan koordinasi tindak lanjut sesuai kewenangan. U1-U4 menjabarkan hasil yang dibutuhkan. [E1, E3-E8]')
]
for label, text in persona:
    field(label, text)

# Halaman 5
h('6 Hubungan Empathy Map dan Persona', new_page=True)
p('Setiap bagian Persona berasal dari pola pada Empathy Map. Tabel berikut memperlihatkan perubahan dari data pengguna menjadi karakteristik Persona dan kebutuhan UX; arah perancangan merupakan hasil analisis, bukan fitur yang telah terbukti berhasil.')
links = [
    ('Says', 'Pencatatan membantu, tetapi status belum menjadi satu-satunya dasar kepastian. [E5, E6, E8]', 'Tujuan dan kebutuhan Ari menekankan pencatatan yang dapat dihubungkan dengan penerimaan dana. U1.'),
    ('Thinks', 'Keputusan memerlukan hasil pemeriksa rekening dan ketelitian. [E1, E3-E7]', 'Motivasi Ari adalah mengurangi risiko salah menentukan pembayaran sebelum menindaklanjuti pesanan. U1 dan U4.'),
    ('Does', 'Mencatat, mencocokkan bukti, mengirim permintaan cek, dan menunggu balasan. [E1, E4, E6]', 'Perilaku Ari melibatkan Fleffy dan WhatsApp, tanpa akses bank langsung. U2 dan U3.'),
    ('Feels', 'Cemas dan sungkan saat menunggu, lalu lega setelah konfirmasi. [E7]', 'Kebutuhan Ari mencakup kejelasan perkembangan pemeriksaan dan tindak lanjut. U3 dan U4.'),
    ('Pain', 'Informasi tersebar dan respons pemeriksa dapat lambat. [E4, E6]', 'Masalah utama Ari adalah pencocokan serta ketergantungan koordinasi. U2 dan U3.'),
    ('Gain', 'Ingin kepastian pembayaran yang mudah diperoleh dan layanan lebih lancar. [E3, E8]', 'Tujuan Ari menggabungkan kelancaran pelayanan dengan ketelitian keputusan. U1-U4.')
]
table(['Bagian Map', 'Pola yang menjadi dasar', 'Turunan pada Persona dan UX'], links, [2.2, 6.6, 7.2])
h('Konsistensi kelompok pengguna', 2)
p('Ari tetap berperan sebagai pencatat yang meminta pemeriksaan rekening. Kemampuan R3 sebagai owner untuk memeriksa dana sendiri tidak dipindahkan ke Ari. Dengan batas ini, masalah menunggu konfirmasi tetap sesuai dengan pengalaman anggota kelompok yang menjadi dasar Persona. [S3, bagian 8]')
p('Says dan Does membantu menjelaskan pola kerja; Feels menunjukkan perubahan emosi pada momen pemeriksaan; Pain dan Gain menuntun kebutuhan perancangan. Thinks menyatukan alasan tindakan sebagai interpretasi yang masih perlu dikonfirmasi kepada pengguna.')

# Halaman 6
h('7 Masalah motivasi dan kebutuhan UX utama', new_page=True)
p('Masalah utama Ari adalah memperoleh kepastian penerimaan dana melalui alur pemeriksaan yang melibatkan pihak lain. Motivasi untuk menghindari salah menentukan pembayaran membuat pemeriksaan tetap penting, sementara penantian pelanggan mendorong kebutuhan koordinasi yang lebih jelas. [E1, E3, E6-E8]')
ux = [
    ('U1 Kejelasan status pembayaran', 'Operator perlu memahami informasi yang sudah dicatat dan kepastian yang masih menunggu pemeriksaan. Dasar: Says dan Thinks; E3, E5, E8.', 'Pada uji rancangan berikutnya, operator dapat menjelaskan apakah status menunjukkan pencatatan atau hasil pemeriksaan penerimaan dana.'),
    ('U2 Kecocokan informasi pesanan', 'Operator perlu menghubungkan nominal, pesanan, bukti pelanggan, dan hasil pemeriksaan yang sesuai. Dasar: Does dan Pain; E1, E4.', 'Operator dapat menunjuk pesanan serta informasi pembayaran yang menjadi dasar konfirmasi, tanpa mengandalkan ingatan semata.'),
    ('U3 Kejelasan koordinasi pemeriksaan', 'Operator perlu mengetahui pihak pemeriksa dan perkembangan permintaannya. Dasar: Does, Feels, dan Pain; E1, E6, E7.', 'Saat pemeriksaan belum selesai, operator dapat menjelaskan siapa yang memeriksa dan tindakan lanjutan yang perlu dilakukan.'),
    ('U4 Dasar tindak lanjut yang meyakinkan', 'Operator perlu mengetahui kapan hasil pemeriksaan cukup untuk melanjutkan pesanan sesuai tanggung jawabnya. Dasar: Thinks, Feels, dan Gain; E3, E4, E7, E8.', 'Operator dapat menentukan tindak lanjut berdasarkan hasil pemeriksaan, tanpa menganggap input pembayaran sebagai bukti dana sudah diterima.')
]
for title, need, criterion in ux:
    h(title, 2)
    p(need)
    p('Kriteria pemeriksaan rancangan: ' + criterion)
h('Kedudukan harapan teknologi', 2)
p('R2 mengusulkan validasi otomatis, integrasi rekening, QRIS dinamis, atau payment gateway. Usulan tersebut dicatat sebagai harapan pengguna. Kebutuhan UX pada U1-U4 berfokus pada hasil yang harus dipahami dan dilakukan operator; pilihan teknologi, kelayakan integrasi, serta manfaatnya belum diuji. [E8]')

# Halaman 7
h('8 Penelusuran informasi penting', new_page=True)
p('Kode berikut digunakan pada Empathy Map, Persona, dan hubungan keduanya. Satu jawaban dapat mendukung lebih dari satu bagian. Catatan wawancara dan ringkasan Worksheet 5 merupakan sumber dari sesi yang sama, sehingga tidak dihitung sebagai responden tambahan.', indent=False, size=11)
evidence = [
    ('O1', 'Layar menunjukkan Lunas dan Bank Transfer Rp57.000 pada transaksi contoh; tidak memperlihatkan mutasi rekening.', 'S1, halaman 2-3, bukti B2; fakta pada layar.'),
    ('E1', 'R2 mencatat pesanan dan pembayaran; owner atau finance memegang akses pemeriksaan rekening.', 'S2 Q1 dan Q8; laporan responden.'),
    ('E2', 'R2 memakai Fleffy setiap hari kerja; menggunakan tablet Android, smartphone, dan sesekali browser laptop.', 'S2 Q2; laporan kebiasaan dan perangkat.'),
    ('E3', 'R2 ingin catatan sesuai dana yang diterima, mengurangi risiko salah bayar, dan merasa yakin setelah pemeriksaan.', 'S2 Q3; tujuan dan alasan pengguna.'),
    ('E4', 'Contoh Rp150.000 untuk dua pasang deep cleaning: mencatat pesanan, melihat bukti, lalu meminta owner memeriksa sebelum pengerjaan.', 'S2 Q4-Q6 dan Q8; cerita pengalaman.'),
    ('E5', 'R2 memahami status sebagai pencatatan; kepastian penerimaan dana tetap perlu diperoleh melalui rekening.', 'S2 Q7; penafsiran pengguna.'),
    ('E6', 'Pencatatan dinilai lancar, sedangkan menunggu respons dapat memerlukan telepon dan menunda layanan atau pengerjaan.', 'S2 Q9 dan Q11; dampak yang dilaporkan.'),
    ('E7', 'R2 merasa tenang sebelum pemeriksaan, cemas dan sungkan saat menunggu, lalu lega setelah konfirmasi.', 'S2 Q10; perasaan yang dinyatakan.'),
    ('E8', 'R2 memerlukan kepastian pembayaran yang lebih mudah diperoleh dan mengusulkan validasi otomatis atau integrasi.', 'S2 Q12-Q13; kebutuhan serta harapan.'),
    ('C1', 'Usia R2 berada pada rentang 20-22 tahun; seluruh jawaban yang tersedia merupakan parafrasa.', 'Klarifikasi lanjutan, 15 Oktober 2026.')
]
table(['Kode', 'Informasi yang menjadi dasar', 'Sumber dan jenis bukti'], evidence, [1.6, 9.5, 4.9], size=11)
p('Data pada tabel adalah bukti asal. Penamaan Persona, pengelompokan Thinks, dan U1-U4 merupakan sintesis peneliti. Rujukan silang membantu memeriksa dasar sintesis tanpa mengubahnya menjadi pernyataan langsung responden.', indent=False, size=11)

# Halaman 8
h('9 Keterbatasan data dan asumsi', new_page=True)
h('Cakupan kelompok dan kedalaman data', 2)
p('Worksheet 5 memuat tiga responden, tetapi hanya R2 yang secara jelas menggambarkan ketergantungan pemeriksaan kepada owner atau finance. Persona ini bertumpu pada satu anggota kelompok tersebut. Sesi R2 berlangsung 12 menit; beberapa rincian frekuensi dan dampak belum didalami. Pola Persona perlu diperiksa pada admin/kasir lain dengan pembagian tugas serupa.')
h('Perbedaan bukti dan interpretasi', 2)
p('Observasi S1 berupa dokumentasi layar satu alur contoh, bukan pengamatan langsung seluruh perilaku R2. Waktu tunggu dan hambatan pada wawancara merupakan laporan pengalaman. Data tidak membuktikan prevalensi hambatan, kejadian penipuan, kerugian, maupun kemampuan teknis integrasi Fleffy. Thinks dan kebutuhan UX merupakan interpretasi yang dapat direvisi setelah pendalaman.')
h('Identitas dan kutipan', 2)
p('Ari adalah nama samaran representasi. Usia 20-22 tahun berasal dari klarifikasi; pendidikan, domisili, gender, penghasilan, dan sifat kepribadian tidak ditambahkan. Kemampuan teknologi dijelaskan dari tugas serta perangkat yang dilaporkan, tanpa pemberian skor kemahiran. Tidak ada kutipan verbatim karena semua jawaban yang tersedia telah diparafrasakan.')
h('10 Kesimpulan', 1)
p('Admin/kasir pada pola R2 membutuhkan kepastian pembayaran yang dapat dihubungkan dengan pesanan dan hasil pemeriksaan pihak yang berwenang. Hambatan utamanya adalah pencocokan informasi serta penantian konfirmasi. Motivasi untuk menghindari kesalahan tetap berjalan bersama kebutuhan melayani pelanggan dengan lancar.')
p('Empathy Map menjelaskan pernyataan, pemikiran hasil interpretasi, tindakan, perasaan, hambatan, dan manfaat yang diinginkan. Persona Ari merangkum pola itu menjadi profil operasional yang jelas. Dasar perancangan berikutnya adalah kejelasan makna status, kecocokan informasi, koordinasi pemeriksaan, dan dasar tindak lanjut. Pemilihan solusi dilakukan setelah kebutuhan tersebut diuji kembali pada kelompok pengguna yang sama.')
h('Sumber data', 2)
p('S1. Rusdany Maestro. Worksheet 1 UX Detective, dokumentasi 19 September 2026, terutama halaman 2-4 dan bukti B2.\nS2. Catatan wawancara R2 Admin Operasional, 15 Oktober 2026, Q1-Q13 beserta pendalaman.\nS3. Rusdany Maestro. Worksheet 5 User Interview, 15 Oktober 2026, terutama bagian 6 dan 8.\nC1. Klarifikasi lanjutan tentang rentang usia R2 dan status parafrasa, 15 Oktober 2026.\nAcuan tugas. Worksheet 6 Empathy Map dan Persona, mata kuliah Rekayasa Interaksi.', indent=False, size=11)

# Hapus tema font dan garis dekoratif bawaan Word.
for tree in (doc.element, doc.styles.element, sec.footer._element):
    for fonts in tree.iter(qn('w:rFonts')):
        fonts.attrib.clear()
        for attr in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
            fonts.set(qn('w:' + attr), 'Times New Roman')
    for border in list(tree.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
    for rp in tree.iter(qn('w:rPr')):
        tracking = rp.find(qn('w:spacing'))
        if tracking is not None:
            rp.remove(tracking)
    for color in tree.iter(qn('w:color')):
        color.attrib.clear()
        color.set(qn('w:val'), '000000')
doc.save(OUT)

# Simpan jejak kerja terpisah dari berkas yang dikumpulkan.
texts = []
for child in doc.element.body:
    texts.append(' '.join(child.itertext()))
plain = []
for para in doc.paragraphs:
    if para.text:
        plain.append(para.text)
for t in doc.tables:
    for row in t.rows:
        plain.append(' | '.join(c.text for c in row.cells))
(TMP / 'report_content.txt').write_text('\n\n'.join(plain), encoding='utf-8')
audit = {
    'persona': 'Ari', 'kelompok': 'Admin/kasir pencatat transfer yang meminta owner/finance memeriksa rekening',
    'dasar_utama': 'R2', 'responden_pembanding': ['R1', 'R3'], 'usia': '20-22 tahun',
    'status_kutipan': 'Semua parafrasa; tidak ada kutipan langsung',
    'empathy_map_visual': str(map_image),
    'bagian_empathy_map': [m[0] for m in map_cells], 'komponen_persona': [label for label, _ in persona],
    'rubrik': [
        {'aspek': 'Kesesuaian data observasi dan wawancara', 'bobot': 25, 'bagian': [2,3,4,5,8,9]},
        {'aspek': 'Kelengkapan Empathy Map', 'bobot': 20, 'bagian': [4]},
        {'aspek': 'Kelengkapan dan kejelasan Persona', 'bobot': 25, 'bagian': [2,5]},
        {'aspek': 'Kesesuaian kebutuhan motivasi dan masalah', 'bobot': 15, 'bagian': [4,5,7,10]},
        {'aspek': 'Keterhubungan Map dan Persona', 'bobot': 10, 'bagian': [6]},
        {'aspek': 'Kerapian dan kualitas penyajian', 'bobot': 5, 'cek': 'Render seluruh halaman sebelum pengumpulan'}
    ],
    'sumber': {
        'S1': str(ROOT/'202210370311406_Rusdany_Maestro_Worksheet1_UXDetective.pdf'),
        'S2': str(ROOT/'tmp'/'worksheet5'/'data'/'R2_Admin_dokumen_sumber.docx'),
        'S3': str(ROOT/'202210370311406_Rusdany_Maestro_Worksheet5_UserInterview.pdf'),
        'C1': 'Konfirmasi pengguna pada percakapan 15 Oktober 2026'
    },
    'batas_waktu': '24 Oktober 2026 pukul 11.59 siang', 'qa_visual': 'Menunggu render'
}
(TMP/'audit_kelengkapan.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(OUT)
print('Kata:', sum(len(s.split()) for s in plain))
print('Komponen Map:', len(map_cells), '| Komponen Persona:', len(persona))
