from pathlib import Path
import json

# Pakai ulang helper tipografi laporan sebelumnya tanpa memuat isinya.
previous=Path(r'D:\Rekayasa Interaksi\tmp\worksheet8\build_worksheet8.py').read_text(encoding='utf-8')
helpers=previous.split('REQS=[')[0].replace("TMP=ROOT/'tmp'/'worksheet8'","TMP=ROOT/'tmp'/'worksheet9'")
helpers=helpers.replace('202210370311406_Rusdany_Maestro_Worksheet8_UXRequirements','202210370311406_Rusdany_Maestro_Worksheet9_InformationArchitecture')
helpers=helpers.replace('Kebutuhan UX Pemeriksaan Pembayaran Transfer pada Fleffy','Struktur Informasi Pesanan dan Pemeriksaan Pembayaran Fleffy')
helpers=helpers.replace('Worksheet 8 Rekayasa Interaksi','Worksheet 9 Rekayasa Interaksi')
exec(compile(helpers,'helper_dokumen','exec'),globals())
DATA=json.loads((TMP/'ia_data.json').read_text(encoding='utf-8'))
INV=DATA['inventory']

# Halaman 1
doc.add_paragraph('Struktur Informasi Pesanan dan Pemeriksaan Pembayaran Fleffy','Title')
doc.add_paragraph('Worksheet 9 Rekayasa Interaksi','Subtitle')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nJenis tugas: Praktikum Individu\nTanggal analisis: 15 Oktober 2026',False)
field('Berkas bukti pendukung','Worksheet 8 UXRequirements; Worksheet 6 EmpathyMapPersona; Worksheet 7 UserJourney. Template: UX Design Hands-on Workbook, Pertemuan 09.',10.5)
h('1 Produk tujuan dan batas struktur')
p('Saya menyusun Information Architecture usulan untuk Fleffy - Kasir Laundry Sepatu pada pencatatan pesanan dan pemeriksaan pembayaran Bank Transfer. Struktur terdiri dari Beranda, tiga kelompok informasi utama, serta lima halaman pendukung. Satu Detail Pesanan menjadi tempat utama untuk menelusuri bukti, hasil pemeriksaan, dan dasar tindak lanjut pesanan.')
p('Tujuannya adalah membantu Ari menemukan pesanan yang benar, membedakan pembayaran tercatat dan hasil pemeriksaan, mengetahui pemeriksa, lalu menentukan tindak lanjut sesuai kewenangan. Enam kebutuhan UX pada Worksheet 8 menjadi dasar inventaris, kategori, dan navigasi. [S8 bagian 3-9]')
h('Pengguna dan cakupan',2)
p('Ari adalah nama samaran Persona admin operasional yang juga menjalankan tugas kasir. Ia mencatat transaksi melalui Fleffy dan meminta owner atau finance memeriksa rekening. Struktur ini menampilkan informasi yang diperlukan untuk koordinasi; akses rekening langsung tidak dimasukkan ke tugas Ari. [S8 bagian 1 dan UX03-UX05]')
p('Cakupan dimulai dari pencatatan atau pencarian pesanan dan berakhir pada keputusan sebelum meneruskan pesanan ke teknisi. Detail pencucian, pengiriman, pengambilan, stok, serta pengaturan usaha di luar pemeriksaan tidak dipetakan. Halaman login dan fitur umum di luar skenario tidak dirinci.')
h('Dasar keputusan struktur',2)
field('Kepastian informasi','UX01 menjelaskan makna informasi; UX02 menghubungkan pesanan, nominal, bukti, dan hasil; UX05 mendukung keputusan tindak lanjut. Informasi utama berada pada Detail Pesanan.')
field('Koordinasi dan kelancaran','UX03 mendasari antrean dan penanggung jawab; UX04 mendasari bantuan saat menunggu; UX06 mempertahankan konteks data agar tidak diisi ulang hanya untuk meminta pemeriksaan.')
p('Seluruh halaman, nama menu, keadaan permintaan, serta tautan pada laporan ini adalah usulan rancangan yang perlu diuji. Diagram menggambarkan pengelompokan dan hubungan informasi, bukan urutan langkah User Flow.',False,11)

