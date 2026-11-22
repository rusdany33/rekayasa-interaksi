from pathlib import Path
import json

ROOT=Path(r'D:\Rekayasa Interaksi')
old=(ROOT/'tmp/worksheet8/build_worksheet8.py').read_text(encoding='utf-8')
helpers=old.split('REQS=[')[0].replace("TMP=ROOT/'tmp'/'worksheet8'", "TMP=ROOT/'tmp'/'worksheet10'")
helpers=helpers.replace('202210370311406_Rusdany_Maestro_Worksheet8_UXRequirements','202210370311406_Rusdany_Maestro_Worksheet10_UserFlow')
helpers=helpers.replace('Kebutuhan UX Pemeriksaan Pembayaran Transfer pada Fleffy','Alur Pengguna Pemeriksaan Pembayaran Transfer pada Fleffy')
helpers=helpers.replace('Worksheet 8 Rekayasa Interaksi','Worksheet 10 Rekayasa Interaksi')
exec(compile(helpers,'helper_dokumen','exec'),globals())

def fig(filename,alt):
    a=doc.add_paragraph();a.alignment=WD_ALIGN_PARAGRAPH.CENTER
    a.paragraph_format.space_after=Pt(2)
    a.paragraph_format.line_spacing=1
    shape=a.add_run().add_picture(str(TMP/filename),width=Cm(26.2))
    shape._inline.docPr.set('descr',alt)

def compact(text):return p(text,False,11)

# A Task Definition
doc.add_paragraph('Alur Pengguna Pemeriksaan Pembayaran Transfer pada Fleffy','Title')
doc.add_paragraph('Worksheet 10 Rekayasa Interaksi','Subtitle')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nJenis tugas: Praktikum Individu\nTanggal analisis: 15 Oktober 2026',False)
field('Berkas bukti pendukung','Worksheet 8 UX Requirements; Worksheet 9 Information Architecture; ringkasan wawancara R2 pada Worksheet 5. Rincian rujukan pada bagian C.',10.5)
h('A Task Definition')
p('Saya merancang alur pemeriksaan pembayaran Bank Transfer pada Fleffy agar admin dapat menentukan apakah satu pesanan boleh diteruskan ke teknisi. Alur usulan menjaga hubungan pesanan, bukti, permintaan, hasil pemeriksaan, dan keputusan. Bagian B membandingkan rekonstruksi alur saat ini dengan rancangan yang menggunakan struktur halaman Worksheet 9.')
field('User Task Goal','Ari ingin memperoleh kepastian penerimaan transfer pada satu pesanan yang sudah tercatat agar dapat menentukan bahwa pesanan boleh diteruskan ke teknisi berdasarkan hasil pemeriksa berwenang.')
field('Pengguna utama','Ari, nama samaran R2, admin operasional yang juga bertugas sebagai kasir, usia 20–22 tahun. Ari meminta owner atau finance memeriksa rekening. [S5 R2 Q1, Q6–Q8; S8; S9]')
field('Skenario','Pesanan deep cleaning dua pasang sepatu, transfer Rp150.000 melalui komunikasi WhatsApp. Pesanan telah dicatat sebelum alur dimulai. [S5 R2 Q4–Q8]')
h('Titik awal dan akhir',2)
compact('Awal usulan: Ari sudah masuk akun pada Beranda N0; pesanan Bank Transfer sudah tersimpan dan perlu diperiksa. Bukti pelanggan dapat tersedia atau masih memerlukan klarifikasi. Pembuatan pesanan dan proses masuk akun merupakan prasyarat, sehingga tidak diulang dalam alur.')
compact('Akhir berhasil: hasil yang memadai untuk pesanan dan data terbaru telah ditinjau, lalu keputusan Teruskan beserta dasarnya berhasil tersimpan. Pesanan siap diteruskan ke teknisi. Penyerahan fisik dan pengerjaan laundry berada di luar batas tugas ini.')
compact('Akhir sementara: T1 perlu klarifikasi data, T2 masih menunggu hasil, atau T3 hasil belum memadai. Ketiganya belum mencapai tujuan. Alur dapat dilanjutkan pada pesanan yang sama setelah kondisi penyebabnya ditangani.')

