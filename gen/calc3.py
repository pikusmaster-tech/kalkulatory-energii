CALC3={}
_H=r'''const $=id=>document.getElementById(id);
const v=id=>parseFloat($(id).value)||0;
const f=(n,d=2)=>Number(n).toLocaleString("pl-PL",{maximumFractionDigits:d});
const zl=n=>Number(n).toLocaleString("pl-PL",{minimumFractionDigits:2,maximumFractionDigits:2})+" zł";
const T=(x,y,t,c="t",a="start")=>`<text class="${c}" x="${x}" y="${y}" text-anchor="${a}">${t}</text>`;
const pl=(n,a,b,c)=>{n=Math.abs(Math.round(n));return n===1?a:(n%10>=2&&n%10<=4&&(n%100<10||n%100>=20))?b:c;};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
'''

# ---------------------------------------------------------------- U
CALC3['wspolczynnik-u']=dict(title='Współczynnik U ściany i dachu: kalkulator WT 2021',
 desc='Ułóż warstwy ściany albo dachu i sprawdź współczynnik U, wymaganie WT 2021, brakującą grubość izolacji i spadek temperatury w przegrodzie.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Współczynnik U: czy ściana spełnia WT 2021</h1>
<p class="lead">Ułóż warstwy przegrody od środka na zewnątrz. Kalkulator policzy opór cieplny i współczynnik U, porówna go z wymaganiem z warunków technicznych i pokaże, jak spada temperatura w ścianie.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="typ">Przegroda</label><select id="typ"><option value="sciana">Ściana zewnętrzna</option><option value="dach">Dach, stropodach</option></select></div>
<div><label for="ti">Temperatura wewnątrz (°C)</label><input id="ti" type="number" value="20" step="1"></div>
<div><label for="te">Temperatura na zewnątrz (°C)</label><input id="te" type="number" value="-20" step="1"></div>
</div>
<p class="sub">Warstwy od wewnątrz</p>
<div class="rowh u"><span>Materiał</span><span>Grubość (cm)</span><span>λ (W/m·K)</span><span></span></div>
<div id="warstwy" class="rows"></div>
<div class="btns"><button class="btn" id="dodaj" type="button">+ Dodaj warstwę</button></div>
<p class="mut">Wartości λ w liście są przykładowe. Wpisz λ deklarowaną z karty produktu, którą kupujesz.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Przekrój i temperatura w przegrodzie <span id="opis"></span></figcaption><svg id="przekroj" viewBox="0 0 640 290" role="img" aria-label="Warstwy przegrody w skali grubości i linia temperatury od wnętrza do zewnątrz"></svg><p class="note">Warstwy w skali grubości. Pomarańczowa linia to temperatura przy wpisanych warunkach, niebieska przerywana to 0°C. Mostki cieplne i łączniki pominięto.</p></figure>
<h2>Wymagania WT 2021</h2>
<p>Dla pomieszczeń ogrzewanych do co najmniej 16°C warunki techniczne podają maksymalne wartości U. Obowiązują dla projektów składanych od 1 stycznia 2021 r.</p>
<table><thead><tr><th>Przegroda</th><th class="num">U max, W/(m²·K)</th></tr></thead><tbody>
<tr><td>Ściany zewnętrzne</td><td class="num">0,20</td></tr>
<tr><td>Dachy, stropodachy, stropy pod nieogrzewanym poddaszem</td><td class="num">0,15</td></tr>
<tr><td>Podłogi na gruncie</td><td class="num">0,30</td></tr>
<tr><td>Okna, drzwi balkonowe</td><td class="num">0,9</td></tr>
<tr><td>Okna połaciowe</td><td class="num">1,1</td></tr>
<tr><td>Drzwi zewnętrzne</td><td class="num">1,3</td></tr>
</tbody></table>
<p class="mut">Źródło: rozporządzenie w sprawie warunków technicznych, jakim powinny odpowiadać budynki i ich usytuowanie (Dz.U. z 2019 r. poz. 1065 ze zm.), zestawienie w <a href="https://muratordom.pl/prawo/formalnosci-budowlane/warunki-techniczne-w-budownictwie-2021-aa-9R3S-4m58-DwiL.html">Muratorze</a>. Sprawdzone 17.10.2026. Przed projektem sprawdź aktualne brzmienie przepisów.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>U pustaka to nie U ściany.</b> Producent często podaje U samego muru albo muru z tynkiem. Ściana to wszystkie warstwy razem z oporami przejmowania ciepła po obu stronach.</div>
<div class="tip"><b>λ z karty, nie „około”.</b> Ten sam opór daje warstwa o grubości proporcjonalnej do λ. Styropian o λ 0,040 musi być o 29% grubszy niż grafitowy o λ 0,031, żeby izolować tak samo.</div>
<div class="tip"><b>WT to minimum.</b> Spełnienie wymagania nie znaczy, że ściana jest najtańsza w użytkowaniu. Grubszą izolację warto policzyć razem z ceną ogrzewania.</div>
<div class="tip"><b>Mostki cieplne zostają.</b> Nadproża, wieńce, płyty balkonowe i łączniki mechaniczne obniżają izolacyjność. Kalkulator liczy ścianę w polu, bez nich.</div>
<details><summary>Jak liczymy</summary>
<p>Opór warstwy to grubość w metrach podzielona przez λ. Opór całej przegrody to suma oporów warstw plus opory przejmowania ciepła: Rsi 0,13 dla ściany i 0,10 dla dachu (ciepło płynie w górę), Rse 0,04, według PN-EN ISO 6946. U to odwrotność całkowitego oporu.</p>
<p>Strumień ciepła to U razy różnica temperatur. Na każdej warstwie temperatura spada o strumień razy opór tej warstwy, stąd linia na rysunku. Brakująca grubość izolacji to różnica między oporem wymaganym (1 / U max) a obecnym, razy λ izolacji o najniższej λ w przegrodzie.</p>
</details>
<p>Powiązane: <a href="/ocieplenie">ocieplenie ścian: ile styropianu i kleju</a>, <a href="/sciany">pustaki na ściany</a>, <a href="/pompa-ciepla">pompa ciepła</a>.</p>
</main>''',
 script=_H+r'''const MAT={tg:["Tynk gipsowy",0.40,"jastrych"],tcw:["Tynk cementowo-wapienny",0.82,"jastrych"],tc:["Tynk cienkowarstwowy",0.70,"jastrych"],gk:["Płyta gipsowo-kartonowa",0.25,"jastrych"],pu:["Pustak ceramiczny",0.30,"mur"],bk:["Beton komórkowy 600",0.17,"mur"],si:["Bloczek silikatowy",0.90,"mur"],zb:["Żelbet",2.30,"beton"],eps:["Styropian EPS biały",0.038,"eps"],epsg:["Styropian grafitowy",0.031,"eps"],we:["Wełna mineralna",0.036,"welna"],xps:["Polistyren XPS",0.035,"xps"],pir:["Płyta PIR",0.022,"xps"],dr:["Drewno iglaste",0.13,"drewno"],inny:["Inny materiał",0.50,"jastrych"]};
const PRESET={sciana:[["tg",1.5],["pu",25],["epsg",15],["tc",0.5]],dach:[["gk",1.25],["we",20],["we",10]]};
let rows=[],dirty=false;
const load=t=>{rows=PRESET[t].map(([m,d])=>({m,d,l:MAT[m][1]}));};
function render(){
  $("warstwy").innerHTML=rows.map((r,i)=>`<div class="row u" data-i="${i}">
<label class="cell"><span>Warstwa ${i+1}</span><select data-k="m" aria-label="Materiał warstwy ${i+1}">${Object.entries(MAT).map(([k,m])=>`<option value="${k}"${k===r.m?" selected":""}>${m[0]}</option>`).join("")}</select></label>
<label class="cell"><span>Grubość (cm)</span><input data-k="d" type="number" min="0" step="0.5" value="${r.d}" aria-label="Grubość warstwy ${i+1} w cm"></label>
<label class="cell"><span>λ (W/m·K)</span><input data-k="l" type="number" min="0.001" step="0.001" value="${r.l}" aria-label="Lambda warstwy ${i+1}"></label>
<button class="btn x" type="button" data-del="${i}" aria-label="Usuń warstwę ${i+1}" title="Usuń warstwę">×</button></div>`).join("");
}
$("warstwy").addEventListener("input",e=>{
  const row=e.target.closest(".row"),k=e.target.dataset.k; if(!row||!k)return;
  const r=rows[+row.dataset.i]; dirty=true;
  if(k==="m"){r.m=e.target.value;r.l=MAT[r.m][1];row.querySelector('[data-k="l"]').value=r.l;}
  else r[k]=parseFloat(e.target.value)||0;
  licz();
});
$("warstwy").addEventListener("click",e=>{const b=e.target.closest("[data-del]");if(!b)return;rows.splice(+b.dataset.del,1);dirty=true;render();licz();});
$("dodaj").addEventListener("click",()=>{rows.push({m:"we",d:5,l:MAT.we[1]});dirty=true;render();licz();});
$("typ").addEventListener("input",()=>{if(!dirty){load($("typ").value);render();}licz();});
["ti","te"].forEach(id=>$(id).addEventListener("input",licz));
function licz(){
  const dach=$("typ").value==="dach", Rsi=dach?0.10:0.13, Rse=0.04, Umax=dach?0.15:0.20, ti=v("ti"), te=v("te");
  const L=rows.filter(r=>r.d>0&&r.l>0);
  if(!L.length){$("wynik").innerHTML="Dodaj co najmniej jedną warstwę z grubością i λ.";$("przekroj").innerHTML="";$("opis").textContent="";return;}
  const Rl=L.map(r=>r.d/100/r.l), R=Rsi+Rse+Rl.reduce((a,b)=>a+b,0), U=1/R, ok=U<=Umax+1e-9;
  const best=L.reduce((a,r)=>r.l<a.l?r:a,L[0]), ins=best.l<=0.06?best:{m:"epsg",l:MAT.epsg[1]};
  const brak=Math.max(0,1/Umax-R)*ins.l*100, dT=ti-te, q=U*dT, grub=L.reduce((a,r)=>a+r.d,0);
  let h=`Współczynnik U: <b>${f(U,3)} W/(m²·K)</b><br>`+
    `WT 2021 dla ${dach?"dachu":"ściany"}: U ≤ ${Umax.toFixed(2).replace(".",",")}, ${ok?'<span class="ok">spełnia</span>':'<span class="warn">nie spełnia</span>'}<br>`;
  h+=ok?`Zapas względem wymagania: ${f((1-U/Umax)*100,0)}%<br>`:`Brakuje ok. <b>${f(Math.ceil(brak),0)} cm</b> warstwy: ${MAT[ins.m][0].toLowerCase()} (λ ${f(ins.l,3)})<br>`;
  h+=`Opór cieplny R: ${f(R,2)} m²·K/W<br>Grubość przegrody: ${f(grub,1)} cm<br>`;
  if(dT>0)h+=`Strata ciepła: ${f(q,1)} W na m², ${f(q/10,2)} kW na 100 m²`;
  h+=`<p class="mut">Bez mostków cieplnych i łączników. Wiążące jest obliczenie w projekcie.</p>`;
  $("wynik").innerHTML=h;
  $("opis").textContent=`U = ${f(U,3)}, ${L.length} ${pl(L.length,"warstwa","warstwy","warstw")}`;
  rysuj(L,Rl,Rsi,Rse,U,ti,te);
}
let lastArgs=null;
addEventListener("resize",()=>{if(lastArgs)rysuj(...lastArgs);});
function rysuj(L,Rl,Rsi,Rse,U,ti,te){
  lastArgs=[L,Rl,Rsi,Rse,U,ti,te];
  const VW=$("przekroj").clientWidth<520?400:640, E=VW===400?46:90;
  const X0=E+20,X1=VW-E-20,Y0=46,Y1=236,W=X1-X0, sum=L.reduce((a,r)=>a+r.d,0);
  let w=L.map(r=>Math.max(5,r.d/sum*W)); const sk=W/w.reduce((a,b)=>a+b,0); w=w.map(x=>x*sk);
  let g="",x=X0; const xs=[X0];
  L.forEach((r,i)=>{
    g+=`<rect class="${MAT[r.m][2]}" x="${x.toFixed(1)}" y="${Y0}" width="${w[i].toFixed(1)}" height="${Y1-Y0}"/>`;
    if(w[i]>=18)g+=`<text class="tm halo" transform="translate(${(x+w[i]/2+4).toFixed(1)} ${Y1-10}) rotate(-90)">${MAT[r.m][0]}</text>`;
    if(w[i]>=34)g+=T((x+w[i]/2).toFixed(1),Y1+16,`${f(r.d,1)} cm`,"tm","middle");
    x+=w[i];xs.push(x);
  });
  g+=T(X0-14,Y1+16,"wnętrze","tm","end")+T(X1+14,Y1+16,"zewnątrz","tm","start");
  const q=U*(ti-te); let Tc=ti-q*Rsi; const P=[[X0-E,ti],[X0,Tc]];
  Rl.forEach((r,i)=>{Tc-=q*r;P.push([xs[i+1],Tc]);});
  P.push([X1+E,te]);
  const span=Math.abs(ti-te)>0.01?ti-te:1, Y=t=>Y0+14+(ti-t)/span*(Y1-Y0-28);
  if(te<0&&ti>0){const y0=Y(0).toFixed(1);g+=`<path class="mroz" d="M${X0-E-6} ${y0}H${X1+E+6}"/>`+T(X1+E+2,(Y(0)-6).toFixed(1),"0°C","tm halo","end");}
  g+=`<path class="temp draw" pathLength="1" d="M${P.map(p=>p[0].toFixed(1)+" "+Y(p[1]).toFixed(1)).join(" L")}"/>`;
  let lastX=-99,lastC=-99;
  P.slice(1,-1).forEach((p,i,a)=>{
    if(p[0]-lastC>=8||i===a.length-1){g+=`<circle class="pkt" cx="${p[0].toFixed(1)}" cy="${Y(p[1]).toFixed(1)}" r="3.5"/>`;lastC=p[0];}
    const first=i===0,last=i===a.length-1;
    if(first)g+=T(p[0]-8,(Y(p[1])-8).toFixed(1),`${f(p[1],1)}°`,"t halo","end");
    else if(last)g+=T(p[0]+8,(Y(p[1])-8).toFixed(1),`${f(p[1],1)}°`,"t halo","start");
    else if(p[0]-lastX>=34&&a[a.length-1][0]-p[0]>=34)g+=T(p[0].toFixed(1),(Y(p[1])-9).toFixed(1),`${f(p[1],1)}°`,"tm halo","middle");
    else return;
    lastX=p[0];
  });
  g+=T(8,Y0-14,`wewnątrz ${f(ti,0)}°C`,"t")+T(VW-8,Y0-14,`na zewnątrz ${f(te,0)}°C`,"t","end");
  const sv=$("przekroj");sv.setAttribute("viewBox",`0 0 ${VW} 290`);sv.innerHTML=g;
}
load("sciana");render();licz();''')

# ---------------------------------------------------------------- harmonogram
_ET=[("prz","Przygotowanie i tyczenie",1),("fun","Wykop i fundamenty",4),("par","Ściany i strop parteru",6),("pod","Ściany poddasza i więźba",4),("dach","Pokrycie dachu",3),("okn","Okna i drzwi zewnętrzne",2),("ele","Ocieplenie i elewacja",5),("ins","Instalacje wewnętrzne",5),("tyn","Tynki wewnętrzne",3),("wyl","Wylewki",1),("wyk","Wykończenie wnętrz",8)]
_inp=''.join(f'<label class="inl" for="t_{k}"><span>{n}</span><input id="t_{k}" type="number" min="0" step="1" value="{d}"></label>' for k,n,d in _ET)
CALC3['harmonogram']=dict(title='Harmonogram budowy domu: etapy na osi czasu',
 desc='Wybierz miesiąc startu i zobacz etapy budowy na osi czasu: stan surowy zamknięty, deweloperski, termin zamówienia okien i prace mokre wypadające zimą.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Harmonogram budowy domu</h1>
<p class="lead">Wybierz miesiąc rozpoczęcia i czasy trwania etapów. Zobaczysz, kiedy dom będzie w stanie surowym zamkniętym i deweloperskim, do kiedy zamówić okna i które prace mokre wypadają zimą.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="start">Rozpoczęcie budowy</label><input id="start" type="month"></div>
<div><label for="dost">Czas dostawy okien (tyg., z oferty)</label><input id="dost" type="number" min="0" step="1" value="8"></div>
<div><label for="schn">Schnięcie wylewki (tyg., przykład)</label><input id="schn" type="number" min="0" step="1" value="6"></div>
</div>
<p class="sub">Czas trwania etapów, w tygodniach</p>
<div class="dur">'''+_inp+r'''</div>
<p class="mut">Czasy trwania są przykładowe. Prawdziwe poda wykonawca, a zmienią je pogoda i dostawy.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Oś czasu budowy <span id="opis"></span></figcaption><svg id="gantt" viewBox="0 0 760 400" role="img" aria-label="Wykres Gantta etapów budowy z zaznaczonymi miesiącami zimowymi"></svg><p class="note">Niebieskie paski to prace mokre, pomarańczowe suche, kreskowany to schnięcie wylewki. Jasnoniebieskie tło to grudzień, styczeń i luty. SSZ: stan surowy zamknięty, SD: stan deweloperski.</p></figure>
<h2>Jak czytać harmonogram</h2>
<p>Etapy idą po sobie, poza ociepleniem i elewacją, które ruszają po wstawieniu okien i biegną równolegle z pracami w środku. Wykończenie wnętrz zaczyna się dopiero po wyschnięciu wylewki. Stan deweloperski liczymy jako koniec wylewek i elewacji.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Okna zamawia się wcześniej, niż się wydaje.</b> Okna robione na wymiar mają czas produkcji. Jeśli zamówisz je po zrobieniu dachu, budowa stanie. Termin dostawy wpisz z oferty.</div>
<div class="tip"><b>Prace mokre zimą wymagają planu.</b> Beton, zaprawa, tynki i wylewki źle znoszą mróz. Zimą potrzebne są domieszki, osłony i ogrzewanie albo przerwa. Policz ją od razu, a nie w listopadzie.</div>
<div class="tip"><b>Schnięcie wylewki to też czas budowy.</b> Na mokrą wylewkę nie kładzie się podłóg. Zanim zamówisz parkiet, wykonawca podłóg powinien zmierzyć wilgotność.</div>
<div class="tip"><b>Ekipy mają swoje kalendarze.</b> Dobry wykonawca jest zajęty na kilka miesięcy do przodu. Harmonogram pokazuje, kiedy kogo potrzebujesz, więc umawiaj ekipy według niego.</div>
<details><summary>Jak liczymy</summary>
<p>Każdy etap zaczyna się po zakończeniu poprzedniego. Ocieplenie i elewacja startują po oknach. Wykończenie startuje po wylewkach i ich schnięciu. Termin zamówienia okien to początek ich montażu minus czas dostawy. Etap mokry oznaczamy, jeśli choć jeden jego tydzień wypada w grudniu, styczniu albo lutym.</p>
</details>
<p>Powiązane: <a href="/etapy-budowy">etapy budowy krok po kroku</a>, <a href="/wylewka">kalkulator wylewki i czas schnięcia</a>, <a href="/kredyt">kredyt na budowę</a>.</p>
</main>''',
 script=_H+r'''const ET=[["prz","Przygotowanie i tyczenie",0,[]],["fun","Wykop i fundamenty",1,["prz"]],["par","Ściany i strop parteru",1,["fun"]],["pod","Ściany poddasza i więźba",1,["par"]],["dach","Pokrycie dachu",0,["pod"]],["okn","Okna i drzwi zewnętrzne",0,["dach"]],["ele","Ocieplenie i elewacja",1,["okn"]],["ins","Instalacje wewnętrzne",0,["okn"]],["tyn","Tynki wewnętrzne",1,["ins"]],["wyl","Wylewki",1,["tyn"]],["sch","Schnięcie wylewki",2,["wyl"]],["wyk","Wykończenie wnętrz",0,["sch"]]];
const MS=["sty","lut","mar","kwi","maj","cze","lip","sie","wrz","paź","lis","gru"];
(()=>{const n=new Date(),y=n.getMonth()>=3?n.getFullYear()+1:n.getFullYear();$("start").value=`${y}-04`;})();
function licz(){
  const p=($("start").value||"2027-04").split("-").map(Number), t0=new Date(p[0],(p[1]||4)-1,1);
  const dt=w=>new Date(t0.getTime()+Math.round(w*7)*864e5);
  const D=w=>dt(w).toLocaleDateString("pl-PL",{day:"numeric",month:"long",year:"numeric"});
  const S={},E={},dur=k=>k==="sch"?Math.max(0,v("schn")):Math.max(0,v("t_"+k));
  ET.forEach(([k,,,dep])=>{S[k]=dep.length?Math.max(...dep.map(d=>E[d])):0;E[k]=S[k]+dur(k);});
  const SSZ=E.okn, SD=Math.max(E.wyl,E.ele), END=Math.max(E.wyk,E.ele), zam=S.okn-Math.max(0,v("dost"));
  const zima=w=>[11,0,1].includes(dt(w).getMonth());
  const mokreZima=ET.filter(([k,,m])=>m===1&&dur(k)>0&&Array.from({length:Math.ceil(dur(k))},(_,i)=>S[k]+i).some(zima)).map(e=>e[1]);
  let h=`Stan surowy zamknięty: <b>${D(SSZ)}</b><br>Stan deweloperski: <b>${D(SD)}</b><br>Koniec wykończenia: <b>${D(END)}</b><br>`+
    `Łącznie ${f(END,0)} ${pl(END,"tydzień","tygodnie","tygodni")}, około ${f(END/4.345,0)} ${pl(END/4.345,"miesiąc","miesiące","miesięcy")}<br>`+
    (zam<0?`Okna zamów <span class="warn">przed startem budowy</span>, do ${D(zam)}<br>`:`Okna zamów najpóźniej: <b>${D(zam)}</b><br>`);
  h+=mokreZima.length?`<span class="warn">Prace mokre zimą:</span> ${mokreZima.join(", ").toLowerCase()}`:`<span class="ok">Żadne prace mokre nie wypadają zimą</span>`;
  h+=`<p class="mut">Czasy trwania są przykładowe. Wpisz terminy z ofert wykonawców.</p>`;
  $("wynik").innerHTML=h;
  $("opis").textContent=`${f(END,0)} ${pl(END,"tydzień","tygodnie","tygodni")} od ${MS[t0.getMonth()]} ${t0.getFullYear()}`;
  rysuj(S,E,SSZ,SD,END,zam,t0,dt,dur);
}
let rz;addEventListener("resize",()=>{clearTimeout(rz);rz=setTimeout(licz,150);});
function rysuj(S,E,SSZ,SD,END,zam,t0,dt,dur){
  const svg=$("gantt"),N=svg.clientWidth<560,VW=N?360:760;
  const LX=N?8:196,RX=VW-(N?8:16),TOP=50,RH=N?34:26,n=ET.length,BOT=TOP+n*RH,tot=Math.max(4,END+1),px=(RX-LX)/tot,X=w=>LX+w*px;
  const by=N?16:5,bh=N?13:RH-10,ty=by+bh/2+4;
  let g=`<defs><pattern id="kres" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect class="kresbg" width="7" height="7"/><path class="kresl" d="M0 0V7"/></pattern></defs>`;
  const endD=dt(tot); let m=new Date(t0.getFullYear(),t0.getMonth(),1), lastLab=-99, lastYear=null;
  while(m<=endD){
    const nx=new Date(m.getFullYear(),m.getMonth()+1,1), w0=(m-t0)/(7*864e5), w1=(nx-t0)/(7*864e5);
    const x0=X(Math.max(0,w0)), x1=X(Math.min(tot,w1));
    if([11,0,1].includes(m.getMonth()))g+=`<rect class="zima" x="${x0.toFixed(1)}" y="${TOP-6}" width="${Math.max(0,x1-x0).toFixed(1)}" height="${BOT-TOP+12}"/>`;
    g+=`<path class="gl" d="M${x0.toFixed(1)} ${TOP-24}V${BOT+6}"/>`;
    if(x0-lastLab>=24&&x1-x0>=14){g+=T((x0+3).toFixed(1),TOP-12,MS[m.getMonth()],"tm");lastLab=x0;}
    if(m.getFullYear()!==lastYear){g+=T((x0+3).toFixed(1),TOP-30,String(m.getFullYear()),"t");lastYear=m.getFullYear();}
    m=nx;
  }
  ET.forEach(([k,name,mk],i)=>{
    const y=TOP+i*RH, d=dur(k), x=X(S[k]), w=Math.max(d>0?3:0,d*px);
    g+=N?T(LX,y+11,name,"tm halo"):T(LX-10,y+RH/2+4,name,"t","end");
    if(d>0){
      const cls=mk===2?'fill="url(#kres)" class="kresr"':`class="${mk?"mokro":"sucho"} pop" style="animation-delay:${i*50}ms"`;
      g+=`<rect ${cls} x="${x.toFixed(1)}" y="${y+by}" width="${w.toFixed(1)}" height="${bh}" rx="${N?3:4}"/>`;
      g+=x+w+50>RX&&w>=56?T((x+w-8).toFixed(1),y+ty,`${f(d,0)} tyg.`,mk===2?"tm halo":"tw","end"):T((x+w+6).toFixed(1),y+ty,`${f(d,0)} tyg.`,"tm halo");
    }
  });
  if(zam>=0){const zx=X(zam),zy=TOP+5*RH+by+bh/2,lft=zx-10>(N?70:LX+60);g+=`<path class="zam" d="M${zx.toFixed(1)} ${zy-6}l6 6-6 6-6-6z"/>`+T((lft?zx-10:zx+10).toFixed(1),zy+4,"zamówienie","tm halo",lft?"end":"start");}
  [[SSZ,"SSZ"],[SD,"SD"]].forEach(([w,l])=>{const x=X(w).toFixed(1);g+=`<path class="dim ms" d="M${x} ${TOP-4}V${BOT+8}"/>`+T(x,BOT+22,l,"t","middle");});
  svg.setAttribute("viewBox",`0 0 ${VW} ${BOT+34}`); svg.innerHTML=g;
}
document.querySelectorAll("input").forEach(e=>e.addEventListener("input",licz));licz();''')

