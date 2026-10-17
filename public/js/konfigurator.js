/* Budlicz: konfigurator domu. Ilości z geometrii, ceny z /dane/ceny.json, model 3D z three.js r128. */
(()=>{
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);return e?parseFloat(e.value):NaN;};
const cl=(x,a,b,d)=>isFinite(x)?Math.min(b,Math.max(a,x)):d;
const f=(n,d=1)=>Number(n).toLocaleString("pl-PL",{maximumFractionDigits:d});
const zl=n=>Math.round(n).toLocaleString("pl-PL")+" zł";
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const pl=(n,a,b,c)=>{n=Math.abs(Math.round(n));return n===1?a:(n%10>=2&&n%10<=4&&(n%100<10||n%100>=20))?b:c;};

let DB=null;const USER={};
const P=(id,w)=>{if(USER[id]!=null)return USER[id];const p=DB&&DB.p[id];if(!p)return NaN;return w==="lo"?(p.lo??p.c):w==="hi"?(p.hi??p.c):p.c;};
const JM=id=>DB&&DB.p[id]?DB.p[id].jm:"";

/* ---------- geometria i ilości ---------- */
function geom(){
  const typ=$("kond").value, pod=typ==="poddasze", nFull=typ==="pietro"?2:1;
  const L=cl(num("dl"),6,30,12), W=cl(num("sz"),5,18,9.5), h=cl(num("h"),2.6,3.6,3);
  const k=pod?cl(num("kol"),0,2,1.2):0, dach4=$("dach").value==="4";
  const a=cl(num("kat"),15,50,38)*Math.PI/180, tg=Math.tan(a), o=cl(num("okap"),0,1.2,0.6);
  const lawy=$("fund").value==="lawy", hz=cl(num("hz"),0.8,1.6,1);
  const cer=$("sc").value==="cer", t=cer?0.25:0.24, eps=cl(num("eps"),5,30,15)/100;
  const okna=Math.max(0,cl(num("okna"),0,200,24)), drzwi=Math.round(cl(num("drzwi"),0,6,1));
  const P_=2*(L+W), Li=L-2*t, Wi=W-2*t, Ai=Li*Wi, hm=h-0.25;
  const wewAuto=Math.round(Li+Wi-t);
  const wew=isFinite(num("wew"))&&$("wew").value!==""?cl(num("wew"),0,200,wewAuto):wewAuto;
  const hs=W/2*tg, gable=dach4?0:W*hs;
  const extGross=P_*(nFull*hm+(pod?k:0))+gable, openA=okna+drzwi*2.2, extNet=Math.max(0,extGross-openA);
  const Llaw=P_+Li, Vlaw=Llaw*0.6*0.4, hf=Math.max(0.3,hz-0.1);
  const Afund=Llaw*hf, Ahydro=P_*hf;
  const Vwyk=lawy?Llaw*1.0*hz:(L+1)*(W+1)*0.4;
  const Lwien=(P_+Li)*nFull+(pod?P_:0), Vwien=Lwien*0.25*0.25;
  const nOk=Math.max(0,Math.round(okna/1.6)), nOtw=nOk+drzwi, Lnad=nOtw*1.75*2;
  const nStrop=typ==="pietro"?2:1, Astrop=Ai*nStrop;
  const Lr=L+2*o, Wr=W+2*o, Adach=Lr*Wr/Math.cos(a), Lryn=dach4?2*(Lr+Wr):2*Lr;
  const Apod=pod?Ai/Math.cos(a):0;
  const Awew=wew*hm*nFull;
  const levels=nFull+(pod?1:0), Afloor=Ai*levels;
  const Atynk=Math.max(0,2*(Li+Wi)*(hm*nFull+(pod?k:0))+(pod&&!dach4?gable:0)-openA)+2*Awew+Ai*nStrop;
  // poddasze: powierzchnia wg wysokości (bez grubości dachu)
  let pd={a22:0,a14:0,a0:0};
  if(pod){
    const x22=Math.max(0,(2.2-k)/tg), x14=Math.max(0,(1.4-k)/tg);
    const ar=x=>dach4?Math.max(0,Li-2*x)*Math.max(0,Wi-2*x):Li*Math.max(0,Wi-2*x);
    pd={a22:ar(x22),a14:ar(x14)-ar(x22),a0:Ai-ar(x14)};
  }
  return {typ,pod,nFull,L,W,h,hm,k,dach4,a,tg,o,lawy,hz,cer,t,eps,okna,drzwi,P:P_,Li,Wi,Ai,wew,wewAuto,hs,gable,extGross,extNet,openA,
    Llaw,Vlaw,hf,Afund,Ahydro,Vwyk,Lwien,Vwien,nOk,nOtw,Lnad,nStrop,Astrop,Lr,Wr,Adach,Lryn,Apod,Awew,levels,Afloor,Atynk,pd};
}