# B Current Flow diagram
landscape()
h('B Current Flow vs Proposed Flow')
compact('1 Alur saat ini direkonstruksi dari penjelasan R2. P1 dan P2 menandai hambatan yang menjadi dasar perbaikan.')
fig('current_flow.png','Alur saat ini dari pesanan tercatat melalui Fleffy dan WhatsApp menuju pemeriksaan owner atau finance, penantian konfirmasi, lalu meneruskan pesanan.')
compact('Gambar 1 Current Flow. Sumber: S5 R2 Q6–Q8; tindak lanjut telepon mengikuti pola kondisional Q9. Ini bukan hasil observasi klik langsung.')

portrait()
h('2 Penjelasan alur saat ini')
p('R2 menjelaskan perpindahan antara catatan Fleffy, bukti transfer pada WhatsApp pelanggan, dan komunikasi dengan owner atau finance. R2 sudah membedakan pencatatan pembayaran dari penerimaan dana; alur saat ini tidak diasumsikan meneruskan pesanan hanya karena label pembayaran. [S5 R2 Q6–Q8]')
table(['ID','Langkah atau keputusan','Hasil dan hubungan berikutnya'],[
('C1','Membuka pesanan yang telah tercatat di Fleffy.','Identitas dan nominal pesanan menjadi acuan saat melihat bukti pelanggan.'),
('C2','Membuka bukti transfer di WhatsApp pelanggan; mencocokkan nominal serta tanggal atau waktu.','Konteks bukti digunakan untuk meminta pemeriksaan. Nominal saja tidak cukup membedakan pesanan.'),
('C3','Mengirim rujukan pesanan dan bukti kepada owner atau finance melalui WhatsApp.','Pemeriksa berwenang mengecek mutasi rekening. Pemeriksaan rekening bukan aktivitas Ari.'),
('D1','Apakah konfirmasi dana masuk telah diterima?','Ya menuju C5. Belum menuju C4; pengiriman pesan belum menjadi konfirmasi penerimaan dana.'),
('C4','Menunggu balasan dan menghubungi kembali bila diperlukan.','Memeriksa kembali apakah hasil sudah diterima. Telepon adalah pola yang dilaporkan pada Q9, bukan kepastian terjadi pada kasus Rp150.000.'),
('C5','Mengonfirmasi pembayaran dan meneruskan pesanan setelah mendapat konfirmasi.','Akhir rekonstruksi: pesanan diteruskan berdasarkan konfirmasi. Tidak diasumsikan telah ada catatan keputusan terstruktur pada aplikasi.')
],[1.2,6.6,8.2],11)
h('Titik masalah pada Current Flow',2)
field('P1 Perpindahan sumber','Rujukan pesanan, bukti, dan balasan pemeriksa berada pada sumber yang berbeda. Ari perlu menghubungkan ketiganya saat memeriksa. [S5 R2 Q6–Q8; S8 UX02]')
field('P2 Penantian konfirmasi','Ari bergantung pada balasan pemeriksa sebelum meneruskan pesanan. R2 melaporkan rasa cemas serta kemungkinan pelayanan atau pengerjaan tertunda. Waktu tunggu rata-rata dan frekuensinya belum diukur. [S5 R2 Q9–Q11; S8 UX03–UX04]')
compact('Cabang bukti tidak cocok, kegagalan penyimpanan, dan hasil tidak berwenang pada rancangan berikut adalah kondisi antisipasi. Wawancara belum membuktikan bahwa kejadian tersebut pernah terjadi.')

