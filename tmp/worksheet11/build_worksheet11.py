from pathlib import Path
import json
from PIL import Image

ROOT=Path(r'D:\Rekayasa Interaksi')
old=(ROOT/'tmp/worksheet8/build_worksheet8.py').read_text(encoding='utf-8')
helpers=old.split('REQS=[')[0].replace("TMP=ROOT/'tmp'/'worksheet8'", "TMP=ROOT/'tmp'/'worksheet11'")
helpers=helpers.replace('202210370311406_Rusdany_Maestro_Worksheet8_UXRequirements','202210370311406_Rusdany_Maestro_Worksheet11_Crazy8Sketch')
helpers=helpers.replace('Kebutuhan UX Pemeriksaan Pembayaran Transfer pada Fleffy','Alternatif Ide dan Sketch Pemeriksaan Transfer pada Fleffy')
helpers=helpers.replace('Worksheet 8 Rekayasa Interaksi','Worksheet 11 Rekayasa Interaksi')
exec(compile(helpers,'helper_dokumen','exec'),globals())
DATA=json.loads((TMP/'concept_briefs.json').read_text(encoding='utf-8'))
ASSETS=TMP/'assets'
CONCEPTS=DATA['concepts']
SCORES=[(5,4,3),(4,4,2),(4,3,3),(4,4,3),(5,3,4),(3,2,4),(4,4,3),(4,3,4)]
RATIONALES=[
 'Nilai tinggi karena identitas, makna pembayaran, keadaan hasil, dan dasar keputusan tetap satu konteks. Accordion dapat disusun mengikuti bagian N1b; risiko rincian tersembunyi perlu dikendalikan.',
 'Urutan mudah diikuti, tetapi kembali saat menunggu dapat terasa seperti mengulang tahap. Kelayakan antarmuka cukup tinggi; pola langkah terpandu relatif umum.',
 'Kuat untuk membandingkan data, tetapi dua kolom pada HP mempersempit teks. Perlu respons tata letak dan pengaturan pembanding agar tetap terbaca.',
 'Riwayat dan sumber mudah ditelusuri. Penyajian peristiwa relatif sederhana; bukti pembanding lama dapat memerlukan gulir sehingga kurang langsung untuk mengambil keputusan.',
 'Kriteria kecukupan terlihat jelas. Penentuan indikator memerlukan hubungan sumber dan aturan yang konsisten; centang tidak boleh menjadi pengesahan dana oleh Ari.',
 'Koordinasi terhubung ke pesanan, tetapi percakapan dapat menambah beban membaca. Penyimpanan, pemisahan hasil resmi dari pesan, dan otorisasi menambah ketidakpastian teknis.',
 'Aksi kontekstual dekat dengan hasil dan dapat diterapkan sebagai panel N1b. Panel menutup sebagian bukti, sehingga perbandingan data memerlukan buka tutup.',
 'Mendukung kembali ke antrean dan mempertahankan pilihan. Dua konteks pada layar HP membutuhkan penandaan pesanan serta pengelolaan navigasi yang lebih teliti.'
]

def compact(text,size=11):return p(text,False,size)

def cell_p(c,text,size=11,bold=False,center=False):
    a=c.add_paragraph()
    a.alignment=WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    a.paragraph_format.line_spacing=1.02
    a.paragraph_format.space_after=Pt(4)
    a.paragraph_format.first_line_indent=Cm(0)
    for line_i,line in enumerate(text.split('\n')):
        if line_i:a.add_run().add_break()
        r=a.add_run(line);r.font.size=Pt(size);r.bold=bold
    return a

def empty_table(cols,widths):
    t=doc.add_table(rows=1,cols=cols);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for col,w in zip(t.columns,widths):col.width=Cm(w)
    for c,w in zip(t.rows[0].cells,widths):
        c.width=Cm(w);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
        c.paragraphs[0].paragraph_format.line_spacing=Pt(1)
        c.paragraphs[0].paragraph_format.space_after=Pt(0)
        pr=c._tc.get_or_add_tcPr()
        mar=OxmlElement('w:tcMar')
        for edge,v in [('top',80),('bottom',80),('left',100),('right',100)]:
            el=OxmlElement('w:'+edge);el.set(qn('w:w'),str(v));el.set(qn('w:type'),'dxa');mar.append(el)
        pr.append(mar)
        borders=OxmlElement('w:tcBorders')
        for edge in ('top','bottom','left','right'):
            el=OxmlElement('w:'+edge)
            for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]:el.set(qn('w:'+k),v)
            borders.append(el)
        pr.append(borders)
    for row in t.rows:
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
    return t

