from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import json

ROOT = Path(r'D:\Rekayasa Interaksi')
OUT = ROOT / '202210370311406_Rusdany_Maestro_Worksheet4_UXResearchPlan.docx'
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)
sec.left_margin, sec.right_margin = Cm(1.8), Cm(1.8)
sec.header_distance, sec.footer_distance = Cm(.75), Cm(.8)
for name, size in [('Normal',11), ('Title',23), ('Subtitle',13), ('Heading 1',16), ('Heading 2',11.5)]:
    st=doc.styles[name]
    st.font.name='Arial'; st.font.size=Pt(size); st.font.color.rgb=RGBColor(0,0,0)
    st.paragraph_format.space_after=Pt(6)
    st.paragraph_format.line_spacing=1.08
    st.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Arial')
for n in ['Heading 1','Heading 2']:
    doc.styles[n].paragraph_format.space_before=Pt(9)
    doc.styles[n].paragraph_format.keep_with_next=True
doc.styles['Normal'].paragraph_format.widow_control=True
doc.core_properties.author='Rusdany Maestro'
doc.core_properties.title='Worksheet 4 UX Research Plan Kepastian Pembayaran Transfer pada Fleffy'
doc.core_properties.subject='Rekayasa Interaksi'

hp=sec.header.paragraphs[0]
hp.text=''
fp=sec.footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for part in ['PAGE','NUMPAGES']:
    if part=='NUMPAGES': fp.add_run(' / ')
    r=fp.add_run(); fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),part); r._r.addnext(fld)

content=[]
def p(text, boldlead=False):
    content.append(text)
    para=doc.add_paragraph()
    if boldlead and '. ' in text:
        a,b=text.split('. ',1); para.add_run(a+'. ').bold=True; para.add_run(b)
    else: para.add_run(text)
    return para
def h(text, level=1):
    content.append(text); return doc.add_paragraph(text, f'Heading {level}')
def page(title):
    doc.add_page_break(); h(title)
def table(headers, rows, widths, size=10):
    content.append(' | '.join(headers))
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    for c,w in zip(t.columns,widths): c.width=Cm(w)
    for i,s in enumerate(headers): t.rows[0].cells[i].text=s
    for row in rows:
        content.append(' | '.join(row))
        for c,s in zip(t.add_row().cells,row): c.text=s
    for ri,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr(); nosplit=OxmlElement('w:cantSplit'); pr.append(nosplit)
        if ri==0:
            rep=OxmlElement('w:tblHeader'); pr.append(rep)
        for ci,cell in enumerate(row.cells):
            cell.width=Cm(widths[ci]); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr=cell._tc.get_or_add_tcPr()
            borders=OxmlElement('w:tcBorders')
            for edge in ['top','left','bottom','right']:
                e=OxmlElement('w:'+edge); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4'); e.set(qn('w:color'),'D9D9D9'); borders.append(e)
            tcpr.append(borders)
            mar=OxmlElement('w:tcMar')
            for edge,n in [('top',85),('bottom',85),('left',100),('right',100)]:
                e=OxmlElement('w:'+edge); e.set(qn('w:w'),str(n)); e.set(qn('w:type'),'dxa'); mar.append(e)
            tcpr.append(mar)
            shade=OxmlElement('w:shd'); shade.set(qn('w:fill'),'E7EDF3' if ri==0 else ('F7F8FA' if ri%2==0 else 'FFFFFF')); tcpr.append(shade)
            for para in cell.paragraphs:
                para.paragraph_format.space_after=Pt(2); para.paragraph_format.line_spacing=1.04
                for r in para.runs: r.font.name='Arial'; r.font.size=Pt(size); r.font.bold=(ri==0)
    doc.add_paragraph().paragraph_format.space_after=Pt(0)
    return t

# PAGE 1
doc.add_paragraph('Worksheet 4 UX Research Plan','Title')
doc.add_paragraph('Rencana riset kepastian pembayaran transfer pada Fleffy','Subtitle')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nMata kuliah: Rekayasa Interaksi\nJenis tugas: Individu\nTanggal penyusunan: 9 Oktober 2026')
h('1 Ringkasan rencana')
p('Saya merencanakan riset untuk memahami bagaimana operator kasir menafsirkan status Lunas dan memastikan penerimaan pembayaran Bank Transfer di Fleffy. Hasilnya akan menjadi dasar perumusan kebutuhan pengguna dan perbaikan How Might We pada worksheet berikutnya. Riset ini dirancang selama tujuh hari dengan observasi kontekstual, wawancara, dan telaah dokumentasi.')
p('Produk dan konteks. Fleffy - Kasir Laundry Sepatu digunakan untuk mencatat pesanan, layanan, dan pembayaran. Konteks utama penelitian adalah pencatatan serta pemeriksaan pembayaran pada usaha Balik Bersih. [1-3]',True)
h('2 Latar belakang masalah')
p('Worksheet 1 mendokumentasikan satu transaksi contoh yang tersimpan dengan Bank Transfer Rp57.000 dan status Lunas. Pengalaman penggunaan menunjukkan bahwa penerimaan transfer masih perlu diperiksa kepada pelanggan. Bukti layar menunjukkan catatan pembayaran; mutasi rekening dan penerimaan dana tidak terlihat pada bukti tersebut. [1]')
p('Worksheet 2 merumuskan kebutuhan kasir dan owner untuk memperoleh kepastian pembayaran dengan usaha pemeriksaan yang lebih ringan. Worksheet 3 menetapkan operator kasir sebagai target utama, termasuk owner atau admin jika benar-benar menjalankan pencatatan dan pemeriksaan transfer. Satu orang dapat merangkap beberapa peran. [2, 3]')
p('Waktu pemeriksaan, frekuensi pemeriksaan ulang, pemahaman pengguna lain, serta pembagian kewenangan belum diukur. Karena itu, riset perlu mengumpulkan bukti tentang praktik kerja dan kebutuhan informasi sebelum menetapkan solusi.')