landscape()
h('3 Proposed Flow bagian A')
compact('Mulai dari pesanan yang sudah tercatat. Pemeriksaan keberadaan permintaan dilakukan sebelum pengiriman atau pengiriman ulang.')
fig('proposed_flow_a.png','Alur usulan bagian A dari Beranda melalui Pesanan dan Detail Pesanan, memeriksa kecukupan bukti, menggunakan permintaan yang ada atau mengirim dengan pemulihan kegagalan, lalu ke konektor A.')
compact('Gambar 2 Bagian A. Kedua konektor A menuju satu titik masuk pada Gambar 3; T1 adalah penundaan untuk klarifikasi.')

# Same landscape section, new page
h('4 Proposed Flow bagian B',page=True)
compact('Hasil yang tersedia diperiksa kecukupannya sebelum keputusan lanjut disimpan. T2 dan T3 merupakan akhir sementara.')
fig('proposed_flow_b.png','Alur usulan bagian B memeriksa ketersediaan dan kecukupan hasil, menunda atau menahan pesanan bila belum memadai, lalu mencatat keputusan lanjut dan memeriksa keberhasilan penyimpanannya.')
compact('Gambar 3 Bagian B. Pemeriksaan rekening tetap dilakukan owner atau finance. Keberhasilan baru terjadi setelah keputusan tersimpan.')

portrait()
h('5 Rincian langkah Proposed Flow bagian A')
compact('Nama menu dan ID halaman mengikuti Worksheet 9. Bagian Pembayaran, Pemeriksaan, dan Tindak Lanjut berada dalam halaman kanonis Detail Pesanan N1b; bukan halaman tambahan.')
table(['ID','Aksi atau keputusan','Informasi dan arah berikutnya'],[
('P0–P1','Dari Beranda N0 memilih Pesanan N1, mencari dan memilih pesanan transfer.','Daftar menampilkan identitas yang membedakan pesanan. Pilihan membuka N1b milik pesanan tersebut.'),
('P2','Pada N1b bagian Pembayaran, meninjau identitas, nominal, dan bukti pelanggan.','Pembayaran tercatat dibedakan dari penerimaan yang telah diperiksa. Bukti/rujukannya disandingkan dengan data pesanan.'),
('D1','Apakah data dan bukti cukup serta cocok untuk pemeriksaan?','Ya menuju P3. Tidak menuju E1. Kecukupan mencakup identitas dan nominal serta informasi waktu/pembanding yang tersedia; bukan nominal saja.'),
('E1–T1','Mengklarifikasi bukti atau memperbaiki catatan yang keliru secara terkontrol.','Bukti asli dipertahankan; sumber dan perubahan dapat ditelusuri. Jika belum selesai, T1. Setelah jelas, lanjutkan P2. Hasil lama tidak berlaku untuk data yang berubah.'),
('P3','Pada N1b bagian Pemeriksaan, meninjau rujukan pesanan dan pemeriksa sesuai prosedur usaha.','Identitas pemeriksa ditampilkan bila telah ditetapkan; jangan mengklaim pemeriksa menerima atau sedang bekerja tanpa dasar.'),
('D2','Apakah permintaan untuk pesanan dan data yang sama sudah ada?','Ya memakai permintaan tersebut melalui konektor A. Tidak menuju P4. Permintaan lama atas data yang berubah perlu klarifikasi atau pembaruan konteks terlebih dahulu.'),
('P4','Mengirim permintaan menggunakan identitas pesanan dan nominal yang tersimpan.','Data yang sudah benar tidak diketik ulang. Permintaan mengacu bukti dan pemeriksa yang tepat.'),
('D3','Apakah permintaan berhasil dicatat?','Ya menuju P5. Gagal atau belum pasti menuju E2. Status berhasil hanya tampil setelah pencatatan terkonfirmasi.'),
('E2','Mempertahankan data, memeriksa kendala dan keberadaan permintaan.','Kembali ke D2 sebelum mencoba kirim ulang. Jika hasil kirim belum diketahui, rekonsiliasi dahulu agar tidak membuat permintaan ganda.'),
('P5–A','Menampilkan rujukan permintaan, pemeriksa sesuai penetapan, dan keadaan Menunggu hasil.','Lanjutkan melalui konektor A ke D4 pada Bagian B. Permintaan tercatat belum berarti dana masuk.')
],[1.4,6.1,8.5],10.8)
compact('Sebelum permintaan dikirim, rujukan yang salah harus diperbaiki. Mekanisme perubahan data serta penetapan dan penggantian pemeriksa perlu disepakati dengan usaha; alur ini tidak menetapkan hak akses baru secara sepihak.')