/* ---------- elementy kosztorysu ---------- */
const GR=[["fund","Fundamenty","sso"],["sciany","Ściany i stropy","sso"],["dach","Dach","sso"],["okna","Okna i drzwi","ssz"],["elew","Ocieplenie","sd"],["inst","Instalacje","sd"],["wn","Wnętrze","sd"]];
const ZAKRES={sso:["sso"],ssz:["sso","ssz"],sd:["sso","ssz","sd"]};
// qty in the unit the price uses
const byUnit=(id,map)=>{const u=JM(id).split("/").pop().trim();for(const k in map)if(k!=="_"&&u.startsWith(k))return map[k];return map._;};
function elementy(g){
  const E=[];const add=(gr,tag,n,qty,lines)=>E.push({gr,tag,n,qty,lines});
  if(g.lawy){
    add("fund","fund","Roboty ziemne: wykop",`${f(g.Vwyk)} m³`,[["r_wykop",g.Vwyk,"r"]]);
    add("fund","fund","Ławy fundamentowe",`${f(g.Vlaw)} m³`,[["m_beton",g.Vlaw,"m"],["m_stal",g.Vlaw*70,"m"],["r_lawy",g.Vlaw,"r"]]);
    add("fund","fund","Szalowanie i zbrojenie ław",`${f(g.Llaw)} mb`,[["r_szal_law",g.Llaw,"r"]]);
    add("fund","fund","Ściany fundamentowe",`${f(g.Afund)} m²`,[["m_sc_fund",g.Afund,"m"],["r_sciany_fund",g.Afund,"r"]]);
    add("fund","fund","Izolacja i ocieplenie fundamentów",`${f(g.Ahydro)} m²`,[["m_hydro",g.Ahydro,"m"],["m_xps",g.Ahydro*0.10,"m"],["r_hydro",g.Ahydro,"r"],["r_xps",g.Ahydro,"r"]]);
    add("fund","fund","Podłoga na gruncie",`${f(g.Ai)} m²`,[["m_beton",g.Ai*0.1,"m"],["m_eps_podl",g.Ai*0.15,"m"],["r_podloga",g.Ai,"r"]]);
  } else {
    add("fund","fund","Roboty ziemne: korytowanie",`${f(g.Vwyk)} m³`,[["r_wykop",g.Vwyk,"r"]]);
    const A=g.L*g.W, V=A*0.25;
    add("fund","fund","Płyta fundamentowa z ociepleniem",`${f(A)} m²`,[["m_beton",V,"m"],["m_stal",V*90,"m"],["m_xps",A*0.20,"m"],["r_plyta",A,"r"]]);
  }
  add("sciany","sc","Ściany zewnętrzne",`${f(g.extNet)} m²`,[[g.cer?"m_sc_cer":"m_sc_bk",g.extNet,"m"],["r_mur",g.extNet,"r"]]);
  add("sciany","sc","Ściany wewnętrzne nośne",`${f(g.Awew)} m²`,[["m_sc_wew",g.Awew,"m"],["r_mur_wew",g.Awew,"r"]]);
  add("sciany","strop","Wieńce",`${f(g.Lwien)} m`,[["m_beton",g.Vwien,"m"],["m_stal",g.Lwien*4.35,"m"],["r_wieniec",byUnit("r_wieniec",{"m³":g.Vwien,_:g.Lwien}),"r"]]);
  add("sciany","sc","Nadproża",`${g.nOtw} ${pl(g.nOtw,"otwór","otwory","otworów")}`,[["m_nadproze",g.Lnad,"m"],["r_nadproze",byUnit("r_nadproze",{"szt":g.nOtw*2,_:g.Lnad}),"r"]]);
  add("sciany","strop",g.nStrop>1?"Stropy gęstożebrowe (2)":"Strop gęstożebrowy",`${f(g.Astrop)} m²`,[["m_teriva",g.Astrop,"m"],["m_beton",g.Astrop*P("z_teriva_beton"),"m"],["r_strop",g.Astrop,"r"]]);
  add("dach","wiezba","Więźba dachowa",`${f(g.Adach)} m²`,[["m_drewno",g.Adach*P("z_drewno"),"m"],["r_wiezba",g.Adach,"r"]]);
  const b=$("pokr").value==="blacho", zap=g.dach4?1.12:1.07;
  add("dach","dach",b?"Pokrycie: blachodachówka":"Pokrycie: dachówka ceramiczna",`${f(g.Adach)} m²`,[[b?"m_blacho":"m_dachowka",g.Adach*zap,"m"],["m_membrana",g.Adach*1.1,"m"],["m_laty",g.Adach,"m"],[b?"r_pokrycie_b":"r_pokrycie_d",g.Adach,"r"]]);
  add("dach","dach","Rynny i rury spustowe",`${f(g.Lryn)} m`,[["m_rynny",g.Lryn,"m"],["r_rynny",g.Lryn,"r"]]);
  add("okna","okna","Okna",`${f(g.okna)} m²`,[["m_okno",g.okna,"m"],["r_okna",byUnit("r_okna",{"szt":g.nOk,_:g.okna}),"r"]]);
  if(g.drzwi)add("okna","okna","Drzwi zewnętrzne",`${g.drzwi} szt.`,[["m_drzwi",g.drzwi,"m"],["r_drzwi",g.drzwi,"r"]]);
  add("elew","elew","Ocieplenie ścian z tynkiem",`${f(g.extNet)} m²`,[["m_eps_graf",g.extNet*g.eps*1.05,"m"],["m_etics",g.extNet,"m"],["r_elewacja",g.extNet,"r"]]);
  if(g.pod)add("elew","wiezba","Ocieplenie poddasza i zabudowa GK",`${f(g.Apod)} m²`,[["m_welna",g.Apod*0.25,"m"],["m_gk",g.Apod,"m"],["r_poddasze",g.Apod,"r"]]);
  else add("elew","strop","Ocieplenie stropu pod dachem",`${f(g.Ai)} m²`,[["m_welna",g.Ai*0.30,"m"],["r_strop_oc",g.Ai,"r"]]);
  add("inst","","Instalacja elektryczna",`${f(g.Afloor)} m²`,[["i_elektryka",g.Afloor,"i"]]);
  add("inst","","Instalacja wodno-kanalizacyjna",`${f(g.Afloor)} m²`,[["i_wodkan",g.Afloor,"i"]]);
  add("inst","","Ogrzewanie podłogowe",`${f(g.Afloor)} m²`,[["i_co",g.Afloor,"i"]]);
  add("inst","","Pompa ciepła z montażem","1 szt.",[["i_pompa",1,"i"]]);
  add("wn","","Tynki wewnętrzne",`${f(g.Atynk)} m²`,[["m_tynk",g.Atynk,"m"],["r_tynk",g.Atynk,"r"]]);
  add("wn","","Wylewki",`${f(g.Afloor)} m²`,[["m_jastrych",g.Afloor,"m"],["r_wylewka",g.Afloor,"r"]]);
  return E;
}
function wycen(E,w){
  return E.map(e=>{const s={m:0,r:0,i:0,miss:[]};e.lines.forEach(([id,q,kind])=>{const c=P(id,w);if(!isFinite(c)){s.miss.push(id);return;}s[kind]+=c*q;});return Object.assign({},e,s,{tot:s.m+s.r+s.i});});
}