# PAGE 2
page('3 Fokus tujuan dan pertanyaan riset')
h('Fokus masalah',2)
p('Kasir dan owner yang mencatat transfer di Fleffy membutuhkan kepastian bahwa pembayaran pelanggan telah diterima. Pada alur awal yang didokumentasikan, status Lunas setelah pengisian nominal belum cukup bagi pengguna untuk memperoleh kepastian tersebut, sehingga diperlukan pemeriksaan tambahan kepada pelanggan. Rumusan ini melanjutkan Problem Statement Worksheet 2. [2]')
p('Batas kajian. Penelitian mencakup pemilihan Bank Transfer, pencatatan nominal, pembacaan status, pemeriksaan informasi pembayaran, koordinasi antarpetugas, dan keputusan tindak lanjut. Tunai, produksi, pengantaran, dan drop point hanya dicatat sebagai konteks bila terkait pemeriksaan transfer, tanpa menjadi fokus masalah baru.',True)
table(['Kode','Tujuan riset yang spesifik','Pertanyaan riset'],[
('T1 / RQ1','Mengidentifikasi makna Lunas bagi operator dan informasi yang dianggap sudah dipastikan.','Apa arti status Lunas bagi operator, dan informasi apa yang menurut mereka sudah serta belum diketahui?'),
('T2 / RQ2','Memetakan urutan pemeriksaan, sumber informasi, pihak yang terlibat, dan dasar keputusan pembayaran.','Kapan dan bagaimana penerimaan transfer diperiksa, oleh siapa, serta berdasarkan informasi apa pembayaran dianggap selesai?'),
('T3 / RQ3','Mendeskripsikan usaha pemeriksaan pada sesi yang diamati dan kondisi pemicu pemeriksaan ulang.','Berapa tindakan, kontak ulang, waktu aktif, dan waktu tunggu yang teramati; dalam kondisi apa pemeriksaan perlu diulang?'),
('T4 / RQ4','Menelusuri dampak pemeriksaan terhadap pelayanan dan keputusan kerja berdasarkan contoh konkret.','Bagaimana pemeriksaan memengaruhi tindak lanjut pesanan atau pelayanan, jika ada?'),
('T5 / RQ5','Merumuskan kebutuhan informasi dan koordinasi dari hambatan maupun praktik yang berhasil.','Informasi dan pembagian tanggung jawab apa yang dibutuhkan agar operator dapat menentukan tindak lanjut pembayaran dengan jelas?')
],[1.7,7.3,8.4])
h('Dugaan yang akan diperiksa',2)
p('Dugaan awal adalah adanya perbedaan antara makna status pembayaran dan kepastian yang dibutuhkan pengguna, serta adanya pemeriksaan terpisah dari pencatatan. Riset menerima kemungkinan bahwa pengguna sudah memahami status dan pemeriksaan berjalan lancar. Kebutuhan integrasi bank, kesalahan pemahaman, kerugian, atau akar penyebab teknis belum ditetapkan. [1, 2]')

# PAGE 3
page('4 Target dan karakteristik responden')
p('Target utama. Operator yang pernah mencatat Bank Transfer di Fleffy dan melakukan atau ikut dalam pemeriksaan penerimaannya. Kasir, owner, dan admin dipilih berdasarkan aktivitas nyata. Teknisi, kurir, atau pengelola drop point hanya memenuhi target jika juga menjalankan aktivitas tersebut. [3]',True)
table(['Kelompok','Jumlah rencana','Karakteristik dan kontribusi'],[
('Pengguna utama','5 orang unik','Pengguna Fleffy yang aktif dalam tiga bulan terakhir; pernah mencatat Bank Transfer, terlibat pemeriksaan, dan dapat menceritakan satu transaksi. Memberi data pemahaman, perilaku, dan usaha kerja.'),
('Informan pendukung','1 orang unik','Owner atau penanggung jawab yang memahami prosedur dan kewenangan pemeriksaan transfer. Memberi konteks pembagian tugas dan keputusan usaha; tidak wajib menjadi operator.'),
('Jumlah keseluruhan','6 orang unik','Satu orang dengan beberapa peran tetap dihitung sekali. Informan pendukung direkrut sebagai orang yang berbeda; status ketersediaannya diperiksa saat rekrutmen.')
],[3.6,2.3,11.5])
h('Kriteria penyertaan dan variasi',2)
p('Responden berusia minimal 18 tahun, bersedia secara sukarela, dapat menjelaskan pengalamannya dalam bahasa Indonesia, dan memenuhi kriteria kelompoknya. Pengalaman lancar maupun pengalaman dengan hambatan sama-sama diterima. Kemampuan teknologi tidak diasumsikan dari nama peran.')
p('Teknik pemilihan adalah purposive sampling. Saya mengupayakan variasi lama penggunaan, frekuensi pencatatan, peran aktual, dan keterlibatan dalam akses informasi penerimaan dana. Kriteria tidak mewajibkan responden pernah mengeluh atau salah memahami Lunas. Daftar pertanyaan penyaringan tersedia pada Lampiran A.')
h('Rekrutmen dan kecukupan jumlah',2)
p('Saya meminta izin pelaksanaan kepada pengelola Balik Bersih, lalu menawarkan partisipasi kepada operator yang sesuai. Kontak digunakan hanya untuk mengatur sesi dan disimpan terpisah dari catatan riset. Dua calon cadangan dapat disiapkan untuk mengganti pembatalan, tanpa menambah target sesi.')
p('Lima sesi utama dipilih karena masing-masing memerlukan 45 menit dan masih dapat dianalisis oleh satu mahasiswa dalam seminggu. Jumlah ini mendukung eksplorasi terarah, bukan estimasi populasi atau jaminan kejenuhan tema.')
h('Rencana jika responden terbatas',2)
p('Jika pengguna yang sesuai di Balik Bersih kurang dari lima, saya dapat merekrut pengguna Fleffy dari usaha laundry sepatu serupa sebagai pembanding, dengan izin outletnya. Asal konteks dicatat dan hasil pembanding dianalisis terpisah. Bila tetap terbatas, saya melaporkan jumlah aktual; kurang dari tiga operator menjadi studi pendahuluan yang memerlukan riset lanjutan. Sesi tambahan orang yang sama tidak dihitung sebagai responden baru.')
p('Jika informan pendukung yang berbeda tidak tersedia, pertanyaan prosedur diajukan kepada operator berwenang yang sudah menjadi peserta. Kontribusinya dicatat tanpa menambah hitungan orang; total responden unik mengikuti kehadiran aktual.')

