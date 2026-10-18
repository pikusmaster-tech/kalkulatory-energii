from calc3 import _H
CALC4={}

# ---------------------------------------------------------------- działka
CALC4['dzialka-zabudowa']=dict(title='Wskaźnik zabudowy działki: kalkulator',
 desc='Policz wskaźnik powierzchni zabudowy, intensywność zabudowy i powierzchnię biologicznie czynną działki. Porównaj wynik z planem miejscowym.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Wskaźnik zabudowy działki: czy dom się zmieści</h1>
<p class="lead">Wpisz wymiary działki i budynku. Kalkulator policzy wskaźnik powierzchni zabudowy, intensywność zabudowy i udział powierzchni biologicznie czynnej. Jeśli znasz wartości z miejscowego planu, wpisz je, a kalkulator powie, ile zostało do limitu.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dz">Powierzchnia działki (m²)</label><input id="dz" type="number" value="1000" min="1" step="10"></div>
<div><label for="kond">Kondygnacje nadziemne</label><select id="kond"><option value="1">Parter</option><option value="2" selected>Piętro</option></select></div>
<div><label for="dl">Długość budynku (m)</label><input id="dl" type="number" value="12" min="0" step="0.1"></div>
<div><label for="sz">Szerokość budynku (m)</label><input id="sz" type="number" value="9.5" min="0" step="0.1"></div>
<div><label for="gar">Garaż, wiata, zadaszenie (m²)</label><input id="gar" type="number" value="0" min="0" step="1"></div>
<div><label for="utw">Podjazd, taras i inne utwardzenia (m²)</label><input id="utw" type="number" value="60" min="0" step="1"></div>
<div><label for="mz">Maks. wskaźnik zabudowy z planu (%)</label><input id="mz" type="number" placeholder="np. 30" min="0" step="1"></div>
<div><label for="mb">Min. powierzchnia biologicznie czynna z planu (%)</label><input id="mb" type="number" placeholder="np. 50" min="0" step="1"></div>
</div>
<p class="mut">Pól z planu nie musisz wypełniać. Bez nich kalkulator policzy same wskaźniki.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Co liczy kalkulator</h2>
<table><thead><tr><th>Wskaźnik</th><th>Jak go liczymy</th></tr></thead><tbody>
<tr><td>Powierzchnia zabudowy</td><td>Rzut budynku na teren, czyli długość razy szerokość, plus garaż i zadaszenia.</td></tr>
<tr><td>Wskaźnik powierzchni zabudowy</td><td>Powierzchnia zabudowy podzielona przez działkę, w procentach.</td></tr>
<tr><td>Intensywność zabudowy</td><td>Powierzchnia wszystkich kondygnacji nadziemnych podzielona przez działkę, w procentach.</td></tr>
<tr><td>Powierzchnia biologicznie czynna</td><td>Działka pomniejszona o zabudowę i wszystkie utwardzenia, w procentach.</td></tr>
</tbody></table>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Plan wygrywa z kalkulatorem.</b> Wskaźniki liczy się wg definicji zapisanej w miejscowym planie albo w decyzji o warunkach zabudowy. Ten kalkulator daje wynik orientacyjny.</div>
<div class="tip"><b>Podjazd też się liczy.</b> Kostka i podjazd nie są budynkiem, ale zabierają powierzchnię biologicznie czynną. Płyty ażurowe plan czasem liczy częściowo, sprawdź to w zapisach.</div>
<div class="tip"><b>Dwa piętra to nie większa zabudowa.</b> Ten sam rzut na dwóch kondygnacjach podnosi intensywność, ale nie wskaźnik zabudowy. Plan zwykle ogranicza oba.</div>
<details><summary>Jak liczymy</summary>
<p>Kalkulator liczy rzut ścian zewnętrznych bez okapu. Jeśli plan wlicza okap, prawdziwy wskaźnik zabudowy jest wyższy, a kalkulator go zaniży. Przy okapie 0,6 m i budynku 12 × 9,5 m różnica to około 27 m², czyli 2,7 punktu procentowego na działce 1000 m².</p>
<p>Powierzchnia biologicznie czynna jest liczona jako działka minus zabudowa minus utwardzenia. Plan może zaliczać część utwardzeń do tej powierzchni, np. kratki trawnikowe, wtedy wynik będzie wyższy niż tutaj.</p>
</details>
<p>Powiązane: <a href="/kostka">kostka i płytki</a>, <a href="/ogrodzenie">ogrodzenie</a>, <a href="/dach">dach</a>.</p>
</main>''',
 script=_H+r'''const num=id=>{const x=parseFloat($(id).value);return isFinite(x)?x:NaN;};
const n0=id=>num(id)||0;
function licz(){
  const dz=n0("dz"),L=n0("dl"),W=n0("sz"),k=parseFloat($("kond").value)||1,gar=n0("gar"),utw=n0("utw"),mz=num("mz"),mb=num("mb");
  if(dz<=0||L<=0||W<=0){$("wynik").innerHTML="Wpisz wymiary działki i budynku.";return;}
  const rzut=L*W, zab=rzut+gar, cal=rzut*k+gar, uts=zab+utw, pbc=Math.max(0,dz-uts);
  const wz=zab/dz*100, wi=cal/dz*100, wb=pbc/dz*100;
  let h=`Wskaźnik zabudowy <b>${f(wz,1)} %</b><br>Intensywność zabudowy <b>${f(wi,1)} %</b><br>Biologicznie czynna <b>${f(wb,1)} %</b>`;
  h+=`<div class="mut">Zabudowa ${f(zab,0)} m², powierzchnia całkowita ${f(cal,0)} m², zabudowa razem z utwardzeniami ${f(uts,0)} m².</div>`;
  if(!isNaN(mz)){const lim=mz/100*dz;
    h+=wz<=mz?`<br><span class="ok">Mieści się w planie.</span> Zostaje ${f(lim-zab,0)} m² do limitu.`:`<br><span class="warn">Przekracza plan.</span> Trzeba zmniejszyć zabudowę o ${f(zab-lim,0)} m².`;}
  if(!isNaN(mb)){const need=mb/100*dz;
    h+=wb>=mb?`<br><span class="ok">Biologicznie czynna spełnia plan.</span>`:`<br><span class="warn">Brakuje ${f(need-pbc,0)} m² powierzchni biologicznie czynnej.</span>`;}
  $("wynik").innerHTML=h;
}
document.querySelector("section.calc").addEventListener("input",licz);
licz();'''
)

# ---------------------------------------------------------------- moc grzewcza
CALC4['moc-grzewcza']=dict(title='Moc grzewcza domu: straty ciepła, kalkulator',
 desc='Oblicz straty ciepła domu przez ściany, dach, podłogę, okna i wentylację. Wynik w kW pomaga dobrać pompę ciepła lub kocioł.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Moc grzewcza domu: ile ciepła ucieka</h1>
<p class="lead">Wpisz wymiary, współczynniki U przegród i temperatury. Kalkulator policzy straty ciepła przez każdą część domu oraz na wentylację. Suma to moc, którą musi dać ogrzewanie w najzimniejszy dzień.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość budynku (m)</label><input id="dl" type="number" value="12" min="0" step="0.1"></div>
<div><label for="sz">Szerokość budynku (m)</label><input id="sz" type="number" value="9.5" min="0" step="0.1"></div>
<div><label for="kond">Kondygnacje ogrzewane</label><select id="kond"><option value="1">Parter</option><option value="2" selected>Dwie kondygnacje</option></select></div>
<div><label for="h">Wysokość kondygnacji (m)</label><input id="h" type="number" value="3" min="2" step="0.1"></div>
<div><label for="usc">U ścian zewnętrznych (W/m²K)</label><input id="usc" type="number" value="0.20" min="0" step="0.01"></div>
<div><label for="udach">U dachu lub stropu (W/m²K)</label><input id="udach" type="number" value="0.15" min="0" step="0.01"></div>
<div><label for="up">U podłogi na gruncie (W/m²K)</label><input id="up" type="number" value="0.30" min="0" step="0.01"></div>
<div><label for="pok">Powierzchnia okien (m²)</label><input id="pok" type="number" value="24" min="0" step="0.5"></div>
<div><label for="uok">U okien (W/m²K)</label><input id="uok" type="number" value="0.9" min="0" step="0.1"></div>
<div><label for="ndr">Drzwi zewnętrzne (szt.)</label><input id="ndr" type="number" value="1" min="0" step="1"></div>
<div><label for="udr">U drzwi (W/m²K)</label><input id="udr" type="number" value="1.3" min="0" step="0.1"></div>
<div><label for="went">Wentylacja</label><select id="went"><option value="gr" selected>Grawitacyjna (0,5 wymiany/h)</option><option value="rek">Rekuperacja, odzysk 80 %</option></select></div>
<div><label for="ti">Temperatura w domu (°C)</label><input id="ti" type="number" value="20" step="1"></div>
<div><label for="te">Najzimniejsza temperatura w Twojej okolicy (°C)</label><input id="te" type="number" value="-20" step="1"></div>
</div>
<p class="mut">Wartości U to przykład zgodny z WT 2021. Wpisz U z kart produktów albo z kalkulatora U, jeśli liczyłeś swoją ścianę.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<div id="rozbicie"></div>
<h2>Jak liczymy</h2>
<p>Straty przez przegrody to suma U razy powierzchnia razy różnica temperatur, dla każdej przegrody osobno. Straty na wentylację to 0,34 razy wymiana powietrza razy kubatura razy różnica temperatur. Wymiana 0,5 na godzinę to typowa wartość dla wentylacji grawitacyjnej. Rekuperacja z odzyskiem 80 % ogranicza tę stratę do około jednej piątej.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Najzimniejszy dzień, nie średnia.</b> Moc liczy się dla temperatury obliczeniowej, a nie dla zimy jako całości. Średnia roczna daje zaniżoną moc.</div>
<div class="tip"><b>Wentylacja potrafi być większa niż ściany.</b> W domu bez rekuperacji wymiana powietrza zwykle odpowiada za dużą część strat. Sam dobry dach tego nie naprawi.</div>
<div class="tip"><b>Pompa z zapasem, ale nie na oko.</b> Moc z kalkulatora to punkt wyjścia. Dobór pompy robi się wg karty producenta przy tej temperaturze, a nie wg metrażu.</div>
<details><summary>Dlaczego podłoga jest zawyżona</summary>
<p>Podłoga na gruncie oddaje ciepło do ziemi wolniej niż powietrzu, a tutaj liczymy ją z pełną różnicą temperatur. Wynik jest więc po stronie bezpiecznej. Dokładny wynik wymaga normy dla podłóg na gruncie i zależy od obwodu płyty.</p>
</details>
<p>Powiązane: <a href="/wspolczynnik-u">współczynnik U ściany i dachu</a>, <a href="/pompa-ciepla">pompa ciepła</a>, <a href="/fotowoltaika">fotowoltaika</a>.</p>
</main>''',
 script=_H+r'''const num=id=>{const x=parseFloat($(id).value);return isFinite(x)?x:NaN;};
const n0=id=>num(id)||0;
function licz(){
  const L=n0("dl"),W=n0("sz"),k=parseFloat($("kond").value)||1,hk=n0("h");
  const dT=n0("ti")-n0("te");
  if(L<=0||W<=0||hk<=0||dT<=0){$("wynik").innerHTML="Sprawdź wymiary i temperatury. Różnica temperatur musi być dodatnia.";$("rozbicie").innerHTML="";return;}
  const H=hk*k, pok=n0("pok"), ndr=n0("ndr"), adr=ndr*2;
  const asc=Math.max(0,2*(L+W)*H-pok-adr);
  const rows=[
    ["Ściany zewnętrzne",asc,n0("usc")],
    ["Dach lub strop nad ostatnią kondygnacją",L*W,n0("udach")],
    ["Podłoga na gruncie (zawyżona, patrz niżej)",L*W,n0("up")],
    ["Okna",pok,n0("uok")],
    ["Drzwi zewnętrzne",adr,n0("udr")]
  ].map(([n,a,u])=>({n,a,u,q:a*u*dT}));
  const n=$("went").value==="rek"?0.5*(1-0.8):0.5, vol=L*W*H;
  rows.push({n:"Wentylacja",a:vol,u:null,q:0.34*n*vol*dT,vol:true});
  const sum=rows.reduce((s,r)=>s+r.q,0), kw=sum/1000, pm=sum/(L*W*k);
  const top=rows.reduce((b,r)=>r.q>b.q?r:b,rows[0]);
  $("wynik").innerHTML=`Moc grzewcza <b>${f(kw,1)} kW</b><br>Na m² ogrzewanej powierzchni <b>${f(pm,0)} W/m²</b><br>Największa strata: ${top.n.toLowerCase()}, ${f(100*top.q/sum,0)} % całości<div class="mut">Różnica temperatur ${f(dT,0)} K. Powierzchnia ogrzewana ${f(L*W*k,0)} m². Wynik orientacyjny, dobór pompy wg projektu i karty producenta.</div>`;
  $("rozbicie").innerHTML=`<h2>Rozbicie strat</h2><div class="tablewrap"><table><thead><tr><th>Element</th><th class="num">Powierzchnia lub kubatura</th><th class="num">U</th><th class="num">Strata, W</th><th class="num">Udział</th></tr></thead><tbody>`+
    rows.map(r=>`<tr><td>${r.n}</td><td class="num">${f(r.a,r.vol?0:1)}</td><td class="num">${r.u===null?"0,34 · n":f(r.u,2)}</td><td class="num">${f(r.q,0)}</td><td class="num">${f(100*r.q/sum,0)} %</td></tr>`).join("")+
    `</tbody><tfoot><tr><td><b>Razem</b></td><td></td><td></td><td class="num"><b>${f(sum,0)}</b></td><td class="num">100 %</td></tr></tfoot></table></div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
licz();'''
)