h('6 Rincian langkah Proposed Flow bagian B',page=True)
table(['ID','Aksi atau keputusan','Feedback dan arah berikutnya'],[
('A–D4','Membuka permintaan yang sama; memeriksa apakah hasil telah tersedia.','Belum menuju P6–T2. Ya menuju P7. Hasil dapat datang dari owner atau finance melalui prosedur yang disepakati; tidak diasumsikan integrasi bank otomatis.'),
('P6–T2','Meninjau keadaan Menunggu hasil dan tindak lanjut bila diperlukan.','Panduan atau kontak pemeriksa dapat dibuka melalui Bantuan Pemeriksaan. Kondisi belum pasti dijelaskan tanpa janji waktu selesai. T2 dapat dilanjutkan saat hasil tersedia.'),
('P7','Membaca hasil, sumber pemeriksa, rujukan pesanan, dan informasi pembanding.','Tampilan membedakan hasil pemeriksaan dari catatan pembayaran. Informasi yang tidak tersedia dinyatakan belum tersedia, bukan ditebak.'),
('D5','Apakah hasil memadai untuk keputusan lanjut?','Ya hanya jika berasal dari pemeriksa berwenang, merujuk pesanan dan data terbaru, cocok dengan informasi pembanding yang diperlukan, serta mengonfirmasi dana diterima. Tidak menuju P8–T3; Ya menuju P9.'),
('P8–T3','Menahan pesanan dan meminta klarifikasi atau pemeriksaan lanjutan sesuai alasan.','Belum ada dasar meneruskan pesanan. Catat alasan/rujukan tindak lanjut. T3 dapat dilanjutkan setelah klarifikasi atau hasil baru untuk konteks data yang benar.'),
('P9','Pada N1b bagian Tindak Lanjut, meninjau dasar dan mencatat keputusan Teruskan.','Keputusan terhubung dengan hasil dan petugas sesuai kewenangan. Tidak ada pengisian ulang identitas atau nominal yang masih benar.'),
('D6\nE3','Memeriksa apakah keputusan berhasil tersimpan.','Ya menuju S. Gagal/belum pasti: tetap pada pesanan, cek catatan keputusan dan kendala sebelum mengulang P9; hindari pencatatan ganda.'),
('S','Menerima konfirmasi bahwa keputusan lanjut berhasil tercatat.','Keputusan, dasar, dan identitas pesanan dapat ditinjau kembali. Pesanan siap diteruskan ke teknisi. Inilah akhir berhasil untuk tugas yang dipilih.')
],[1.4,6.1,8.5],11)
h('Jalur kembali tanpa kehilangan konteks',2)
compact('Dari T2, Ari dapat membuka Pemeriksaan Pembayaran N2, memilih pesanan yang sama, lalu mengikuti TS1 menuju N1b bagian Pemeriksaan. Antrean memuat pesanan Belum diminta, Menunggu hasil, atau Hasil tersedia sesuai keadaan yang memiliki dasar. Pemilihan pesanan tidak membuat permintaan baru.')
compact('Bantuan bersifat opsional melalui TS2 ke N3a Arti Status Pembayaran, N3b Panduan saat Menunggu, atau N3c Kontak Pemeriksa. Kembali dari bantuan mempertahankan pesanan dan bagian asal. Navigasi NH1 menghubungkan bagian dalam N1b. Pilihan kembali ke antrean mempertahankan pencarian atau filter. [S9]')