# PAGE 4
page('5 Metode dan pelaksanaan pengumpulan data')
table(['Metode','Teknik pelaksanaan','Informasi yang dicari'],[
('Telaah dokumentasi','Menelaah Worksheet 1-3 dan tampilan pembayaran yang sudah disamarkan. Catat versi dan tanggal bukti.','Dasar masalah dan batas bukti; konteks RQ1-RQ5.'),
('Observasi kontekstual','Mengamati langkah operator pada konteks kerja yang diizinkan; klarifikasi singkat pada jeda aman. Jika transaksi tidak tersedia, gunakan rekonstruksi dengan data dummy.','Urutan tindakan, sumber informasi, koordinasi, keputusan, dan durasi teramati; RQ2-RQ4.'),
('Wawancara semi terstruktur','Pertanyaan terbuka tentang pengalaman terakhir, makna status, pemeriksaan, contoh lancar/bermasalah, dan kebutuhan.','Alasan di balik tindakan, variasi praktik, dan kebutuhan; RQ1-RQ5.')
],[3.5,7.7,6.2])
p('Metode utama bersifat kualitatif dan dilengkapi catatan deskriptif tindakan serta waktu. Kuesioner massal tidak dipilih karena pertanyaan utama membutuhkan penelusuran konteks dan alasan, sedangkan cakupan responden serta waktunya terbatas.')
h('Alur sesi pengguna utama',2)
table(['Tahap','Durasi','Kegiatan'],[
('Pembukaan','5 menit','Jelaskan tujuan, hak responden, batas data, dan pilihan rekaman; isi persetujuan.'),
('Observasi','15 menit','Telusuri satu alur pembayaran. Catat tindakan tanpa mengarahkan. Hentikan pengamatan bila muncul data sensitif.'),
('Wawancara','20 menit','Tanyakan makna status dengan stimulus B2, alasan pemeriksaan, pembagian tugas, dampak, dan kebutuhan.'),
('Penutup','5 menit','Konfirmasi ringkasan, beri kesempatan koreksi, dan jelaskan penarikan data serta tindak lanjut.')
],[3.5,2.3,11.6])
p('Informan pendukung diwawancarai sekitar 20 menit dengan panduan khusus Lampiran C. Peneliti dan moderator adalah Rusdany Maestro. Sesi dilakukan individual agar bawahan dapat menjelaskan pengalaman tanpa kehadiran atasan.')
h('Lokasi media dan sarana',2)
p('Lokasi utama adalah area kerja Balik Bersih pada waktu yang disepakati dan tidak mengganggu pelayanan. Sesi jarak jauh dapat dilakukan melalui Google Meet, dengan berbagi hanya tampilan Fleffy yang aman. Sarana: perangkat responden, stopwatch, catatan lokal, stimulus B2, dan lembar instrumen. Perangkat, versi aplikasi, mode sesi, dan gangguan dicatat; hasil perangkat berbeda tidak dianggap identik.')
p('Transaksi nyata diamati hanya bila aman dan memperoleh persetujuan pihak yang terlibat. Jika tidak, gunakan demonstrasi dengan data dummy atau rekonstruksi pengalaman. Data nyata, rekonstruksi, dan simulasi diberi kode berbeda serta dianalisis terpisah.')