# Halaman 2 dan 3
for start in (0,8):
    h('2 Bagian A Content Inventory' if start==0 else 'Content Inventory lanjutan',page=True)
    p('Tiga kolom mengikuti template workbook. C01-C16 adalah kode informasi atau fitur; N0-N3c adalah lokasi pada sitemap. Prioritas Must menandai informasi inti untuk kebutuhan wajib, sedangkan Should menandai dukungan atau pemeliharaan pengalaman. [S8 UX01-UX06]',False,11)
    rows=[(x['id']+' '+x['name']+'\nLokasi: '+x['location'],x['need'],x['priority']) for x in INV[start:start+8]]
    table(['Content / Feature','User Need','Priority'],rows,[6.5,7.2,2.3],size=11)
    if start==0:
        p('C01-C08 mencakup informasi inti dan akses ke pesanan. Pencarian ditempatkan bersama daftar pesanan untuk mendukung pencocokan; nominal saja tidak menjadi identitas pesanan.',False,11)
    else:
        p('C09 adalah pencatatan dasar yang dipertahankan; Should mengikuti fokus pemeliharaan UX06, bukan berarti pencatatan boleh dihilangkan dari produk. Panduan lengkap C11 berprioritas Should; penjelasan makna inti tetap Must pada C02. C14 dan C16 adalah dukungan penemuan informasi yang diturunkan dari kebutuhan, belum merupakan permintaan fitur yang diuji.',False,11)

# Halaman 4
landscape()
h('3 Bagian B Sitemap')
p('Sitemap usulan dengan tiga kelompok utama. Garis penuh menunjukkan hierarki; panah putus-putus TS1 menghubungkan antrean ke Detail Pesanan yang sama.',False,11)
pic=doc.add_paragraph();pic.alignment=WD_ALIGN_PARAGRAPH.CENTER
pic.paragraph_format.space_after=Pt(2)
shape=pic.add_run().add_picture(str(TMP/'sitemap_fleffy.png'),width=Cm(26.2))
shape._inline.docPr.set('descr','Sitemap usulan Fleffy. Beranda memiliki Pesanan, Pemeriksaan Pembayaran, dan Bantuan Pemeriksaan. Pesanan memiliki Buat Pesanan dan Detail Pesanan. Detail memuat empat bagian. Bantuan memiliki Arti Status Pembayaran, Panduan saat Menunggu, dan Kontak Pemeriksa. Tautan TS1 membuka Detail Pesanan bagian Pemeriksaan dari antrean.')
p('Sembilan halaman, kedalaman maksimum L2. TS2 bantuan dan NH1 navigasi bagian dijelaskan pada bagian 6.',False,11)