h('7 Kemungkinan kesalahan hambatan dan pemulihan',page=True)
compact('Tabel ini mengantisipasi kondisi rancangan, kecuali penantian yang memang dilaporkan R2. Penanganan rinci mengikuti kewenangan dan prosedur usaha yang masih perlu dikonfirmasi.')
table(['Kondisi dan letak','Dampak pada tujuan','Penanganan dan jalur pemulihan'],[
('Pesanan keliru atau dua pesanan bernominal sama; P1–D1.','Bukti atau hasil dapat dikaitkan ke pesanan yang salah.','Tampilkan identitas selain nominal; kembali ke P1 jika salah memilih. D1 belum lolos sebelum konteks pesanan cocok.'),
('Bukti tidak jelas, kurang informasi, atau tidak cocok; D1–E1.','Pemeriksa belum memiliki dasar pembanding yang cukup.','Klarifikasi ke pelanggan; pertahankan bukti asli. T1 bila belum jelas; setelah benar, tinjau ulang pada P2.'),
('Data pesanan berubah setelah permintaan atau hasil dibuat; P2–P3 dan D5.','Hasil lama dapat merujuk konteks yang tidak lagi berlaku.','Tandai perubahan; jangan memakai hasil lama sebagai dasar lanjut. Klarifikasi atau perbarui pemeriksaan untuk data terbaru; kembali P2–P3.'),
('Koneksi gagal, pengiriman terputus, atau hasil kirim belum pasti; D3–E2.','Ari tidak tahu apakah permintaan tercatat; mencoba ulang berisiko duplikat.','Pertahankan input; jelaskan kendala. Cek keberadaan permintaan melalui D2 sebelum kirim ulang; gunakan rujukan yang sudah tercatat jika ada.'),
('Owner/finance belum memberi hasil; D4–P6. Dilaporkan R2 Q9–Q11.','Keputusan lanjut belum memiliki dasar; pelayanan atau pengerjaan dapat tertunda.','T2 tetap Menunggu hasil. Tampilkan penanggung jawab sesuai penetapan serta panduan/kontak; kembali melalui N2 dan TS1 tanpa membuat permintaan baru.'),
('Hasil tidak cocok, rujukan tidak jelas, sumber tidak berwenang, atau dana belum terkonfirmasi; D5–P8.','Keputusan lanjut belum memiliki dasar yang memadai.','T3 tahan pesanan dengan alasan; minta pemeriksaan lanjutan. Setelah hasil yang benar tersedia, ulangi P7–D5. Dana belum terkonfirmasi tidak otomatis berarti belum ditransfer.'),
('Penyimpanan keputusan gagal atau belum pasti; D6–E3.','Klik Teruskan dapat dianggap berhasil padahal catatan belum pasti.','Jangan tampilkan sukses. Pertahankan konteks, cek catatan yang sudah tersimpan, lalu ulangi P9 dengan aman bila belum tercatat.')
],[5.0,4.0,7.0],11)
h('Penghentian oleh pengguna',2)
compact('Jika Ari meninggalkan alur sebelum S, tidak ada klaim tujuan berhasil. Permintaan atau keputusan yang sudah benar-benar tersimpan tetap dapat ditemukan pada pesanan yang sama. Data yang belum tersimpan perlu diberi penjelasan sebelum pengguna keluar; alur tidak mengasumsikan penyimpanan otomatis.')