# PAGE 5
page('6 Jadwal pelaksanaan selama satu minggu')
p('Hari 1 dimulai setelah akses dan waktu riset disepakati. Jadwal memakai hari relatif agar dapat disesuaikan dengan batas waktu Google Classroom tanpa mengarang tanggal pengumpulan. Persiapan dan pelaksanaan berikut direncanakan selesai dalam tujuh hari.')
table(['Hari','Kegiatan','Alokasi','Hasil kerja'],[
('1','Finalisasi fokus, izin outlet, penyaringan dan penjadwalan calon responden.','90 menit','Daftar kode calon, kriteria terpenuhi, jadwal sesi.'),
('2','Siapkan stimulus, persetujuan, lembar catatan; latihan instrumen secara mandiri dengan data dummy. Perbaiki pertanyaan yang mengarahkan.','120 menit','Instrumen siap pakai dan perangkat pencatatan diperiksa.'),
('3','Tiga sesi pengguna utama; rapikan catatan segera setelah setiap sesi.','180 menit','Catatan P01-P03; 135 menit sesi dan 45 menit jeda/perapian.'),
('4','Dua sesi pengguna utama dan satu informan pendukung; penggantian peserta jika batal.','140 menit','Catatan P04-P05 dan I01; 110 menit sesi dan 30 menit jeda/perapian.'),
('5','Rapikan catatan atau transkrip, samarkan identitas, kodekan bukti, dan susun matriks awal.','150 menit','Catatan anonim, log tindakan, dan kode awal.'),
('6','Analisis tema, bandingkan sumber/kasus berbeda, dan konfirmasi ringkasan yang belum jelas jika responden bersedia.','150 menit','Tema, alur pemeriksaan, kebutuhan, dan batas temuan.'),
('7','Susun laporan, kaitkan insight dengan pertanyaan riset, periksa instrumen/etika, ekspor dan periksa PDF.','90 menit','Laporan hasil untuk worksheet berikutnya dan dokumen rapi.')
],[1.1,8.5,2.3,5.5])
h('Kelayakan dan penyesuaian',2)
p('Total alokasi sekitar 920 menit atau 15 jam 20 menit selama satu minggu. Pengumpulan utama memerlukan 245 menit atau 4 jam 5 menit; alokasi hari 3-4 juga memuat jeda dan perapian. Penjadwalan sesi dapat ditukar tanpa mengurangi waktu analisis dan pemeriksaan dokumen.')
p('Bila tidak ada transaksi nyata pada sesi, saya tetap menjalankan rekonstruksi atau demonstrasi. Waktu tunggu pembayaran yang melampaui sesi dicatat sebagai belum selesai. Jika peserta batal, gunakan calon cadangan; jika target tidak tercapai, laporkan jumlah aktual dan keterbatasannya.')
p('Kesiapan pelaksanaan dinilai dari terpenuhinya izin, persetujuan, responden yang sesuai, stimulus yang aman, serta instrumen pada Lampiran A-D. Kehadiran responden dan jumlah transaksi nyata belum dinyatakan sebagai hasil riset.')

# PAGE 6
page('7 Definisi data dan ukuran deskriptif')
p('Unit analisis adalah satu kejadian pencatatan dan pemeriksaan transfer yang ditelusuri bersama responden. Kode P01-P05 dipakai untuk pengguna utama, I01 untuk informan, dan K01 dan seterusnya untuk kejadian. Jenis bukti ditandai N untuk observasi nyata, R untuk rekonstruksi, atau S untuk simulasi. Pernyataan wawancara ditandai W.')
table(['Data atau ukuran','Definisi dan cara pencatatan'],[
('Makna Lunas','Catat jawaban spontan sebelum penjelasan peneliti. Kode awal: catatan nominal, dana diterima, tidak pasti, atau makna lain. Simpan alasan dan kutipan anonim; kode boleh berkembang.'),
('Tindakan pemeriksaan','Satu tindakan bertujuan memeriksa, misalnya membuka sumber, mencocokkan informasi, meminta konfirmasi, atau menyerahkan pemeriksaan. Klik navigasi berulang tidak dihitung sebagai tindakan terpisah.'),
('Waktu aktif pemeriksaan','Jumlah interval aktif dari tindakan pemeriksaan pertama sampai keputusan atau penyerahan terakhir yang teramati. Catat menit/detik dengan stopwatch; keluarkan waktu tunggu dan gangguan. Tidak menaksir dari timestamp screenshot lama.'),
('Waktu tunggu','Interval ketika proses tertahan menunggu respons atau informasi. Catat terpisah dari waktu aktif. Jika pemeriksaan melampaui sesi, tandai belum selesai dan durasi sebagai batas pengamatan.'),
('Kontak ulang','Permintaan konfirmasi kedua dan berikutnya kepada pihak yang sama untuk kejadian yang sama. Konfirmasi pertama dan penyerahan kepada pihak lain dicatat terpisah.'),
('Pemeriksaan berulang','Langkah pemeriksaan yang dilakukan kembali karena kepastian belum diperoleh. Catat pemicu dan urutannya. Pemeriksaan awal yang sesuai prosedur tidak otomatis dianggap berulang atau tidak perlu.'),
('Frekuensi pada pengamatan','Untuk kejadian nyata hari 3-4, laporkan x berulang, y tidak berulang terkonfirmasi, dan u belum dapat ditentukan. Ringkasan x dari (x+y) disertai u serta total n=x+y+u. Kejadian terpotong tidak otomatis dianggap tidak berulang.'),
('Dampak dan keputusan','Catat keputusan akhir, tugas yang tertunda jika ada, serta sumber buktinya. Pisahkan kejadian yang diamati, laporan pengalaman, dan penafsiran peneliti.')
],[4.5,12.9])
h('Batas interpretasi ukuran',2)
p('Waktu R/S dilabeli sebagai waktu rekonstruksi/simulasi, bukan durasi pelayanan nyata. Jika interval tidak dapat diukur, tulis tidak terukur. Untuk data nyata yang selesai, laporkan nilai per kejadian serta median dan rentang bila jumlahnya memadai, selalu dengan n. Jika n=0, laporkan bahwa ukuran lapangan belum tersedia.')
p('Jumlah responden purposive dan jumlah kejadian kecil tidak digunakan untuk menyatakan prevalensi seluruh pengguna. Jawaban makna Lunas juga tidak diberi label salah secara teknis tanpa penjelasan sistem yang terverifikasi.')

