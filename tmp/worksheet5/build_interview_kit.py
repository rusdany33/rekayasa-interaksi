from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(r'D:\Rekayasa Interaksi')
STEM='202210370311406_Rusdany_Maestro_Worksheet5'
PDF=ROOT/(STEM+'_PanduanWawancara.pdf')
TXT=ROOT/(STEM+'_Catatan_R1_R2_R3.txt')
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold',r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold')
styles={
 'title':ParagraphStyle('title',fontName='ArialBold',fontSize=22,leading=26,spaceAfter=12),
 'h1':ParagraphStyle('h1',fontName='ArialBold',fontSize=16,leading=20,spaceAfter=12),
 'h2':ParagraphStyle('h2',fontName='ArialBold',fontSize=11.5,leading=15,spaceBefore=9,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=11,leading=14.7,spaceAfter=8),
 'q':ParagraphStyle('q',fontName='Arial',fontSize=11,leading=14.7,spaceAfter=11),
 'small':ParagraphStyle('small',fontName='Arial',fontSize=9.5,leading=12.5,spaceAfter=7),
}
story=[]
def p(text,kind='body'):
 story.append(Paragraph(escape(text).replace('\n','<br/>'),styles[kind]))
def h(text):p(text,'h2')
def page(title):story.append(PageBreak());p(title,'h1')
questions=[
('Ceritakan tugas Anda dalam penggunaan Fleffy dan penanganan pembayaran pelanggan.','Bagian mana yang Anda kerjakan sendiri? Siapa lagi yang terlibat?'),
('Ceritakan pola penggunaan Fleffy dalam pekerjaan Anda sehari-hari.','Sejak kapan, seberapa sering, dengan perangkat apa, dan dalam situasi seperti apa?'),
('Apa yang ingin Anda capai ketika mencatat pembayaran transfer, dan mengapa hal itu penting bagi Anda?','Apa yang membuat Anda merasa urusan pembayaran sudah selesai dengan baik?'),
('Ceritakan transaksi transfer terakhir yang Anda tangani, dari awal sampai menentukan tindak lanjutnya.','Kapan kira-kira terjadi? Bagian mana yang Anda tangani langsung?'),
('Sebelum mulai mencatat transaksi tersebut, apa yang Anda lakukan atau siapkan?','Informasi berasal dari mana? Apa yang memicu Anda mulai mencatat?'),
('Saat menggunakan Fleffy pada transaksi itu, langkah apa yang Anda lakukan dan informasi apa yang Anda perhatikan?','Apa alasan memilih langkah tersebut? Adakah perpindahan ke sumber informasi lain?'),
('Setelah melihat gambar B2, apa arti informasi pada layar ini bagi Anda?','Informasi apa yang sudah dan belum diketahui? Apa dasar penafsiran Anda? Tampilkan stimulus halaman 4 setelah cerita pengalaman; catat jawaban spontan sebelum penjelasan.'),
('Setelah pencatatan atau status itu muncul, apa yang Anda lakukan berikutnya sampai memutuskan tindak lanjut pembayaran?','Siapa yang memastikan penerimaan, informasi apa yang digunakan, dan bagaimana hasil pemeriksaan disampaikan?'),
('Dalam pengalaman tersebut, bagian mana yang berjalan lancar dan bagian mana yang memerlukan usaha tambahan, jika ada?','Jika pernah memeriksa atau menghubungi kembali, apa pemicunya? Apa yang Anda lakukan dan bagaimana hasilnya? Jika tidak pernah, catat apa adanya.'),
('Bagaimana perasaan Anda sebelum, selama, dan setelah menangani pembayaran tersebut?','Pada momen apa perasaan itu muncul dan apa yang menimbulkannya?'),
('Apa pengaruh proses pemeriksaan itu terhadap pekerjaan atau pelayanan, jika ada?','Adakah tindak lanjut yang tertunda? Mana yang benar-benar dialami dan mana yang merupakan perkiraan?'),
('Informasi atau dukungan apa yang Anda perlukan untuk menentukan tindak lanjut pembayaran? Apa harapan Anda untuk proses ini ke depan?','Apa yang sudah membantu? Jika satu hal dapat diperbaiki, hasil apa yang paling penting dan mengapa?'),
('Dari ringkasan yang saya sampaikan, apa yang perlu dikoreksi atau ditambahkan?','Adakah pengalaman penting lain yang belum dibahas? Bacakan ringkasan tanpa menambahkan penilaian.')
]