h('8 Peluang perbaikan dan hubungan kebutuhan UX',page=True)
p('Perbaikan utama adalah menyediakan satu konteks Detail Pesanan untuk meninjau pembayaran, permintaan, hasil, dan dasar keputusan. Kebutuhan kepastian dan koordinasi tetap lebih penting daripada sekadar mengurangi langkah. Permintaan, hasil tersedia, dan hasil memadai menjadi tiga kondisi yang berbeda. [S8 UX01–UX05; S9 N1b]')
table(['Kebutuhan dan prioritas S8','Penerapan pada alur usulan','Manfaat yang dituju'],[
('UX05 Must urutan 1','D5, P8–T3, P9, D6, S: lanjut hanya berdasar hasil memadai dan keputusan tersimpan.','Keputusan meneruskan atau menahan memiliki dasar untuk pesanan yang sama.'),
('UX03 Must urutan 2','P3–P5 dan D4: pemeriksa sesuai penetapan, rujukan permintaan, serta keadaan hasil.','Ari mengetahui pihak yang dituju dan apakah hasil sudah tersedia.'),
('UX02 Must urutan 3','P1–P2, D1–D2, P7–D5: identitas, nominal, bukti, dan hasil terhubung pada N1b.','Konteks pembayaran dapat ditelusuri, termasuk bila nominal dua pesanan sama.'),
('UX01 Must urutan 4','P2, P5, P7: informasi pembayaran tercatat, permintaan, dan hasil diperjelas.','Ari dapat menjelaskan kepastian yang sudah ada serta yang masih perlu diperoleh.'),
('UX04 Should urutan 5','P6–T2 dan jalur bantuan TS2 ke N3a–N3c.','Tindak lanjut saat menunggu dan penjelasan kepada pelanggan mengikuti kondisi sebenarnya.'),
('UX06 Should urutan 6','P4 memakai identitas/nominal tersimpan; E2 dan E3 menjaga konteks ketika mencoba ulang.','Kelancaran pencatatan yang dinilai baik tetap terjaga; mengisi ulang bukan masalah yang telah terbukti terjadi.')
],[4.0,7.0,5.0],11)
h('Perbandingan Current Flow dan Proposed Flow',2)
compact('Pada P1 alur saat ini, informasi dipadankan melalui sumber terpisah. Usulan menyatukan rujukannya pada N1b dan memakai data pesanan yang benar. Kebutuhan tetap dapat dipenuhi melalui prosedur pencatatan hasil yang disepakati; alur belum menetapkan API bank atau akses rekening bagi Ari.')
compact('Pada P2 alur saat ini, pengguna menunggu balasan pemeriksa. Usulan menjelaskan keadaan yang diketahui, pihak yang dituju, dan jalur kembali ke pesanan. Kejelasan ini belum membuktikan owner merespons lebih cepat atau waktu pelayanan berkurang.')
compact('Sebelum diterapkan, usaha perlu memastikan siapa yang boleh mengirim hasil, cara menautkan hasil ke pesanan/data terbaru, penanganan selisih, serta kewenangan pencatatan keputusan. Penambahan ini adalah rancangan yang perlu diuji, bukan perilaku Fleffy yang telah diverifikasi.')