# PAGE 7
page('8 Rencana analisis dan luaran riset')
h('Tahapan analisis',2)
p('1. Merapikan dan menyamarkan data. Gabungkan catatan dengan rekaman yang disetujui, hapus identitas, dan simpan kode kejadian serta jenis bukti. Setiap potongan data diberi rujukan responden, kejadian, dan waktu atau nomor catatan.')
p('2. Membuat kode awal. Kelompokkan pernyataan tentang makna status, sumber bukti, kewenangan, pemicu pemeriksaan, waktu tunggu, dampak, dan kebutuhan. Tambahkan kode baru jika data menunjukkan hal di luar dugaan awal.')
p('3. Menyusun matriks dan alur. Bandingkan kasus berdasarkan tugas nyata dan konteks outlet. Petakan urutan pencatatan, pembacaan status, pemeriksaan, penyerahan tugas, dan keputusan. Pisahkan N/R/S serta data informan.')
p('4. Membentuk tema dan mencari kasus berbeda. Gabungkan kode yang berkaitan, lalu periksa pengalaman lancar dan temuan yang bertentangan. Kebiasaan responden yang sudah dikenal peneliti tidak diperlakukan sebagai aturan umum.')
p('5. Memeriksa bukti. Bandingkan apa yang dilakukan dengan apa yang diceritakan serta dokumentasi awal. Bila berbeda, simpan keduanya dan telusuri konteksnya. Konfirmasi ringkasan kepada responden bila memungkinkan tanpa memaksakan persetujuan.')
p('6. Merumuskan insight dan kebutuhan. Tulis kebutuhan berdasarkan bukti, sertakan keterbatasan dan pertanyaan terbuka, lalu perbarui Problem Statement/HMW bila didukung hasil. Prioritas mempertimbangkan dampak, kejadian berulang pada sampel, dan kekuatan bukti; tidak mengklaim sebab teknis dari wawancara saja.')
table(['RQ','Bukti utama','Luaran yang direncanakan'],[
('RQ1','Jawaban stimulus B2 dan alasan responden.','Peta penafsiran status dan informasi yang belum jelas.'),
('RQ2','Log tindakan, sumber informasi, wawancara operator/informan.','Alur pemeriksaan dan peta tanggung jawab aktual.'),
('RQ3','Log waktu/tindakan/kontak dengan jenis bukti dan n.','Baseline usaha pemeriksaan serta kondisi pemicunya.'),
('RQ4','Keputusan dan contoh dampak beserta rujukan kejadian.','Daftar dampak teramati atau dilaporkan, termasuk kasus tanpa hambatan.'),
('RQ5','Tema, kasus pembanding, kebutuhan dan informasi yang dianggap cukup.','Kebutuhan pengguna dan HMW untuk worksheet berikutnya.')
],[1.4,7.4,8.6])
p('Luaran akhir berupa laporan ringkas temuan, matriks bukti anonim, peta alur, ringkasan ukuran beserta batasnya, dan kebutuhan yang diprioritaskan. Format temuan memuat masalah, konteks, bukti, dampak, kebutuhan, serta informasi yang masih perlu diuji. Seluruh luaran tersebut baru diisi setelah pengumpulan data.')

# PAGE 8
page('9 Etika dan kerahasiaan data')
h('Persetujuan dan kenyamanan',2)
p('Izin outlet dan persetujuan individu diminta terpisah. Responden menerima penjelasan tujuan akademik, durasi, aktivitas, penggunaan data, dan hak menolak pertanyaan atau berhenti tanpa konsekuensi terhadap pekerjaan. Persetujuan partisipasi tidak otomatis menjadi persetujuan rekaman. Formulir ada pada Lampiran A.')
p('Sesi tidak dilakukan di hadapan atasan dan tidak digunakan sebagai penilaian kinerja. Kutipan atau pengalaman bawahan tidak dibagikan kepada owner dalam bentuk yang dapat mengungkap identitas. Peneliti menggunakan pertanyaan netral, mengamati sebelum menjelaskan dugaan, dan mengakui kemungkinan bias dari pengalaman pribadi sebelumnya.')
h('Pembatasan data dan keselamatan sesi',2)
p('Data yang dikumpulkan hanya peran aktual, kategori pengalaman penggunaan, proses pemeriksaan, penafsiran status, tindakan, waktu, dan kebutuhan. Nomor rekening, saldo, mutasi lengkap, PIN, OTP, kredensial, nama pelanggan, nomor telepon pelanggan, dan bukti transfer pribadi tidak dikumpulkan.')
p('Peneliti tidak meminta login bank atau transfer nyata dan tidak mengubah transaksi usaha. Jika diperlukan ilustrasi, responden menjelaskan jenis informasi atau menggunakan data dummy. Saat informasi sensitif muncul, hentikan rekaman/berbagi layar dan hapus bagian yang terlanjur tersimpan. Pelanggan yang ikut diamati langsung harus memberi persetujuan tersendiri; jika tidak, gunakan demonstrasi tanpa pelanggan.')
h('Penyimpanan dan penarikan data',2)
p('Catatan dan rekaman yang disetujui disimpan pada folder lokal berakses terbatas di perangkat yang dilindungi sandi. Daftar kontak penjadwalan dipisahkan dan dihapus setelah kebutuhan konfirmasi selesai. Data mentah tidak diunggah ke layanan publik; laporan hanya memuat data anonim dan kutipan yang aman.')
p('Responden dapat meminta penghapusan data dengan menyebut kode sesi sampai akhir hari 6, sebelum agregasi laporan hari 7. Sesudah data digabung secara anonim, sebagian pernyataan mungkin tidak dapat ditelusuri lagi. Batas ini dijelaskan saat persetujuan. Rekaman dan catatan mentah dihapus paling lambat 30 hari setelah penilaian akhir/revisi selesai; laporan anonim dipertahankan untuk keperluan akademik.')
h('10 Sumber dasar rencana')
p('[1] Rusdany Maestro. Worksheet 1 UX Detective Pengamatan alur transaksi Fleffy. Dokumentasi 19 September 2026, halaman 1-5; khususnya bukti B2-B3 dan rumusan M1.')
p('[2] Rusdany Maestro. Worksheet 2 Design Challenge Merumuskan Masalah UX. 21 September 2026; Problem Statement, How Might We, tujuan awal, dan pertanyaan riset berikutnya.')
p('[3] Rusdany Maestro. Worksheet 3 User and Stakeholder pada Fleffy. Penyusunan 21 September dan revisi 28 September 2026; target riset, peran aktual, dan batas kewenangan.')
p('[4] Instruksi Tugas Worksheet 4 UX Research Plan mata kuliah Rekayasa Interaksi yang diberikan untuk pengerjaan ini; komponen, format pengumpulan, dan rubrik penilaian.')