# Halaman 5
portrait()
h('4 Bagian C Card Sorting Mini Exercise')
p('Saya melakukan latihan pengelompokan oleh peneliti berdasarkan tujuan dan kebutuhan pada Worksheet 8. Latihan ini menggunakan 15 kartu C01-C13 serta C15-C16, kemudian menempatkan setiap kartu pada satu dari tiga kategori. Ini belum merupakan sesi card sorting bersama pengguna dan belum membuktikan mental model Ari.')
groups=[
('Category 1 Pesanan','C01 Ringkasan pesanan; C02 Catatan pembayaran; C03 Bukti dan pembanding; C06 Dasar keputusan; C08 Daftar dan pencarian; C09 Pencatatan pesanan; C10 Pemanfaatan ulang konteks.','Dikelompokkan karena membantu mencatat, menemukan, dan menentukan tindak lanjut satu pesanan. Mendukung UX01, UX02, UX05, dan UX06.'),
('Category 2 Pemeriksaan Pembayaran','C04 Permintaan pemeriksaan; C05 Hasil dan sumber; C07 Antrean dan penanggung jawab; C15 Jejak pemeriksaan dan keputusan; C16 Penyaringan antrean.','Dikelompokkan karena membantu memperoleh serta menelusuri hasil dari pemeriksa yang berwenang. Mendukung UX01, UX02, UX03, dan UX05.'),
('Category 3 Bantuan Pemeriksaan','C11 Arti status; C12 Panduan saat menunggu; C13 Kontak pemeriksa.','Dikelompokkan karena memberi penjelasan dan dukungan ketika pengguna perlu memahami keadaan atau menindaklanjuti penantian. Mendukung UX01 dan UX04.')
]
table(['Kategori','Daftar kartu','Alasan pengelompokan'],groups,[3.6,6.8,5.6],size=11)
h('Perlakuan terhadap Beranda dan konten bersama',2)
p('C14 Beranda tidak menjadi kartu kategori terpisah karena isinya merupakan ringkasan dan pintasan dari ketiga kelompok. Dengan demikian, seluruh 16 item inventaris tetap memiliki tempat: 15 kartu dikategorikan dan satu item menjadi agregasi lintas kategori.')
p('Kategori adalah pengelompokan tujuan informasi, sedangkan halaman menentukan lokasi penyajiannya. C04, C05, dan C15 termasuk kelompok Pemeriksaan Pembayaran, tetapi informasi rinci tetap berada dalam Detail Pesanan. Antrean N2 menautkan informasi itu melalui TS1, tanpa membuat salinan bukti atau hasil pemeriksaan.')
h('Alasan pemilihan nama kategori',2)
p('Pesanan mengacu pada objek kerja Ari. Pemeriksaan Pembayaran menjelaskan kegiatan memperoleh kepastian dana, berbeda dari sekadar mencatat pembayaran. Bantuan Pemeriksaan menyatakan isi panduan dan kontak. Ketiga label perlu diperiksa keterpahamannya pada pengguna dengan tugas serupa; label belum dinyatakan tervalidasi.')

# Halaman 6
h('5 Hierarki halaman utama dan halaman pendukung',page=True)
p('L0 adalah halaman awal, L1 adalah kelompok utama, dan L2 adalah halaman pendukung. Kedalaman maksimum dua hubungan di bawah Beranda dipilih agar informasi inti tidak tersembunyi dalam banyak lapisan. Empat bagian pada Detail Pesanan tetap berada pada L2.',False,11)
table(['ID','Halaman','Level','Isi dan hubungan'],DATA['pages'],[1.2,4.2,1.4,9.2],size=11)
h('Detail Pesanan sebagai tempat utama',2)
p('Ringkasan Pesanan memuat identitas dan tagihan. Pembayaran memuat catatan pembayaran serta bukti pelanggan. Pemeriksaan memuat permintaan, pemeriksa, keadaan permintaan, dan hasil. Tindak Lanjut memuat dasar serta catatan keputusan. Identitas pesanan tetap terlihat ketika pengguna berpindah bagian.')
p('Isi yang sama dapat ditemukan melalui Pesanan maupun Pemeriksaan Pembayaran, tetapi rujukannya tetap satu Detail Pesanan. Perbedaan jalur masuk mempermudah penemuan tanpa membuat dua versi hasil pemeriksaan. Informasi hasil tidak diganti menjadi akses mutasi bank penuh untuk Ari.',False,11)