/* ---------- wynik ---------- */
let lastG=null;
function licz(){
  if(!DB)return;
  const g=geom();lastG=g;
  $("wKol").hidden=!g.pod;$("wHz").hidden=!g.lawy;
  $("wew").placeholder=String(g.wewAuto);
  const E=elementy(g), Y=wycen(E), LO=wycen(E,"lo"), HI=wycen(E,"hi");
  const zak=$("zak").value, inc=ZAKRES[zak], grOf=Object.fromEntries(GR.map(x=>[x[0],x[2]]));
  const sum=(R,st)=>R.filter(e=>st.includes(grOf[e.gr])).reduce((a,e)=>a+e.tot,0);
  const sso=sum(Y,["sso"]), ssz=sum(Y,["sso","ssz"]), sd=sum(Y,["sso","ssz","sd"]);
  const R=Y.filter(e=>inc.includes(grOf[e.gr]));
  const tot=R.reduce((a,e)=>a+e.tot,0), m=R.reduce((a,e)=>a+e.m,0), r=R.reduce((a,e)=>a+e.r,0), i=R.reduce((a,e)=>a+e.i,0);
  const lo=sum(LO,inc), hi=sum(HI,inc), miss=[...new Set(R.flatMap(e=>e.miss))];
  const nz={sso:"stanu surowego otwartego",ssz:"stanu surowego zamkniętego",sd:"stanu deweloperskiego"}[zak];
  let h=`<div class="cols2"><div>Koszt do ${nz}: <b>${zl(tot)}</b><br>Zakres z cen min. i maks.: ${zl(lo)} do ${zl(hi)}<br>Na m² podłóg: ${zl(tot/g.Afloor)}<br>`+
    `Powierzchnia podłóg: ${f(g.Afloor)} m²`+(g.pod?`, w tym poddasze ${f(g.Ai)} m² (wysokość od 2,2 m: ${f(g.pd.a22)} m², od 1,4 do 2,2 m: ${f(g.pd.a14)} m²)`:"")+`</div>`+
    `<div>Stan surowy otwarty: ${zl(sso)}<br>Stan surowy zamknięty: ${zl(ssz)}<br>Stan deweloperski: ${zl(sd)}<br>Materiały: ${zl(m)} · robocizna: ${zl(r)}`+(i?`<br>Instalacje (materiał z montażem): ${zl(i)}`:"")+`</div></div>`;
  if(miss.length)h+=`<p class="mut"><span class="warn">Brak ceny:</span> ${miss.map(id=>esc(DB.p[id]?DB.p[id].n:id)).join(", ")}. Wpisz ją w tabeli cen poniżej.</p>`;
  h+=`<p class="mut">Ceny z bazy Budlicz, ${esc(DB.opis)}. Szacunek do planowania, bez projektu, przyłączy, schodów i wykończenia. Wiążąca jest wycena wykonawcy.</p>`;
  $("wynik").innerHTML=h;
  // tabela
  let t=`<table class="kt"><thead><tr><th>Element</th><th class="num">Ilość</th><th class="num cm">Materiał</th><th class="num cr">Robocizna</th><th class="num">Razem</th></tr></thead>`;
  GR.forEach(([gk,gn,st])=>{
    const rows=R.filter(e=>e.gr===gk);if(!rows.length)return;
    const s=rows.reduce((a,e)=>a+e.tot,0);
    t+=`<tbody><tr class="gh"><th colspan="4">${gn}</th><th class="num">${zl(s)}</th></tr>`;
    rows.forEach(e=>{t+=`<tr data-tag="${e.tag}"><td>${esc(e.n)}<span class="qm mut"> · ${e.qty}</span></td><td class="num q">${e.qty}</td>`+
      (e.i?`<td colspan="2" class="num mut cmr">z materiałem</td>`:`<td class="num cm">${zl(e.m)}</td><td class="num cr">${zl(e.r)}</td>`)+`<td class="num"><b>${zl(e.tot)}</b></td></tr>`;});
    t+=`</tbody>`;
  });
  t+=`<tfoot>`+(i?`<tr><td>Instalacje</td><td></td><td colspan="2" class="num mut cmr">z materiałem</td><td class="num">${zl(i)}</td></tr>`:"")+
    `<tr><td>Razem</td><td></td><td class="num cm">${zl(m)}</td><td class="num cr">${zl(r)}</td><td class="num">${zl(tot)}</td></tr></tfoot></table>`;
  $("tab").innerHTML=t;
  $("ilosci").innerHTML=`Ściany zewnętrzne ${f(g.extNet)} m² (po odjęciu okien i drzwi), dach ${f(g.Adach)} m², stropy ${f(g.Astrop)} m², ściany wewnętrzne ${f(g.wew)} m na kondygnację.`;
  model.update(g);
}