# PAGE 9
page('Lampiran A Penyaringan dan persetujuan responden')
h('A1 Formulir penyaringan',2)
p('Kode calon: __________  Tanggal: __________  Kelompok: utama / pendukung\nGunakan kode, tanpa nama pada lembar analisis. Kontak penjadwalan dicatat terpisah.')
p('S1. Apakah Anda berusia minimal 18 tahun? Ya / Tidak.\nS2. Apa tugas yang Anda lakukan dalam pencatatan atau pemeriksaan pembayaran? Catat aktivitas dan peran; boleh lebih dari satu.\nS3. Kapan terakhir menggunakan Fleffy? Dalam 3 bulan terakhir / Lebih lama / Tidak pernah.\nS4. Apakah Anda pernah mencatat pembayaran Bank Transfer di Fleffy? Ya / Tidak.\nS5. Apakah Anda pernah melakukan atau ikut dalam pemeriksaan penerimaannya? Ya / Tidak. Jelaskan keterlibatan Anda.\nS6. Bisakah Anda menceritakan satu transaksi transfer yang pernah ditangani tanpa membuka informasi pribadi? Ya / Tidak.\nS7. Berapa lama menggunakan Fleffy dan seberapa sering melakukan tugas ini? Lama: <1 bulan / 1-6 bulan / >6 bulan; frekuensi: harian / mingguan / lebih jarang.\nS8. Untuk informan pendukung, apakah Anda memahami prosedur serta pihak yang berwenang memeriksa penerimaan pembayaran? Ya / Tidak. Apa peran Anda?')
p('Keputusan. Kelompok utama memenuhi S1, S3 dalam 3 bulan terakhir, S4, S5, dan S6. Pendukung memenuhi S1 dan S8 serta memiliki pengalaman prosedur di outlet. Pilih setelah persetujuan sukarela. Frekuensi/masa pakai digunakan untuk variasi, bukan untuk menyaring keluhan. Hasil: memenuhi / tidak memenuhi / perlu klarifikasi; alasan: __________.',True)
h('A2 Naskah penjelasan dan catatan persetujuan',2)
p('Saya Rusdany Maestro, mahasiswa Informatika Universitas Muhammadiyah Malang. Saya meneliti bagaimana pengguna Fleffy memahami status pembayaran dan memastikan transfer untuk tugas Rekayasa Interaksi. Sesi pengguna berlangsung sekitar 45 menit; sesi informan sekitar 20 menit. Anda akan menjelaskan pengalaman dan, bila aman, menunjukkan alur dengan data yang tidak sensitif. Tidak diperlukan data bank pribadi atau transfer nyata.')
p('Partisipasi bersifat sukarela. Anda boleh melewati pertanyaan, meminta jeda, atau berhenti tanpa konsekuensi. Laporan memakai kode dan data anonim. Rekaman audio atau tampilan hanya dibuat jika Anda memilih setuju; jika tidak, saya menggunakan catatan. Anda dapat meminta penghapusan data dengan kode sesi sampai akhir hari 6, sebelum laporan digabung. Data mentah dihapus paling lambat 30 hari setelah penilaian akhir/revisi selesai. Untuk penarikan, hubungi peneliti melalui saluran yang digunakan saat penjadwalan.')
p('Kode sesi: __________  Tanggal: __________\nPartisipasi: Setuju / Tidak setuju\nRekaman audio: Setuju / Tidak setuju\nDokumentasi tampilan Fleffy yang telah aman: Setuju / Tidak setuju\nIzin kutipan anonim untuk laporan akademik: Setuju / Tidak setuju\nBentuk persetujuan: Lisan / Tertulis  Dicatat oleh: __________')