p('Panduan wawancara pengguna Fleffy','title')
p('Worksheet 5 User Interview\nRusdany Maestro | 202210370311406\nRekayasa Interaksi | Informatika | Universitas Muhammadiyah Malang')
p('Gunakan panduan ini untuk mengumpulkan jawaban asli dari minimal tiga orang yang berbeda. Produk dan fokus melanjutkan Worksheet 1-4, yaitu pencatatan Bank Transfer, pemahaman status Lunas, dan pemeriksaan penerimaan pembayaran. Dokumen ini merupakan instrumen pelaksanaan, bukan laporan hasil wawancara.')
h('Tujuan wawancara')
p('Memahami tujuan dan motivasi operator; kebiasaan serta pengalaman sebelum, saat, dan setelah memakai Fleffy; makna status pembayaran; proses dan pembagian tugas pemeriksaan; serta masalah, cara mengatasi, kebutuhan, perasaan, dan harapan pengguna.')
h('Siapa yang diwawancarai')
p('Pilih pengguna Fleffy berusia minimal 18 tahun yang aktif dalam tiga bulan terakhir, pernah mencatat Bank Transfer, melakukan atau ikut memeriksa penerimaannya, dan dapat menceritakan satu pengalaman nyata. Kasir, owner, atau admin memenuhi target berdasarkan tugas aktual. Satu orang dengan beberapa peran tetap satu responden. Gunakan kode R1, R2, dan R3.')
p('Worksheet 4 merencanakan lima operator dan satu informan pendukung. Worksheet 5 mensyaratkan minimal tiga responden. Catat jumlah yang benar-benar diwawancarai dan alasan perubahan rencana jika ada; jangan menghitung pengawas yang tidak melakukan tugas kasir sebagai pengganti operator tanpa penjelasan konteks.')
h('Pelaksanaan sekitar 25 sampai 35 menit per orang')
p('1. Konfirmasi kriteria, jadwal, dan tempat/media. Lakukan sesi secara individual.\n2. Jelaskan tujuan dan minta persetujuan, sekitar 3 menit.\n3. Ajukan Q1-Q12 serta pendalaman yang relevan, sekitar 20-28 menit.\n4. Bacakan ringkasan untuk Q13 dan beri kesempatan koreksi, sekitar 2-4 menit. Catat durasi aktual; tidak harus sama untuk semua orang.')
h('Naskah persetujuan singkat')
p('Saya Rusdany Maestro. Wawancara ini untuk tugas Rekayasa Interaksi tentang pengalaman memakai Fleffy. Anda boleh melewati pertanyaan atau berhenti tanpa konsekuensi. Laporan menggunakan kode dan data anonim. Tidak diperlukan data rekening atau pelanggan. Apakah Anda bersedia ikut? Secara terpisah, apakah Anda mengizinkan rekaman suara, foto/tampilan, serta kutipan anonim? Jika tidak, saya memakai catatan sesuai izin Anda.')
p('Data mentah disimpan aman dan dihapus paling lambat 30 hari setelah penilaian akhir/revisi selesai. Untuk penarikan data, gunakan saluran penjadwalan dan kode responden sebelum laporan digabung. Sampaikan waktu penutupan data yang benar-benar disepakati sebelum sesi.','small')

page('Pertanyaan tentang tujuan dan pengalaman penggunaan')
p('Ajukan pertanyaan utama dengan bahasa yang nyaman. Pendalaman digunakan saat jawaban belum jelas, bukan sebagai daftar pilihan jawaban. Dengarkan tanpa menyela atau menilai. Mintalah contoh yang dialami sendiri.')
for i in range(7):
 q,probe=questions[i]
 p(f'Q{i+1}. {q}\nPendalaman: {probe}','q')
