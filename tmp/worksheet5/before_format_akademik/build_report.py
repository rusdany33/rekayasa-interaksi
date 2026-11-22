from pathlib import Path
import json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(r'D:\Rekayasa Interaksi')
TMP=ROOT/'tmp'/'worksheet5'
META=json.loads((TMP/'data'/'metadata_pelaksanaan.json').read_text(encoding='utf-8'))
FINAL=META.get('siap_final',False)
NAME='202210370311406_Rusdany_Maestro_Worksheet5_UserInterview'
OUT=(ROOT/(NAME+'.docx')) if FINAL else TMP/(NAME+'_DrafVerifikasi.docx')
doc=Document(); sec=doc.sections[0]
sec.page_width=Cm(21); sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.75); sec.bottom_margin=Cm(1.75)
sec.left_margin=Cm(1.8); sec.right_margin=Cm(1.8)
sec.footer_distance=Cm(.8)
for name,size in [('Normal',11),('Title',23),('Subtitle',13),('Heading 1',16),('Heading 2',11.5)]:
 st=doc.styles[name];st.font.name='Arial';st.font.size=Pt(size);st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.06
 st.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Arial')
for name in ['Heading 1','Heading 2']:
 doc.styles[name].paragraph_format.space_before=Pt(8)
 doc.styles[name].paragraph_format.keep_with_next=True
doc.core_properties.author='Rusdany Maestro'
doc.core_properties.title='Worksheet 5 User Interview Kepastian Pembayaran Transfer pada Fleffy'
doc.core_properties.subject='Rekayasa Interaksi'
f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for code in ['PAGE','NUMPAGES']:
 if code=='NUMPAGES': f.add_run(' / ')
 fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),code);f._p.append(fld)
content=[]
def p(text):
 content.append(text);return doc.add_paragraph(text)
def h(text,level=1):
 content.append(text);return doc.add_paragraph(text,f'Heading {level}')