# PAGE 10
page('Lampiran B Panduan observasi pengguna')
h('B1 Persiapan dan skenario',2)
p('Kode responden/kejadian: __________  Hari dan jam: __________\nOutlet/konteks: __________  Peran aktual: __________\nPerangkat dan versi Fleffy: __________  Mode: langsung / jarak jauh\nJenis kegiatan: N nyata / R rekonstruksi / S simulasi\nPersetujuan partisipasi dan dokumentasi diperiksa: Ya / Tidak')
p('Instruksi moderator. Amati cara yang biasa digunakan; jangan memberi petunjuk tentang makna Lunas atau menawarkan solusi. Klarifikasi pada jeda aman. Gunakan stopwatch untuk interval pemeriksaan dan catat waktu tunggu terpisah. Batasi observasi sekitar 15 menit; pemeriksaan yang belum tuntas tetap dicatat sebagai belum selesai.')
p('Skenario. Pilih satu transaksi Bank Transfer yang sedang ditangani dan aman diamati. Jika tidak tersedia, minta responden merekonstruksi transaksi terakhir atau memperagakan alur dengan data dummy tanpa menyimpan perubahan pada transaksi usaha. Rekonstruksi dan simulasi bukan bukti kejadian pelayanan saat ini.')
h('B2 Tugas dan pertanyaan klarifikasi',2)
p('O1. "Tunjukkan bagaimana Anda biasanya mencatat pembayaran transfer untuk pesanan ini." Amati pilihan metode, nominal, pembacaan informasi, dan perpindahan sumber.\nO2. "Lanjutkan seperti yang biasa Anda lakukan sampai menentukan tindak lanjut pembayaran." Amati apakah ada pemeriksaan, kepada siapa, sumber yang digunakan, serta keputusan akhirnya.\nO3. Pada jeda: "Informasi apa yang Anda gunakan pada langkah tadi? Apa yang membuat Anda memilih langkah itu?" Catat alasan tanpa menyimpulkan tindakan salah.')
h('B3 Checklist dan pencatatan',2)
p('Untuk tiap aspek, tandai Teramati / Tidak teramati / Tidak relevan; tulis buktinya.\n1. Pencatatan metode dan nominal pembayaran.\n2. Membaca atau menyebut status pembayaran.\n3. Menggunakan informasi di dalam/di luar Fleffy.\n4. Membandingkan informasi pembayaran dengan catatan pesanan.\n5. Meminta konfirmasi pertama atau melakukan kontak ulang.\n6. Menyerahkan pemeriksaan kepada pihak berwenang.\n7. Menunggu informasi atau respons; ada gangguan lain.\n8. Mengulangi pemeriksaan dan menyebut pemicunya.\n9. Menentukan tindakan akhir serta dasar keputusannya.\n10. Menjelaskan proses yang lancar atau kebutuhan yang belum terpenuhi.')
p('Tidak teramati berarti langkah tidak terlihat selama sesi, bukan bukti langkah tersebut tidak pernah dilakukan. Catat waktu mulai/selesai tiap interval pada Lampiran D. Deskripsikan tindakan faktual lebih dahulu; tambahkan penafsiran pada kolom terpisah.')
h('B4 Stimulus makna status untuk wawancara',2)
p('Gunakan cuplikan B2 pada Lampiran E yang memperlihatkan Rincian Pembayaran, status Lunas, dan Bank Transfer Rp57.000. Perlihatkan setelah observasi untuk mengurangi pengaruh stimulus terhadap perilaku. Sebelum pertanyaan W3, jangan menjelaskan asal status atau meminta peserta membuktikan dana masuk.')
p('Rp57.000 merupakan transaksi contoh pada dokumentasi terdahulu. Stimulus digunakan untuk menanyakan pemahaman; tidak membuktikan transfer nyata dan tidak diganti dengan bukti bank pribadi. [1, 2]')

# PAGE 11
page('Lampiran C Panduan wawancara')
p('Kode responden: __________  Peran aktual: __________\nWawancara utama sekitar 20 menit. Ajukan pertanyaan terbuka sesuai alur; gunakan pendalaman hanya jika relevan. Untuk jawaban "tidak pernah" atau "tidak tahu", catat apa adanya.')
h('C1 Pengguna utama',2)
p('W1. Apa tugas Anda dalam pencatatan pembayaran dan pemeriksaan transfer? Sejak kapan serta seberapa sering Anda menjalankannya? [RQ2]\nPendalaman: Siapa lagi yang terlibat dan apa yang menjadi kewenangan Anda?')
p('W2. Ceritakan satu transaksi transfer terakhir yang Anda tangani, mulai dari mencatat sampai menentukan tindak lanjut. [RQ2, RQ4]\nPendalaman: Kapan dilakukan? Bagian mana yang Anda lakukan sendiri?')
p('W3. Setelah melihat stimulus B2, apa arti informasi pada layar ini bagi Anda? Informasi apa yang sudah dan belum diketahui? [RQ1]\nPendalaman: Apa yang membuat Anda menafsirkannya demikian? Catat jawaban spontan terlebih dahulu.')
p('W4. Setelah status seperti itu muncul, apa yang biasanya Anda lakukan berikutnya, jika ada? Mengapa? [RQ1, RQ2]')
p('W5. Bagaimana Anda memutuskan pembayaran dapat dianggap selesai? Informasi apa yang digunakan dan siapa yang memastikan penerimaannya? [RQ2, RQ5]\nPendalaman: Jika informasi belum tersedia, apa tindak lanjutnya? Tidak meminta membuka rekening.')
p('W6. Dalam kondisi apa pemeriksaan perlu dilakukan lagi? Ceritakan satu contoh jika pernah; bila tidak pernah, jelaskan proses yang berjalan lancar. [RQ3]\nPendalaman: Apakah ada pihak yang dihubungi kembali dan apa alasannya?')
p('W7. Apa pengaruh pemeriksaan tersebut terhadap pekerjaan atau pelayanan, jika ada? [RQ4]\nPendalaman: Adakah tindak lanjut yang tertunda? Mana yang Anda alami dan mana yang Anda perkirakan?')
p('W8. Bagian mana yang sudah membantu Anda memperoleh kepastian pembayaran? Bagian mana yang memerlukan usaha tambahan, jika ada? [RQ3, RQ5]')
p('W9. Informasi apa yang Anda perlukan ketika belum dapat menentukan tindak lanjut pembayaran, jika pernah? Apakah pembagian tugas saat ini sudah cukup jelas; adakah kebutuhan lain? [RQ5]\nPendalaman: Mengapa informasi atau pembagian itu dibutuhkan? Jangan menyebut fitur tertentu terlebih dahulu.')
p('W10. Dari ringkasan yang saya sampaikan, adakah yang kurang tepat atau pengalaman penting yang belum dibahas? [RQ1-RQ5]')
h('C2 Informan pendukung',2)
p('I1. Bagaimana prosedur pencatatan, pemeriksaan penerimaan, dan keputusan akhir pembayaran; siapa yang berwenang pada tiap langkah? [RQ2]\nI2. Ketika informasi belum cukup atau berbeda, bagaimana koordinasi dan tindak lanjut dilakukan? Ceritakan contoh atau jelaskan jika belum pernah terjadi. [RQ2, RQ4]\nI3. Informasi apa yang dibutuhkan agar catatan pembayaran dapat dipakai untuk keputusan operasional? Praktik apa yang sudah berjalan baik? [RQ5]')