def image_in(c,key,maxw,maxh,alt):
    key={'checklist':'checklist_v2'}.get(key,key)
    path=ASSETS/(key+'.png')
    with Image.open(path) as im:w,h=im.size
    width=min(maxw,maxh*w/h)
    a=c.add_paragraph();a.alignment=WD_ALIGN_PARAGRAPH.CENTER
    a.paragraph_format.space_after=Pt(3);a.paragraph_format.line_spacing=1
    shp=a.add_run().add_picture(str(path),width=Cm(width));shp._inline.docPr.set('descr',alt)

def overview():
    for start in (0,4):
        t=empty_table(4,[6.5]*4)
        for j,c in enumerate(t.rows[0].cells):
            n=start+j;item=CONCEPTS[n]
            cell_p(c,f"{n+1} {item['name']}",10.5,True,True)
            image_in(c,item['key'],5.2,6.6,item['name'])
        a=doc.add_paragraph();a.paragraph_format.line_spacing=Pt(2);a.paragraph_format.space_after=Pt(1)

def pair(start):
    h(f"Alternatif {start+1} dan {start+2}",page=True)
    compact('Seluruh alternatif menunjukkan keadaan hasil masih ditunggu. Perbedaannya terletak pada susunan informasi dan cara interaksi, bukan warna.')
    t=empty_table(2,[13.0,13.0])
    for j,c in enumerate(t.rows[0].cells):
        n=start+j;item=CONCEPTS[n]
        cell_p(c,f"{n+1} {item['name']}",12,True,True)
        image_in(c,item['key'],9.5,11.1,f"Alternatif {n+1} {item['name']}")
        cell_p(c,item['structure']+' '+item['interaction'],10.8)
        cell_p(c,'Manfaat: '+item['value'],10.8)
        cell_p(c,'Risiko: '+item['risk'],10.8)
        if n==2:
            cell_p(c,'ID di kolom Bukti adalah tautan aplikasi, bukan isi yang diasumsikan tertulis pada bukti bank.',10.5)

def selected_pair(keys,labels,captions,heading,page=True):
    h(heading,page=page)
    compact('Keadaan tampilan dari konsep 1 pada N1b yang sama. ID, rujukan, waktu, dan hasil di gambar merupakan data ilustrasi.')
    t=empty_table(2,[13.0,13.0])
    for c,key,label,cap in zip(t.rows[0].cells,keys,labels,captions):
        image_in(c,key,7.5,15.2,label)
        cell_p(c,cap,10.5)