h('Catatan moderator')
p('Untuk Q4-Q6, telusuri satu kejadian yang sama agar alur sebelum, saat, dan sesudah dapat dibandingkan. Jika peserta tidak ingat, catat ketidakpastian. Jangan meminta peserta membenarkan dugaan bahwa Lunas menyesatkan atau menawarkan integrasi bank sebelum kebutuhan dipahami.')

page('Pertanyaan tentang pemeriksaan dan kebutuhan pengguna')
for i in range(7,13):
 q,probe=questions[i]
 p(f'Q{i+1}. {q}\nPendalaman: {probe}','q')
h('Cara mencatat jawaban')
p('Catat inti jawaban beserta contoh, alasan, dan pertanyaan lanjutannya. Kutipan langsung hanya memakai kata-kata yang dicatat persis; jika berupa rangkuman, beri label parafrasa. Pisahkan catatan peneliti dari jawaban responden. Jawaban tidak pernah, tidak tahu, atau tidak ingin menjawab tetap dicatat apa adanya.')
p('Perkiraan waktu atau frekuensi berdasarkan ingatan diberi label perkiraan responden. Wawancara tidak membuktikan durasi pelayanan yang terukur, penerimaan dana bank, atau logika internal sistem. Catat pengalaman yang lancar dan yang mengalami hambatan agar analisis tidak hanya mencari keluhan.')
h('Berkas pencatatan')
p('Gunakan berkas Catatan R1 R2 R3 yang disertakan. Isi identitas sesi dan jawaban Q1-Q13 secara terpisah untuk setiap orang. Bila ada pertanyaan yang tidak sempat diajukan, tulis belum ditanyakan, kemudian lengkapi melalui tindak lanjut jika memungkinkan.')

page('Stimulus dan kelengkapan data yang dikirim kembali')
p('B2 digunakan hanya untuk Q7. Perlihatkan gambar ini tanpa membacakan penafsiran peneliti. Jangan meminta responden membuka rekening atau bukti transfer pribadi.')
img=ROOT/'tmp'/'worksheet4'/'stimulus_B2.png'
im=Image(str(img),width=15.5*cm,height=9*cm)
im.hAlign='CENTER'; story.append(im);story.append(Spacer(1,8))
p('Sumber B2: dokumentasi Detail Transaksi Fleffy 19 September 2026, digunakan pada Worksheet 1-2 dan stimulus Worksheet 4. Cuplikan mempertahankan status serta nominal. Gambar memperlihatkan catatan aplikasi pada transaksi contoh, bukan bukti dana bank. Keterangan ini untuk moderator; sampaikan setelah jawaban spontan.','small')
h('Data wajib untuk masing masing R1 R2 dan R3')
p('Kode dan peran aktual; lama dan frekuensi penggunaan; keterlibatan Bank Transfer; tanggal; jam mulai-selesai atau durasi aktual; tempat secara umum atau nama media daring; persetujuan partisipasi serta pilihan dokumentasi; jawaban Q1-Q13; contoh kejadian; dan hasil koreksi ringkasan.')
p('Foto atau rekaman hanya disertakan jika diizinkan dan sudah disamarkan. Jika tidak diizinkan, catatan tertulis yang akurat tetap digunakan. Jangan kirim nama lengkap, nomor telepon, alamat pribadi, rekening, saldo, mutasi, PIN, OTP, atau data pelanggan.')
h('Langkah setelah wawancara')
p('Kirim catatan R1 lebih dahulu bila sudah selesai; R2 dan R3 dapat menyusul. Catatan akan diolah menjadi ringkasan setiap responden, perbandingan tema, temuan berbasis bukti, masalah, kebutuhan, harapan, dan kesimpulan. Laporan akhir baru disusun dari data yang benar-benar terkumpul.')
p('Batas yang diinformasikan dari Google Classroom: 17 Oktober 2026 pukul 11.59 siang. Upayakan pengumpulan data selesai 16 Oktober agar tersedia waktu untuk analisis, pemeriksaan, dan ekspor PDF. Cocokkan kembali zona waktu di Classroom.','small')