# PAGE 12
page('Lampiran D Lembar pencatatan dan analisis')
h('D1 Log kejadian dan interval pemeriksaan',2)
p('Kode responden/kejadian: __________  Jenis N/R/S: __________\nTanggal dan rentang pengamatan: __________  Konteks/outlet: __________\nKeputusan akhir: __________  Status pengamatan: selesai / belum selesai\nGunakan lembar tambahan bila tindakan melebihi baris yang tersedia.')
table(['No dan interval','Tindakan serta sumber informasi','Aktif atau tunggu','Hasil atau kontak'],[
('1\n__:__:__ sampai __:__:__','________________\n________________','A / T / gangguan\nDurasi: ______','Jenis: ______\nPihak/kode: ______\nHasil: ______'),
('2\n__:__:__ sampai __:__:__','________________\n________________','A / T / gangguan\nDurasi: ______','Jenis: ______\nPihak/kode: ______\nHasil: ______'),
('3\n__:__:__ sampai __:__:__','________________\n________________','A / T / gangguan\nDurasi: ______','Jenis: ______\nPihak/kode: ______\nHasil: ______')
],[4.3,5.8,3.4,3.9])
p('Jenis kontak: pertama / ulang / serah tugas / tidak ada. Pihak dicatat sebagai peran atau kode anonim yang konsisten, tanpa nama. Ringkasan: tindakan ____; kontak ulang ____; waktu aktif ____; tunggu ____; pemeriksaan berulang Ya / Tidak terkonfirmasi / Belum dapat ditentukan. Bagian tidak terukur: __________. Perkiraan responden tidak masuk durasi teramati.')
h('D2 Catatan bukti dan masalah',2)
table(['Kode bukti','Fakta atau kutipan anonim','Jenis bukti','Interpretasi sementara'],[
('________','________________\n________________','N / R / S / W\nRQ: ______','________________\n________________'),
('________','________________\n________________','N / R / S / W\nRQ: ______','________________\n________________')
],[2.2,6.3,2.3,6.6])
p('Untuk satu masalah, catat: kode masalah; tahap/konteks; bukti pendukung; bukti yang berbeda; dampak teramati atau dilaporkan; kebutuhan yang tersirat; tingkat keyakinan beserta alasannya; hal yang masih harus dikonfirmasi. Masalah yang tidak muncul juga dicatat sebagai kasus pembanding.')
h('D3 Matriks pengolahan dan format insight',2)
p('Kolom matriks: kode responden dan kejadian | tugas nyata | konteks outlet | makna Lunas | urutan/sumber pemeriksaan | kewenangan | tindakan/waktu/kontak | keputusan/dampak | jenis bukti | RQ | kebutuhan. Rekap observasi nyata, rekonstruksi, dan simulasi pada bagian berbeda.')
p('Format insight: "Pada konteks ____, operator membutuhkan ____ karena ____. Hal ini didukung oleh bukti ____; kasus yang berbeda adalah ____. Batas temuan ____." HMW diperbarui dari kebutuhan tersebut. Semua kolom instrumen ini merupakan isian untuk pelaksanaan riset, bukan hasil pengumpulan yang sudah dilakukan.')

# PAGE 13
page('Lampiran E Stimulus penafsiran status pembayaran')
p('Stimulus untuk pertanyaan W3. Perlihatkan gambar terlebih dahulu, lalu ajukan pertanyaan tanpa menjelaskan makna Lunas atau dugaan peneliti. Gunakan gambar yang sama untuk seluruh pengguna utama.')
from PIL import Image
stimulus=ROOT / 'tmp' / 'worksheet4' / 'stimulus_B2.png'
Image.open(ROOT / 'tmp' / 'worksheet4' / 'stimulus2.png').crop((10,245,785,695)).save(stimulus)
para=doc.add_paragraph(); para.alignment=WD_ALIGN_PARAGRAPH.CENTER
para.add_run().add_picture(str(stimulus),width=Cm(15.5))
p('B2 Rincian Pembayaran pada Detail Transaksi Fleffy. Cuplikan dokumentasi 19 September 2026 yang dipakai pada Worksheet 1-2. Pemotongan membatasi area gambar; label, nominal, dan keadaan antarmuka dipertahankan. [1, 2]')
h('Pertanyaan moderator',2)
p('"Apa arti informasi pada layar ini bagi Anda? Informasi apa yang sudah dan belum diketahui?"\nPendalaman setelah jawaban spontan: "Apa yang membuat Anda menafsirkannya demikian?"')
h('Lembar jawaban stimulus',2)
p('Kode responden: __________  Tanggal: __________\nJawaban spontan atau kutipan anonim:\n________________________________________________________________\n________________________________________________________________\nAlasan atau informasi yang dirujuk:\n________________________________________________________________\n________________________________________________________________\nInformasi yang dianggap belum diketahui:\n________________________________________________________________\n________________________________________________________________')
p('Catatan untuk analisis. Stimulus memperlihatkan catatan aplikasi pada transaksi contoh, bukan mutasi rekening atau bukti penerimaan dana. Jawaban peserta dicatat sebelum diberi klarifikasi. Penafsiran responden tidak dinilai sebagai kesalahan teknis tanpa penjelasan sistem yang terverifikasi.')

doc.save(OUT)
(ROOT / 'tmp' / 'worksheet4' / 'draft_content.txt').write_text('\n\n'.join(content),encoding='utf-8')
print(str(OUT))
print('Words:',len(' '.join(content).split()))
