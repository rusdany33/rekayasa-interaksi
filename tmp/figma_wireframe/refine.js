// Uses screen-authoring helpers from screens.js, with verified persisted IDs.
const prior=STATE_SCREENS;
const affected=new Set(),added={};
async function get(key){return await figma.getNodeByIdAsync(prior.screens[key].root);}
async function replaceText(key,from,to){const root=await get(key);const n=root.query('TEXT').toArray().find(n=>n.characters===from);if(!n)throw new Error('Text missing: '+key+' '+from);for(const s of n.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);n.characters=to;affected.add(n.id);return n;}
function overrideButton(root,oldLabel,newLabel){const n=root.query('INSTANCE').toArray().find(n=>n.name===oldLabel);if(!n)throw new Error('Button missing '+oldLabel);prop(n,'Label',newLabel);n.name=newLabel;affected.add(n.id);return n;}
// Help pages are global guidance; native Back preserves the screen and order of origin.
await replaceText('Guide','Konteks tetap tersimpan','Pertahankan pesanan asal');
await replaceText('Guide','PSN-015 · PRM-015 · Owner','Gunakan ID pesanan dan permintaan pada detail yang sedang diperiksa.');
const guideRoot=await get('Guide');const guideBack=overrideButton(guideRoot,'Kembali ke pemeriksaan','Kembali ke halaman asal');
const contactRoot=await get('Contact');
await replaceText('Contact','Konteks permintaan','Gunakan konteks pesanan asal');
await replaceText('Contact','PSN-015 · PRM-015','Gunakan ID pesanan dan nomor permintaan jika sudah tercatat.');
await replaceText('Contact','Pemeriksa yang ditetapkan','Pemeriksa mengikuti pesanan');
await replaceText('Contact','Peran','Sumber kontak');await replaceText('Contact','Owner','Detail pesanan');
await replaceText('Contact','Nomor atau kanal kontak belum tersedia pada contoh ini. Gunakan saluran yang disepakati outlet.','Lihat pemeriksa yang ditetapkan di bagian Pemeriksaan. Nomor atau kanal kontak belum tersedia pada contoh ini.');
await replaceText('Contact','Sertakan PSN-015, PRM-015, nominal Rp150.000 dan bagian yang perlu diklarifikasi.','Sertakan identitas pesanan, nomor permintaan jika ada, nominal dan bagian yang perlu diklarifikasi. Gunakan saluran yang disepakati outlet.');
const contactBack=overrideButton(contactRoot,'Kembali ke pemeriksaan','Kembali ke halaman asal');
const helpContent=await figma.getNodeByIdAsync(prior.screens.Help.content);const helpBack=await link(helpContent,'Kembali ke halaman asal','BACK',358);affected.add(helpContent.id);
// Confirm a hold decision with an explicit reason, including when the result was adequate.
const compArea=await figma.getNodeByIdAsync('2:21');compArea.name='03 · Komponen & dialog keputusan';affected.add(compArea.id);
const holder=stack(compArea,'HoldReview',470,12);holder.x=1490;holder.y=100;await text(holder,'Dialog · Tahan untuk klarifikasi',470,'heading');
const dialog=figma.createAutoLayout('VERTICAL');holder.appendChild(dialog);dialog.name='Dialog alasan keputusan tahan';dialog.resize(390,1);dialog.primaryAxisSizingMode='AUTO';dialog.counterAxisSizingMode='FIXED';pad(dialog,16);gap(dialog,12);bg(dialog);edge(dialog);corners(dialog,12);
await text(dialog,'Tahan untuk klarifikasi',358,'title');await text(dialog,'PSN-015 · Dasar HAS-015',358,'label');await text(dialog,'Jelaskan alasan tambahan sebelum menyimpan keputusan tahan.',358);
const field=stack(dialog,'Alasan keputusan',358,8,16);bg(field,'soft');corners(field);await text(field,'Alasan (wajib)',326,'label');input(field,'Perlu klarifikasi pembayaran\nuntuk pesanan ini.','Multiline');await text(field,'Contoh isian prototype. Pada implementasi, alasan harus diisi admin.',326,'caption','secondary');
const dialogButtons=stack(dialog,'Aksi keputusan tahan',358,8,16);button(dialogButtons,'Simpan keputusan Tahan','Hold');button(dialogButtons,'Batal','CLOSE','Secondary');
await text(holder,'Overlay sebelum penyimpanan. Alasan ditinjau admin; tidak menyimpulkan semua hasil yang memadai masih bermasalah.',470,'body14','secondary');
screens.HoldReview={root:dialog.id,holder:holder.id};
await replaceText('Hold','Alasan: hasil memerlukan klarifikasi untuk pesanan ini.','Alasan: perlu klarifikasi pembayaran untuk pesanan ini.');
// Context variants keep primary navigation from resetting the request/decision state.
const sourceHolder=await figma.getNodeByIdAsync(prior.screens.Orders.holder);
for(const [i,key,label,badgeLabel,dest] of [[16,'OrdersWaiting','P17 · Pesanan / permintaan tercatat','Menunggu hasil','Waiting'],[17,'OrdersResult','P18 · Pesanan / hasil tersedia','Hasil tersedia','Result'],[18,'OrdersSaved','P19 · Pesanan / keputusan lanjut','Keputusan Teruskan','Saved'],[19,'OrdersHold','P20 · Pesanan / keputusan tahan','Keputusan Tahan','Hold']]){
 const h=sourceHolder.clone();areas.support.appendChild(h);h.name=key;h.x=32+(i%4)*510;h.y=110+Math.floor(i/4)*1015;
 const root=h.children.find(n=>n.type==='FRAME'&&n.width===390&&n.height===844);root.name=key+' / '+label;
 const title=h.children.find(n=>n.type==='TEXT');title.characters=label;const caption=h.children.filter(n=>n.type==='TEXT').at(-1);caption.characters='N1 · Variasi konteks daftar pesanan agar kembali dari detail tidak mengulang keadaan sebelumnya.';
 const badgeNode=root.query('INSTANCE').toArray().find(n=>n.name==='Belum diminta');prop(badgeNode,'Label',badgeLabel);badgeNode.name=badgeLabel;
 const open=root.query('INSTANCE').toArray().find(n=>n.name==='Buka PSN-015');links.push({id:open.id,dest});
 const other=root.query('INSTANCE').toArray().find(n=>n.name==='Buka PSN-016');links.push({id:other.id,dest:'WaitingB'});
 const search=root.query('INSTANCE').toArray().find(n=>n.name==='Cari');links.push({id:search.id,dest:'Empty'});
 for(const [labelNav,keyDest] of [['Beranda','Home'],['Pesanan',key],['Pemeriksaan',key==='OrdersWaiting'?'QueueWait':'Queue'],['Bantuan','Help']]){const nav=root.query('INSTANCE').toArray().find(n=>n.name===labelNav&&n.parent.name==='Navigasi utama');if(nav)links.push({id:nav.id,dest:keyDest});}
 screens[key]={root:root.id,holder:h.id,content:root.query('FRAME[name=Konten]').first().id,viewport:root.query('FRAME[name="Konten / gulir vertikal"]').first().id};added[key]=screens[key];
}
areas.support.resize(2100,5480);affected.add(areas.support.id);compArea.y=8390;
// Fix the multiline component grid using actual per-row height, leaving clear gaps.
const inputs=comps.input.children;inputs.forEach((n,i)=>{n.x=16+(i%2)*346;n.y=i<2?16:108;affected.add(n.id);});comps.input.resize(704,180);affected.add(comps.input.id);
const guideNote=areas.guide.query('TEXT').toArray().find(n=>n.characters.startsWith('Prototype A:'));
guideNote.characters='Prototype A: 01 → 02 → 03 → 04 (menunggu). Prototype B: 05 → 06 → 07 (hasil Owner tersedia). Cabang tahan memakai dialog alasan. Hasil Owner merupakan skenario terpisah; tidak ada verifikasi bank otomatis.';affected.add(guideNote.id);
const mainInfo=areas.main.query('TEXT').toArray().find(n=>n.characters.startsWith('01 →'));
mainInfo.characters='01 → 02 → 03 → 04 | Skenario hasil Owner tersedia: 05 → 06 → 07. Bantuan: 08. Daftar pesanan mengikuti state asal.';affected.add(mainInfo.id);
return {createdNodeIds:[...holder.query('*').map(n=>n.id),holder.id,...Object.values(added).flatMap(v=>{const h=areas.support.children.find(n=>n.id===v.holder);return [h.id,...h.query('*').map(n=>n.id)];}),helpBack.id,...helpBack.query('*').map(n=>n.id)],mutatedNodeIds:[...affected],screens,links:links.map(l=>[l.id,l.dest]),overrides:[[guideBack.id,'BACK'],[contactBack.id,'BACK']],counts:{primary:8,support:20,dialog:1,total:29}};