def footer(c,d):
 c.saveState();c.setFont('Arial',9);c.setFillColor(colors.black)
 c.drawRightString(19.2*cm,1.05*cm,f'{d.page} / 4');c.restoreState()

SimpleDocTemplate(str(PDF),pagesize=(21*cm,29.7*cm),leftMargin=1.8*cm,rightMargin=1.8*cm,topMargin=1.65*cm,bottomMargin=1.65*cm,title='Panduan Wawancara Worksheet 5 pada Fleffy',author='Rusdany Maestro').build(story,onFirstPage=footer,onLaterPages=footer)
assert len(PdfReader(PDF).pages)==4,'Periksa luapan halaman panduan'

chunks=[
'CATATAN WAWANCARA NYATA WORKSHEET 5\nFleffy - Kasir Laundry Sepatu\nPewawancara: Rusdany Maestro | NIM 202210370311406\n\nPETUNJUK\nIsi dari jawaban orang yang benar-benar diwawancarai. Gunakan kode, bukan nama asli. Boleh kirim R1 dahulu. Ringkasan diberi label parafrasa; tanda kutip hanya untuk kata-kata yang dicatat persis. Jangan menulis ulang jawaban agar sesuai dugaan. Jika tidak ditanyakan, tulis belum ditanyakan.\n'
]
for respondent in ['R1','R2','R3']:
 chunks.append(f'\n========================================\n{respondent}\n========================================\n\nPROFIL DAN PELAKSANAAN\nPeran/tugas nyata di Fleffy:\nKonteks outlet (Balik Bersih / outlet pembanding; tanpa alamat pribadi):\nUsia minimal 18 tahun (ya/tidak; tidak perlu tanggal lahir):\nLama menggunakan Fleffy:\nFrekuensi penggunaan/tugas (menurut responden):\nPenggunaan terakhir dalam 3 bulan (ya/tidak):\nPernah mencatat Bank Transfer (ya/tidak; jelaskan):\nPernah melakukan/ikut pemeriksaan penerimaan (ya/tidak; jelaskan):\nTanggal wawancara:\nJam mulai dan selesai atau durasi aktual:\nMetode (langsung/daring):\nTempat secara umum atau media daring:\nPersetujuan ikut (setuju/tidak):\nPersetujuan rekaman suara (setuju/tidak):\nPersetujuan foto/tampilan (setuju/tidak):\nPersetujuan kutipan anonim (setuju/tidak):\nBatas penarikan data yang disepakati sebelum laporan digabung:\nDokumentasi yang tersedia dan diizinkan (jika ada):\n\nJAWABAN ASLI\n')
 for i,(q,probe) in enumerate(questions,1):
  chunks.append(f'Q{i}. {q}\nJawaban (parafrasa atau kutipan persis):\n\nPertanyaan lanjutan dan jawaban jika ada:\n\n')
 chunks.append('CATATAN PENELITI TERPISAH DARI JAWABAN\nGangguan/keterbatasan sesi:\nBagian yang belum jelas dan perlu ditanyakan kembali:\nKonfirmasi ringkasan (tanggal dan koreksi, jika ada):\n\n')
chunks.append('\nREKAP PELAKSANAAN\nJumlah orang unik yang benar-benar diwawancarai:\nJika berbeda dari rencana Worksheet 4, apa alasan sebenarnya:\nApakah ada sesi tambahan dari orang yang sama (jangan dihitung orang baru):\n')
TXT.write_text(''.join(chunks),encoding='utf-8')
(ROOT/'tmp'/'worksheet5'/'questions.txt').write_text('\n\n'.join(f'Q{i}. {q}\nPendalaman: {probe}' for i,(q,probe) in enumerate(questions,1)),encoding='utf-8')
print(PDF)
print(TXT)
print('Guide pages:',len(PdfReader(PDF).pages))