def page(text):doc.add_page_break();h(text)
def table(headers,rows,widths,size=10):
 content.append(' | '.join(headers))
 t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
 for col,w in zip(t.columns,widths): col.width=Cm(w)
 for c,x in zip(t.rows[0].cells,headers):c.text=x
 for row in rows:
  content.append(' | '.join(row))
  for c,x in zip(t.add_row().cells,row):c.text=x
 for ri,row in enumerate(t.rows):
  pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
  if ri==0:pr.append(OxmlElement('w:tblHeader'))
  for ci,c in enumerate(row.cells):
   c.width=Cm(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   cp=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for edge in ['top','bottom','left','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
   cp.append(b);m=OxmlElement('w:tcMar')
   for edge,val in [('top',85),('bottom',85),('left',100),('right',100)]:
    e=OxmlElement('w:'+edge);e.set(qn('w:w'),str(val));e.set(qn('w:type'),'dxa');m.append(e)
   cp.append(m);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E7EDF3' if ri==0 else ('F7F8FA' if ri%2==0 else 'FFFFFF'));cp.append(shade)
   for pp in c.paragraphs:
    pp.paragraph_format.space_after=Pt(2);pp.paragraph_format.line_spacing=1.03
    for r in pp.runs:r.font.size=Pt(size);r.bold=(ri==0)
 doc.add_paragraph().paragraph_format.space_after=Pt(0)
 return t

# 1
doc.add_paragraph('Worksheet 5 User Interview','Title')
doc.add_paragraph('Wawancara tentang kepastian pembayaran transfer pada Fleffy','Subtitle')
if not FINAL:p('Draf verifikasi data pelaksanaan')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nMata kuliah: Rekayasa Interaksi\nJenis tugas: Individu\nTanggal wawancara: 15 Oktober 2026')
h('1 Ringkasan hasil')
p('Jawaban tiga pengguna Fleffy menunjukkan bahwa pencatatan pembayaran membantu pekerjaan mereka, sedangkan kepastian penerimaan transfer diperoleh melalui pemeriksaan rekening atau konfirmasi pihak yang memegang akses rekening. Cara pemeriksaan berbeda menurut tugas: kasir dapat memeriksa sendiri, admin berkoordinasi dengan owner atau finance, dan owner memeriksa rekening secara langsung. [R1 Q1, Q8-Q9; R2 Q1, Q8; R3 Q1, Q6-Q8]')
p('Perpindahan aplikasi dan penantian konfirmasi menjadi usaha tambahan yang dilaporkan. Pemeriksaan juga dipandang berguna untuk menentukan tindak lanjut dan mengurangi risiko kesalahan pembayaran. Kebutuhan utamanya adalah informasi pembayaran yang jelas, dapat dicocokkan dengan pesanan, dan didukung pembagian tanggung jawab pemeriksaan. [R1-R3 Q9-Q12]')
h('2 Produk latar belakang dan tujuan')
p('Fleffy - Kasir Laundry Sepatu digunakan dalam pencatatan pesanan, layanan, dan pembayaran usaha laundry sepatu. Worksheet 1-4 mengangkat kebutuhan memastikan penerimaan transfer ketika catatan aplikasi sudah menunjukkan Lunas. Wawancara ini melanjutkan fokus tersebut melalui pengalaman operator yang menjalankan tugas pembayaran. [S1-S4]')
p('Tujuan wawancara adalah memahami tujuan dan motivasi pengguna; kebiasaan serta proses sebelum, saat, dan setelah menggunakan Fleffy; penafsiran status pembayaran; langkah dan kewenangan pemeriksaan; serta masalah, kebutuhan, perasaan, dan harapan pengguna.')

# 2
page('3 Responden dan pelaksanaan wawancara')
p('Tiga orang dipilih berdasarkan aktivitas pencatatan atau pemeriksaan pembayaran Bank Transfer. Peran aktual digunakan untuk menentukan relevansi responden; owner dan admin termasuk pengguna utama ketika menjalankan tugas tersebut. Satu orang tetap dihitung satu responden meskipun memiliki beberapa tugas.')
table(['Kode dan peran','Karakteristik penggunaan yang dilaporkan','Keterlibatan pemeriksaan'],[
 ('R1 Kasir laundry sepatu','Penggunaan harian, terutama saat melayani transaksi. Memakai tablet kasir dan ponsel untuk pemeriksaan.','Memeriksa rekening sendiri; meminta bantuan owner atau finance bila diperlukan.'),
 ('R2 Admin Operasional yang menjalankan tugas kasir','Menerima pesanan, memilih layanan, menerbitkan nota, dan mencatat pembayaran. Menggunakan perangkat operasional dalam pekerjaan harian.','Meminta owner atau finance memeriksa mutasi, kemudian menindaklanjuti konfirmasi.'),
 ('R3 Owner yang juga mencatat transaksi','Menggunakan Fleffy melalui HP setiap hari saat ada transaksi atau pemeriksaan status.','Mencocokkan transaksi dengan rekening sendiri sebelum melanjutkan pesanan.')
],[3.8,8.0,5.6])
p('Jumlah aktual adalah tiga pengguna, sedangkan Worksheet 4 merencanakan lima operator dan satu informan pendukung. Laporan ini memuat cakupan pelaksanaan Worksheet 5 yang memenuhi minimal tiga responden. Temuan diperlakukan sebagai eksplorasi pada ketiga pengguna, dengan kedalaman yang mengikuti durasi sesi aktual.')
rows=[]
for r in ['R1','R2','R3']:
 dur=META.get('durasi',{}).get(r) or 'Perlu dilengkapi'
 tempat=META.get('lokasi_wawancara_per_responden',{}).get(r) or META.get('tempat') or 'Perlu dikonfirmasi'
 rows.append((r,META['tanggal'],str(dur),tempat))
table(['Kode','Tanggal','Durasi sesi','Tempat wawancara'],rows,[1.5,4.0,3.0,8.9])
p('Pesenkopi merupakan lokasi pertemuan untuk wawancara. Konteks pekerjaan yang dibahas tetap pencatatan dan pemeriksaan pembayaran pada usaha laundry sepatu yang menggunakan Fleffy.')
p('Metode: wawancara langsung dengan panduan 13 pertanyaan terbuka. Pewawancara: Rusdany Maestro. Catatan hasil disajikan sebagai parafrasa agar inti jawaban dan rujukan pertanyaannya dapat ditelusuri. Isi percakapan tidak diperlakukan sebagai hasil observasi atau pengukuran waktu proses pembayaran.')
h('Persetujuan dan kerahasiaan',2)
p('Ketiga responden menyetujui partisipasi, penggunaan jawaban anonim, dan dokumentasi foto. Laporan menggunakan kode R1-R3; nomor telepon, alamat pribadi, data pelanggan, dan informasi rekening tidak dicantumkan. Foto kegiatan digunakan sesuai persetujuan responden untuk kebutuhan pembelajaran. Data mentah disimpan terbatas dan dihapus paling lambat 30 hari setelah penilaian akhir atau revisi selesai.')

# 3
page('4 Panduan pertanyaan wawancara')
p('Pertanyaan dimulai dari pekerjaan sehari-hari, dilanjutkan pengalaman transaksi konkret, kemudian pemeriksaan dan kebutuhan. Pertanyaan pendalaman digunakan untuk memperjelas contoh dan alasan. Responden dapat menjelaskan proses yang lancar maupun pengalaman dengan hambatan.')
qs=[
('Q1','Ceritakan tugas Anda dalam penggunaan Fleffy dan penanganan pembayaran pelanggan.','Bagian mana yang Anda kerjakan sendiri? Siapa lagi yang terlibat?'),
('Q2','Ceritakan pola penggunaan Fleffy dalam pekerjaan Anda sehari-hari.','Sejak kapan, seberapa sering, dengan perangkat apa, dan dalam situasi seperti apa?'),
('Q3','Apa yang ingin Anda capai ketika mencatat pembayaran transfer, dan mengapa hal itu penting bagi Anda?','Apa yang membuat urusan pembayaran dianggap selesai dengan baik?'),
('Q4','Ceritakan transaksi transfer terakhir yang Anda tangani, dari awal sampai menentukan tindak lanjutnya.','Kapan kira-kira terjadi? Bagian mana yang Anda tangani langsung?'),
('Q5','Sebelum mulai mencatat transaksi tersebut, apa yang Anda lakukan atau siapkan?','Informasi berasal dari mana? Apa yang memicu pencatatan?'),
('Q6','Saat menggunakan Fleffy pada transaksi itu, langkah apa yang Anda lakukan dan informasi apa yang Anda perhatikan?','Apa alasan memilih langkah tersebut? Adakah perpindahan ke sumber lain?'),
('Q7','Setelah melihat gambar B2, apa arti informasi pada layar ini bagi Anda?','Informasi apa yang sudah dan belum diketahui? Apa dasar penafsiran tersebut?'),
('Q8','Setelah pencatatan atau status itu muncul, apa yang Anda lakukan berikutnya sampai memutuskan tindak lanjut pembayaran?','Siapa yang memastikan penerimaan, informasi apa yang digunakan, dan bagaimana hasilnya disampaikan?'),
('Q9','Dalam pengalaman tersebut, bagian mana yang berjalan lancar dan bagian mana yang memerlukan usaha tambahan, jika ada?','Jika pernah memeriksa atau menghubungi kembali, apa pemicunya dan bagaimana hasilnya?'),
('Q10','Bagaimana perasaan Anda sebelum, selama, dan setelah menangani pembayaran tersebut?','Pada momen apa perasaan itu muncul dan apa yang menimbulkannya?'),
('Q11','Apa pengaruh proses pemeriksaan itu terhadap pekerjaan atau pelayanan, jika ada?','Adakah tindak lanjut yang tertunda? Mana yang dialami dan mana yang diperkirakan?'),
('Q12','Informasi atau dukungan apa yang Anda perlukan untuk menentukan tindak lanjut pembayaran? Apa harapan Anda untuk proses ini ke depan?','Apa yang sudah membantu? Jika satu hal dapat diperbaiki, hasil apa yang paling penting dan mengapa?'),
('Q13','Dari ringkasan yang saya sampaikan, apa yang perlu dikoreksi atau ditambahkan?','Adakah pengalaman penting lain yang belum dibahas?')
]
for code,q,probe in qs[:7]:
 h(code,2);p(q+'\nPendalaman: '+probe)

# 4
page('Panduan pemeriksaan dan kebutuhan pengguna')
for code,q,probe in qs[7:]:
 h(code,2);p(q+'\nPendalaman: '+probe)
h('Stimulus dan pencatatan jawaban',2)
p('B2 merujuk tampilan Rincian Pembayaran Fleffy pada dokumentasi Worksheet 1-4: status Lunas dan Bank Transfer Rp57.000 pada transaksi contoh. Nominal ini merupakan konteks stimulus, bukan nominal transaksi baru dari ketiga responden. [S1, S4]')
p('Seluruh ringkasan berikut merupakan parafrasa. Penanda seperti [R2 Q8] menunjukkan responden dan nomor jawaban sumber. Pernyataan mengenai waktu tunggu, antrean, dan perilaku aplikasi diatribusikan kepada responden. Analisis peneliti ditempatkan pada bagian perbandingan serta temuan, terpisah dari ringkasan jawaban.')

# 5
page('5 Ringkasan jawaban R1 Kasir laundry sepatu')
h('Peran kebiasaan dan tujuan Q1 sampai Q3',2)
p('R1 menangani pencatatan transaksi dan pembayaran pelanggan. Ia memasukkan nominal, memilih metode pembayaran, dan memeriksa rekening atau notifikasi mobile banking sendiri. Owner atau finance dapat membantu saat ada keraguan. Penggunaan Fleffy berlangsung setiap hari melalui tablet kasir dan ponsel, termasuk saat pelayanan ramai. Tujuannya adalah catatan akurat, kepastian dana masuk, dan kesesuaian pencatatan di akhir pelayanan. [R1 Q1-Q3]')
h('Pengalaman sebelum dan saat pencatatan Q4 sampai Q6',2)
p('Dalam uraian pengalaman, R1 menerima informasi pembayaran serta bukti dari pelanggan, mencocokkan nominal dengan catatan Fleffy, dan menentukan tindak lanjut. Ia menyiapkan aplikasi serta sarana pengecekan rekening. Ketika mencatat, R1 berpindah antara layar Fleffy, bukti dari pelanggan, dan mobile banking untuk memeriksa kecocokan informasi pembayaran. [R1 Q4-Q6]')
h('Penafsiran status Q7',2)
p('R1 memahami tampilan sebagai catatan pembayaran pada sistem. Ia masih mempertanyakan apakah Lunas juga menjamin dana sudah diterima secara langsung. Pengalamannya dengan input manual menjadi dasar untuk tetap melakukan pemeriksaan rekening. [R1 Q7]')
h('Tindak lanjut usaha dan perasaan Q8 sampai Q11',2)
p('Setelah nominal dan informasi penerimaan sesuai, R1 melanjutkan transaksi serta memberi konfirmasi kepada pelanggan. Pencatatan dinilai cepat, tetapi memeriksa mobile banking atau menunggu bantuan owner membutuhkan usaha tambahan. R1 melaporkan pengaruh terhadap antrean, terutama saat ramai; lama penundaan tidak diukur. [R1 Q8-Q9, Q11]')
p('Sebelum pemeriksaan, R1 merasa waspada, terutama jika bukti kurang jelas atau respons informasi rekening lambat. Saat memeriksa, ia fokus pada kecocokan angka. Setelah kepastian pembayaran diperoleh, ia merasa lega. [R1 Q10]')
h('Kebutuhan harapan dan penutup Q12 sampai Q13',2)
p('R1 mengharapkan kepastian pembayaran yang lebih mudah diperoleh tanpa sering berpindah aplikasi. Notifikasi validasi atau integrasi bank menjadi usulan yang disampaikan. Pada penutup, R1 menilai pokok ringkasan sudah sesuai dan menambahkan kekhawatiran tentang bukti transfer yang disunting. Kekhawatiran tersebut tidak menyatakan bahwa penipuan atau kerugian benar-benar telah terjadi. [R1 Q12-Q13]')

# 6
page('6 Ringkasan jawaban R2 Admin Operasional')
h('Peran kebiasaan dan tujuan Q1 sampai Q3',2)
p('R2 menjalankan tugas admin sekaligus kasir: menerima pesanan langsung atau melalui WhatsApp, mencatat sepatu dan layanan, menerbitkan nota, serta mencatat pembayaran. Owner atau finance memegang akses pemeriksaan rekening, sedangkan teknisi menerima informasi pengerjaan. Fleffy digunakan dalam aktivitas harian melalui perangkat operasional. R2 menyebut kisaran 15-30 transaksi per hari sebagai keterangannya, bukan hasil hitung peneliti. [R2 Q1-Q2]')
p('Tujuannya adalah memastikan pencatatan sesuai penerimaan dana dan mengurangi risiko kesalahan atau bukti transfer yang tidak sah. Pembayaran dianggap selesai dengan baik setelah pemeriksaan owner atau finance menghasilkan kecocokan informasi yang diperlukan. [R2 Q3]')
h('Pengalaman sebelum dan saat pencatatan Q4 sampai Q6',2)
p('R2 menceritakan pesanan deep cleaning dua pasang sepatu dengan transfer Rp150.000. Ia menerima bukti melalui WhatsApp, mencatat pesanan pada Fleffy, dan meneruskan permintaan pemeriksaan kepada owner sebelum menindaklanjuti pengerjaan. [R2 Q4]')
p('Persiapan mencakup rincian pesanan dan layanan serta informasi pembayaran pelanggan. R2 memperhatikan kesesuaian nominal dan informasi waktu pada bukti, lalu berpindah dari Fleffy ke WhatsApp pelanggan serta percakapan dengan owner. [R2 Q5-Q6]')
h('Penafsiran status dan tindak lanjut Q7 sampai Q8',2)
p('R2 menafsirkan status sebagai informasi pencatatan, sementara kepastian penerimaan diperoleh dari pemeriksaan owner atau finance. Ia meminta verifikasi dan menunggu konfirmasi, kemudian menindaklanjuti pesanan. Penjelasan R2 tentang integrasi perbankan dicatat sebagai pemahamannya mengenai aplikasi. [R2 Q7-Q8]')
h('Usaha dampak dan perasaan Q9 sampai Q11',2)
p('Input pesanan dan penerbitan nota dinilai lancar. Hambatan yang dilaporkan adalah menunggu owner merespons, kadang disertai panggilan telepon atau permintaan agar pelanggan menunggu. Contoh pengambilan sepatu diperlakukan sebagai pengalaman layanan tambahan, terpisah dari contoh sebelum pengerjaan pada Q4. [R2 Q9]')
p('R2 merasa cemas saat menunggu kepastian dan sungkan kepada pelanggan. Sesudah konfirmasi, ia merasa lega. Ia melaporkan antrean tersendat dan pengerjaan yang kadang tertunda beberapa jam; durasi ini merupakan laporan pengalaman, bukan pengukuran. Penurunan kepuasan pelanggan disebut sebagai perkiraan. [R2 Q10-Q11]')
h('Kebutuhan harapan dan penutup Q12 sampai Q13',2)
p('R2 membutuhkan informasi penerimaan pembayaran yang jelas dan koordinasi lebih cepat. Ia mengusulkan validasi otomatis, integrasi rekening, QRIS dinamis, atau payment gateway. Pada penutup, R2 menyatakan ringkasan sesuai dengan pengalamannya dan mengharapkan perbaikan verifikasi menjadi prioritas. Ia tetap menilai pencatatan Fleffy membantu pekerjaan. Usulan teknologi tersebut menjadi harapan responden untuk dievaluasi lebih lanjut. [R2 Q12-Q13]')

# 7
page('7 Ringkasan jawaban R3 Owner')
h('Peran kebiasaan dan tujuan Q1 sampai Q3',2)
p('R3 adalah owner yang menggunakan Fleffy untuk mencatat transaksi dan memantau pembayaran pelanggan. Ia melakukan pengecekan rekening sendiri. Aplikasi diakses melalui HP setiap hari ketika ada transaksi atau saat perlu memeriksa status. Tujuannya adalah catatan pembayaran yang benar dan kepastian bahwa uang benar-benar masuk ke rekening. [R3 Q1-Q3]')
h('Pengalaman sebelum dan saat pencatatan Q4 sampai Q6',2)
p('R3 menceritakan pembayaran transfer yang diperiksa dengan mencocokkan transaksi di Fleffy dan mutasi rekening sebelum pesanan dilanjutkan. Persiapannya mencakup informasi pesanan, nominal, data pelanggan, dan bukti transfer. Ia membuka transaksi, membaca nominal serta status pembayaran, kemudian memeriksa mobile banking untuk memastikan penerimaan dana. [R3 Q4-Q6]')
h('Penafsiran status dan tindak lanjut Q7 sampai Q8',2)
p('R3 menafsirkan status di layar sebagai kondisi transaksi menurut aplikasi. Kepastian penerimaan uang tetap diperoleh dari rekening. Setelah mutasi serta nominal sesuai, ia memberi konfirmasi pembayaran dan melanjutkan pesanan. [R3 Q7-Q8]')
h('Usaha dampak dan perasaan Q9 sampai Q11',2)
p('Pencatatan Fleffy dinilai membantu, tetapi R3 masih perlu berpindah ke mobile banking. Ia merasa tenang ketika catatan benar dan khawatir apabila status belum sesuai dengan rekening. Pemeriksaan tambahan membutuhkan waktu, sekaligus membantu mengurangi risiko salah menentukan pembayaran. R3 tidak memberikan ukuran menit atau frekuensi penundaan proses. [R3 Q9-Q11]')
h('Kebutuhan harapan dan penutup Q12 sampai Q13',2)
p('R3 membutuhkan informasi pembayaran yang akurat dan mengharapkan integrasi bank agar pengecekan lebih praktis. Pada penutup, ia menegaskan manfaat Fleffy untuk pencatatan serta kebiasaannya memastikan dana sebelum menganggap pembayaran selesai. [R3 Q12-Q13]')
h('Interpretasi atas pengalaman R3',2)
p('Jawaban R3 menunjukkan bahwa pemeriksaan merupakan bagian dari kendali pembayaran yang dianggap bermanfaat. Karena R3 memiliki akses pemeriksaan sendiri, pengalamannya membatasi anggapan bahwa semua pengguna harus menunggu konfirmasi orang lain. Interpretasi ini digunakan dalam perbandingan berikut, tanpa menganggap praktik owner mewakili seluruh peran.')

# 8
page('8 Perbandingan jawaban antarresponden')
p('Matriks merangkum perbedaan praktik yang dilaporkan. Perbandingan dilakukan menurut aktivitas serta akses informasi, sehingga nama peran tidak otomatis menentukan pola pemeriksaan yang sama.')
table(['Aspek','R1 Kasir','R2 Admin Operasional','R3 Owner'],[
 ('Tujuan','Catatan tepat dan dana dipastikan sebelum tindak lanjut.','Pencatatan sesuai hasil pemeriksaan owner atau finance.','Catatan benar dan dana masuk ke rekening.'),
 ('Makna status','Catatan pembayaran; masih mempertanyakan jaminan penerimaan dana.','Konfirmasi pencatatan; menunggu hasil pemeriksaan.','Kondisi transaksi menurut aplikasi; rekening tetap diperiksa.'),
 ('Sumber kepastian','Pemeriksaan rekening sendiri; bantuan bila ragu.','Konfirmasi owner atau finance yang memeriksa rekening.','Pemeriksaan rekening sendiri.'),
 ('Usaha tambahan','Pindah aplikasi atau menunggu bantuan.','Pindah sumber dan menunggu respons pihak lain.','Pindah aplikasi dan waktu pemeriksaan.'),
 ('Dampak yang dilaporkan','Antrean dapat tertunda saat ramai.','Penantian pelanggan dan penundaan pengerjaan dalam pengalamannya.','Ada tambahan waktu; pemeriksaan membantu mengurangi risiko salah bayar.'),
 ('Perasaan','Waspada, fokus mencocokkan, lalu lega.','Cemas dan sungkan saat menunggu, lalu lega.','Tenang bila sesuai; khawatir bila catatan belum sesuai rekening.'),
 ('Harapan','Notifikasi atau integrasi bank.','Validasi otomatis dan koordinasi lebih cepat; mengusulkan beberapa teknologi pembayaran.','Status akurat dan integrasi bank yang praktis.')
],[3.1,4.6,5.1,4.6],size=10)
p('Dasar perbandingan: tujuan Q3, makna Q7, sumber kepastian Q1/Q8, usaha dan dampak Q9/Q11, perasaan Q10, dan harapan Q12-Q13 pada masing-masing responden.')
h('Persamaan dan perbedaan yang penting',2)
p('Ketiganya membutuhkan kecocokan antara catatan dan penerimaan dana serta menilai pencatatan Fleffy membantu. Perbedaan utamanya adalah siapa yang dapat memperoleh bukti penerimaan dan bagaimana hasilnya diteruskan. R2 menyoroti koordinasi antarorang, sedangkan R3 menjalankan pemeriksaan sendiri. R1 menyebut kedua pola tersebut bergantung pada kondisi.')
p('R1 masih mempertanyakan cakupan jaminan label Lunas, sementara R2 dan R3 sudah membedakan pencatatan dari kepastian dana. Karena itu, temuan tidak menyatakan bahwa seluruh responden salah memahami status pembayaran.')

# 9
page('9 Temuan utama dan interpretasi peneliti')
h('T1 Keputusan pembayaran memerlukan informasi penerimaan',2)
p('Dasar jawaban: ketiganya mencocokkan catatan dengan rekening atau konfirmasi pemeriksa dana. Interpretasi: kebutuhan inti adalah kepastian yang dapat dijelaskan untuk menentukan tindak lanjut, termasuk informasi apa yang telah dicatat dan apa yang telah dipastikan. Perbedaan pemahaman status tetap dipertahankan. [R1 Q3, Q7-Q8; R2 Q3, Q7-Q8; R3 Q3, Q7-Q8]')
h('T2 Akses dan tanggung jawab membentuk alur kerja',2)
p('Dasar jawaban: R1 dan R3 dapat memeriksa sendiri, sedangkan R2 meminta pemeriksaan owner atau finance. Interpretasi: hambatan dan dukungan yang diperlukan berbeda menurut kewenangan. Memperjelas pemeriksa serta cara menyampaikan hasil dapat membantu koordinasi, tanpa menyimpulkan setiap kasir perlu memperoleh akses bank langsung. [R1 Q1, Q8-Q9; R2 Q1, Q8; R3 Q1, Q6-Q8]')
h('T3 Pemeriksaan menghubungkan beberapa sumber informasi',2)
p('Dasar jawaban: operator menggunakan catatan Fleffy, informasi pelanggan, serta hasil pemeriksaan rekening; R2 menghubungkannya melalui komunikasi dengan pihak lain. Interpretasi: pencocokan informasi membutuhkan kesinambungan identitas pesanan dan hasil pemeriksaan. Kepastian dana dalam kasus tersebut merupakan keterangan responden. [R1 Q4-Q6; R2 Q4-Q8; R3 Q4-Q8]')
h('T4 Usaha tambahan dapat berupa perpindahan atau penantian',2)
p('Dasar jawaban: R1 menyebut perpindahan dan bantuan, R2 menunggu konfirmasi, sedangkan R3 menyoroti waktu pemeriksaan. Interpretasi: upaya perbaikan perlu menangani jenis usaha yang benar-benar terjadi. Besaran waktu dan frekuensinya belum diukur; laporan ini tidak menetapkan rata-rata keterlambatan. [R1-R3 Q9, Q11]')
h('T5 Pemeriksaan juga melindungi keputusan kerja',2)
p('Dasar jawaban: R3 menyatakan pemeriksaan membantu mengurangi risiko kesalahan, dan ketiganya baru menindaklanjuti setelah memperoleh kepastian. Interpretasi: langkah pemeriksaan yang diperlukan perlu tetap didukung. Pengurangan usaha dinilai bersama ketelitian, bukan semata kecepatan. [R1 Q3, Q8; R2 Q3-Q4, Q8; R3 Q4, Q8, Q11]')
h('T6 Perasaan yakin mengikuti kecocokan informasi',2)
p('Dasar jawaban: ketiganya menyebut kewaspadaan, kekhawatiran, atau ketenangan yang terkait kondisi pembayaran; kekhawatiran bukti palsu lebih eksplisit pada R1 dan R2. Interpretasi: informasi dan tanggung jawab yang jelas dapat menjadi arah dukungan pengalaman pengguna. Kekhawatiran tersebut tidak membuktikan telah terjadi penipuan atau kerugian. [R1 Q10, Q12-Q13; R2 Q10, Q12; R3 Q10, Q13]')

# 10
page('10 Masalah kebutuhan harapan dan kesimpulan')
table(['Masalah yang dilaporkan','Kebutuhan pengguna hasil interpretasi','Harapan yang disampaikan'],[
 ('Kepastian penerimaan belum diperoleh hanya dari catatan status.','Memahami informasi yang ditunjukkan status dan dasar untuk menentukan tindak lanjut.','Status yang akurat, notifikasi, atau validasi pembayaran.'),
 ('Pencocokan memerlukan perpindahan sumber atau penantian konfirmasi.','Mencocokkan pesanan dengan hasil pemeriksaan secara jelas dan memperoleh tindak lanjut yang dapat ditelusuri.','Integrasi bank agar pengecekan lebih praktis; R2 juga mengusulkan QRIS dinamis atau payment gateway.'),
 ('Pihak pencatat dan pemeriksa dapat berbeda.','Mengetahui penanggung jawab pemeriksaan, status tindak lanjut, dan cara konfirmasi hasil.','Koordinasi yang lebih cepat dengan owner atau finance.')
],[5.1,6.7,5.6],size=10)
p('Harapan teknologi dicatat sebagai usulan responden. Kelayakan integrasi, pengaruhnya terhadap ketelitian, serta kemampuan mengatasi risiko perlu dievaluasi sebelum alternatif perancangan dipilih. Kebutuhan pada tabel berasal dari interpretasi atas jawaban dan tidak dianggap sebagai fitur yang sudah disepakati.')
h('Kesimpulan',2)
p('Dalam ketiga jawaban, kepastian pembayaran diperoleh melalui pencocokan catatan Fleffy dengan informasi penerimaan dana. Praktik pemeriksaan mengikuti akses dan pembagian tugas: ada pengguna yang memeriksa sendiri dan ada yang menunggu konfirmasi. Pencatatan dinilai membantu, sementara perpindahan sumber serta koordinasi memerlukan usaha tambahan. Temuan mendukung kebutuhan informasi pembayaran dan tanggung jawab pemeriksaan yang jelas, dengan ketelitian keputusan tetap dipertahankan.')
h('Batas dan penggunaan hasil berikutnya',2)
p('Temuan berasal dari tiga wawancara dengan durasi berbeda. Pengalaman tersebut tidak digunakan untuk menyatakan prevalensi seluruh pengguna, logika internal aplikasi, penerimaan dana yang diperiksa peneliti, atau besaran waktu layanan. Rincian dampak dan harapan tetap diatribusikan kepada responden. Data tujuan, perilaku, perasaan, serta kebutuhan dapat menjadi dasar Empathy Map, Persona, dan Journey pada worksheet berikutnya; pendalaman perlu dilakukan pada contoh kejadian yang masih umum.')
h('Sumber dan penelusuran data',2)
p('S1-S4: Rusdany Maestro, Worksheet 1 UX Detective, Worksheet 2 Design Challenge, Worksheet 3 User and Stakeholder, serta Worksheet 4 UX Research Plan pada Fleffy.\nR1-R3: catatan jawaban wawancara kasir laundry sepatu, Admin Operasional, dan owner, 15 Oktober 2026. Penanda Q1-Q13 merujuk panduan pada bagian 4 dan jawaban masing-masing responden. Ringkasan merupakan parafrasa; sumber asli disimpan terpisah.\nAcuan tugas: Instruksi Worksheet 5 User Interview mata kuliah Rekayasa Interaksi.')

# Foto disertakan sesuai label sesi yang diberikan pengguna.
for i,photo in enumerate(META.get('foto',[])):
 page('Lampiran dokumentasi wawancara '+photo.get('responden',''))
 path=Path(photo['path'])
 if path.exists():
  from PIL import Image as PILImage
  with PILImage.open(path) as im: w,hh=im.size
  width=min(15.0,15.5*w/hh)
  para=doc.add_paragraph();para.alignment=WD_ALIGN_PARAGRAPH.CENTER
  para.add_run().add_picture(str(path),width=Cm(width))
  p(photo['caption'])

doc.save(OUT)
(TMP/'report_content.txt').write_text('\n\n'.join(content),encoding='utf-8')
print(OUT)
print('Words:',len(' '.join(content).split()))