# Halaman 7
h('6 Hubungan antarhalaman',page=True)
p('Hubungan H1-H3 membentuk hierarki; TS1-TS2 merupakan tautan lintas kelompok; NH1 menghubungkan bagian dalam satu halaman. Tabel menjelaskan perilaku perpindahan yang menjadi dasar User Flow berikutnya, tanpa mengubah sitemap menjadi urutan tindakan.',False,11)
table(['ID','Asal dan tujuan','Jenis hubungan','Tujuan dan konteks yang dijaga'],DATA['links'],[1.2,4.8,3.2,6.8],size=11)
h('Hubungan setelah pencatatan',2)
p('Setelah pesanan disimpan dari N1a, pengguna membuka N1b untuk pesanan yang baru dicatat. Identitas dan nominal yang sudah benar digunakan kembali ketika permintaan pemeriksaan dibuat. Hubungan ini mendukung UX06; cara penyimpanan serta rincian interaksi akan dirancang pada User Flow dan wireframe.')
h('Hubungan hasil dan tindak lanjut',2)
p('Dalam N1b, hasil dari pemeriksa dihubungkan dengan rujukan pesanan serta informasi pembanding. Bagian Tindak Lanjut memakai hasil itu sebagai dasar keputusan. Jika hasil belum tersedia, tidak cocok, atau rujukannya belum jelas, pengguna mendapat arah untuk pemeriksaan lanjutan sesuai prosedur. Cabang tersebut adalah usulan rancangan, bukan kejadian baru dari riset. [S8 UX02, UX03, UX05]')

# Halaman 8
h('7 Struktur navigasi dan penamaan informasi',page=True)
h('Navigasi global dan lokal',2)
p('Navigasi global memuat empat tujuan: Beranda, Pesanan, Pemeriksaan Pembayaran, dan Bantuan Pemeriksaan. Beranda adalah pintu masuk agregasi; tiga tujuan lain mengikuti kategori latihan pengelompokan. Tujuan aktif ditandai secara konsisten. Susunan ini membatasi jumlah tujuan utama dan memakai istilah yang menjelaskan isi halaman.')
p('Navigasi lokal Pesanan menyediakan Buat Pesanan, daftar/pencarian, dan akses Detail Pesanan. Pada N1b, tautan Ringkasan Pesanan, Pembayaran, Pemeriksaan, serta Tindak Lanjut berpindah bagian dalam halaman. Bantuan dapat dibuka secara global maupun dari konteks Pemeriksaan.')
field('Petunjuk lokasi','Contoh jejak lokasi: Pesanan > Detail Pesanan. Saat masuk dari antrean, penanda asal Pemeriksaan Pembayaran dipertahankan agar Kembali membawa pengguna ke antrean dan penyaring sebelumnya.',11)
h('Tiga jenis informasi yang perlu dibedakan',2)
table(['Jenis informasi','Label dan makna yang diusulkan','Lokasi'],[
('Catatan pembayaran','Pembayaran tercatat menunjukkan data pembayaran yang disimpan; tidak sendirinya menjamin dana sudah masuk.','N1b Pembayaran'),
('Keadaan permintaan','Belum diminta berarti permintaan belum dibuat; pemeriksa belum tentu ditetapkan. Menunggu hasil atau Hasil tersedia mengikuti catatan permintaan. Hasil tersedia belum berarti hasil sesuai.','N2 dan N1b Pemeriksaan'),
('Hasil pemeriksaan','Hasil sesuai atau Perlu pemeriksaan lanjutan disertai rujukan pesanan, sumber pemeriksa, dan penjelasan yang tersedia.','N1b Pemeriksaan dan dasar Tindak Lanjut')
],[3.3,9.0,3.7],size=11)
p('Label keadaan dan hasil adalah usulan penyajian. Sistem tidak boleh menyatakan pemeriksa sedang bekerja, dana pasti masuk, atau waktu selesai tanpa dasar informasi yang tersedia. Hak mencatat hasil dan mengubah keputusan perlu mengikuti kewenangan usaha serta diperiksa pada rancangan berikutnya. [S8 UX01, UX03-UX05]',False,11)
h('Pencarian dan bantuan kontekstual',2)
p('Pencarian pesanan menggunakan identitas pesanan atau konteks pelanggan, dengan nominal sebagai informasi pembanding. Penyaring N2 mengelompokkan keadaan permintaan. Tautan bantuan memakai label Arti Status Pembayaran, Panduan saat Menunggu, dan Kontak Pemeriksa agar tujuan dapat diperkirakan sebelum dibuka. Hasil pencarian kosong perlu memberi arah untuk memeriksa kata pencarian tanpa menghilangkan konteks yang sudah ada.',False,11)