/* ---------- tabela cen ---------- */
function cenyTab(){
  const kind={m:"Materiały",r:"Robocizna",i:"Instalacje (z materiałem)",z:"Zużycie według producentów"};
  let h="";
  ["m","r","i","z"].forEach(k=>{
    const ids=Object.keys(DB.p).filter(id=>DB.p[id].k===k);if(!ids.length)return;
    h+=`<h3>${kind[k]}</h3><div class="ceny">`;
    ids.forEach(id=>{const p=DB.p[id];
      h+=`<label class="inl"><span>${esc(p.n)} <small class="mut">${p.lo!=null&&p.hi!=null&&p.lo!==p.hi?`${f(p.lo,2)} do ${f(p.hi,2)}, `:""}${esc(p.jm)}</small></span><input type="number" min="0" step="any" data-id="${id}" value="${p.c}" aria-label="${esc(p.n)}, ${esc(p.jm)}"></label>`;});
    h+=`</div>`;
  });
  h+=`<p class="btns"><button class="btn" type="button" id="reset">Przywróć ceny z bazy</button></p>`;
  $("cenyTab").innerHTML=h;
}
document.addEventListener("input",e=>{
  const id=e.target.dataset&&e.target.dataset.id;
  if(id){const x=parseFloat(e.target.value);if(isFinite(x)&&x>=0)USER[id]=x;else delete USER[id];licz();return;}
  if(e.target.closest&&e.target.closest("#par"))licz();
});
document.addEventListener("click",e=>{if(e.target.id==="reset"){for(const k in USER)delete USER[k];cenyTab();licz();}});
$("tab").addEventListener("mouseover",e=>{const tr=e.target.closest("tr[data-tag]");model.hi(tr?tr.dataset.tag:"");});
$("tab").addEventListener("mouseleave",()=>model.hi(""));
$("kond").addEventListener("input",()=>{if(!$("kat").dataset.touched)$("kat").value=$("kond").value==="poddasze"?38:30;});
$("kat").addEventListener("input",()=>{$("kat").dataset.touched=1;});