# 1
doc.add_paragraph('Alternatif Ide dan Sketch Pemeriksaan Transfer pada Fleffy','Title')
doc.add_paragraph('Worksheet 11 Rekayasa Interaksi','Subtitle')
p('Nama: Rusdany Maestro\nNIM: 202210370311406\nProgram studi: Informatika\nInstitusi: Universitas Muhammadiyah Malang\nJenis tugas: Praktikum Individu\nTanggal analisis: 15 Oktober 2026',False)
field('Berkas bukti pendukung','Worksheet 8 UX Requirements; Worksheet 9 Information Architecture; Worksheet 10 User Flow; workbook Pertemuan 11. Rincian sumber di bagian akhir.',10.5)
p('Saya mengembangkan delapan alternatif untuk membantu Ari meninjau dasar pemeriksaan transfer sebelum menentukan tindak lanjut satu pesanan. Konsep 1 Ringkasan bertingkat dipilih karena menjaga konteks pesanan, memisahkan pencatatan dari hasil pemeriksaan, dan menggunakan empat bagian Detail Pesanan yang telah dirancang pada Worksheet 9.')
h('Fokus masalah dan aktivitas')
field('Pengguna','Ari, nama samaran admin operasional yang juga menjalankan tugas kasir, usia 20–22 tahun. Owner atau finance memeriksa rekening; Ari menggunakan hasilnya untuk menentukan tindak lanjut. [S8; S10 bagian A]')
field('Masalah','Rujukan pesanan, bukti pelanggan, dan konfirmasi pemeriksa perlu dicocokkan. Saat hasil belum tersedia, Ari bergantung pada pihak lain dan perlu mengetahui tindak lanjut yang benar. [S8 UX02–UX05; S10 bagian B]')
field('Bagian yang dirancang','Detail Pesanan N1b pada HP, khususnya Pembayaran, Pemeriksaan, dan Tindak Lanjut. Tujuannya adalah keputusan lanjut tersimpan setelah ada hasil yang memadai; pesanan lalu siap diteruskan ke teknisi.')
h('Metode dan batas perancangan')
compact('Eksplorasi Crazy 8 dilakukan secara digital berbantuan AI dengan batas delapan menit. Delapan rumusan dan visual awal diselesaikan pada 15 Oktober 2026 pukul 19.28.56–19.36.39 WIB, selama 7 menit 43 detik. Evaluasi, perapian dokumen, dan pengembangan sketch terpilih dilakukan sesudahnya. Penilaian konsep merupakan penilaian awal peneliti, belum hasil uji pengguna.')
compact('Semua gambar memakai data ilustrasi PSN-015 dan Rp150.000. ID, rujukan bukti/permintaan, penetapan Owner, waktu, serta hasil pada sketch bukan rekaman transaksi asli. Contoh hasil hanya menjelaskan keadaan rancangan; tidak menyatakan dana transaksi nyata telah diperiksa.')

# 2–6
landscape()
h('A Crazy 8s Description and Sketches')
compact('Delapan panel eksplorasi untuk satu aktivitas. Halaman berikut memperbesar tiap alternatif beserta manfaat dan risikonya.')
overview()
compact('Gambar 1 Ringkasan delapan alternatif. Keadaan menunggu dan tombol lanjut yang belum tersedia dipertahankan pada seluruh alternatif.')
for start in (0,2,4,6):pair(start)

# 7
portrait()
h('B Evaluate Idea Matrix')
compact('Skor 1–5 menilai konsep pada konteks Ari. Total adalah penjumlahan tiga kriteria dengan bobot sama, maksimum 15. Tidak ada angka hasil pengujian pengguna dalam matriks ini.')
matrix=table(['Konsep','User Value','Feasibility','Innovation','Total'],[
    (f"{i+1} {x['name']}",*SCORES[i],sum(SCORES[i])) for i,x in enumerate(CONCEPTS)
],[6.4,2.5,2.5,2.5,2.1],11)
for row in matrix.rows[1:]:
    for c in row.cells[1:]:
        for a in c.paragraphs:a.alignment=WD_ALIGN_PARAGRAPH.CENTER
h('Arti kriteria dan dasar pemberian skor',2)
compact('User Value: kontribusi pada pencocokan pesanan, kejelasan keadaan pemeriksaan, dan keputusan yang benar. Skor 1 sangat lemah, 3 membantu sebagian, 5 mendukung tujuan inti secara jelas. Feasibility: perkiraan awal kelayakan struktur antarmuka dan perilaku yang diperlukan; skor 1 sangat rumit/tidak jelas, 3 memerlukan penanganan tambahan, 5 paling sederhana dalam asumsi yang sama. Kesiapan data, otorisasi, dan implementasi Fleffy belum diverifikasi, sehingga belum ada konsep yang diberi nilai 5 untuk Feasibility.')
compact('Innovation: perbedaan pendekatan dalam kumpulan alternatif ini, bukan klaim kebaruan di pasar. Skor 1 mengulang pendekatan lain, 3 mengubah penekanan atau pola interaksi, 5 mengubah pendekatan secara kuat. Nilai 2 dan 4 berada di antara jangkar tersebut; skala antara berlaku pada semua kriteria.')
h('Hasil evaluasi',2)
compact('Konsep 1 dan 5 sama-sama memperoleh total 12. Aturan pemilihan ketika total sama adalah User Value lebih tinggi, kemudian Feasibility lebih tinggi. Nilai User Value keduanya 5; konsep 1 dipilih karena Feasibility 4 dibanding 3 pada konsep 5. Aturan ini menjaga keputusan tetap berorientasi kebutuhan, kemudian kelayakan, tanpa menambah bobot setelah melihat hasil.')
h('Dasar penilaian setiap konsep',page=True)
compact('Penilaian berikut menghubungkan manfaat dan risiko yang tampak pada delapan alternatif dengan skor matriks. Semua konsep masih membutuhkan verifikasi data dan kewenangan pemeriksa, sehingga kelayakan implementasi belum dapat dipastikan.')
for i,item in enumerate(CONCEPTS):
    field(f"Konsep {i+1} {item['name']}",RATIONALES[i],11.5)