# Halaman 9
h('8 Potensi kebingungan dan peluang perbaikan',page=True)
p('Risiko berikut adalah penilaian terhadap struktur usulan. Risiko ini belum merupakan hasil pengujian pengguna atau bukti bahwa kesalahan tersebut telah terjadi pada aplikasi.',False,11)
table(['Informasi yang berpotensi membingungkan','Dampak terhadap pengguna','Peluang perbaikan struktur'],[
('Catatan pembayaran dianggap hasil pemeriksaan. UX01.','Pengguna dapat mengira input pembayaran sudah cukup untuk menentukan penerimaan.','Pisahkan bagian Pembayaran dan Pemeriksaan; beri penjelasan makna inti pada N1b. Panduan lengkap tersedia di N3a.'),
('Hasil tersedia dianggap hasil sudah sesuai. UX03, UX05.','Pengguna dapat melewati pemeriksaan isi hasil sebelum mengambil keputusan.','Pisahkan keadaan permintaan dari kesimpulan hasil; dekatkan sumber dan rujukan hasil dengan Tindak Lanjut.'),
('Bukti atau hasil yang nominalnya sama tertukar konteks. UX02.','Pengguna berpotensi memilih pesanan yang keliru bila hanya melihat nominal.','Tampilkan identitas pesanan serta konteks pelanggan; hubungkan bukti dan hasil pada N1b yang sama. Nominal bukan identitas tunggal.'),
('Antrean dan Detail Pesanan memuat versi informasi berbeda. UX02, UX03, UX05.','Pengguna sulit mengetahui rujukan hasil yang harus dipercaya.','N2 hanya memberi ringkasan dan tautan TS1 ke N1b. Hindari halaman detail pemeriksaan duplikat.'),
('Kontak atau panduan menunggu tersembunyi di bantuan umum. UX04.','Pengguna perlu meninggalkan konteks pesanan saat mencari langkah berikutnya.','Sediakan kategori Bantuan Pemeriksaan dan tautan TS2 dari bagian Pemeriksaan; pertahankan konteks ketika kembali.'),
('Hubungan ke pemeriksaan meminta pengetikan ulang atau mengubah data awal. UX06.','Kelancaran pencatatan yang sudah dinilai baik dapat menurun.','Pertahankan identitas dan nominal tersimpan saat masuk ke pemeriksaan; tinjau kembali rincian sebelum memakai konteks itu.')
],[5.2,4.5,6.3],size=11)
h('Urutan peluang perbaikan',2)
p('Prioritas mengikuti Worksheet 8: UX05 dasar keputusan, UX03 koordinasi pemeriksaan, UX02 kecocokan informasi, UX01 makna informasi, kemudian UX04 bantuan saat menunggu dan UX06 kelancaran pencatatan. Empat kebutuhan Must saling mendukung dan dirancang sebagai satu struktur inti. Urutan kepentingan ini bukan perkiraan biaya atau urutan pengerjaan teknis.')
p('Penyajian informasi belum tentu mempercepat respons owner atau finance. Kecepatan pemeriksaan dan efektivitas label perlu diuji; laporan ini tidak menjanjikan waktu tunggu atau penurunan kesalahan tertentu.',False,11)