/* ---------- model 3D ---------- */
const ETAPY=["Teren","Fundamenty","Ściany parteru","Strop nad parterem","Ściany wyżej i szczyty","Więźba","Pokrycie i rynny","Okna i drzwi","Ocieplenie i elewacja"];
const model=(()=>{
  const cv=$("model3d");
  if(!window.THREE||!cv){const n=$("brak3d");if(n)n.hidden=false;return {update(){},hi(){},etap(){}};}
  let r;try{r=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true});}catch(e){$("brak3d").hidden=false;cv.hidden=true;return {update(){},hi(){},etap(){}};}
  r.setPixelRatio(Math.min(2,window.devicePixelRatio||1));
  const sc=new THREE.Scene(),cam=new THREE.PerspectiveCamera(35,1,0.1,800);
  sc.add(new THREE.HemisphereLight(0xffffff,0x8a7a66,0.8));
  const sun=new THREE.DirectionalLight(0xffffff,0.7);sun.position.set(25,40,18);sc.add(sun);
  const grp=new THREE.Group();sc.add(grp);
  const gnd=new THREE.Mesh(new THREE.CircleGeometry(60,64),new THREE.MeshLambertMaterial({color:0x8fa882,transparent:true,opacity:0.55,depthWrite:false}));
  gnd.rotation.x=-Math.PI/2;gnd.renderOrder=-1;sc.add(gnd);
  const C={beton:0xb9bec4,lawa:0x9ea4ab,cer:0xc8714a,bk:0xe7e4dc,strop:0xa3a9b0,drewno:0xc9a176,blacho:0x3b4048,dachowka:0x9c3b24,ram:0xf3f3f1,szyba:0x5d7d99,otw:0x30353b,elew:0xf1ece2,drzwi:0x6b4a2f,rynna:0x8d939a,xps:0xe9c94a};
  const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
  let etap=8,G=null,tagHi="",born={};
  function mat(c,tag,st){const m=new THREE.MeshLambertMaterial({color:c,side:THREE.DoubleSide});m.userData={tag,st};return m;}
  function box(w,hh,d,x,y,z,c,tag,st){const m=new THREE.Mesh(new THREE.BoxGeometry(w,hh,d),mat(c,tag,st));m.position.set(x,y,z);m.userData={tag,st,y};grp.add(m);return m;}
  function poly(pts,faces,c,tag,st){const g=new THREE.BufferGeometry();const a=[];faces.forEach(fc=>fc.forEach(i=>a.push(...pts[i])));g.setAttribute("position",new THREE.Float32BufferAttribute(a,3));g.computeVertexNormals();const m=new THREE.Mesh(g,mat(c,tag,st));m.userData={tag,st,y:0};grp.add(m);return m;}
  function prism(tri,dx,c,tag,st){ // trójkąt w płaszczyźnie x=const, grubość dx w osi x
    const [p,q,s]=tri, P2=tri.map(v=>[v[0]+dx,v[1],v[2]]);
    const pts=[p,q,s,...P2];return poly(pts,[[0,1,2],[3,5,4],[0,3,4],[0,4,1],[1,4,5],[1,5,2],[2,5,3],[2,3,0]],c,tag,st);}
  function beam(a,b,th,c,tag,st){const d=new THREE.Vector3(b[0]-a[0],b[1]-a[1],b[2]-a[2]),len=d.length();const m=new THREE.Mesh(new THREE.BoxGeometry(len,th,th*0.5),mat(c,tag,st));
    m.position.set((a[0]+b[0])/2,(a[1]+b[1])/2,(a[2]+b[2])/2);m.quaternion.setFromUnitVectors(new THREE.Vector3(1,0,0),d.normalize());m.userData={tag,st,y:m.position.y};grp.add(m);return m;}
  function walls(g,yb,yt,c,tag,st,grubosc,odsun){ // 4 ściany jako pierścień
    const th=grubosc,o=odsun||0,L=g.L+2*o,W=g.W+2*o,hh=yt-yb,y=(yb+yt)/2;
    box(L,hh,th,0,y,W/2-th/2,c,tag,st);box(L,hh,th,0,y,-W/2+th/2,c,tag,st);
    box(th,hh,W-2*th,L/2-th/2,y,0,c,tag,st);box(th,hh,W-2*th,-L/2+th/2,y,0,c,tag,st);
  }
  function okna(g,y0){ // pozycje okien na kondygnacjach pełnych
    const out=[];const n=g.nOk,per=Math.ceil(n/g.nFull)||0;let left=n;
    for(let s=0;s<g.nFull;s++){
      const cnt=Math.min(per,left);left-=cnt;const yb=y0+s*g.h+0.9;
      const fr=Math.ceil(cnt*0.4),bk=Math.ceil((cnt-fr)*0.6),sd=cnt-fr-bk,sl=Math.ceil(sd/2),sr=sd-sl;
      const along=(c,len)=>Array.from({length:c},(_,i)=>-len/2+len*(i+1)/(c+1));
      const door=s===0&&g.drzwi>0;
      along(fr+(door?1:0),g.L).forEach((x,i,arr)=>{if(door&&i===Math.floor(arr.length/2)){out.push({side:"z+",x,yb:y0,w:1.0,h:2.1,door:1});}else out.push({side:"z+",x,yb,w:1.2,h:1.35});});
      along(bk,g.L).forEach(x=>out.push({side:"z-",x,yb,w:1.2,h:1.35}));
      along(sl,g.W-1).forEach(x=>out.push({side:"x+",x,yb,w:1.2,h:1.35}));
      along(sr,g.W-1).forEach(x=>out.push({side:"x-",x,yb,w:1.2,h:1.35}));
    }
    return out;
  }
  function build(g,E){
    while(grp.children.length){const m=grp.children.pop();m.geometry.dispose();m.material.dispose();}
    const y0=0.3,ccol=g.cer?C.cer:C.bk,top=y0+g.nFull*g.h+(g.pod?g.k:0);
    // 1 fundamenty
    if(E>=1){
      if(g.lawy){
        const yl=-g.hz+0.2;
        box(g.L+0.35,0.4,0.6,0,yl,g.W/2-g.t/2,C.lawa,"fund",1);box(g.L+0.35,0.4,0.6,0,yl,-g.W/2+g.t/2,C.lawa,"fund",1);
        box(0.6,0.4,g.W-0.25,g.L/2-g.t/2,yl,0,C.lawa,"fund",1);box(0.6,0.4,g.W-0.25,-g.L/2+g.t/2,yl,0,C.lawa,"fund",1);
        box(g.Li,0.4,0.6,0,yl,0,C.lawa,"fund",1);
        walls(g,-g.hz+0.4,y0,C.beton,"fund",1,0.24);box(g.Li,y0+g.hz-0.4,0.24,0,(y0-g.hz+0.4)/2,0,C.beton,"fund",1);
        box(g.Li,0.1,g.Wi,0,y0-0.05,0,C.strop,"fund",1);
      } else {
        box(g.L,0.2,g.W,0,-0.05,0,C.xps,"fund",1);box(g.L,0.25,g.W,0,0.175,0,C.beton,"fund",1);
      }
    }
    // 2-4 ściany i stropy
    const ok=E>=2?okna(g,y0):[];
    for(let s=0;s<g.nFull;s++){
      const st=s===0?2:4,yb=y0+s*g.h;
      if(E>=st){walls(g,yb,yb+g.hm,ccol,"sc",st,g.t);box(g.Li,g.hm,g.t*0.8,0,yb+g.hm/2,0,ccol,"sc",st);}
      const ss=s===0?3:4;
      if(E>=ss){box(g.L,0.25,g.W,0,yb+g.hm+0.125,0,C.strop,"strop",ss);}
    }
    if(g.pod&&E>=4){const yb=y0+g.h;
      if(g.dach4)walls(g,yb,yb+g.k,ccol,"sc",4,g.t);
      else{box(g.L,g.k,g.t,0,yb+g.k/2,g.W/2-g.t/2,ccol,"sc",4);box(g.L,g.k,g.t,0,yb+g.k/2,-g.W/2+g.t/2,ccol,"sc",4);}
    }
    if(!g.dach4&&E>=4){
      [-1,1].forEach(sg=>{const x=sg>0?g.L/2-g.t:-g.L/2;
        if(g.pod)box(g.t,g.k,g.W-2*g.t,x+g.t/2,y0+g.h+g.k/2,0,ccol,"sc",4);
        prism([[x,top,-g.W/2],[x,top,g.W/2],[x,top+g.hs,0]],g.t,ccol,"sc",4);
      });
    }
    // otwory i okna
    ok.forEach(w=>{
      const st=w.yb<y0+g.h?2:4;if(E<st)return;
      const e8=E>=8,e7=E>=7,dep=g.t+0.04+(e8?2*g.eps:0);
      let x,z,sx,sz;
      if(w.side==="z+"){x=w.x;z=g.W/2-g.t/2+(e8?g.eps/2:0);sx=w.w;sz=dep;}
      else if(w.side==="z-"){x=w.x;z=-g.W/2+g.t/2-(e8?g.eps/2:0);sx=w.w;sz=dep;}
      else if(w.side==="x+"){x=g.L/2-g.t/2+(e8?g.eps/2:0);z=w.x;sx=dep;sz=w.w;}
      else {x=-g.L/2+g.t/2-(e8?g.eps/2:0);z=w.x;sx=dep;sz=w.w;}
      const y=w.yb+w.h/2;
      if(!e7){box(sx,w.h,sz,x,y,z,C.otw,"okna",st);return;}
      box(sx,w.h,sz,x,y,z,w.door?C.drzwi:C.ram,"okna",7);
      if(!w.door){const gl=0.12,ins=(w.side[0]==="z")?[w.w-gl,w.h-gl,sz+0.01]:[sx+0.01,w.h-gl,w.w-gl];box(ins[0],ins[1],ins[2],x,y,z,C.szyba,"okna",7);}
    });
    // dach
    const lx=g.L/2+g.o,wz=g.W/2+g.o,ye=top-g.o*g.tg,yr=top+g.W/2*g.tg,lr=Math.max(0,lx-wz);
    if(E>=5){
      const off=0.12,sp=0.9;
      box(g.L,0.14,0.14,0,top+0.07,g.W/2-g.t/2,C.drewno,"wiezba",5);box(g.L,0.14,0.14,0,top+0.07,-g.W/2+g.t/2,C.drewno,"wiezba",5);
      if(!g.dach4){
        beam([-lx,yr-off,0],[lx,yr-off,0],0.18,C.drewno,"wiezba",5);
        for(let x=-lx+0.2;x<=lx-0.19;x+=sp){[1,-1].forEach(sg=>beam([x,ye-off,sg*wz],[x,yr-off,0],0.16,C.drewno,"wiezba",5));}
      } else {
        if(lr>0)beam([-lr,yr-off,0],[lr,yr-off,0],0.18,C.drewno,"wiezba",5);
        [[1,1],[1,-1],[-1,1],[-1,-1]].forEach(([sx,sz])=>beam([sx*lx,ye-off,sz*wz],[sx*lr,yr-off,0],0.18,C.drewno,"wiezba",5));
        for(let x=-lx+0.5;x<=lx-0.49;x+=sp){const u=Math.min(wz,lx-Math.abs(x));if(u<0.3)continue;[1,-1].forEach(sg=>beam([x,ye-off,sg*wz],[x,ye-off+u*g.tg,sg*(wz-u)],0.14,C.drewno,"wiezba",5));}
        for(let z=-wz+0.5;z<=wz-0.49;z+=sp){const u=wz-Math.abs(z);if(u<0.3)continue;[1,-1].forEach(sg=>beam([sg*lx,ye-off,z],[sg*(lx-u),ye-off+u*g.tg,z],0.14,C.drewno,"wiezba",5));}
      }
    }
    if(E>=6){
      const rc=$("pokr").value==="blacho"?C.blacho:C.dachowka;
      if(!g.dach4){const p=[[-lx,ye,-wz],[lx,ye,-wz],[lx,ye,wz],[-lx,ye,wz],[-lx,yr,0],[lx,yr,0]];poly(p,[[0,1,5],[0,5,4],[3,4,5],[3,5,2]],rc,"dach",6);}
      else{const p=[[-lx,ye,-wz],[lx,ye,-wz],[lx,ye,wz],[-lx,ye,wz],[-lr,yr,0],[lr,yr,0]];poly(p,[[0,1,5],[0,5,4],[3,4,5],[3,5,2],[0,4,3],[1,2,5]],rc,"dach",6);}
      const ry=ye-0.08;
      [[-lx,ry,wz,lx,ry,wz],[-lx,ry,-wz,lx,ry,-wz]].forEach(q=>beam(q.slice(0,3),q.slice(3),0.12,C.rynna,"dach",6));
      if(g.dach4)[[lx,ry,-wz,lx,ry,wz],[-lx,ry,-wz,-lx,ry,wz]].forEach(q=>beam(q.slice(0,3),q.slice(3),0.12,C.rynna,"dach",6));
    }
    // elewacja
    if(E>=8){
      const e=g.eps,yb=y0;
      walls(g,yb,top,C.elew,"elew",8,e,e);
      if(!g.dach4){[-1,1].forEach(sg=>{const x=sg>0?g.L/2:-g.L/2-e;prism([[x,top,-g.W/2-e],[x,top,g.W/2+e],[x,top+g.hs+e*g.tg,0]],e,C.elew,"elew",8);});}
    }
    // animacja nowych elementów
    const now=performance.now();
    grp.children.forEach(m=>{if(m.userData.st===E&&born[E]!=="done"){m.userData.t0=now;}});
    born[E]="done";
    const R=Math.hypot(g.L,g.W)/2+g.o+1;cam.userData={R,top:yr+0.5,mid:(yr-g.hz)/2};
    hi(tagHi);
  }
  function hi(tag){tagHi=tag;grp.children.forEach(m=>{m.material.emissive&&m.material.emissive.setHex(tag&&m.userData.tag===tag?0x6a2c00:0x000000);});}
  let ang=0.75,drag=null,auto=!reduce;
  function frame(now){
    const w=cv.clientWidth,h=cv.clientHeight;
    if(w&&cv.width!==Math.round(w*r.getPixelRatio())){r.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix();}
    if(auto&&!drag)ang+=0.0025;
    grp.children.forEach(m=>{const t0=m.userData.t0;if(t0==null)return;const t=Math.min(1,(now-t0)/500),e=1-Math.pow(1-t,3);if(!m.material.transparent){m.material.transparent=true;m.material.needsUpdate=true;}m.material.opacity=e;m.position.y=(m.userData.y||0)+(1-e)*1.2;if(t>=1){m.userData.t0=null;m.position.y=m.userData.y||0;m.material.transparent=false;m.material.opacity=1;m.material.needsUpdate=true;}});
    const u=cam.userData||{},asp=cam.aspect||1,d=1.05*Math.max(((u.top||8)+2)/0.62,(u.R||8)/(0.31*asp));
    cam.position.set(Math.sin(ang)*d,d*0.45,Math.cos(ang)*d);cam.lookAt(0,(u.top||6)*0.38,0);
    r.render(sc,cam);requestAnimationFrame(frame);
  }
  cv.addEventListener("pointerdown",e=>{drag={x:e.clientX,a:ang};auto=false;cv.setPointerCapture(e.pointerId);});
  cv.addEventListener("pointermove",e=>{if(drag)ang=drag.a-(e.clientX-drag.x)*0.01;});
  cv.addEventListener("pointerup",()=>{drag=null;});
  requestAnimationFrame(frame);
  let timer=null;
  function setE(e){etap=e;$("etap").value=e;$("etapTxt").textContent=`${e}/8 · ${ETAPY[e]}`;if(G)build(G,etap);}
  function play(){clearInterval(timer);born={};let e=0;setE(0);timer=setInterval(()=>{e++;setE(e);if(e>=8)clearInterval(timer);},reduce?0:650);}
  $("etap").addEventListener("input",()=>{clearInterval(timer);born[+$("etap").value]=null;setE(+$("etap").value);});
  $("graj").addEventListener("click",play);
  return {update(g){const first=!G;G=g;if(first){reduce?setE(8):play();}else build(g,etap);},hi,etap:setE};
})();

/* ---------- start ---------- */
fetch("/dane/ceny.json").then(r=>{if(!r.ok)throw 0;return r.json();}).then(d=>{DB=d;$("baza").textContent=d.opis;cenyTab();licz();})
 .catch(()=>{$("wynik").innerHTML='Nie udało się wczytać bazy cen. Odśwież stronę.';});
})();