compact('Skor adalah alat untuk membandingkan rancangan awal, bukan bukti bahwa konsep terpilih pasti paling mudah digunakan. Jika pengujian menunjukkan alternatif lain lebih sesuai, keputusan pemilihan dapat direvisi berdasarkan temuan tersebut.')

# 8
h('C Selected Concept',page=True)
field('Konsep terpilih','1 Ringkasan bertingkat dengan empat accordion dalam Detail Pesanan N1b.')
p('Saya memilih konsep 1 karena Ari dapat tetap melihat identitas pesanan dan ringkasan keadaan pembayaran saat membuka rincian yang diperlukan. Pencatatan pembayaran tidak menutup kebutuhan hasil owner atau finance. Hasil pemeriksaan, sumber, dan dasar keputusan berada pada konteks pesanan yang sama. Struktur ini langsung mengikuti empat bagian N1b pada Worksheet 9.')
p('Risiko konsep ini adalah informasi penting tersembunyi di bagian tertutup. Karena itu, identitas pesanan, nominal, ringkasan hasil, dan alasan tindakan belum tersedia selalu terlihat. Bagian yang terkait kesalahan terbuka saat diperlukan. Pengguna dapat membuka lebih dari satu bagian agar bukti dan hasil tidak harus diingat ketika dibandingkan.')
table(['Kebutuhan pengguna S8','Penerapan dalam sketch terpilih'],[
('UX05 Must urutan 1','S3 menampilkan dasar hasil dari pemeriksa berwenang. Keputusan lanjut baru dapat dicatat bila hasil memadai; S4 menyatakan keputusan berhasil tersimpan.'),
('UX03 Must urutan 2','S1 memperjelas tujuan permintaan; S2 menunjukkan rujukan, pemeriksa sesuai penetapan, dan hasil masih ditunggu.'),
('UX02 Must urutan 3','ID pesanan tetap terlihat. Bukti pelanggan dan hasil mengacu pesanan/data terbaru; nominal saja tidak menjadi identitas.'),
('UX01 Must urutan 4','Label Pembayaran tercatat dan hasil pemeriksaan dipisahkan. Permintaan tercatat tidak diperlakukan sebagai dana diterima.'),
('UX04 Should urutan 5','S2 menyediakan Panduan saat Menunggu dan Kontak Pemeriksa. Kembali dari bantuan mempertahankan pesanan dan bagian asal.'),
('UX06 Should urutan 6','S1 menggunakan ID/nominal tersimpan. Catatan tambahan tidak menggantikan atau meminta pengisian ulang data yang sudah benar.')
],[4.5,11.5],11)
h('Posisi dalam struktur informasi',2)
compact('Ringkasan Pesanan, Pembayaran, Pemeriksaan, dan Tindak Lanjut adalah bagian N1b, bukan empat halaman baru. Navigasi bagian mengikuti NH1. Akses dari antrean N2 memakai TS1; bantuan memakai TS2 ke N3a, N3b, atau N3c. Beranda, Pesanan, Pemeriksaan Pembayaran, dan Bantuan Pemeriksaan tetap menjadi tujuan global. [S9]')