# Halaman 10
h('9 Hubungan kebutuhan UX dan pemeriksaan struktur',page=True)
p('Tabel menghubungkan enam kebutuhan Worksheet 8 dengan lokasi serta tugas penelusuran pada rancangan. Pemeriksaan yang diusulkan dapat memakai sitemap atau tree test dan data pesanan fiktif; belum dilakukan kepada pengguna.',False,11)
table(['Kebutuhan','Lokasi utama','Tugas pemeriksaan yang diusulkan'],[
('UX01 Makna informasi','C02, C05; N1b dan N3a','Temukan catatan dan hasil pemeriksaan, lalu jelaskan perbedaan maknanya.'),
('UX02 Kecocokan informasi','C01, C03, C05, C08; N1 dan N1b','Temukan bukti serta hasil yang benar untuk dua pesanan bernominal sama.'),
('UX03 Koordinasi','C04, C07, C15, C16; N2 dan N1b','Temukan permintaan yang masih menunggu, pemeriksanya, dan tempat membaca hasil.'),
('UX04 Tindak lanjut saat menunggu','C12-C13; N3b-N3c melalui TS2','Temukan panduan atau kontak pemeriksa, lalu kembali ke pesanan yang sama.'),
('UX05 Dasar keputusan','C05-C06, C15; N1b','Temukan sumber hasil dan dasar keputusan; bedakan hasil yang sesuai dan yang perlu ditinjau.'),
('UX06 Kelancaran pencatatan','C09-C10; N1a dan N1b','Telusuri hubungan setelah pencatatan ke pemeriksaan dan tentukan data yang digunakan kembali.')
],[3.5,4.3,8.2],size=11)
p('Catat jalur yang dipilih, keberhasilan menemukan informasi, penjelasan peserta, dan bantuan yang diperlukan. Sasaran awal: setiap informasi inti dapat ditemukan pada tujuan yang tepat tanpa arahan moderator. Pengujian prototipe berikutnya diperlukan untuk memastikan pengisian ulang benar-benar dapat dihindari dan keputusan tindak lanjut tepat; sitemap saja belum membuktikan keduanya.',False,11)
h('10 Sumber dan batas hasil',2)
p('S8. Rusdany Maestro. Worksheet 8 UX Requirements, 15 Oktober 2026; UX01-UX06, FR01-FR06, User Stories, prioritas dan alasan.\nS6 dan S7. Rusdany Maestro. Worksheet 6 Empathy Map dan Persona serta Worksheet 7 User Journey, 15 Oktober 2026; konteks Persona Ari dan pemeriksaan oleh owner atau finance.\nAcuan utama. UX Design Hands-on Workbook, Pertemuan 09 Information Architecture, petunjuk dan template mahasiswa bagian A Content Inventory, B Sitemap, dan C Card Sorting Mini Exercise.\nAcuan penilaian. Instruksi Worksheet 9 Information Architecture, Rekayasa Interaksi.',False,10.5)
p('Struktur mengikuti kebutuhan riset yang telah disintesis pada Worksheet 8. Pengelompokan, nama menu, dan hubungan halaman masih berupa usulan peneliti. Tidak ada klaim sesi card sorting baru, hasil tree test, integrasi bank, atau hak akses aplikasi yang telah diverifikasi melalui worksheet ini.',False,10.5)

for tree in (doc.element,doc.styles.element,sec.footer._element):
    for fonts in tree.iter(qn('w:rFonts')):
        fonts.attrib.clear()
        for attr in ('ascii','hAnsi','eastAsia','cs'):fonts.set(qn('w:'+attr),'Times New Roman')
    for border in list(tree.iter(qn('w:pBdr'))):border.getparent().remove(border)
    for rp in tree.iter(qn('w:rPr')):
        spacing=rp.find(qn('w:spacing'))
        if spacing is not None:rp.remove(spacing)
    for color in tree.iter(qn('w:color')):
        color.attrib.clear();color.set(qn('w:val'),'000000')
out=TMP/(STEM+'_sebelum_sanitasi.docx');doc.save(out)
content=[]
for x in doc.element.body:
    if x.tag==qn('w:p'):
        from docx.text.paragraph import Paragraph
        content.append(Paragraph(x,doc).text)
    elif x.tag==qn('w:tbl'):
        from docx.table import Table
        for row in Table(x,doc).rows:content.append(' | '.join(c.text for c in row.cells))
(TMP/'report_content.txt').write_text('\n\n'.join(content),encoding='utf-8')
print(out)