# ---------------------------------------------------------------- ogrzewanie podłogowe
CALC4['ogrzewanie-podlogowe']=dict(title='Ogrzewanie podłogowe: ile rur i pętli',
 desc='Policz długość rury PEX, liczbę pętli, obiegi rozdzielacza i rolki dla ogrzewania podłogowego. Wynik zależy od rozstawu rur i powierzchni.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Ogrzewanie podłogowe: ile rury i ile pętli</h1>
<p class="lead">Podaj powierzchnię do ogrzania i rozstaw rur. Kalkulator policzy, ile metrów rury kupić, na ile pętli ją podzielić i ile obiegów powinien mieć rozdzielacz.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="pow">Powierzchnia do ogrzania (m²)</label><input id="pow" type="number" value="80" min="0" step="1"></div>
<div><label for="odl">Pod meblami i zabudową, bez rur (m²)</label><input id="odl" type="number" value="8" min="0" step="0.5"></div>
<div><label for="roz">Rozstaw rur (cm)</label><select id="roz"><option value="10">10 cm, więcej mocy</option><option value="15" selected>15 cm</option><option value="20">20 cm, mniej rury</option></select></div>
<div><label for="maxp">Maks. długość jednej pętli (m)</label><input id="maxp" type="number" value="100" min="10" step="5"></div>
<div><label for="rol">Długość rolki rury (m)</label><input id="rol" type="number" value="200" min="10" step="10"></div>
</div>
<p class="mut">Maksymalną długość pętli sprawdź w karcie systemu. Dla rury 16 × 2 mm to zwykle około 100 m, ale producenci podają różne wartości.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Rury układa się tam, gdzie ma być ciepło. Pod szafkami i wyspą kuchenną rury nie są potrzebne, więc odejmujemy tę powierzchnię. Długość rury to powierzchnia netto podzielona przez rozstaw, plus 10 % na zagięcia i dojazdy do rozdzielacza. Pętle dzielimy tak, żeby żadna nie przekraczała maksymalnej długości.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Mniejszy rozstaw to więcej rury.</b> Przy 10 cm zamiast 15 cm rury jest o jedną trzecią więcej, ale więcej ciepła idzie do podłogi. Łazienka zwykle bierze gęstszy rozstaw.</div>
<div class="tip"><b>Pętle powinny być podobnej długości.</b> Nierówne pętle dają nierówne temperatury w pomieszczeniach. Rozdzielacz i pętle dobiera się razem, nie osobno.</div>
<div class="tip"><b>Rozdzielacz ma zapas.</b> Liczba obiegów z kalkulatora to minimum. Zwykle bierze się najbliższy większy rozdzielacz, bo dodatkowy obieg przydaje się przy późniejszej zmianie układu.</div>
<details><summary>Ile rury na m²</summary>
<p>Przy rozstawie 15 cm wychodzi około 6,7 m rury na każdy metr kwadratowy, a z zapasem 10 % około 7,3 m. Przy 10 cm te wartości rosną do około 10 m na m². To miara do porównania ofert, bo producenci liczą to różnie.</p>
</details>
<p>Powiązane: <a href="/wylewka">wylewka</a>, <a href="/moc-grzewcza">moc grzewcza domu</a>, <a href="/pompa-ciepla">pompa ciepła</a>.</p>
</main>''',
 script=_H+r'''const num=id=>{const x=parseFloat($(id).value);return isFinite(x)?x:NaN;};
const n0=id=>num(id)||0;
function licz(){
  const area=n0("pow"), odl=n0("odl"), roz=parseFloat($("roz").value)/100, maxp=n0("maxp"), rol=n0("rol");
  const net=Math.max(0,area-odl);
  if(net<=0||maxp<=0||roz<=0){$("wynik").innerHTML="Podaj powierzchnię większą niż to, co odejmujesz.";return;}
  const len=net/roz*1.1;
  const pet=Math.ceil(len/maxp), sred=len/pet, rolek=rol>0?Math.ceil(len/rol):0;
  const obiegi=pet<=12?`${pet} ${pl(pet,"obieg","obiegi","obiegów")}`:`${pet} obiegów, czyli więcej niż jeden rozdzielacz`;
  $("wynik").innerHTML=`Rury łącznie <b>${f(len,0)} m</b><br>Pętle <b>${pet}</b>, średnio ${f(sred,0)} m każda<br>Rozdzielacz: ${obiegi}<br>Rolek po ${f(rol,0)} m: <b>${rolek}</b><div class="mut">Na m² ogrzewanej powierzchni ${f(len/net,1)} m rury. Zapas 10 % na zagięcia i dojazdy. Maksymalna długość pętli ${f(maxp,0)} m, sprawdź w karcie systemu.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
licz();'''
)

# ---------------------------------------------------------------- taras
CALC4['taras']=dict(title='Taras: ile desek, legarów i stóp',
 desc='Policz deski tarasowe, legary i stopy dla tarasu drewnianego albo kompozytowego. Wynik z zapasem na docinki i odpad.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Taras: ile desek, legarów i stóp kupić</h1>
<p class="lead">Podaj wymiary tarasu i deski, którą wybierasz. Kalkulator policzy deski, legary i podpory z zapasem na docinki. Wymiary deski i rozstaw legarów zwykle są w karcie produktu.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość tarasu (m)</label><input id="dl" type="number" value="4" min="0" step="0.1"></div>
<div><label for="sz">Szerokość tarasu (m)</label><input id="sz" type="number" value="3" min="0" step="0.1"></div>
<div><label for="kier">Deski biegną wzdłuż</label><select id="kier"><option value="dl" selected>długości tarasu</option><option value="sz">szerokości tarasu</option></select></div>
<div><label for="szd">Szerokość deski (mm)</label><select id="szd"><option value="90">90</option><option value="120">120</option><option value="140" selected>140</option><option value="145">145</option></select></div>
<div><label for="dld">Długość deski (m)</label><select id="dld"><option value="2.4">2,4</option><option value="3">3,0</option><option value="3.6">3,6</option><option value="4" selected>4,0</option><option value="4.8">4,8</option></select></div>
<div><label for="szc">Szczelina między deskami (mm)</label><input id="szc" type="number" value="5" min="0" step="1"></div>
<div><label for="roz">Rozstaw legarów (cm)</label><select id="roz"><option value="40" selected>40</option><option value="50">50</option><option value="60">60</option></select></div>
<div><label for="stop">Rozstaw stóp pod legarami (m)</label><input id="stop" type="number" value="1.5" min="0.5" step="0.1"></div>
</div>
<p class="mut">Szczelinę i rozstaw legarów podaje producent. Rozstaw legarów zależy od deski i producenta. Kompozyt zwykle wymaga 40 cm, a drewno w grubej desce nawet 60 cm.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Deski układamy w poprzek kierunku legarów. Liczba desek to szerokość tarasu podzielona przez szerokość deski plus szczelinę. Do tego dodajemy 8 % na docinki i odpad. Legary biegną prostopadle do desek, a ich liczba zależy od rozstawu. Stopy stoją w siatce, co rozstaw stóp w obu kierunkach.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Kierunek desek zmienia ilość docinków.</b> Deski układane wzdłuż dłuższego boku dają mniej łączeń i mniej odpadu. Przy krótkim tarasie różnica jest mała, przy długim spora.</div>
<div class="tip"><b>Legary na stopach, nie na gruncie.</b> Legar leżący bezpośrednio na ziemi szybko chłonie wilgoć. Stopy regulowane pozwalają wypoziomować taras na nierównym terenie.</div>
<div class="tip"><b>Zapas na docinki to nie błąd.</b> Każda deska ma przycięte końce. Kupując tylko tyle, ile wyszło, kończysz z jedną deską za mało.</div>
<details><summary>Ile wychodzi odpadu</summary>
<p>Odpad zależy od tego, ile docinków wychodzi z każdego rzędu. Im krótsza deska względem długości tarasu, tym więcej łączeń i tym większy odpad. Kalkulator dolicza 8 %, co zwykle wystarcza przy desce dłuższej niż połowa tarasu. Przy krótszych deskach warto dać więcej.</p>
</details>
<p>Powiązane: <a href="/kostka">kostka i płytki</a>, <a href="/ogrodzenie">ogrodzenie</a>, <a href="/wylewka">wylewka</a>.</p>
</main>''',
 script=_H+r'''const num=id=>{const x=parseFloat($(id).value);return isFinite(x)?x:NaN;};
const n0=id=>num(id)||0;
function licz(){
  const L=n0("dl"),W=n0("sz"),dl=parseFloat($("dld").value),szd=n0("szd")/1000,szc=n0("szc")/1000;
  const rozst=parseFloat($("roz").value)/100, stop=n0("stop");
  if(L<=0||W<=0||stop<=0){$("wynik").innerHTML="Podaj wymiary tarasu i rozstaw stóp.";return;}
  const A=$("kier").value==="dl"?L:W, B=$("kier").value==="dl"?W:L;
  const nd=Math.ceil(B/(szd+szc));
  const mbDeski=nd*A*1.08, sztDeski=Math.ceil(mbDeski/dl);
  const nLeg=Math.floor(A/rozst)+1, mbLeg=nLeg*B*1.05, sztLeg=nLeg*Math.ceil(B/4);
  const nA=Math.floor(A/stop)+1, nB=Math.floor(B/stop)+1, stopy=nA*nB;
  $("wynik").innerHTML=`Deski <b>${sztDeski} szt.</b> po ${f(dl,1)} m, razem ${f(mbDeski,1)} mb<br>Legary <b>${nLeg}</b> rzędów, ${f(mbLeg,1)} mb, sztuk po 4 m: ${sztLeg}<br>Stopy pod legary: <b>${stopy} szt.</b><div class="mut">Deski liczone z 8 % zapasu, legary z 5 %. Liczba stóp to siatka ${nA} × ${nB} co ${f(stop,1)} m. Przed zakupem sprawdź nośność legarów w karcie producenta.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
licz();'''
)

# ---------------------------------------------------------------- przyłącza
CALC4['przylacza']=dict(title='Przyłącza do domu: koszt z ofert',
 desc='Wybierz typ każdego przyłącza, wpisz długość i stawkę z oferty. Kalkulator policzy sumę i koszt każdych 10 metrów więcej.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Przyłącza do domu: porównaj oferty</h1>
<p class="lead">Ceny przyłączy zależą od odległości od sieci, od typu przyłącza i od firmy. Wybierz typ, wpisz długość i stawkę za metr z oferty. Kalkulator policzy sumę i pokaże, ile dołoży każde 10 metrów więcej.</p>
<section class="calc"><div class="panel">
<div class="rowh p pl"><span>Przyłącze i typ</span><span>Długość (m)</span><span>zł za m</span><span>Opłata (zł)</span><span></span></div>
<div class="rows" id="media"></div>
<p class="mut">Pole zostaw puste, jeśli media nie są potrzebne albo wykonasz je sam. Opłaty za warunki przyłączenia wpisz osobno, w kolumnie opłat.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Co dokładnie porównujesz</h2>
<table><thead><tr><th>Pozycja w ofercie</th><th>Dlaczego ma znaczenie</th></tr></thead><tbody>
<tr><td>Typ i średnica</td><td>Trójfazowe prąd, grubsza rura albo przepompownia zmieniają cenę. Porównuj oferty na tym samym typie.</td></tr>
<tr><td>Długość przyłącza</td><td>Różnica między sąsiadującymi ofertami zwykle wynika z długości, a nie ze stawki.</td></tr>
<tr><td>Odtworzenie nawierzchni</td><td>Kostka, trawnik albo asfalt po wykopie często są poza stawką za metr.</td></tr>
<tr><td>Opłaty za warunki i odbiór</td><td>Dokumenty i odbiór zakładu lub wodociągów zwykle płaci się osobno.</td></tr>
<tr><td>Wspólny wykop</td><td>Kilka mediów w jednym wykopie może obniżyć koszt, jeśli wykonuje to jedna firma.</td></tr>
</tbody></table>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Oferta bez opłat nie jest pełna.</b> Warunki przyłączenia wydaje dostawca mediów i ich koszt bywa wyższy niż samo wykonanie. Zapytaj, co jest w cenie.</div>
<div class="tip"><b>Najtańszy metr nie daje najtańszego przyłącza.</b> Firma z niższą stawką może liczyć dłuższe przyłącze albo doliczać odtworzenie nawierzchni.</div>
<div class="tip"><b>Szambo to nie przyłącze.</b> Jeśli kanalizacji nie ma w ulicy, zbiornik bezodpływowy albo oczyszczalnia to osobna inwestycja i osobne koszty wywozu.</div>
<details><summary>Jak liczymy</summary>
<p>Dla każdego medium koszt to długość razy stawka za metr plus jednorazowa opłata. Suma to wszystkie media razem. Koszt każdych kolejnych 10 metrów to 10 razy suma stawek za metr, bez opłat jednorazowych i bez szamba, bo przy zbiorniku długość nie jest długością rury. Kalkulator nie zna cen na Twojej działce, więc liczy tylko z tego, co wpiszesz.</p>
</details>
<p>Powiązane: <a href="/konfigurator-domu">konfigurator domu z kosztem elementów</a>, <a href="/ceny-budowlane">ceny materiałów i robocizny</a>.</p>
</main>''',
 script=_H+r'''const MEDIA=[
 {n:"Prąd",o:[["jednofazowe 230 V","Dla mniejszych odbiorów. Moc przyłącza ustala projekt instalacji."],["trójfazowe 400 V","Dla większych odbiorów. Zapytaj dostawcę, czy przy Twojej mocy wystarczy jednofazowe."]]},
 {n:"Woda",o:[["rura PE 32 mm","Najczęściej spotykana w domach jednorodzinnych."],["rura PE 40 mm","Dla dłuższej trasy albo większego poboru wody."]]},
 {n:"Kanalizacja",o:[["grawitacyjna","Spadek wystarcza do kanału, bez przepompowni."],["ciśnieniowa z przepompownią","Gdy dom leży niżej niż kanał. Oferta powinna wyceniać przepompownię osobno."],["szambo zamiast kanalizacji","To zbiornik, nie przyłącze. Długość to odległość od domu do zbiornika, a w cenie są zbiornik i wywóz."]]},
 {n:"Gaz",o:[["sieciowy, niskie ciśnienie","Gaz z sieci niskiego ciśnienia, dla domu jednorodzinnego."],["sieciowy, średnie ciśnienie","Gdy sieć jest średniego ciśnienia. Oferta powinna wyceniać stację redukcyjną, jeśli jest potrzebna."],["zbiornik LPG","Zbiornik nie jest przyłączem. Długość to instalacja od zbiornika do domu."]]}
];
const num=x=>{const y=parseFloat(x);return isFinite(y)?y:NaN;};
$("media").innerHTML=MEDIA.map((m,i)=>`<div class="row p pl" data-i="${i}">
<div class="cell pn"><b>${m.n}</b>
<select data-k="t" aria-label="Typ: ${m.n}">${m.o.map(([t],j)=>`<option value="${j}">${t}</option>`).join("")}</select>
<small class="hint"></small></div>
<label class="cell"><span>Długość (m)</span><input type="number" min="0" step="1" data-k="d" aria-label="Długość: ${m.n} w metrach" placeholder="0"></label>
<label class="cell"><span>zł za m</span><input type="number" min="0" step="1" data-k="s" aria-label="Stawka za metr: ${m.n}" placeholder="0"></label>
<label class="cell"><span>Opłata (zł)</span><input type="number" min="0" step="1" data-k="o" aria-label="Opłata: ${m.n}" placeholder="0"></label>
<span class="ph"></span></div>`).join("");
function licz(){
  let suma=0,perM=0,any=false,typy=[];
  document.querySelectorAll("#media .row").forEach(r=>{
    const m=MEDIA[+r.dataset.i], sel=r.querySelector('[data-k="t"]'), t=m.o[+sel.value];
    r.querySelector(".hint").textContent=t[1];
    const d=num(r.querySelector('[data-k="d"]').value), s=num(r.querySelector('[data-k="s"]').value), o=num(r.querySelector('[data-k="o"]').value);
    if(!isFinite(d)&&!isFinite(s)&&!isFinite(o))return;
    any=true;
    const dd=isFinite(d)?d:0, ss=isFinite(s)?s:0, oo=isFinite(o)?o:0;
    suma+=dd*ss+oo;
    if(!t[0].startsWith("szambo"))perM+=ss;
    typy.push(`${m.n.toLowerCase()}: ${t[0]}`);
  });
  if(!any){$("wynik").innerHTML="Wybierz typ, wpisz długość i stawkę z przynajmniej jednej oferty.";return;}
  $("wynik").innerHTML=`Razem media <b>${f(suma,0)} zł</b><br>Każde 10 m więcej <b>${f(10*perM,0)} zł</b><div class="mut">Wybrane typy: ${typy.join(", ")}. Suma zawiera długość razy stawkę i opłaty jednorazowe. Kwoty dotyczą tylko wpisanych pozycji i nie obejmują odtworzenia nawierzchni, jeśli oferta jej nie zawiera.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
licz();'''
)