h('C Flow Check Evaluation',page=True)
compact('Pemeriksaan berikut merupakan inspeksi rancangan oleh peneliti terhadap diagram dan tabel. Penandaan terpenuhi tidak menyatakan bahwa pengujian pengguna sudah dilaksanakan.')
table(['Cek','Kriteria workbook','Dasar pemeriksaan rancangan'],[
('[x]','User goal jelas','Bagian A menetapkan satu tugas, titik awal P0 dan sukses S. Penyerahan fisik ke teknisi berada di luar batas tugas.'),
('[x]','Tidak ada langkah tidak perlu','Tidak mengulang masuk akun atau membuat pesanan. D2 memakai permintaan yang ada; P4 memakai data tersimpan. Bantuan hanya ketika diperlukan.'),
('[x]','Error condition diperhatikan','D1–E1, D3–E2, D5–P8, dan D6–E3 mempunyai penanganan, jalur kembali, atau akhir sementara yang dijelaskan pada bagian 7.'),
('[x]','Feedback diberikan','P5 memberi rujukan dan keadaan permintaan; P6 menjelaskan penantian; P7 menunjukkan sumber hasil; D3/D6 membedakan gagal atau belum pasti dari berhasil.'),
('[x]','Success state jelas','S dicapai sesudah D5 memadai dan D6 mengonfirmasi keputusan tersimpan. T1–T3 tidak ditandai sebagai sukses.')
],[1.1,5.0,9.9],11)
h('Rencana validasi sebelum wireframe ditetapkan',2)
compact('Uji alur dengan Ari atau pengguna yang memiliki tugas serupa: (1) hasil sesuai sampai S; (2) dua pesanan bernominal sama; (3) bukti kurang jelas dan perubahan data; (4) hasil masih ditunggu serta kembali dari bantuan; (5) hasil tidak cocok atau sumber tidak jelas; (6) koneksi terputus ketika mengirim permintaan atau menyimpan keputusan.')
compact('Catat apakah pengguna memilih pesanan yang benar, membedakan catatan dan hasil, menahan saat dasar belum cukup, menemukan jalur kembali, serta mengenali keberhasilan penyimpanan. Keberhasilan tugas harus didukung tindakan dan penjelasan pengguna, bukan hanya pengakuan mudah digunakan. Belum ada hasil uji, angka keberhasilan, atau penghematan waktu yang dilaporkan.')
h('Sumber dan batas bukti',2)
compact('S8: Rusdany Maestro, Worksheet 8 UX Requirements, bagian pemetaan, daftar UX01–UX06, prioritas, serta kriteria keterpenuhan. S9: Rusdany Maestro, Worksheet 9 Information Architecture, bagian inventaris, struktur halaman N0–N3c, dan hubungan TS1, TS2, NH1.')
compact('S5: Rusdany Maestro, Worksheet 5 User Interview, jawaban R2 Q4 serta Q6–Q11. Wawancara langsung 15 Oktober 2026 di Pesenkopi sebagai tempat pertemuan, durasi 12 menit; konteks usaha laundry sepatu. Jawaban merupakan parafrasa, bukan kutipan verbatim. Rekonstruksi Current Flow tidak menggantikan observasi langsung.')
compact('W: UX Design Hands-on Workbook, Pertemuan 10 User Flow, bagian A Task Definition, B Current Flow vs. Proposed Flow, C Flow Check Evaluation. Instruksi dan rubrik Worksheet 10 dari Google Classroom menjadi acuan tambahan. Seluruh diagram dibuat untuk analisis ini.')

# Deterministic font/theme cleanup for Word and Google Docs
for tree in (doc.element,doc.styles.element,doc.sections[0].footer._element):
    for fonts in tree.iter(qn('w:rFonts')):
        fonts.attrib.clear()
        for attr in ('ascii','hAnsi','eastAsia','cs'):fonts.set(qn('w:'+attr),'Times New Roman')
    for border in list(tree.iter(qn('w:pBdr'))):border.getparent().remove(border)
    for rp in tree.iter(qn('w:rPr')):
        sp=rp.find(qn('w:spacing'))
        if sp is not None:rp.remove(sp)
    for color in tree.iter(qn('w:color')):
        color.attrib.clear();color.set(qn('w:val'),'000000')

raw=TMP/(STEM+'_sebelum_sanitasi.docx')
doc.save(raw)
texts=[a.text for a in doc.paragraphs if a.text.strip()]
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:texts.extend(a.text for a in c.paragraphs if a.text.strip())
(TMP/'report_content.txt').write_text('\n\n'.join(texts),encoding='utf-8')
(TMP/'content_blocks.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'raw_docx':str(raw),'paragraphs':len(doc.paragraphs),'tables':len(doc.tables),'images':len(doc.inline_shapes),'sections':len(doc.sections)},ensure_ascii=False))