landscape()
selected_pair(['selected_before','selected_waiting'],['S1 Sebelum permintaan','S2 Menunggu hasil'],[
 'S1 P2–P5, D1–D3. Tinjau bukti dan minta pemeriksaan untuk pesanan yang sama.',
 'S2 D4, P6, T2. Hasil ditunggu; tindak lanjut dan bantuan tersedia.'
],'Sketch terpilih sebelum permintaan dan saat menunggu',page=False)
selected_pair(['selected_result','selected_saved'],['S3 Hasil memadai dan tinjauan keputusan','S4 Keputusan lanjut tersimpan'],[
 'S3 P7, D5, P9. Tinjau sumber dan dasar sebelum menyimpan keputusan.',
 'S4 D6 menuju S. Keputusan tersimpan; pesanan siap diteruskan.'
],'Sketch terpilih hasil pemeriksaan dan keadaan berhasil')

portrait()
h('Hubungan sketch dengan User Flow dan elemen antarmuka')
compact('S1–S4 adalah keadaan tampilan konsep yang sama, bukan empat halaman baru. Tabel berikut mengikat elemen yang tampak dan perilakunya ke Worksheet 10.')
table(['Elemen atau keadaan','Hubungan dengan langkah alur S10','Perilaku yang diperlukan'],[
('Menu dan kembali','P0–P1; N0/N1/N2 ke N1b.','Header kembali ke asal; pilihan/filter antrean terjaga. Menu global mengikuti S9 dan tidak membuat tujuan tambahan.'),
('Identitas dan nominal','P2; D1; UX02, UX06.','ID, metode dan tagihan menggunakan data tersimpan. Pesanan bernominal sama dibedakan dengan ID/konteks lain. Nominal serta tanggal/waktu yang tersedia ditinjau pada bukti dan hasil.'),
('Bukti dan input catatan','P2–P3; E1–T1.','Bukti/rujukan dapat dilihat; catatan tambahan opsional, bukan pengesahan dana. Data kurang jelas diklarifikasi sebelum permintaan; bukti asli dipertahankan.'),
('Minta pemeriksaan','D2, P4, D3, P5.','Cek permintaan pesanan/data yang sama. Jika sudah ada, tampilkan Lihat permintaan; jika belum, kirim dengan konteks tersimpan. Feedback sukses hanya setelah tercatat.'),
('Menunggu hasil','D4, P6, T2.','S2 memisahkan permintaan dari hasil. Owner hanya contoh penetapan pemeriksa. Panduan/kontak sesuai prosedur; tidak ada ETA yang tidak diketahui.'),
('Ringkasan hasil dan sumber','P7–D5.','Sumber berwenang, pesanan/data terbaru sama, perbandingan sesuai, dan penerimaan terkonfirmasi harus menjadi dasar lanjut. Hasil tersedia saja belum cukup.'),
('Simpan keputusan Teruskan','P9; D6.','Tinjau dasar lalu simpan keputusan dan petugas. Ini bukan tombol konfirmasi dana oleh Ari; jika hasil belum memadai, alasan tindakan belum tersedia terlihat.'),
('Konfirmasi tersimpan','D6 menuju S.','S4 menampilkan keputusan, pesanan, dan dasar yang dapat ditinjau. Pesanan siap diteruskan ke teknisi; tidak mengklaim pengerjaan sudah dimulai.')
],[4.0,4.2,7.8],11)
h('Prinsip keterbacaan sketch',2)
compact('Teks keadaan menyertai ikon; makna tidak bergantung warna. Tombol utama memiliki label tindakan yang spesifik. Rancangan tombol tidak aktif menyertakan alasan dan tindakan pemulihan. Ukuran sentuh, kepadatan teks, fokus, dan pembacaan pada HP akan diperiksa lagi pada wireframe; ukuran final belum ditetapkan dari gambar ini.')

