const page=figma.root.children.find(p=>p.id==='0:1');await figma.setCurrentPageAsync(page);
await Promise.all(['Regular','Medium','Bold'].map(style=>figma.loadFontAsync({family:'Roboto',style})));
const state=STATE_FOUNDATIONS;
const areas={guide:await figma.getNodeByIdAsync('2:18'),main:await figma.getNodeByIdAsync('2:19'),support:await figma.getNodeByIdAsync('2:20')};
const vars=Object.fromEntries(await Promise.all(Object.entries(state.variables).map(async([k,id])=>[k,await figma.variables.getVariableByIdAsync(id)])));
const comps=Object.fromEntries(await Promise.all(Object.entries(state.components).map(async([k,id])=>[k,await figma.getNodeByIdAsync(id)])));
const imported=await Promise.all(['1e92164361231ef1ed79f8fd256e78e0f6fbf250','4aeaa89a2f980c69d11b84a0e2a4f1268119c277'].map(k=>figma.importStyleByKeyAsync(k)));
const styles={...state.styles,body14:imported[0].id,body16:imported[1].id};
const screens={},links=[],accordions=[],stats=[];
function paint(k){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',vars['color/'+k]);}
function bg(n,k='surface'){n.fills=[paint(k)];}
function edge(n){n.strokes=[paint('border')];n.strokeWeight=1;}
function bind(n,key,val){n.setBoundVariable(key,vars[val]);}
function pad(n,size){for(const key of ['paddingTop','paddingBottom','paddingLeft','paddingRight'])bind(n,key,'space/'+size);}
function gap(n,size){bind(n,'itemSpacing','space/'+size);}
function corners(n,size=6){for(const key of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])bind(n,key,'radius/'+size);}
function stack(parent,name,w=358,space=8,padding=0){const n=figma.createAutoLayout('VERTICAL');parent.appendChild(n);n.name=name;n.resize(w,1);n.primaryAxisSizingMode='AUTO';n.counterAxisSizingMode='FIXED';gap(n,space);if(padding)pad(n,padding);n.fills=[];return n;}
function row(parent,name,w=326,h=44){const n=figma.createAutoLayout('HORIZONTAL');parent.appendChild(n);n.name=name;n.resize(w,h);n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';n.counterAxisAlignItems='CENTER';n.primaryAxisAlignItems='SPACE_BETWEEN';n.fills=[];return n;}
async function text(parent,str,w=326,style='body14',color='text'){const n=figma.createText();parent.appendChild(n);await n.setTextStyleIdAsync(styles[style]);n.characters=str;n.textAutoResize='HEIGHT';n.resize(w,n.height);n.fills=[paint(color)];n.name=str;return n;}
function prop(inst,key,value){const def=inst.componentProperties;const k=Object.keys(def).find(k=>k.startsWith(key+'#'));if(k)inst.setProperties({[k]:value});}
function instance(parent,family,variant,name){const main=comps[family].children.find(c=>Object.entries(variant).every(([k,v])=>c.variantProperties[k]===v));if(!main)throw new Error('Missing variant '+family);const n=main.createInstance();parent.appendChild(n);n.name=name;return n;}
function button(parent,label,dest=null,appearance='Primary',disabled=false){const n=instance(parent,'button',{Appearance:appearance,State:disabled?'Disabled':'Enabled'},label);prop(n,'Label',label);if(dest&&!disabled)links.push({id:n.id,dest});return n;}
function input(parent,value,state='Single'){const n=instance(parent,'input',{State:state},value);prop(n,'Value',value);return n;}
function badge(parent,label,strong=false){const n=instance(parent,'badge',{Tone:strong?'Strong':'Neutral'},label);prop(n,'Label',label);return n;}
async function link(parent,label,dest,w=326){const n=row(parent,label,w,44);const t=await text(n,label,w,'label');if(dest)links.push({id:n.id,dest});return n;}
async function card(parent,title,body,w=358){const n=stack(parent,title,w,8,16);bg(n);edge(n);corners(n);if(title)await text(n,title,w-32,'heading');if(body)await text(n,body,w-32);return n;}
async function kv(parent,k,v,w=326){const n=row(parent,k,w,24);await text(n,k,Math.round(w*.47),'body14','secondary');const t=await text(n,v,Math.floor(w*.53),'label');t.textAlignHorizontal='RIGHT';return n;}
async function note(parent,title,body){const n=stack(parent,title,358,4,12);bg(n,'soft');corners(n);await text(n,title,334,'label');await text(n,body,334,'body14');return n;}
async function accordion(parent,title,open,build){const n=stack(parent,title,358,0);bg(n);edge(n);corners(n);const h=instance(n,'accordion',{State:open?'Open':'Closed'},title);prop(h,'Title',title);if(open&&build){const b=stack(n,'Isi '+title,358,8,16);await build(b);}accordions.push({headerId:h.id,title,open});return n;}
async function payment(parent,open=true){return accordion(parent,'Pembayaran',open,async b=>{badge(b,'Pembayaran tercatat');await text(b,'Pencatatan belum memastikan dana masuk.',326,'body14','secondary');await link(b,'Lihat bukti BKT-015','Bukti');});}
async function identity(root){const n=stack(root,'Identitas pesanan tetap',390,4,16);n.resize(390,92);n.primaryAxisSizingMode='FIXED';bg(n);await text(n,'Detail pesanan',358,'title');await text(n,'PSN-015  ·  Bank Transfer  ·  Rp150.000',358,'label');}
async function top(root,detail,title){const n=row(root,'Bilah atas',390,48);bind(n,'paddingLeft','space/16');bind(n,'paddingRight','space/16');bg(n);if(detail){await link(n,'‹ Kembali','BACK',110);await link(n,'Bantuan','Help',92);}else{await text(n,'FLEFFY',180,'heading');const t=await text(n,'Ari · Admin',148,'caption','secondary');t.textAlignHorizontal='RIGHT';}}
async function navigation(root,active){const n=row(root,'Navigasi utama',390,64);n.paddingLeft=16;n.paddingRight=16;bg(n);edge(n);for(const [title,key] of [['Beranda','Home'],['Pesanan','Orders'],['Pemeriksaan','Queue'],['Bantuan','Help']]){const i=instance(n,'nav',{State:active===key?'Active':'Inactive'},title);prop(i,'Label',title);links.push({id:i.id,dest:key});}}
async function screen(area,key,label,index,desc,{detail=false,title=label,active='Orders',rowIndex=null}={}){if(area.children.some(n=>n.name===key))throw new Error('Screen exists '+key);const holder=stack(area,key,470,12);holder.x=32+(index%4)*510;holder.y=110+Math.floor(index/4)*1015;holder.counterAxisAlignItems='CENTER';await text(holder,label,470,'heading');const root=figma.createAutoLayout('VERTICAL');holder.appendChild(root);root.name=key+' / '+label;root.resize(390,844);root.primaryAxisSizingMode='FIXED';root.counterAxisSizingMode='FIXED';root.clipsContent=true;root.cornerRadius=12;edge(root);bg(root);await top(root,detail,title);if(detail)await identity(root);const viewport=figma.createAutoLayout('VERTICAL');root.appendChild(viewport);viewport.name='Konten / gulir vertikal';viewport.resize(390,detail?640:732);viewport.primaryAxisSizingMode='FIXED';viewport.counterAxisSizingMode='FIXED';viewport.clipsContent=true;viewport.overflowDirection='VERTICAL';bg(viewport,'canvas');const content=stack(viewport,'Konten',390,8,16);if(!detail)await text(content,title,358,'title');screens[key]={root:root.id,holder:holder.id,content:content.id,viewport:viewport.id,label,active};await text(holder,desc,470,'body14','secondary');return {root,content,viewport,holder};}
async function finish(key,s){await navigation(s.root,screens[key].active);stats.push({key,id:s.root.id,contentHeight:s.content.height,viewportHeight:s.viewport.height,scrolls:s.content.height>s.viewport.height});}
async function mainHeaders(){for(const [area,title,subtitle] of [[areas.main,'01  ALUR UTAMA · 8 LAYAR','01 → 02 → 03 → 04 | Skenario hasil Owner tersedia: 05 → 06 → 07. Bantuan: 08.'],[areas.support,'02  KONDISI & HALAMAN PENDUKUNG','Cabang pemulihan, bantuan dan variasi state. Data dan hasil di bawah adalah ilustrasi prototype.']]){const n=stack(area,title,2036,8);n.x=32;n.y=24;await text(n,title,2036,'title');await text(n,subtitle,2036,'body16','secondary');}}
await mainHeaders();
{
 const s=await screen(areas.main,'Home','01 · Beranda',0,'N0 · Titik awal. Admin sudah masuk. Data pada seluruh layar adalah ilustrasi.',{title:'Beranda',active:'Home'});
 await text(s.content,'Halo, Ari',358,'heading');await text(s.content,'Periksa pembayaran sebelum pesanan diteruskan.',358,'body16','secondary');
 let c=await card(s.content,'Pemeriksaan pembayaran','Pantau permintaan dan tindak lanjut pesanan.');button(c,'Buka pemeriksaan','Queue');
 c=await card(s.content,'Pesanan laundry sepatu','Temukan pesanan melalui ID atau nama pelanggan.');button(c,'Lihat pesanan','Orders','Secondary');
 await note(s.content,'Pisahkan status dan keputusan','Pembayaran tercatat belum memastikan dana masuk. Gunakan hasil pemeriksa yang berwenang.');
 await link(s.content,'Bantuan pemeriksaan','Help',358);await finish('Home',s);
}
async function orderCard(parent,id,name,status,dest,extra=''){const c=await card(parent,id+' · '+name,'Laundry sepatu · Bank Transfer');await kv(c,'Tagihan','Rp150.000');badge(c,status);if(extra)await text(c,extra,326,'body14','secondary');button(c,'Buka '+id,dest,'Secondary');return c;}
{
 const s=await screen(areas.main,'Orders','02 · Daftar pesanan',1,'N1 · Identitas pesanan menjadi acuan. Nominal sama tidak berarti pesanan sama.',{title:'Pesanan'});
 const search=await card(s.content,'Cari pesanan',null);input(search,'Cari ID / nama pelanggan');button(search,'Cari','Empty','Secondary');
 await orderCard(s.content,'PSN-015','Pelanggan A','Belum diminta','Before');await orderCard(s.content,'PSN-016','Pelanggan B','Menunggu hasil','WaitingB');await finish('Orders',s);
}
{
 const s=await screen(areas.main,'Before','03 · Detail / belum diminta',2,'N1b / S1 · UX01, UX02, UX03. Data pesanan dipakai ulang; catatan bersifat opsional.',{detail:true});
 await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content);
 await accordion(s.content,'Pemeriksaan',true,async b=>{badge(b,'Belum diminta');await kv(b,'Tujuan pemeriksa','Owner');await text(b,'Identitas, nominal dan bukti mengikuti pesanan ini.',326,'body14','secondary');input(b,'Catatan tambahan (opsional)');button(b,'Minta pemeriksaan','Waiting');});
 await accordion(s.content,'Tindak lanjut',true,async b=>{button(b,'Teruskan',null,'Primary',true);await text(b,'Belum ada hasil pemeriksa yang dapat menjadi dasar keputusan.',326,'body14','secondary');});await finish('Before',s);
}
async function waitingContent(s,id='PSN-015',req='PRM-015'){
 await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);
 await accordion(s.content,'Pemeriksaan',true,async b=>{badge(b,'Menunggu hasil');await kv(b,'Permintaan',req);await kv(b,'Pemeriksa','Owner');await text(b,'Permintaan tercatat. Hasil belum tersedia.',326,'body16');await link(b,'Panduan saat menunggu','Guide');await link(b,'Kontak pemeriksa','Contact');});
 await accordion(s.content,'Tindak lanjut',true,async b=>{button(b,'Teruskan',null,'Primary',true);await text(b,'Tunggu hasil yang sesuai dengan pesanan dan data terbaru.',326,'body14','secondary');});
}
{
 const s=await screen(areas.main,'Waiting','04 · Detail / menunggu',3,'N1b / S2 · Permintaan tercatat tidak sama dengan hasil tersedia. Tidak ada janji waktu.',{detail:true});await waitingContent(s);await finish('Waiting',s);
}
async function queueContent(s,stateLabel){const c=await card(s.content,'Cari pemeriksaan',null);input(c,'Cari ID pesanan');const filters=stack(s.content,'Filter status',358,8);for(const [label,key] of [['Belum diminta','QueueBefore'],['Menunggu hasil','QueueWait'],['Hasil tersedia','Queue']]){const f=await link(filters,(label===stateLabel?'●  ':'○  ')+label,key,358);bg(f,label===stateLabel?'soft':'surface');corners(f);pad(f,12);}await text(s.content,stateLabel,358,'heading');if(stateLabel==='Hasil tersedia')await orderCard(s.content,'PSN-015','Pelanggan A','Hasil tersedia','Result','Owner · HAS-015. Baca isi hasil sebelum mengambil keputusan.');else if(stateLabel==='Menunggu hasil')await orderCard(s.content,'PSN-015','Pelanggan A','Menunggu hasil','Waiting','PRM-015 · Owner · hasil belum tersedia.');else await orderCard(s.content,'PSN-015','Pelanggan A','Belum diminta','Before','Belum ada permintaan untuk data terbaru.');}
{
 const s=await screen(areas.main,'Queue','05 · Antrean / hasil tersedia',4,'N2 → TS1 → N1b/Pemeriksaan. Skenario: Owner sudah menyampaikan hasil. Bukan hasil otomatis.',{title:'Pemeriksaan pembayaran',active:'Queue'});await queueContent(s,'Hasil tersedia');await finish('Queue',s);
}
async function resultContent(s){await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',true,async b=>{badge(b,'Hasil tersedia',true);await kv(b,'Sumber berwenang','Owner');await kv(b,'Hasil / permintaan','HAS-015 / PRM-015');await text(b,'Untuk PSN-015 · data terbaru',326,'label');await text(b,'✓ Identitas pesanan dan bukti sesuai\n✓ Nominal sesuai: Rp150.000\n✓ Waktu transfer cocok dengan data bukti\n✓ Dana diterima menurut hasil Owner',326);});await accordion(s.content,'Tindak lanjut',true,async b=>{await text(b,'Dasar keputusan: HAS-015',326,'label');button(b,'Simpan keputusan Teruskan','Saved');button(b,'Tahan untuk klarifikasi','Hold','Secondary');});}
{
 const s=await screen(areas.main,'Result','06 · Detail / hasil memadai',5,'N1b / S3 · UX05. Admin menilai hasil berwenang; bukan mengesahkan mutasi rekening sendiri.',{detail:true});await resultContent(s);await finish('Result',s);
}
{
 const s=await screen(areas.main,'Saved','07 · Keputusan tersimpan',6,'N1b / S4 · Sukses sesudah penyimpanan terkonfirmasi. Pengerjaan teknisi di luar alur.',{detail:true});
 await note(s.content,'Keputusan lanjut tersimpan','Pesanan siap diteruskan ke teknisi.');await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',false);await accordion(s.content,'Tindak lanjut',true,async b=>{await kv(b,'Keputusan','Teruskan');await kv(b,'Dasar','HAS-015');await kv(b,'Petugas','Ari · Admin');await text(b,'Status ini mencatat keputusan. Pesanan belum dinyatakan selesai dikerjakan.',326,'body14','secondary');button(b,'Lihat catatan keputusan','Decision','Secondary');});await finish('Saved',s);
}
{
 const s=await screen(areas.main,'Guide','08 · Panduan saat menunggu',7,'N3b · TS2 kembali ke pesanan dan bagian asal. Bantuan tidak menjanjikan ETA.',{title:'Panduan saat menunggu',active:'Help'});
 await note(s.content,'Konteks tetap tersimpan','PSN-015 · PRM-015 · Owner');
 for(const [title,body] of [['1. Pastikan permintaan tercatat','Gunakan nomor permintaan yang sudah ada. Hindari mengirim ulang sebelum memeriksa riwayat.'],['2. Hubungi pemeriksa yang ditetapkan','Sampaikan ID pesanan dan permintaan agar pemeriksa dapat menemukan data yang tepat.'],['3. Jelaskan status kepada pelanggan','Sampaikan bahwa hasil pemeriksaan masih ditunggu. Belum ada kepastian dana masuk dari aplikasi.']])await card(s.content,title,body);
 const c=await card(s.content,'Tindak lanjut',null);button(c,'Kontak pemeriksa','Contact');button(c,'Kembali ke pemeriksaan','Waiting','Secondary');await finish('Guide',s);
}
// Supporting frames: 16 states/destinations, kept on the same page.
{
 const s=await screen(areas.support,'Bukti','P01 · Lihat bukti',0,'Bukti ilustrasi. Bukan dokumen bank asli dan bukan verifikasi penerimaan dana.',{title:'Bukti pembayaran'});
 await note(s.content,'Terkait PSN-015','BKT-015 · Bank Transfer · Rp150.000');let c=await card(s.content,'Pratinjau bukti','Area berkas bukti transfer pelanggan.');const box=stack(c,'Placeholder bukti',326,8,16);box.resize(326,200);box.primaryAxisSizingMode='FIXED';bg(box,'soft');box.primaryAxisAlignItems='CENTER';await text(box,'BUKTI TRANSFER\nBKT-015\nRp150.000',294,'heading');await text(box,'Data contoh · gambar bukti belum disertakan',294,'caption','secondary');await kv(c,'Tanggal bukti','15 Okt 2026');await kv(c,'Waktu bukti','10.20 WIB');await text(c,'Tanggal dan waktu adalah ilustrasi. Gunakan data pada bukti asli ketika diimplementasikan.',326,'body14','secondary');button(c,'Kembali ke pesanan','BACK','Secondary');await finish('Bukti',s);
}
{
 const s=await screen(areas.support,'Incomplete','P02 · Bukti belum jelas',1,'T1 · Klarifikasi data sebelum permintaan; tombol lanjut tetap nonaktif.',{detail:true});await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',true,async b=>{badge(b,'Perlu klarifikasi');await text(b,'Nominal atau waktu pada bukti belum terbaca. Cocokkan dengan data pesanan sebelum meminta pemeriksaan.',326);button(b,'Lihat bukti','Bukti','Secondary');button(b,'Minta pemeriksaan',null,'Primary',true);});await accordion(s.content,'Tindak lanjut',true,async b=>{button(b,'Teruskan',null,'Primary',true);await text(b,'Klarifikasi data kepada pelanggan sesuai prosedur outlet.',326);});await finish('Incomplete',s);
}
{
 const s=await screen(areas.support,'SendUncertain','P03 · Pengiriman belum pasti',2,'E2 · Periksa permintaan yang sudah ada sebelum mencoba mengirim ulang.',{detail:true});await note(s.content,'Pengiriman belum terkonfirmasi','Data pesanan dan catatan tetap tersedia. Jangan mengirim ulang sebelum memeriksa permintaan.');await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',true,async b=>{await text(b,'PSN-015 · Rp150.000 · BKT-015\nTujuan: Owner',326);input(b,'Catatan sebelumnya tetap tersimpan','ReadOnly');button(b,'Periksa permintaan','QueueWait');await text(b,'Jika belum tercatat, kembali dan coba kirim. Jika sudah ada, gunakan permintaan tersebut.',326,'body14','secondary');});await accordion(s.content,'Tindak lanjut',false);await finish('SendUncertain',s);
}
{
 const s=await screen(areas.support,'Insufficient','P04 · Hasil belum memadai',3,'T3 · Hasil tersedia belum cukup untuk mengizinkan Teruskan.',{detail:true});await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',true,async b=>{badge(b,'Perlu klarifikasi');await kv(b,'Sumber','Owner');await kv(b,'Hasil','HAS-015');await text(b,'Nominal cocok, tetapi kecocokan waktu transfer belum jelas. Penerimaan untuk pesanan ini belum dapat dipastikan.',326);});await accordion(s.content,'Tindak lanjut',true,async b=>{button(b,'Teruskan',null,'Primary',true);await text(b,'Hasil belum memenuhi dasar keputusan untuk data terbaru.',326,'body14','secondary');button(b,'Tahan untuk klarifikasi','Hold','Secondary');});await finish('Insufficient',s);
}
{
 const s=await screen(areas.support,'Changed','P05 · Data pesanan berubah',4,'Hasil versi lama tidak berlaku untuk data terbaru. Pemeriksaan ulang mengikuti konteks terbaru.',{detail:true});await note(s.content,'Hasil sebelumnya perlu diperbarui','HAS-015 dibuat untuk data sebelumnya. Jangan gunakan hasil tersebut sebagai dasar keputusan terbaru.');await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',true,async b=>{await text(b,'Tinjau ulang identitas, nominal dan bukti terbaru sebelum meminta pemeriksaan.',326);button(b,'Tinjau data pembayaran','Before','Secondary');});await accordion(s.content,'Tindak lanjut',true,async b=>{button(b,'Teruskan',null,'Primary',true);await text(b,'Diperlukan hasil yang cocok dengan data terbaru.',326,'body14','secondary');});await finish('Changed',s);
}
{
 const s=await screen(areas.support,'SaveUncertain','P06 · Penyimpanan belum pasti',5,'E3 · Tidak menampilkan sukses. Periksa catatan keputusan sebelum menyimpan ulang.',{detail:true});await note(s.content,'Keputusan belum terkonfirmasi','Periksa catatan untuk mengetahui apakah keputusan sudah tersimpan.');await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',false);await accordion(s.content,'Tindak lanjut',true,async b=>{await kv(b,'Pilihan keputusan','Teruskan');await kv(b,'Dasar','HAS-015');await text(b,'Pilihan dan data pesanan tetap tersedia.',326);button(b,'Periksa catatan keputusan','Decision');await text(b,'Jika catatan sudah ada, gunakan catatan itu. Jika belum ada, kembali ke peninjauan hasil sebelum mencoba ulang.',326,'body14','secondary');});await finish('SaveUncertain',s);
}
{
 const s=await screen(areas.support,'Empty','P07 · Pencarian tanpa hasil',6,'Empty state · Tidak menyimpulkan pesanan hilang. Pengguna dapat memperbaiki atau mereset pencarian.',{title:'Pesanan'});const c=await card(s.content,'Cari pesanan',null);input(c,'PSN-999');button(c,'Cari','Empty','Secondary');await note(s.content,'Pesanan tidak ditemukan','Tidak ada hasil untuk “PSN-999”. Periksa ID atau nama pelanggan, lalu coba kembali.');const r=await card(s.content,'Coba pencarian lain','Periksa ejaan atau kosongkan kata pencarian.');button(r,'Hapus pencarian','Orders');await finish('Empty',s);
}
{
 const s=await screen(areas.support,'Hold','P08 · Keputusan tahan tersimpan',7,'Akhir cabang T3. Pesanan tidak dinyatakan siap diteruskan.',{detail:true});await note(s.content,'Keputusan tahan tersimpan','PSN-015 menunggu klarifikasi. Pesanan belum siap diteruskan.');await accordion(s.content,'Ringkasan pesanan',false);await payment(s.content,false);await accordion(s.content,'Pemeriksaan',false);await accordion(s.content,'Tindak lanjut',true,async b=>{await kv(b,'Keputusan','Tahan');await kv(b,'Dasar','HAS-015');await text(b,'Alasan: hasil memerlukan klarifikasi untuk pesanan ini.',326);button(b,'Kontak pemeriksa','Contact','Secondary');button(b,'Teruskan',null,'Primary',true);});await finish('Hold',s);
}
{
 const s=await screen(areas.support,'Help','P09 · Bantuan pemeriksaan',8,'N3 · Tiga kategori bantuan sesuai struktur informasi Worksheet 9.',{title:'Bantuan pemeriksaan',active:'Help'});await text(s.content,'Pilih bantuan sesuai kondisi pesanan.',358,'body16','secondary');for(const [title,body,dest] of [['Arti status pembayaran','Bedakan pencatatan, permintaan, hasil dan keputusan.','Status'],['Panduan saat menunggu','Tindak lanjut saat hasil pemeriksaan belum tersedia.','Guide'],['Kontak pemeriksa','Temukan tujuan pemeriksa pada pesanan yang dipilih.','Contact']]){const c=await card(s.content,title,body);button(c,'Buka panduan',dest,'Secondary');}await finish('Help',s);
}
{
 const s=await screen(areas.support,'Status','P10 · Arti status pembayaran',9,'N3a · Label menjelaskan kondisi yang diketahui, bukan dugaan penerimaan dana.',{title:'Arti status pembayaran',active:'Help'});for(const [title,body] of [['Pembayaran tercatat','Transaksi tercatat di aplikasi; penerimaan dana masih membutuhkan pemeriksaan.'],['Menunggu hasil','Permintaan sudah tercatat, hasil pemeriksa belum tersedia.'],['Hasil tersedia','Ada hasil untuk dibaca. Nilai kecocokan pesanan, data terbaru dan kewenangan sumber.'],['Keputusan lanjut tersimpan','Admin sudah menyimpan keputusan berdasarkan hasil memadai. Pesanan siap diteruskan.']])await card(s.content,title,body);const c=await card(s.content,'Kembali',null);button(c,'Kembali ke bantuan','Help','Secondary');await finish('Status',s);
}
{
 const s=await screen(areas.support,'Contact','P11 · Kontak pemeriksa',10,'N3c · Informasi kontak belum tersedia dalam riset. Tidak mengarang nomor, kanal, atau SLA.',{title:'Kontak pemeriksa',active:'Help'});await note(s.content,'Konteks permintaan','PSN-015 · PRM-015');let c=await card(s.content,'Pemeriksa yang ditetapkan',null);await kv(c,'Peran','Owner');await text(c,'Nomor atau kanal kontak belum tersedia pada contoh ini. Gunakan saluran yang disepakati outlet.',326);c=await card(s.content,'Informasi yang disampaikan','Sertakan PSN-015, PRM-015, nominal Rp150.000 dan bagian yang perlu diklarifikasi.');await text(c,'Hindari mengirim ulang permintaan yang sudah tercatat.',326,'body14','secondary');button(c,'Kembali ke pemeriksaan','Waiting','Secondary');await finish('Contact',s);
}
{
 const s=await screen(areas.support,'Decision','P12 · Catatan keputusan',11,'Catatan contoh yang terkonfirmasi. Pemeriksaan catatan membantu mencegah duplikasi.',{title:'Catatan keputusan'});await note(s.content,'Catatan ditemukan','Keputusan untuk PSN-015 sudah tersimpan.');const c=await card(s.content,'PSN-015',null);await kv(c,'Keputusan','Teruskan');await kv(c,'Dasar hasil','HAS-015');await kv(c,'Permintaan','PRM-015');await kv(c,'Petugas','Ari · Admin');await kv(c,'Status','Tersimpan');await text(c,'Pesanan siap diteruskan ke teknisi.',326,'body16');button(c,'Kembali ke detail','Saved','Secondary');await finish('Decision',s);
}
for(const [key,label,status,index] of [['QueueBefore','P13 · Antrean / belum diminta','Belum diminta',12],['QueueWait','P14 · Antrean / menunggu','Menunggu hasil',13]]){const s=await screen(areas.support,key,label,index,'N2 · Filter tetap jelas. Membuka item menuju bagian Pemeriksaan pada pesanan yang sama.',{title:'Pemeriksaan pembayaran',active:'Queue'});await queueContent(s,status);await finish(key,s);}
{
 const s=await screen(areas.support,'Summary','P15 · Ringkasan terbuka',14,'N1b · Variasi accordion, tetap pada halaman detail pesanan yang sama.',{detail:true});await accordion(s.content,'Ringkasan pesanan',true,async b=>{await kv(b,'ID pesanan','PSN-015');await kv(b,'Pelanggan','Pelanggan A');await kv(b,'Layanan','Laundry sepatu');await kv(b,'Metode','Bank Transfer');await kv(b,'Tagihan','Rp150.000');await text(b,'Gunakan identitas pesanan dan bukti untuk mencocokkan pembayaran; nominal saja tidak cukup.',326,'body14','secondary');});await payment(s.content,false);await accordion(s.content,'Pemeriksaan',false);await accordion(s.content,'Tindak lanjut',false);const c=await card(s.content,'Pemeriksaan pembayaran',null);button(c,'Buka pemeriksaan','Before','Secondary');await finish('Summary',s);
}
{
 const s=await screen(areas.support,'WaitingB','P16 · Pesanan lain / PSN-016',15,'Contoh kedua dengan nominal sama. Identitas dan bukti tetap milik PSN-016.',{detail:true});const ident=s.root.query('FRAME[name="Identitas pesanan tetap"] TEXT').last();if(ident){ident.characters='PSN-016  ·  Bank Transfer  ·  Rp150.000';}
 await accordion(s.content,'Ringkasan pesanan',true,async b=>{await kv(b,'Pelanggan','Pelanggan B');await kv(b,'Bukti','BKT-016');});await accordion(s.content,'Pembayaran',true,async b=>{badge(b,'Pembayaran tercatat');await text(b,'Bukti BKT-016 terkait PSN-016. Pencatatan belum memastikan dana masuk.',326);});await accordion(s.content,'Pemeriksaan',true,async b=>{badge(b,'Menunggu hasil');await kv(b,'Permintaan','PRM-016');await kv(b,'Pemeriksa','Owner');await text(b,'Hasil untuk PSN-015 tidak digunakan bagi pesanan ini.',326);});await accordion(s.content,'Tindak lanjut',false);await finish('WaitingB',s);
}
// Review cover remains outside the mobile product screens.
{
 const g=stack(areas.guide,'Penjelasan rancangan',2036,12);g.x=32;g.y=24;
 await text(g,'FLEFFY  /  WIREFRAME',2036,'display');
 await text(g,'Pemeriksaan pembayaran Bank Transfer · Kasir laundry sepatu',2036,'title');
 await text(g,'Rusdany Maestro  ·  202210370311406  ·  Rekayasa Interaksi',2036,'body16','secondary');
 await text(g,'Dasar rancangan: WS8 kebutuhan UX → WS9 arsitektur informasi → WS10 user flow → WS11 konsep terpilih “Ringkasan bertingkat”. Persona: Ari, Admin Operasional.',2036,'body16');
 await text(g,'Navigasi global: Beranda / Pesanan / Pemeriksaan / Bantuan. Detail pesanan N1b terdiri dari empat bagian; layar S1–S4 adalah state satu halaman, bukan empat halaman IA baru.',2036,'body16');
 await text(g,'Prototype A: 01 → 02 → 03 → 04 (menunggu). Prototype B: 05 → 06 → 07 (hasil Owner tersedia). Perpindahan hasil adalah skenario terpisah; tidak ada verifikasi bank otomatis atau tombol admin untuk membuat hasil Owner.',2036,'body16');
 await text(g,'Seluruh ID, nominal, nama pelanggan, waktu dan hasil merupakan data ilustrasi. Kontak pemeriksa belum diberikan. Field teks dalam prototype adalah contoh statis; semua layer dapat diedit.',2036,'body14','secondary');
 await text(g,'Visual: hitam, putih, abu-abu. 390 × 844 px; konten panjang dapat digulir; navigasi utama tetap di bawah. File satu halaman dengan komponen lokal dan satu mode variable.',2036,'body14','secondary');
}
return {createdNodeIds:Object.values(areas).flatMap(a=>a.query('*').map(n=>n.id)),mutatedNodeIds:Object.values(areas).map(a=>a.id),screens:Object.fromEntries(Object.entries(screens).map(([k,v])=>[k,{root:v.root,holder:v.holder,content:v.content,viewport:v.viewport}])),links:links.map(l=>[l.id,l.dest]),stats:stats.map(s=>[s.key,s.contentHeight,s.viewportHeight]),counts:{primary:8,support:16,total:24}};
