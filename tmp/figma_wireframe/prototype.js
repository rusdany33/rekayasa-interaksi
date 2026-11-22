const page=figma.root.children.find(p=>p.id==='0:1');await figma.setCurrentPageAsync(page);
await Promise.all(['Regular','Medium','Bold'].map(style=>figma.loadFontAsync({family:'Roboto',style})));
const state=STATE_ALL,refs=state.screens,ids=new Map(Object.entries(refs).map(([k,v])=>[v.root,k]));
const routes=new Map(state.links);for(const [id,dest] of state.overrides)routes.set(id,dest);
const affected=new Set(),connected=[],errors=[];
function context(n){let cur=n;while(cur){if(ids.has(cur.id))return ids.get(cur.id);cur=cur.parent;}return null;}
function orderTarget(key){if(['Waiting','WaitingB','QueueWait','OrdersWaiting','SendUncertain'].includes(key))return 'OrdersWaiting';if(['Saved','Decision','OrdersSaved'].includes(key))return 'OrdersSaved';if(['Hold','OrdersHold'].includes(key))return 'OrdersHold';if(['Result','Insufficient','Changed','SaveUncertain','Queue','OrdersResult'].includes(key))return 'OrdersResult';return 'Orders';}
function queueTarget(key){if(orderTarget(key)==='OrdersWaiting')return 'QueueWait';if(orderTarget(key)==='Orders')return 'QueueBefore';return 'Queue';}
for(const [id,raw] of routes){const n=await figma.getNodeByIdAsync(id);if(!n){errors.push({id,error:'Missing node'});continue;}const key=context(n);let dest=raw;
 if(n.parent?.name==='Navigasi utama'&&raw==='Orders')dest=orderTarget(key);
 if(n.parent?.name==='Navigasi utama'&&raw==='Queue')dest=queueTarget(key);
 if(key==='Home'&&n.name==='Buka pemeriksaan')dest='QueueBefore';
 if(raw==='Hold'&&key!=='HoldReview')dest='HoldReview';
 if(raw==='BACK'&&['Before','Waiting','WaitingB','Result','Saved','Hold','Incomplete','Changed','Insufficient','SaveUncertain'].includes(key))dest=orderTarget(key);
 if(key==='Summary'&&n.name==='Buka pemeriksaan'){
  const props=n.componentProperties;const label=Object.keys(props).find(k=>k.startsWith('Label#'));n.setProperties({[label]:'Kembali ke detail'});n.name='Kembali ke detail';dest='BACK';
 }
 if(refs[dest]?.root===refs[key]?.root){await n.setReactionsAsync([]);affected.add(id);continue;}
 let action;if(dest==='BACK'||dest==='CLOSE')action={type:dest};else if(refs[dest])action={type:'NODE',destinationId:refs[dest].root,navigation:dest==='HoldReview'?'OVERLAY':'NAVIGATE',transition:null,resetScrollPosition:true};else{errors.push({id,dest,error:'Unknown destination'});continue;}
 await n.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[action]}]);affected.add(id);connected.push({id,from:key,to:dest});
}
// Ringkasan is a state of N1b; Back restores the original detail state.
for(const key of Object.keys(refs).filter(k=>!['Summary','WaitingB','HoldReview'].includes(k))){const root=await figma.getNodeByIdAsync(refs[key].root);const hs=root.query('INSTANCE[name="Ringkasan pesanan"]').toArray();for(const h of hs){await h.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:refs.Summary.root,navigation:'NAVIGATE',transition:null,resetScrollPosition:true}]}]);affected.add(h.id);connected.push({id:h.id,from:key,to:'Summary'});}}
page.flowStartingPoints=[{nodeId:refs.Home.root,name:'A · Minta pemeriksaan → Menunggu hasil'},{nodeId:refs.Queue.root,name:'B · Hasil Owner tersedia → Keputusan lanjut'},{nodeId:refs.Insufficient.root,name:'C · Hasil belum memadai → Tahan'},{nodeId:refs.SendUncertain.root,name:'D · Pengiriman belum pasti → Periksa permintaan'},{nodeId:refs.SaveUncertain.root,name:'E · Penyimpanan belum pasti → Periksa catatan'}];affected.add(page.id);
const cover=await figma.getNodeByIdAsync('2:18');const notice=cover.query('TEXT').toArray().find(n=>n.characters.startsWith('Seluruh ID,'));notice.characters='Seluruh ID, nominal, nama pelanggan, waktu dan hasil adalah ilustrasi. Input prototype memakai contoh statis. Hubungan utama dapat diklik; variasi accordion ditampilkan sebagai state wireframe. Kontak asli belum diberikan.';affected.add(notice.id);
const results=[];
for(const [key,ref] of Object.entries(refs)){const root=await figma.getNodeByIdAsync(ref.root);const txt=root.query('TEXT').toArray();const disabled=root.query('INSTANCE[name=Teruskan]').toArray().filter(n=>n.componentProperties.State?.value==='Disabled');const zero=txt.filter(t=>t.width<=0||t.hasMissingFont);results.push({key,width:root.width,height:root.height,texts:txt.length,instances:root.query('INSTANCE').length,badText:zero.map(n=>n.id),imageFills:root.query('*').filter(n=>'fills' in n&&Array.isArray(n.fills)&&n.fills.some(p=>p.type==='IMAGE')).length,disabledActions:disabled.map(n=>({id:n.id,reactions:n.reactions.length}))});}
const overflows=[];for(const areaId of ['8:294','8:295','8:296']){const area=await figma.getNodeByIdAsync(areaId);for(const n of area.query('FRAME,COMPONENT,INSTANCE')){if(n.layoutMode==='NONE'||n.name==='Konten / gulir vertikal')continue;for(const c of n.children){if(c.visible&&c.x+c.width>n.width+1)overflows.push({parent:n.name,id:n.id,child:c.name,edge:'right',extra:c.x+c.width-n.width});if(c.visible&&c.y+c.height>n.height+1)overflows.push({parent:n.name,id:n.id,child:c.name,edge:'bottom',extra:c.y+c.height-n.height});}}}
figma.viewport.scrollAndZoomIntoView([await figma.getNodeByIdAsync('8:294')]);
return {mutatedNodeIds:[...affected],connections:connected.length,errors,flows:page.flowStartingPoints,screenChecks:results,unexpectedOverflows:overflows,routeChecks:connected.filter(c=>['Minta pemeriksaan','Simpan keputusan Teruskan','Simpan keputusan Tahan'].some(label=>label===c.id)),navigationChecks:connected.filter(c=>['Before','Waiting','Result','Saved','Hold'].includes(c.from)&&['Orders','OrdersWaiting','OrdersResult','OrdersSaved','OrdersHold','HoldReview'].includes(c.to))};