h('Penanganan kondisi lain dan rencana pengembangan',page=True)
compact('Gambar memperlihatkan jalur utama dan keadaan menunggu. Kondisi di bawah tetap menjadi bagian rancangan; tidak boleh hilang ketika sketch dikembangkan menjadi wireframe.')
table(['Kondisi alur S10','Perubahan tampilan dan tindakan'],[
('D1 Tidak; E1–T1','Buka bagian Pembayaran; tandai informasi yang kurang/cocoknya belum jelas dan jelaskan cara klarifikasi. Jangan menganggap bukti pelanggan sebagai kepastian dana masuk. Setelah benar, tinjau ulang data.'),
('D3 Tidak atau belum pasti; E2','Pertahankan data, tampilkan kendala pengiriman dan Periksa permintaan. Rekonsiliasi keberadaan permintaan melalui D2 sebelum menawarkan kirim ulang.'),
('D5 Tidak; P8–T3','Tampilkan Hasil belum memadai beserta sumber/alasan yang diketahui. Tindakan lanjut belum tersedia; tawarkan Tahan dan minta klarifikasi sesuai kewenangan. Setelah hasil baru tersedia, tinjau ulang P7–D5.'),
('Data berubah setelah hasil dibuat','Tandai bahwa hasil mengacu data sebelumnya. Hasil lama tidak menjadi dasar lanjut untuk versi terbaru; minta pemeriksaan atau klarifikasi yang sesuai.'),
('D6 Tidak atau belum pasti; E3','Jangan tampilkan S4. Tampilkan Keputusan belum terkonfirmasi; tetap pada pesanan, cek catatan keputusan dan kendala, lalu ulangi aman bila memang belum tersimpan.')
],[5.0,11.0],11)
h('Langkah berikutnya dan validasi',2)
compact('Kembangkan konsep 1 menjadi wireframe lalu uji pada pengguna dengan tugas serupa. Gunakan skenario hasil sesuai, dua pesanan bernominal sama, bukti kurang jelas, hasil masih ditunggu, hasil tidak cocok, serta kirim/simpan terputus. Amati apakah pengguna memilih pesanan yang tepat, membedakan catatan dari hasil, menemukan sumber, menahan ketika dasar belum cukup, dan mengenali keputusan benar-benar tersimpan.')
compact('Uji khusus accordion memeriksa apakah pengguna dapat menemukan bukti dan hasil tanpa kehilangan konteks. Jika informasi inti sering terlewat, pertahankan ringkasannya di luar bagian yang tertutup atau buka bagian terkait secara kontekstual. Belum ada hasil uji, tingkat keberhasilan, atau penghematan waktu yang diklaim.')
h('Sumber dan catatan penyusunan',2)
compact('S8: Rusdany Maestro, Worksheet 8 UX Requirements, daftar UX01–UX06 dan prioritas. S9: Rusdany Maestro, Worksheet 9 Information Architecture, N1b, empat bagian, TS1, TS2, dan NH1. S10: Rusdany Maestro, Worksheet 10 User Flow, bagian A, diagram usulan A/B, rincian langkah, serta kondisi kesalahan dan pemulihan.')
compact('W: UX Design Hands-on Workbook, Pertemuan 11, A Crazy 8s Description / Sketches, B Evaluate Idea Matrix, C Selected Concept. Instruksi dan rubrik Worksheet 11 dari Google Classroom menjadi acuan pengumpulan. Referensi tampilan pembayaran diambil dari dokumentasi Worksheet 1 sebagai konteks awal; susunan pada gambar merupakan usulan baru. Gambar divisualisasikan dengan alat AI dan diperiksa terhadap sumber, bukan tangkapan layar produk yang sudah diterapkan.')

# Keep the empty paragraph carrying the last section break small enough for Docs.
break_paragraphs=[a for a in doc.paragraphs if a._p.pPr is not None and a._p.pPr.find(qn('w:sectPr')) is not None]
last_break=break_paragraphs[-1]
last_break.paragraph_format.space_before=Pt(0)
last_break.paragraph_format.space_after=Pt(0)
last_break.paragraph_format.line_spacing=Pt(1)
pr=last_break._p.get_or_add_pPr()
rp=OxmlElement('w:rPr')
for tag in ('sz','szCs'):
    el=OxmlElement('w:'+tag);el.set(qn('w:val'),'2');rp.append(el)
pr.append(rp)

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

raw=TMP/(STEM+'_sebelum_sanitasi.docx');doc.save(raw)
texts=[a.text for a in doc.paragraphs if a.text.strip()]
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:texts.extend(a.text for a in c.paragraphs if a.text.strip())
(TMP/'report_content.txt').write_text('\n\n'.join(texts),encoding='utf-8')
(TMP/'content_blocks.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'raw_docx':str(raw),'tables':len(doc.tables),'images':len(doc.inline_shapes),'sections':len(doc.sections)},ensure_ascii=False))