# ---------------------------------------------------------------- rozkroj
CALC3['rozkroj-pretow']=dict(title='Rozkrój prętów zbrojeniowych i zestawienie stali',
 desc='Wpisz pręty z zestawienia: średnica, długość, liczba sztuk. Kalkulator policzy masę stali, liczbę prętów 12 m do zamówienia i plan cięcia z najmniejszym odpadem.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Dla firm</div>
<h1>Rozkrój prętów i zestawienie stali</h1>
<p class="lead noprint">Wpisz pozycje z zestawienia stali. Kalkulator policzy masę według średnic, ile prętów handlowych zamówić i jak je pociąć, żeby odpad był jak najmniejszy.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="stock">Długość pręta handlowego (m)</label><input id="stock" type="number" min="1" step="0.5" value="12"></div>
<div><label for="rzaz">Strata na cięcie (mm na cięcie)</label><input id="rzaz" type="number" min="0" step="1" value="0"></div>
<div><label for="resz">Resztki do wykorzystania od (m)</label><input id="resz" type="number" min="0" step="0.1" value="1"></div>
</div>
<p class="sub">Pozycje zestawienia</p>
<div class="rowh p"><span>Opis</span><span>Średnica</span><span>Długość (m)</span><span>Sztuk</span><span></span></div>
<div id="prety" class="rows"></div>
<div class="btns"><button class="btn" id="dodaj" type="button">+ Dodaj pozycję</button></div>
<p class="mut">Długość pręta wpisz razem z hakami, odgięciami i zakładami, tak jak w zestawieniu z projektu.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Zestawienie stali</h2>
<div id="tab"></div>
<div class="btns noprint"><button class="btn" id="kopiuj" type="button">Kopiuj do Excela</button><button class="btn" id="druk" type="button">Drukuj albo zapisz PDF</button><span class="mut" id="kop" aria-live="polite"></span></div>
<figure class="panel fig"><figcaption>Plan cięcia prętów <span id="opis"></span></figcaption><svg id="plan" viewBox="0 0 640 200" role="img" aria-label="Plan cięcia prętów handlowych z odcinkami i odpadem"></svg><p class="note">Każdy wiersz to jeden sposób pocięcia pręta handlowego, liczba z przodu mówi, ile prętów tniesz tak samo. Szare pole to odpad albo resztka.</p></figure>
<h2 class="noprint">Na czym ludzie się mylą</h2>
<div class="tip"><b>Masa z zestawienia to nie masa do zamówienia.</b> Hurtownia sprzedaje całe pręty. Do masy z projektu dochodzi odpad z cięcia, który przy krótkich i długich pozycjach potrafi być spory.</div>
<div class="tip"><b>Długie pozycje tnij najpierw.</b> Krótkie odcinki, na przykład strzemiona, dobrze wypełniają resztki po długich prętach tej samej średnicy. Dlatego liczymy rozkrój dla wszystkich pozycji danej średnicy razem.</div>
<div class="tip"><b>Pręt dłuższy niż handlowy to łączenie.</b> Takiej pozycji nie da się wyciąć z jednego pręta. Długość i miejsce zakładu podaje projekt, a w kalkulatorze wpisz osobno odcinki do zakładu.</div>
<div class="tip"><b>Resztki mają wartość.</b> Odcinki powyżej metra przydadzą się na dodatki, szpilki czy zbrojenie nadproży. Kalkulator wylicza je osobno, żeby nie trafiły od razu na złom.</div>
<details><summary>Jak liczymy</summary>
<p>Masa metra pręta to pole przekroju razy gęstość stali 7850 kg/m³, czyli dla Ø12 to 0,888 kg/m. Masa pozycji to łączna długość razy masa metra.</p>
<p>Rozkrój liczymy osobno dla każdej średnicy. Odcinki sortujemy od najdłuższego i każdy kładziemy w tym pręcie, w którym zostanie najmniej wolnego miejsca. Gdy żaden nie pasuje, zaczynamy nowy pręt. To szybka metoda, która daje wynik bliski najlepszemu, ale nie zawsze idealny.</p>
</details>
<p class="noprint">Powiązane: <a href="/beton">beton i stal na ławy, płytę i strop</a>, <a href="/kosztorys">kosztorys ofertowy</a>.</p>
</main>''',
 script=_H+r'''const FI=[6,8,10,12,14,16,20,25,28,32], kgm=d=>Math.PI*Math.pow(d/1000,2)/4*7850;
let rows=[{o:"Ławy, pręty główne",d:12,l:4.35,n:16},{o:"Ławy, pręty montażowe",d:12,l:2.8,n:10},{o:"Strzemiona ław",d:8,l:1.1,n:120},{o:"Wieniec, pręty podłużne",d:12,l:6.2,n:8}], last=[];
function render(){
  $("prety").innerHTML=rows.map((r,i)=>`<div class="row p" data-i="${i}">
<label class="cell o"><span>Opis</span><input data-k="o" type="text" value="${esc(r.o)}" aria-label="Opis pozycji ${i+1}"></label>
<label class="cell"><span>Średnica</span><select data-k="d" aria-label="Średnica pozycji ${i+1}">${FI.map(d=>`<option value="${d}"${d===r.d?" selected":""}>Ø${d}</option>`).join("")}</select></label>
<label class="cell"><span>Długość (m)</span><input data-k="l" type="number" min="0" step="0.05" value="${r.l}" aria-label="Długość pręta pozycji ${i+1} w metrach"></label>
<label class="cell"><span>Sztuk</span><input data-k="n" type="number" min="0" step="1" value="${r.n}" aria-label="Liczba sztuk pozycji ${i+1}"></label>
<button class="btn x" type="button" data-del="${i}" aria-label="Usuń pozycję ${i+1}" title="Usuń pozycję">×</button></div>`).join("");
}
$("prety").addEventListener("input",e=>{const row=e.target.closest(".row"),k=e.target.dataset.k;if(!row||!k)return;const r=rows[+row.dataset.i];r[k]=k==="o"?e.target.value:(parseFloat(e.target.value)||0);licz();});
$("prety").addEventListener("click",e=>{const b=e.target.closest("[data-del]");if(!b)return;rows.splice(+b.dataset.del,1);render();licz();});
$("dodaj").addEventListener("click",()=>{rows.push({o:"",d:12,l:3,n:10});render();licz();});
["stock","rzaz","resz"].forEach(id=>$(id).addEventListener("input",licz));
$("druk").addEventListener("click",()=>window.print());
$("kopiuj").addEventListener("click",()=>{
  const t=[["Średnica","Długość łączna (m)","kg/m","Masa (kg)","Pręty handlowe (szt.)","Masa zakupu (kg)","Odpad (%)"].join("\t")].concat(last.map(g=>[`Ø${g.d}`,f(g.len/1000,2),f(kgm(g.d),3),f(g.len/1000*kgm(g.d),1),g.bars.length,f(g.buy/1000*kgm(g.d),1),f(g.buy?g.odp/g.buy*100:0,1)].join("\t"))).join("\n");
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>$("kop").textContent="Skopiowano. Wklej w arkuszu.",()=>$("kop").textContent="Przeglądarka nie pozwoliła skopiować. Zaznacz tabelę ręcznie.");
});
function licz(){
  const S=Math.round(v("stock")*1000), k=Math.max(0,Math.round(v("rzaz"))), minOff=Math.round(v("resz")*1000), by={};
  let cut=false;
  rows.forEach(r=>{const L=Math.round(r.l*1000),n=Math.max(0,Math.floor(r.n));if(L<=0||n<=0||S<=0)return;
    const g=by[r.d]=by[r.d]||{d:r.d,pcs:[],len:0,dlugie:0};g.len+=L*n;
    if(L>S){g.dlugie+=n;return;}
    for(let i=0;i<n;i++){if(g.pcs.length>=20000){cut=true;break;}g.pcs.push(L);}});
  last=Object.values(by).sort((a,b)=>a.d-b.d).map(g=>{
    g.pcs.sort((a,b)=>b-a); const bars=[];
    for(const p of g.pcs){const need=p+k;let best=-1,br=Infinity;
      for(let j=0;j<bars.length;j++){const r=bars[j].rem;if(r>=need&&r<br){br=r;best=j;}}
      if(best<0){bars.push({rem:S+k,items:[]});best=bars.length-1;}
      bars[best].rem-=need;bars[best].items.push(p);}
    const pat={};bars.forEach(b=>{const key=b.items.join(",");(pat[key]=pat[key]||{items:b.items,n:0,odp:Math.max(0,b.rem-k)}).n++;});
    const used=g.pcs.reduce((a,b)=>a+b,0),buy=bars.length*S,offc=bars.map(b=>Math.max(0,b.rem-k)).filter(x=>minOff>0&&x>=minOff);
    return Object.assign(g,{bars,pat:Object.values(pat).sort((a,b)=>b.n-a.n),used,buy,odp:buy-used,offc});
  });
  if(!last.length){$("wynik").innerHTML="Dodaj pozycję z długością i liczbą sztuk.";$("tab").innerHTML="";$("plan").innerHTML="";$("opis").textContent="";return;}
  const mPro=last.reduce((a,g)=>a+g.len/1000*kgm(g.d),0), mBuy=last.reduce((a,g)=>a+g.buy/1000*kgm(g.d),0), nBar=last.reduce((a,g)=>a+g.bars.length,0);
  const oBuy=last.reduce((a,g)=>a+g.buy,0), oOdp=last.reduce((a,g)=>a+g.odp,0), resz=last.reduce((a,g)=>a+g.offc.reduce((x,y)=>x+y,0),0), dl=last.reduce((a,g)=>a+g.dlugie,0);
  let h=`Masa według zestawienia: <b>${f(mPro,1)} kg</b><br>Do zamówienia: <b>${nBar} ${pl(nBar,"pręt","pręty","prętów")} po&nbsp;${f(S/1000,2)}&nbsp;m</b><br>Masa zakupu: <b>${f(mBuy,1)} kg</b>${dl?" bez pozycji dłuższych niż pręt handlowy":""}<br>Odpad i resztki: ${f(oBuy?oOdp/oBuy*100:0,1)}% długości`;
  if(resz>0)h+=`, z czego ${f(resz/1000,1)} m to resztki do wykorzystania`;
  h+=`<br>`+last.map(g=>`Ø${g.d}: ${g.bars.length} szt., ${f(g.buy/1000*kgm(g.d),1)} kg`).join("<br>");
  if(dl)h+=`<br><span class="warn">${dl} szt. dłuższych niż pręt handlowy</span>: rozbij je na odcinki z zakładem według projektu`;
  if(cut)h+=`<br><span class="warn">Bardzo dużo sztuk</span>: rozkrój policzony dla pierwszych 20 000 odcinków danej średnicy`;
  h+=`<p class="mut">Masa z gęstości stali 7850 kg/m³. Pręty dłuższe od handlowego liczymy do masy, ale nie do rozkroju.</p>`;
  $("wynik").innerHTML=h;
  const tr=last.map(g=>`<tr><td>Ø${g.d}</td><td class="num">${f(g.len/1000,2)}</td><td class="num">${f(kgm(g.d),3)}</td><td class="num">${f(g.len/1000*kgm(g.d),1)}</td><td class="num">${g.bars.length}</td><td class="num">${f(g.buy/1000*kgm(g.d),1)}</td><td class="num">${f(g.buy?g.odp/g.buy*100:0,1)}%</td></tr>`).join("");
  $("tab").innerHTML=`<div class="scrollx"><table><thead><tr><th>Średnica</th><th class="num">Długość łączna (m)</th><th class="num">kg/m</th><th class="num">Masa (kg)</th><th class="num">Pręty ${f(S/1000,2)} m</th><th class="num">Masa zakupu (kg)</th><th class="num">Odpad</th></tr></thead><tbody>${tr}</tbody><tfoot><tr><td>Razem</td><td class="num">${f(last.reduce((a,g)=>a+g.len,0)/1000,2)}</td><td></td><td class="num">${f(mPro,1)}</td><td class="num">${nBar}</td><td class="num">${f(mBuy,1)}</td><td class="num">${f(oBuy?oOdp/oBuy*100:0,1)}%</td></tr></tfoot></table></div>`;
  rysuj(S);
}
let rz;addEventListener("resize",()=>{clearTimeout(rz);rz=setTimeout(licz,150);});
function rysuj(S){
  const N=$("plan").clientWidth<520,VW=N?380:640,LX=N?40:78,RX=VW-(N?8:12),RH=24,MAXR=32; let y=10,g="",shown=0,all=0;
  last.forEach(gr=>{
    all+=gr.pat.length; if(shown>=MAXR)return;
    g+=T(4,y+14,`Ø${gr.d}`,"t")+T(LX,y+14,`${gr.bars.length} ${gr.bars.length===1?"pręt":gr.bars.length%10>=2&&gr.bars.length%10<=4&&(gr.bars.length%100<10||gr.bars.length%100>=20)?"pręty":"prętów"} po ${f(S/1000,2)} m`,"tm");
    y+=22;
    gr.pat.forEach(p=>{
      if(shown>=MAXR)return; shown++;
      g+=T(LX-10,y+RH/2+2,`${p.n} ×`,"t","end");
      let x=LX; const sc=(RX-LX)/S;
      p.items.forEach((L,i)=>{const w=L*sc;g+=`<rect class="${i%2?"pc2":"pc1"}" x="${x.toFixed(1)}" y="${y}" width="${Math.max(1,w-1).toFixed(1)}" height="${RH-6}" rx="2"/>`;
        if(w>=30)g+=T((x+w/2).toFixed(1),y+RH/2+1,f(L/1000,2),"tp","middle");x+=w;});
      if(p.odp>0){const w=RX-x;g+=`<rect class="odp" x="${x.toFixed(1)}" y="${y}" width="${Math.max(0.5,w).toFixed(1)}" height="${RH-6}" rx="2"/>`;if(w>=40)g+=T((x+w/2).toFixed(1),y+RH/2+1,f(p.odp/1000,2),"tp","middle");}
      y+=RH;
    });
    y+=8;
  });
  if(all>shown){g+=T(4,y+12,`Pokazano ${shown} z ${all} sposobów cięcia.`,"tm");y+=20;}
  const svg=$("plan");svg.setAttribute("viewBox",`0 0 ${VW} ${Math.max(60,y+4)}`);svg.innerHTML=g;
  $("opis").textContent=`${all} ${all===1?"sposób":all%10>=2&&all%10<=4&&(all%100<10||all%100>=20)?"sposoby":"sposobów"} cięcia`;
}
render();licz();''')

# ---------------------------------------------------------------- kosztorys
CALC3['kosztorys']=dict(title='Kosztorys ofertowy online: robocizna, materiał, narzuty, VAT',
 desc='Prosty kosztorys ofertowy dla firmy budowlanej: pozycje z nakładami, stawka roboczogodziny, koszty pośrednie, zysk i VAT. Tabela do oferty, kopiowanie do Excela, wydruk.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Dla firm</div>
<h1 class="noprint">Kosztorys ofertowy: robocizna, materiał, narzuty</h1>
<p class="printonly"><b>Kosztorys ofertowy</b>, <span id="dzis"></span></p>
<p class="lead noprint">Wpisz pozycje robót z nakładami i cenami, swoją stawkę roboczogodziny i narzuty. Dostaniesz cenę jednostkową każdej pozycji, wartość oferty netto i brutto oraz tabelę gotową do skopiowania albo wydruku.</p>
<section class="calc wide"><div class="panel">
<div class="grid g4">
<div><label for="stawka">Stawka r-g (zł, przykład)</label><input id="stawka" type="number" min="0" step="1" value="50"></div>
<div><label for="kp">Koszty pośrednie Kp (% od R i S)</label><input id="kp" type="number" min="0" step="1" value="60"></div>
<div><label for="kz">Koszty zakupu Kz (% od M)</label><input id="kz" type="number" min="0" step="0.5" value="5"></div>
<div><label for="zy">Zysk Z (%)</label><input id="zy" type="number" min="0" step="0.5" value="10"></div>
<div><label for="zod">Zysk naliczany od</label><select id="zod"><option value="rs">R + S + Kp</option><option value="all">wszystkich składników</option></select></div>
<div><label for="vat">VAT</label><select id="vat"><option value="8">8% (budownictwo mieszkaniowe)</option><option value="23">23%</option></select></div>
</div>
<p class="sub">Pozycje kosztorysu</p>
<div class="rowh k"><span>Opis roboty</span><span>j.m.</span><span>Ilość</span><span>r-g / j.m.</span><span>Materiał zł / j.m.</span><span>Sprzęt zł / j.m.</span><span></span></div>
<div id="poz" class="rows"></div>
<div class="btns"><button class="btn" id="dodaj" type="button">+ Dodaj pozycję</button></div>
<p class="mut">Pozycje, nakłady i ceny w formularzu są przykładowe. Wpisz własne albo z katalogów nakładów (KNR) i aktualnych cenników.</p>
</div>
<div class="out noprint" id="wynik" aria-live="polite"></div></section>
<h2>Zestawienie do oferty</h2>
<div id="tab"></div>
<div class="btns noprint"><button class="btn" id="kopiuj" type="button">Kopiuj do Excela</button><button class="btn" id="druk" type="button">Drukuj albo zapisz PDF</button><span class="mut" id="kop" aria-live="polite"></span></div>
<figure class="panel fig noprint"><figcaption>Z czego składa się cena <span id="opis"></span></figcaption><svg id="str" viewBox="0 0 640 130" role="img" aria-label="Struktura wartości netto: robocizna, materiały, sprzęt, koszty pośrednie, koszty zakupu i zysk"></svg></figure>
<h2 class="noprint">Na czym ludzie się mylą</h2>
<div class="tip"><b>Narzuty to Twoje koszty, nie cudze.</b> Koszty pośrednie obejmują biuro, dojazdy, ubezpieczenia, sprzęt drobny i czas na wyceny. Średnie publikują wydawnictwa cenowe, ale prawdziwy procent wynika z kosztów Twojej firmy.</div>
<div class="tip"><b>Nakład r-g z normy to nie zawsze nakład Twojej ekipy.</b> Katalogi nakładów podają średnie. Porównaj je z tym, ile Twoja ekipa robi naprawdę, i popraw stawki po kilku budowach.</div>
<div class="tip"><b>Stawka VAT zależy od obiektu.</b> Przy budowie domu do 300 m² powierzchni użytkowej usługa ma zwykle 8%, powyżej limitu część wartości ma 23%. Policz to w <a href="/vat-budowa">kalkulatorze VAT 8% czy 23%</a>.</div>
<div class="tip"><b>Materiał w ofercie z kosztami zakupu.</b> Transport, rozładunek, magazyn i straty na budowie to koszty zakupu. Bez nich materiał w ofercie wychodzi taniej, niż kosztuje Cię naprawdę.</div>
<details><summary>Jak liczymy</summary>
<p>Robocizna R to ilość razy nakład r-g razy stawka. Materiały M to ilość razy cena materiału, sprzęt S to ilość razy koszt sprzętu. Koszty pośrednie Kp to procent od R i S. Koszty zakupu Kz to procent od M. Zysk Z to procent od sumy R, S i Kp albo, po zmianie ustawienia, od wszystkich składników.</p>
<p>Cena jednostkowa pozycji to suma R, M, S, Kp, Kz i Z podzielona przez ilość. Wartość netto oferty to suma pozycji, a brutto to netto plus VAT.</p>
</details>
<p class="noprint">Powiązane: <a href="/rozkroj-pretow">rozkrój prętów i zestawienie stali</a>, <a href="/vat-budowa">VAT 8% czy 23%</a>, <a href="/harmonogram">harmonogram budowy</a>.</p>
</main>''',
 script=_H+r'''const JM=["m²","m³","mb","szt.","kpl.","t","kg"];
let rows=[{o:"Murowanie ścian z pustaków ceramicznych 25 cm",j:"m²",q:120,r:1.1,m:95,s:4},{o:"Wieniec żelbetowy z betonem i stalą",j:"m³",q:4,r:14,m:1000,s:60},{o:"Tynk gipsowy maszynowy",j:"m²",q:380,r:0.3,m:18,s:3}], last=null;
function render(){
  $("poz").innerHTML=rows.map((r,i)=>`<div class="row k" data-i="${i}">
<label class="cell o"><span>Opis roboty</span><input data-k="o" type="text" value="${esc(r.o)}" aria-label="Opis pozycji ${i+1}"></label>
<label class="cell"><span>j.m.</span><select data-k="j" aria-label="Jednostka pozycji ${i+1}">${JM.map(j=>`<option${j===r.j?" selected":""}>${j}</option>`).join("")}</select></label>
<label class="cell"><span>Ilość</span><input data-k="q" type="number" min="0" step="0.01" value="${r.q}" aria-label="Ilość pozycji ${i+1}"></label>
<label class="cell"><span>r-g / j.m.</span><input data-k="r" type="number" min="0" step="0.01" value="${r.r}" aria-label="Nakład roboczogodzin na jednostkę, pozycja ${i+1}"></label>
<label class="cell"><span>Materiał zł / j.m.</span><input data-k="m" type="number" min="0" step="0.01" value="${r.m}" aria-label="Materiał w zł na jednostkę, pozycja ${i+1}"></label>
<label class="cell"><span>Sprzęt zł / j.m.</span><input data-k="s" type="number" min="0" step="0.01" value="${r.s}" aria-label="Sprzęt w zł na jednostkę, pozycja ${i+1}"></label>
<button class="btn x" type="button" data-del="${i}" aria-label="Usuń pozycję ${i+1}" title="Usuń pozycję">×</button></div>`).join("");
}
$("poz").addEventListener("input",e=>{const row=e.target.closest(".row"),k=e.target.dataset.k;if(!row||!k)return;const r=rows[+row.dataset.i];r[k]=(k==="o"||k==="j")?e.target.value:(parseFloat(e.target.value)||0);licz();});
$("poz").addEventListener("click",e=>{const b=e.target.closest("[data-del]");if(!b)return;rows.splice(+b.dataset.del,1);render();licz();});
$("dodaj").addEventListener("click",()=>{rows.push({o:"",j:"m²",q:1,r:0,m:0,s:0});render();licz();});
["stawka","kp","kz","zy","zod","vat"].forEach(id=>$(id).addEventListener("input",licz));
$("druk").addEventListener("click",()=>window.print());
$("kopiuj").addEventListener("click",()=>{
  if(!last)return; const n2=x=>x.toFixed(2).replace(".",",");
  const t=[["Lp.","Opis","j.m.","Ilość","Cena jedn. netto","Wartość netto"].join("\t")].concat(last.L.map((r,i)=>[i+1,r.o,r.j,String(r.q).replace(".",","),n2(r.cj),n2(r.W)].join("\t")),["","Razem netto","","","",n2(last.net)].join("\t"),["",`VAT ${last.vp}%`,"","","",n2(last.vat)].join("\t"),["","Razem brutto","","","",n2(last.net+last.vat)].join("\t")).join("\n");
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>$("kop").textContent="Skopiowano. Wklej w arkuszu.",()=>$("kop").textContent="Przeglądarka nie pozwoliła skopiować. Zaznacz tabelę ręcznie.");
});
function licz(){
  const st=v("stawka"),kp=v("kp")/100,kz=v("kz")/100,zy=v("zy")/100,vp=+$("vat").value,all=$("zod").value==="all";
  const t={R:0,M:0,S:0,Kp:0,Kz:0,Z:0};
  const L=rows.map(r=>{const R=r.q*r.r*st,M=r.q*r.m,S=r.q*r.s,Kp=(R+S)*kp,Kz=M*kz,Z=(R+S+Kp+(all?M+Kz:0))*zy,W=R+M+S+Kp+Kz+Z;
    t.R+=R;t.M+=M;t.S+=S;t.Kp+=Kp;t.Kz+=Kz;t.Z+=Z;return Object.assign({},r,{W,cj:r.q>0?W/r.q:0});});
  const net=L.reduce((a,r)=>a+r.W,0),vat=net*vp/100;
  last={L,net,vat,vp};
  $("wynik").innerHTML=`<div class="cols2"><div>Wartość netto: <b>${zl(net)}</b><br>VAT ${vp}%: ${zl(vat)}<br>Wartość brutto: <b>${zl(net+vat)}</b></div>`+
    `<div>Robocizna R: ${zl(t.R)}<br>Materiały M: ${zl(t.M)}<br>Sprzęt S: ${zl(t.S)}<br>Koszty pośrednie Kp: ${zl(t.Kp)}<br>Koszty zakupu Kz: ${zl(t.Kz)}<br>Zysk Z: ${zl(t.Z)}</div></div>`+
    `<p class="mut">Pozycje, nakłady i ceny są przykładowe. Wynik to kalkulacja, nie wycena wiążąca.</p>`;
  const tr=L.map((r,i)=>`<tr><td>${i+1}</td><td>${esc(r.o)||"bez opisu"}</td><td>${r.j}</td><td class="num">${f(r.q,2)}</td><td class="num">${zl(r.cj)}</td><td class="num">${zl(r.W)}</td></tr>`).join("");
  $("tab").innerHTML=`<div class="scrollx"><table><thead><tr><th>Lp.</th><th>Opis</th><th>j.m.</th><th class="num">Ilość</th><th class="num">Cena jedn. netto</th><th class="num">Wartość netto</th></tr></thead><tbody>${tr}</tbody><tfoot><tr><td></td><td colspan="4">Razem netto</td><td class="num">${zl(net)}</td></tr><tr><td></td><td colspan="4">VAT ${vp}%</td><td class="num">${zl(vat)}</td></tr><tr><td></td><td colspan="4">Razem brutto</td><td class="num">${zl(net+vat)}</td></tr></tfoot></table></div>`;
  rysuj(t,net);
}
function rysuj(t,net){
  const P=[["R","Robocizna","s1"],["M","Materiały","s2"],["S","Sprzęt","s3"],["Kp","Koszty pośrednie","s4"],["Kz","Koszty zakupu","s5"],["Z","Zysk","s6"]];
  let g="",x=10;const W=620;
  if(net<=0){$("str").innerHTML=T(10,40,"Brak pozycji z wartością.","tm");$("opis").textContent="";return;}
  P.forEach(([k,,c],i)=>{const w=t[k]/net*W;if(w<=0)return;g+=`<rect class="${c} pop" style="animation-delay:${i*60}ms" x="${x.toFixed(1)}" y="14" width="${w.toFixed(1)}" height="34"/>`;if(w>=40)g+=T((x+w/2).toFixed(1),36,`${f(t[k]/net*100,0)}%`,"tw","middle");x+=w;});
  P.forEach(([k,n,c],i)=>{const cx=10+(i%3)*210,cy=74+Math.floor(i/3)*26;g+=`<rect class="${c}" x="${cx}" y="${cy-10}" width="12" height="12" rx="2"/>`+T(cx+18,cy,`${n}: ${f(t[k]/net*100,1)}%`,"tm");});
  $("str").innerHTML=g;$("opis").textContent=`robocizna ${f(t.R/net*100,0)}%, materiały ${f(t.M/net*100,0)}%`;
}
$("dzis").textContent=new Date().toLocaleDateString("pl-PL",{day:"numeric",month:"long",year:"numeric"});
render();licz();''')

# ---------------------------------------------------------------- VAT
CALC3['vat-budowa']=dict(title='VAT na budowę domu: 8% czy 23%, limit 300 m²',
 desc='Policz VAT na usługę budowy domu: 8% do 300 m² powierzchni użytkowej, proporcja 8% i 23% powyżej limitu oraz różnica przy materiałach kupowanych samodzielnie.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>VAT na budowę domu: 8% czy 23%</h1>
<p class="lead">Usługa budowy domu ma zwykle 8% VAT, ale tylko do 300 m² powierzchni użytkowej. Wpisz metraż i wartość robót, a kalkulator rozdzieli VAT na część 8% i 23% oraz pokaże, ile kosztuje kupowanie materiałów samemu.</p>
<section class="calc"><div class="panel"><div class="grid">
<div><label for="rodz">Obiekt</label><select id="rodz"><option value="300">Dom (limit 300 m²)</option><option value="150">Mieszkanie (limit 150 m²)</option></select></div>
<div><label for="pu">Powierzchnia użytkowa (m²)</label><input id="pu" type="number" min="1" step="1" value="180"></div>
<div><label for="net">Wartość usługi netto (zł, przykład)</label><input id="net" type="number" min="0" step="1000" value="400000"></div>
<div><label for="mat">W tym materiały (zł netto)</label><input id="mat" type="number" min="0" step="1000" value="200000"></div>
</div></div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Stawka a powierzchnia i kto kupuje materiały <span id="opis"></span></figcaption><svg id="wyk" viewBox="0 0 640 196" role="img" aria-label="Podział powierzchni na część z VAT 8% i 23% oraz porównanie kosztu brutto przy materiałach od wykonawcy i kupowanych samodzielnie"></svg><p class="note">Górny pasek: powierzchnia użytkowa, pomarańczowa część ma 8%, a część ponad limit 23%. Dolne paski: koszt brutto całej inwestycji w dwóch wariantach zakupu materiałów.</p></figure>
<h2>Kiedy jest 8%</h2>
<ul>
<li><b>Rodzaj pracy:</b> budowa, remont, modernizacja, termomodernizacja, przebudowa albo roboty konserwacyjne.</li>
<li><b>Rodzaj obiektu:</b> budynek mieszkalny stałego zamieszkania (dział 11 PKOB) albo lokal mieszkalny, czyli budownictwo objęte społecznym programem mieszkaniowym.</li>
<li><b>Limit powierzchni:</b> dom jednorodzinny do 300 m² powierzchni użytkowej, mieszkanie do 150 m². Powyżej limitu 8% dotyczy tylko części wartości odpowiadającej limitowi.</li>
<li><b>Muszą być spełnione oba warunki naraz:</b> właściwa praca i właściwy obiekt. Montowane elementy powinny być trwale związane z budynkiem.</li>
</ul>
<h2>Kiedy jest 23%</h2>
<ul>
<li>Część wartości przypadająca na powierzchnię ponad limit.</li>
<li>Materiały kupione samodzielnie w sklepie albo hurtowni. Sprzedaż towaru to nie usługa budowlana, więc ma stawkę podstawową.</li>
<li>Obiekty, które nie są budownictwem mieszkaniowym, oraz prace, które nie są budową ani remontem.</li>
</ul>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Materiał od wykonawcy bywa tańszy o różnicę stawek.</b> Jeśli wykonawca kupuje materiał i rozlicza go w usłudze, materiał ma stawkę usługi. Ten sam materiał kupiony samemu ma 23%. Przy dużych zakupach to realne pieniądze, ale porównuj ceny netto, bo wykonawca dolicza swoje koszty zakupu.</div>
<div class="tip"><b>Liczy się powierzchnia użytkowa, nie zabudowy.</b> Weź ją z projektu. Powierzchnia zabudowy i całkowita to inne liczby.</div>
<div class="tip"><b>Garaż w bryle domu to inna sprawa niż wolnostojący.</b> To, czy dana część jest budownictwem mieszkaniowym, zależy od klasyfikacji obiektu. W wątpliwych sprawach zapytaj Krajową Informację Skarbową albo złóż wniosek o interpretację.</div>
<details><summary>Jak liczymy</summary>
<p>Jeśli powierzchnia użytkowa nie przekracza limitu, VAT to 8% wartości netto. Jeśli przekracza, 8% stosujemy do części wartości równej udziałowi limitu w całej powierzchni (na przykład 300 / 360 = 83,3%), a 23% do reszty.</p>
<p>Wariant „materiały kupuję sam” zakłada te same ceny netto materiałów, ale ze stawką 23%, a usługa wykonawcy bez materiałów ma stawkę jak wyżej.</p>
</details>
<p class="mut">Podstawa: ustawa o podatku od towarów i usług, art. 41 ust. 12–12c (stawka 8%, limity 300 m² i 150 m², proporcja), na podstawie <a href="https://ksiegowosc.infor.pl/podatki/vat/stawki-vat/5351325,Stawka-8-VAT-w-budownictwie-mieszkaniowym.html">omówienia w serwisie INFOR</a>. Sprawdzone 17.10.2026. Kalkulator nie jest poradą podatkową, a wiążące są przepisy i interpretacja dla Twojej sytuacji.</p>
<p>Powiązane: <a href="/kosztorys">kosztorys ofertowy</a>, <a href="/kredyt">kredyt na budowę</a>, <a href="/harmonogram">harmonogram budowy</a>.</p>
</main>''',
 script=_H+r'''function licz(){
  const lim=+$("rodz").value,pu=Math.max(1,v("pu")),net=Math.max(0,v("net")),mat=Math.min(Math.max(0,v("mat")),net);
  const u8=Math.min(1,lim/pu),stawka=u8*0.08+(1-u8)*0.23,vat=net*stawka;
  const usl=net-mat,bruA=net+vat,bruB=usl*(1+stawka)+mat*1.23,roz=bruB-bruA;
  let h=pu<=lim?`Stawka: <b>8% na całość</b><br>`:`Stawka: <b>8% na ${f(u8*100,1)}%</b> wartości, 23% na resztę<br>Średnio: <b>${f(stawka*100,2)}%</b><br>`;
  h+=`VAT: <b>${zl(vat)}</b><br>Brutto: <b>${zl(bruA)}</b><br>`;
  if(mat>0)h+=`Materiały kupione samemu: <span class="warn">+${zl(roz)}</span> brutto`;
  h+=`<p class="mut">Przy założeniu tych samych cen netto materiałów. Kalkulator nie jest poradą podatkową.</p>`;
  $("wynik").innerHTML=h;$("opis").textContent=pu<=lim?"cała powierzchnia w limicie":`${f(pu-lim,0)} m² ponad limit`;
  const N=$("wyk").clientWidth<520,VW=N?380:640,X0=N?8:150,W=N?364:470,s=W/Math.max(pu,lim),Y=N?24:34,BH=N?24:28,xl=X0+lim*s;
  let g=N?T(X0,14,"Powierzchnia użytkowa","t"):T(X0-10,Y+18,"Powierzchnia","t","end");
  const w8=Math.min(pu,lim)*s;
  if(pu<lim)g+=`<rect class="trk" x="${X0}" y="${Y}" width="${W}" height="${BH}" rx="4"/>`;
  g+=`<rect class="odsetki pop" x="${X0}" y="${Y}" width="${w8.toFixed(1)}" height="${BH}" rx="4"/>`;
  if(w8>=90)g+=T((X0+w8/2).toFixed(1),Y+BH/2+4,`${f(Math.min(pu,lim),0)} m² · 8%`,"tw","middle");
  if(pu>lim){const w2=(pu-lim)*s;g+=`<rect class="kapital pop" style="animation-delay:80ms" x="${(X0+w8).toFixed(1)}" y="${Y}" width="${w2.toFixed(1)}" height="${BH}" rx="4"/>`;if(w2>=90)g+=T((X0+w8+w2/2).toFixed(1),Y+BH/2+4,`${f(pu-lim,0)} m² · 23%`,"tw","middle");}
  const la=xl>X0+W-60?"end":"middle";
  g+=`<path class="dim ms" d="M${xl.toFixed(1)} ${Y-(N?4:8)}V${Y+BH+(N?4:8)}"/>`+(N?T(xl.toFixed(1),Y+BH+17,`limit ${lim} m²`,"tm",la):T(xl.toFixed(1),Y-13,`limit ${lim} m²`,"tm",la));
  const mx=Math.max(bruA,bruB,1),k=W/mx,thr=N?110:170;
  [[bruA,"Materiał od wykonawcy","odsetki",N?86:94],[bruB,"Materiał kupiony samemu","kapital",N?140:144]].forEach(([b,n,c,y],i)=>{
    const by=N?y+6:y+4;
    g+=N?T(X0,y,n,"t"):T(X0-10,y+18,n.split(" ").slice(0,2).join(" "),"t","end")+T(X0-10,y+32,n.split(" ").slice(2).join(" "),"tm","end");
    g+=`<rect class="${c} pop" style="animation-delay:${160+i*80}ms" x="${X0}" y="${by}" width="${Math.max(2,b*k).toFixed(1)}" height="${BH}" rx="4"/>`;
    g+=b*k>=thr?T((X0+b*k-8).toFixed(1),by+BH/2+4,zl(b),"tw","end"):T((X0+b*k+8).toFixed(1),by+BH/2+4,zl(b),"t","start");
  });
  $("wyk").setAttribute("viewBox",`0 0 ${VW} ${N?176:196}`);
  $("wyk").innerHTML=g;
}
let rz;addEventListener("resize",()=>{clearTimeout(rz);rz=setTimeout(licz,150);});
document.querySelectorAll("input,select").forEach(e=>e.addEventListener("input",licz));licz();''')
