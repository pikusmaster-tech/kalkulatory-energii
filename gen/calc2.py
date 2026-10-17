CALC={}
CALC['schody']=dict(title='Kalkulator schodów: liczba stopni i wysokość',
 desc='Policz liczbę stopni, wysokość i szerokość stopnia oraz długość biegu. Sprawdź regułę 2h + s i zobacz przekrój schodów.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Schody: ile stopni i jaka wysokość stopnia</h1>
<p class="lead">Wpisz wysokość między gotowymi posadzkami i wymiary stopnia. Kalkulator policzy liczbę stopni, długość biegu i sprawdzi, czy schody są wygodne.</p>
<section class="calc"><div class="panel"><div class="grid">
<div><label for="H">Wysokość między posadzkami (cm)</label><input id="H" type="number" value="280" step="1"></div>
<div><label for="h">Wysokość stopnia, plan (cm)</label><input id="h" type="number" value="17" step="0.5"></div>
<div><label for="s">Szerokość stopnia (cm)</label><input id="s" type="number" value="29" step="0.5"></div>
</div></div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Przekrój biegu <span id="opis"></span></figcaption><svg id="bieg" viewBox="0 0 640 300" role="img" aria-label="Przekrój biegu schodów z zaznaczonymi stopniami"></svg><p class="note">Schemat prostego biegu jednobiegowego. Spoczniki i schody kręcone liczy się inaczej.</p></figure>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Mierz od gotowej posadzki.</b> Wysokość liczy się od wykończonej podłogi na dole do wykończonej na górze. Jeśli pominiesz wylewkę i płytki, ostatni stopień wyjdzie inny niż reszta.</div>
<div class="tip"><b>Stopnie muszą być równe.</b> Różnica kilku milimetrów między stopniami jest czuć w nodze. Liczba stopni i ich wysokość zawsze idą razem.</div>
<div class="tip"><b>Reguła 2h + s.</b> Dwie wysokości i szerokość stopnia to w praktyce około 60–65 cm. Poza tym zakresem schody są mniej wygodne.</div>
<div class="tip"><b>Dla żelbetu wymiary podaje projekt.</b> Kalkulator służy do planu i wstępnej rozmowy z wykonawcą, a nie do zamówienia elementów.</div>
<details><summary>Jak liczymy</summary>
<p>Liczba stopni to wysokość między posadzkami podzielona przez wysokość stopnia, zaokrąglona do liczby całkowitej. Po zaokrągleniu wysokość jednego stopnia to wysokość między posadzkami podzielona przez tę liczbę.</p>
<p>Biegu w poziomie jest o jeden stopień mniej niż stopni, bo górny stopień to już posadzka piętra. Długość biegu to więc (liczba stopni minus 1) razy szerokość stopnia. Nachylenie to arcus tangens z wysokości przez szerokość.</p>
</details>
</main>''',
 script='''const v=id=>parseFloat(document.getElementById(id).value)||0;
const f=(n,d=1)=>n.toLocaleString("pl-PL",{maximumFractionDigits:d});
const T=(x,y,t,c="t",a="start")=>`<text class="${c}" x="${x}" y="${y}" text-anchor="${a}">${t}</text>`;
function licz(){
  const H=v("H"), h0=Math.max(10,v("h")), s=Math.max(10,v("s"));
  const n=Math.max(2,Math.round(H/h0)), h=H/n, bl=2*h+s, bieg=(n-1)*s, kat=Math.atan(h/s)*180/Math.PI;
  const ok=bl>=60&&bl<=65;
  document.getElementById("wynik").innerHTML=
    `Liczba stopni: <b>${n}</b> (wysokość ${f(h,1)} cm)<br>`+
    `Długość biegu: <b>${f(bieg/100,2)} m</b><br>`+
    `Nachylenie: <b>${f(kat,0)}°</b><br>`+
    `Reguła 2h + s: <b>${f(bl,0)} cm</b> ${ok?"(w normie)":"(poza zakresem 60–65 cm)"}`+
    `<p class="mut">Liczone od gotowej posadzki na dole do gotowej posadzki na górze.</p>`;
  rysuj(n,h,s,H);
}
function rysuj(n,h,s,H){
  const W=640, base=270, x0=70, run=(n-1)*s, tot=n*h;
  const k=Math.min(470/Math.max(run,1),190/Math.max(tot,1));
  let d=`M${x0} ${base}`;
  for(let i=0;i<n;i++){
    d+=` V${(base-(i+1)*h*k).toFixed(1)}`;
    if(i<n-1) d+=` H${(x0+(i+1)*s*k).toFixed(1)}`;
  }
  const xe=x0+(n-1)*s*k, ye=base-tot*k;
  let g=`<rect class="grunt" x="0" y="${base}" width="${W}" height="${300-base}"/>`;
  g+=`<path class="beton" d="${d} V${base} Z"/>`;
  g+=`<path class="schod draw" pathLength="1" d="${d}"/>`;
  g+=`<path class="dim" d="M${xe.toFixed(1)} ${ye.toFixed(1)}H${(xe+60).toFixed(1)}"/>`;
  g+=`<path class="dim" d="M${x0-16} ${base}V${ye.toFixed(1)}M${x0-22} ${base}h12M${x0-22} ${ye.toFixed(1)}h12"/>`;
  g+=T(x0-26,(base+ye)/2+4,`${f(H,0)} cm`,"t","end");
  g+=T(x0,24,`Stopień: wysokość ${f(h,1)} cm, szerokość ${f(s,0)} cm`,"tm");
  document.getElementById("bieg").innerHTML=g;
  document.getElementById("opis").textContent=`${n} stopni, bieg ${f((n-1)*s/100,2)} m`;
}
document.querySelectorAll("input").forEach(e=>e.addEventListener("input",licz));licz();''')

CALC['wykop']=dict(title='Ile ziemi z wykopu: objętość i kursy wywozu',
 desc='Policz objętość wykopu, ilość ziemi po spulchnieniu i liczbę kursów samochodu. Wykres pokazuje, dlaczego ziemi wychodzi więcej, niż wykopano.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Ile ziemi wywieźć z wykopu</h1>
<p class="lead">Wpisz wymiary wykopu pod fundamenty. Zobaczysz objętość w stanie naturalnym, po spulchnieniu i liczbę kursów samochodu.</p>
<section class="calc"><div class="panel"><div class="grid">
<div><label for="dl">Długość wykopu (m)</label><input id="dl" type="number" value="14" step="0.5"></div>
<div><label for="szer">Szerokość wykopu (m)</label><input id="szer" type="number" value="10" step="0.5"></div>
<div><label for="gl">Głębokość wykopu (m)</label><input id="gl" type="number" value="1.6" step="0.1"></div>
<div><label for="nach">Nachylenie ścian (°, 0 = pionowe)</label><input id="nach" type="number" value="0" step="5"></div>
<div><label for="spul">Spulchnienie gruntu (współczynnik, przykład)</label><input id="spul" type="number" value="1.25" step="0.05"></div>
<div><label for="zasyp">Ziemia wracająca na zasypkę (m³)</label><input id="zasyp" type="number" value="0" step="1"></div>
<div><label for="kurs">Pojemność samochodu (m³)</label><input id="kurs" type="number" value="10" step="1"></div>
</div></div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Przekrój i objętości <span>w stanie naturalnym i po wykopie</span></figcaption><svg id="wykop" viewBox="0 0 640 260" role="img" aria-label="Przekrój wykopu z ławą oraz słupki objętości przed i po wykopie"></svg><p class="note">Schemat poglądowy. Współczynnik spulchnienia zależy od rodzaju gruntu, wpisz wartość z badania gruntu albo od przewoźnika.</p></figure>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Ziemia rośnie.</b> Grunt po wykopie zajmuje więcej miejsca niż w ziemi. Samochód, który wydaje się wystarczający, w praktyce potrzebuje więcej kursów.</div>
<div class="tip"><b>Część ziemi zostaje na miejscu.</b> Wokół ścian fundamentowych ziemia wraca do wykopu jako zasypka. Nie zamawiaj wywozu na całą objętość, jeśli część wróci.</div>
<div class="tip"><b>Woda zmienia plan.</b> Przy wysokim poziomie wód gruntowych wykop trzeba zabezpieczyć i odwodnić, a to osobny koszt. Sprawdź to w badaniu gruntu przed wyceną.</div>
<div class="tip"><b>Ściany wykopu muszą być stabilne.</b> Pionowe ściany wymagają obudowy albo odpowiedniego nachylenia skarpy. Decyduje o tym rodzaj gruntu i projekt.</div>
<details><summary>Jak liczymy</summary>
<p>Objętość wykopu liczymy jak ściętą piramidę: wysokość razy suma pola dna, pola góry i pierwiastka z ich iloczynu, podzielona przez trzy. Przy nachyleniu góra jest szersza o podwójne przesunięcie ścian na każdym boku.</p>
<p>Ziemia po wykopie to objętość razy współczynnik spulchnienia. Do wywozu idzie to, co zostaje po odjęciu zasypki. Liczba kursów to ilość do wywozu podzielona przez pojemność samochodu, zaokrąglona w górę.</p>
<p>Wykop pod ławy i płytę zwykle jest płytszy niż wykop pod piwnicę. Zmierz głębokość od poziomu terenu do dna, w miejscu najgłębszym.</p>
</details>
</main>''',
 script='''const v=id=>parseFloat(document.getElementById(id).value)||0;
const f=(n,d=1)=>n.toLocaleString("pl-PL",{maximumFractionDigits:d});
const T=(x,y,t,c="t",a="start")=>`<text class="${c}" x="${x}" y="${y}" text-anchor="${a}">${t}</text>`;
function licz(){
  const L=v("dl"), B=v("szer"), D=v("gl"), t=Math.tan(v("nach")*Math.PI/180);
  const A1=L*B, A2=(L+2*D*t)*(B+2*D*t);
  const V=D*(A1+A2+Math.sqrt(A1*A2))/3;
  const luz=V*v("spul"), wyw=Math.max(0,luz-v("zasyp")), kursy=v("kurs")>0?Math.ceil(wyw/v("kurs")):0;
  document.getElementById("wynik").innerHTML=
    `Objętość wykopu: <b>${f(V)} m³</b><br>`+
    `Po wykopie (luźna): <b>${f(luz)} m³</b><br>`+
    `Do wywozu: <b>${f(wyw)} m³</b><br>`+
    `Kursy samochodu: <b>${kursy}</b>`+
    `<p class="mut">Spulchnienie to współczynnik wzrostu objętości. Wartość wpisz z badania gruntu albo od przewoźnika.</p>`;
  rysuj(B,D,t,V,luz);
}
function rysuj(B,D,t,V,luz){
  const Wt=B+2*D*t, k=Math.min(240/Math.max(Wt,0.1),150/Math.max(D,0.1));
  const cx=170, gy=60, dy=gy+D*k;
  const xtL=cx-Wt*k/2, xtR=cx+Wt*k/2, xbL=cx-B*k/2, xbR=cx+B*k/2;
  const hb=Math.min(14,D*k*0.15);
  let g=`<rect class="grunt" x="20" y="${gy}" width="300" height="190"/><rect class="grunt2" x="20" y="${gy}" width="300" height="5"/>`;
  g+=`<polygon class="eps" points="${xtL.toFixed(1)},${gy} ${xtR.toFixed(1)},${gy} ${xbR.toFixed(1)},${dy.toFixed(1)} ${xbL.toFixed(1)},${dy.toFixed(1)}"/>`;
  g+=`<rect class="beton pop" x="${(cx-B*k*0.3).toFixed(1)}" y="${(dy-hb).toFixed(1)}" width="${(B*k*0.6).toFixed(1)}" height="${hb.toFixed(1)}"/>`;
  g+=`<path class="dim" d="M${(xtL-12).toFixed(1)} ${gy}V${dy.toFixed(1)}"/>`;
  g+=T(xtL-16,(gy+dy)/2+4,`${f(D,2)} m`,"tm","end");
  g+=T(cx,gy-10,"teren","tm","middle");
  const bx=400, base=230, mh=170, mx=Math.max(V,luz,0.001);
  const hV=V/mx*mh, hL=luz/mx*mh;
  g+=`<rect class="jastrych pop" x="${bx}" y="${(base-hV).toFixed(1)}" width="70" height="${hV.toFixed(1)}"/>`;
  g+=`<rect class="beton pop" x="${bx+110}" y="${(base-hL).toFixed(1)}" width="70" height="${hL.toFixed(1)}"/>`;
  g+=T(bx+35,(base-hV-8).toFixed(1),`${f(V)} m³`,"t","middle")+T(bx+145,(base-hL-8).toFixed(1),`${f(luz)} m³`,"t","middle");
  g+=T(bx+35,base+18,"w wykopie","tm","middle")+T(bx+145,base+18,"po wykopie","tm","middle");
  g+=`<path class="dim" d="M${bx-10} ${base}H${bx+200}"/>`;
  document.getElementById("wykop").innerHTML=g;
}
document.querySelectorAll("input").forEach(e=>e.addEventListener("input",licz));licz();''')

CALC['ocieplenie']=dict(title='Ocieplenie ścian: ile styropianu i kleju',
 desc='Policz płyty izolacji z zapasem, zużycie kleju i liczbę dybli dla ocieplenia ścian. Przekrój pokazuje warstwy od zewnątrz.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Ocieplenie ścian: ile styropianu i kleju</h1>
<p class="lead">Wpisz powierzchnię elewacji po odjęciu okien i drzwi oraz parametry z karty produktu. Zobaczysz liczbę płyt, kleju i dybli.</p>
<section class="calc"><div class="panel"><div class="grid">
<div><label for="pow">Powierzchnia elewacji netto (m²)</label><input id="pow" type="number" value="150" step="1"></div>
<div><label for="gr">Grubość izolacji (cm)</label><input id="gr" type="number" value="15" step="1"></div>
<div><label for="plyta">Powierzchnia jednej płyty (m²)</label><input id="plyta" type="number" value="0.72" step="0.01"></div>
<div><label for="zapas">Zapas na cięcia i straty (%)</label><input id="zapas" type="number" value="7" step="1"></div>
<div><label for="klej">Klej (kg na m², z karty)</label><input id="klej" type="number" value="5" step="0.5"></div>
<div><label for="worek">Worek kleju (kg)</label><input id="worek" type="number" value="25" step="1"></div>
<div><label for="dybel">Dyble (szt. na m², z karty)</label><input id="dybel" type="number" value="6" step="1"></div>
</div></div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Warstwy ściany <span>od zewnątrz, grubość izolacji w skali</span></figcaption><svg id="przekroj" viewBox="0 0 640 300" role="img" aria-label="Przekrój ściany: tynk, izolacja z dyblami, klej i ściana nośna"></svg><p class="note">Schemat poglądowy. Grubości tynku i kleju są symboliczne, prawdziwe wartości podaje karta systemu.</p></figure>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Zapas to nie zapas na błędy.</b> Płyty docina się przy narożach, otworach i na końcach ścian. Zapas pokrywa cięcia, nie pomyłki w wymiarach.</div>
<div class="tip"><b>Klej nie zastępuje dybli.</b> System mocuje się klejem i dyblami razem. Liczbę dybli wpisz z karty, bo zależy od podłoża i wysokości budynku.</div>
<div class="tip"><b>Grubość bierz z projektu.</b> Izolacja ma konkretną grubość wynikającą z wymagań energetycznych budynku. Nie kopiuj jej od sąsiada.</div>
<div class="tip"><b>Ocieplenie zaczyna się od fundamentu.</b> Pas przy cokole i pod gruntem wykonuje się innymi materiałami. Nie licz go tu razem z elewacją.</div>
<details><summary>Jak liczymy</summary>
<p>Liczba płyt to powierzchnia netto razy (1 + zapas), podzielona przez powierzchnię jednej płyty i zaokrąglona w górę. Objętość izolacji to powierzchnia razy grubość.</p>
<p>Klej to powierzchnia razy zużycie z karty, a worki to ilość kleju podzielona przez wagę worka. Dyble to powierzchnia razy liczba na metr kwadratowy.</p>
</details>
<p>Czy ściana z tą grubością spełni wymagania, sprawdzisz w kalkulatorze <a href="/wspolczynnik-u">współczynnika U</a>.</p>
</main>''',
 script='''const v=id=>parseFloat(document.getElementById(id).value)||0;
const f=(n,d=1)=>n.toLocaleString("pl-PL",{maximumFractionDigits:d});
const T=(x,y,t,c="t",a="start")=>`<text class="${c}" x="${x}" y="${y}" text-anchor="${a}">${t}</text>`;
function licz(){
  const pow=v("pow"), zap=1+v("zapas")/100, plyta=Math.max(0.01,v("plyta"));
  const plyty=Math.ceil(pow*zap/plyta), klej=pow*v("klej"), worki=Math.ceil(klej/Math.max(1,v("worek"))), dyble=Math.ceil(pow*v("dybel")), m3=pow*v("gr")/100;
  document.getElementById("wynik").innerHTML=
    `Płyty izolacji: <b>${plyty} szt.</b> (ok. ${f(m3,2)} m³)<br>`+
    `Klej: <b>${f(klej,0)} kg</b>, czyli ${worki} worków<br>`+
    `Dyble: <b>${dyble} szt.</b>`+
    `<p class="mut">Płyty liczone z zapasem na cięcia. Zużycie kleju i dybli wpisz z karty systemu.</p>`;
  rysuj();
}
function rysuj(){
  const gr=Math.min(30,Math.max(2,v("gr"))), k=6, x0=60, yT=70, hH=170;
  const ti=gr*k;
  let x=x0, g="";
  g+=`<rect class="jastrych" x="${x}" y="${yT}" width="6" height="${hH}"/>`; x+=6;
  const xi=x;
  g+=`<rect class="eps" x="${x}" y="${yT}" width="${ti}" height="${hH}"/>`; x+=ti;
  g+=`<rect class="chudy" x="${x}" y="${yT}" width="3" height="${hH}"/>`; x+=3;
  const xm=x;
  g+=`<rect class="mur" x="${xm}" y="${yT}" width="150" height="${hH}"/>`;
  for(let i=1;i<=4;i++){const yy=yT+i*hH/5; g+=`<path class="strzem draw" pathLength="1" d="M${xi} ${yy}H${xm}"/>`;}
  g+=T(x0+3,yT+hH+16,"tynk","tm","start")+T(xi+ti/2,yT-12,`izolacja ${f(gr,0)} cm`,"t","middle");
  g+=T(xi+ti+1,yT+hH+16,"klej","tm","middle")+T(xm+75,yT+hH+36,"ściana nośna","tm","middle");
  g+=T(xi+ti/2,yT+hH+36,"dybel","tm","middle");
  document.getElementById("przekroj").innerHTML=g;
}
document.querySelectorAll("input").forEach(e=>e.addEventListener("input",licz));licz();''')

CALC['sciana-dzialowa']=dict(title='Ścianka z płyt GK: ile płyt, profili i wełny',
 desc='Policz płyty gipsowo-kartonowe, słupki, prowadnice i wełnę na ściankę działową. Przekrój pokazuje warstwy ścianki.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Ścianka działowa z płyt GK: ile materiału</h1>
<p class="lead">Wpisz długość i wysokość ścianki oraz wymiary płyty. Zobaczysz liczbę płyt, profili i wełny mineralnej.</p>
<section class="calc"><div class="panel"><div class="grid">
<div><label for="dl">Długość ścianki (m)</label><input id="dl" type="number" value="4" step="0.1"></div>
<div><label for="wys">Wysokość ścianki (m)</label><input id="wys" type="number" value="2.6" step="0.1"></div>
<div><label for="plsz">Szerokość płyty (m)</label><input id="plsz" type="number" value="1.2" step="0.01"></div>
<div><label for="plwys">Wysokość płyty (m)</label><input id="plwys" type="number" value="2.6" step="0.01"></div>
<div><label for="warst">Warstwy płyt na stronę</label><input id="warst" type="number" value="1" step="1"></div>
<div><label for="strony">Strony ścianki</label><input id="strony" type="number" value="2" step="1"></div>
<div><label for="rozst">Rozstaw słupków (m)</label><input id="rozst" type="number" value="0.6" step="0.05"></div>
<div><label for="prof">Długość profilu handlowego (m)</label><input id="prof" type="number" value="3" step="0.1"></div>
<div><label for="plgr">Grubość płyty (mm)</label><input id="plgr" type="number" value="12.5" step="0.5"></div>
<div><label for="profgr">Grubość ścianki z profilem (mm)</label><input id="profgr" type="number" value="50" step="5"></div>
<div><label for="zapas">Zapas na docinki (%)</label><input id="zapas" type="number" value="10" step="1"></div>
</div></div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Przekrój ścianki <span>warstwy od lewej do prawej</span></figcaption><svg id="przekroj" viewBox="0 0 640 300" role="img" aria-label="Przekrój ścianki działowej: płyta, wełna ze słupkiem, płyta"></svg><p class="note">Schemat poglądowy. Układ profili, wkręty i wypełnienie określa karta systemu wybranego producenta.</p></figure>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Rodzaj płyty zależy od pomieszczenia.</b> W łazience i kuchni potrzebne są płyty przystosowane do wilgoci. Oznaczenie na płycie mówi, do czego jest przeznaczona.</div>
<div class="tip"><b>Wysokość płyty decyduje o łączeniach.</b> Płyta o długości równej wysokości ścianki nie daje poziomych styków. Krótsze płyty to więcej spoin do szpachlowania.</div>
<div class="tip"><b>Profile liczy się z długości handlowej.</b> Każdy odcinek kończy się resztką z cięcia. Dlatego liczba profili jest większa niż suma metrów podzielona przez długość profilu.</div>
<div class="tip"><b>Wkręty, taśmy i masy to osobne pozycje.</b> Kalkulator nie liczy ich, bo zależą od systemu i od tego, jak wykończysz spoiny.</div>
<details><summary>Jak liczymy</summary>
<p>Płyty na stronę to liczba płyt w poziomie (długość podzielona przez szerokość płyty, w górę) razy liczba w pionie (wysokość podzielona przez wysokość płyty, w górę) razy liczba warstw. Razem z obu stron i zapasem.</p>
<p>Słupki to liczba słupków (długość podzielona przez rozstaw, w górę, plus jeden) razy liczba profili na każdy słupek, czyli wysokość podzielona przez długość handlową, w górę. Prowadnice to dwa odcinki długości ścianki, też z zaokrągleniem do profili.</p>
<p>Wełna to pole ścianki, bo wypełnia całą przestrzeń między płytami.</p>
</details>
</main>''',
 script='''const v=id=>parseFloat(document.getElementById(id).value)||0;
const f=(n,d=1)=>n.toLocaleString("pl-PL",{maximumFractionDigits:d});
const T=(x,y,t,c="t",a="start")=>`<text class="${c}" x="${x}" y="${y}" text-anchor="${a}">${t}</text>`;
function licz(){
  const L=v("dl"), H=v("wys"), zap=1+v("zapas")/100, pw=Math.max(0.1,v("plsz")), ph=Math.max(0.1,v("plwys"));
  const naStrone=Math.ceil(L/pw)*Math.ceil(H/ph)*v("warst");
  const plyty=Math.ceil(naStrone*v("strony")*zap);
  const dl=Math.max(0.5,v("prof")), nsl=Math.ceil(L/Math.max(0.1,v("rozst")))+1;
  const sztSl=nsl*Math.ceil(H/dl), sztPr=2*Math.ceil(L/dl), wel=L*H;
  document.getElementById("wynik").innerHTML=
    `Płyty GK: <b>${plyty} szt.</b><br>`+
    `Słupki: <b>${nsl} szt.</b> po ${f(H,2)} m, czyli ${sztSl} profili<br>`+
    `Prowadnice: <b>${sztPr} szt.</b> po ${f(dl,1)} m (góra i dół)<br>`+
    `Wełna: <b>${f(wel,2)} m²</b>`+
    `<p class="mut">Profile liczone z długości handlowych, bez wykorzystania resztek z cięć. Wkręty, taśmy i masy są osobno.</p>`;
  rysuj();
}
function rysuj(){
  const t=Math.max(5,v("plgr")), p=Math.max(10,v("profgr"));
  const total=2*t+p, k=Math.min(2.2,400/total);
  const tp=t*k, tw=p*k, x0=(640-(2*tp+tw))/2, yT=60, hh=200;
  let g=`<rect class="eps" x="${x0.toFixed(1)}" y="${yT}" width="${tp.toFixed(1)}" height="${hh}"/>`;
  g+=`<rect class="xps" x="${(x0+tp).toFixed(1)}" y="${yT}" width="${tw.toFixed(1)}" height="${hh}"/>`;
  g+=`<rect class="chudy" x="${(x0+tp+tw/2-3).toFixed(1)}" y="${yT}" width="6" height="${hh}"/>`;
  g+=`<rect class="eps" x="${(x0+tp+tw).toFixed(1)}" y="${yT}" width="${tp.toFixed(1)}" height="${hh}"/>`;
  g+=T((x0+tp/2).toFixed(1),yT-12,"płyta","tm","middle")+T((x0+tp+tw/2).toFixed(1),yT-12,"wełna i słupek","tm","middle")+T((x0+tp+tw+tp/2).toFixed(1),yT-12,"płyta","tm","middle");
  g+=`<path class="dim" d="M${x0.toFixed(1)} ${yT+hh+18}H${(x0+2*tp+tw).toFixed(1)}"/>`;
  g+=T((x0+(2*tp+tw)/2).toFixed(1),yT+hh+38,`${f(total,1)} mm`,"t","middle");
  document.getElementById("przekroj").innerHTML=g;
}
document.querySelectorAll("input").forEach(e=>e.addEventListener("input",licz));licz();''')

CALC['kostka']=dict(title='Kostka brukowa i płytki: ile m² z zapasem',
 desc='Policz m² kostki lub płytek z zapasem, liczbę elementów, podbudowę i podsypkę. Zobacz plan układu w dwóch wariantach.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Kostka brukowa i płytki: ile m² z zapasem</h1>
<p class="lead">Wpisz wymiary powierzchni i element. Zobaczysz liczbę sztuk z zapasem, ilość podbudowy i podsypki oraz plan układu.</p>
<section class="calc"><div class="panel"><div class="grid">
<div><label for="dl">Długość obszaru (m)</label><input id="dl" type="number" value="6" step="0.1"></div>
<div><label for="szer">Szerokość obszaru (m)</label><input id="szer" type="number" value="4" step="0.1"></div>
<div><label for="odj">Odejmij słupy, studzienki (m²)</label><input id="odj" type="number" value="0" step="0.1"></div>
<div><label for="eldl">Długość elementu (cm)</label><input id="eldl" type="number" value="20" step="1"></div>
<div><label for="elszer">Szerokość elementu (cm)</label><input id="elszer" type="number" value="10" step="1"></div>
<div><label for="spoina">Spoina (mm)</label><input id="spoina" type="number" value="3" step="1"></div>
<div><label for="zapas">Zapas na docinki (%)</label><input id="zapas" type="number" value="10" step="1"></div>
<div><label for="podb">Podbudowa (cm, kruszywo)</label><input id="podb" type="number" value="15" step="1"></div>
<div><label for="pods">Podsypka (cm, piasek)</label><input id="pods" type="number" value="4" step="1"></div>
<div style="grid-column:1/-1"><label for="uklad">Układ</label><select id="uklad"><option value="rzedy">W rzędach</option><option value="polowki">W przesunięte rzędy</option></select></div>
</div></div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Plan układu <span>w skali obszaru</span></figcaption><svg id="plan" viewBox="0 0 640 300" role="img" aria-label="Plan układu kostki na wpisanym obszarze"></svg><p class="note">Plan poglądowy. Kolory i wzór kostki zależą od producenta, na rysunku pokazano sam kształt układu.</p></figure>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Liczy się powierzchnia netto.</b> Odejmij słupy, studzienki i wpusty. Zamawiając na całość, płacisz za materiał, który nie trafi na podjazd.</div>
<div class="tip"><b>Krzywe ściany kosztują kostkę.</b> Jeśli pierwszy rząd wytyczasz od ściany, a ściana nie jest prosta, każdy kolejny rząd będzie się rozjeżdżał. Wytycz od prostej linii.</div>
<div class="tip"><b>Układ w przesunięte rzędy daje więcej docinków.</b> Przy jodełce i przy układzie na połówki zapas zwykle trzeba zwiększyć.</div>
<div class="tip"><b>Podbudowa decyduje o trwałości.</b> Pod samochód potrzebna jest grubsza podbudowa niż pod taras. Grubość i rodzaj kruszywa wpisz z projektu.</div>
<details><summary>Jak liczymy</summary>
<p>Powierzchnia netto to długość razy szerokość minus odejmowane elementy. Powierzchnia jednego elementu to wymiary elementu powiększone o spoinę. Liczba sztuk to powierzchnia razy (1 + zapas), podzielona przez powierzchnię elementu i zaokrąglona w górę.</p>
<p>Podbudowę i podsypkę liczymy jako objętość: powierzchnia razy grubość warstwy. Grubości w formularzu są przykładowe i zależą od obciążenia i gruntu.</p>
</details>
</main>''',
 script='''const v=id=>parseFloat(document.getElementById(id).value)||0;
const f=(n,d=1)=>n.toLocaleString("pl-PL",{maximumFractionDigits:d});
function licz(){
  const pole=Math.max(0,v("dl")*v("szer")-v("odj"));
  const ea=((v("eldl")+v("spoina")/10)/100)*((v("elszer")+v("spoina")/10)/100);
  const szt=Math.ceil(pole*(1+v("zapas")/100)/Math.max(0.0001,ea));
  document.getElementById("wynik").innerHTML=
    `Powierzchnia do ułożenia: <b>${f(pole)} m²</b><br>`+
    `Elementów z zapasem: <b>${szt} szt.</b><br>`+
    `Podbudowa: <b>${f(pole*v("podb")/100,2)} m³</b> kruszywa<br>`+
    `Podsypka: <b>${f(pole*v("pods")/100,2)} m³</b> piasku`+
    `<p class="mut">Zapas liczony od powierzchni netto. Przy układzie w przesunięte rzędy docinków będzie więcej.</p>`;
  rysuj();
}
function rysuj(){
  const dl=Math.max(0.5,v("dl")), sz=Math.max(0.5,v("szer")), elL=Math.max(5,v("eldl")), elW=Math.max(5,v("elszer")), sp=v("spoina")/10;
  const uklad=document.getElementById("uklad").value;
  const k=Math.min(560/(dl*100),240/(sz*100)), ox=40, oy=30;
  const pitchX=elL+sp, pitchY=elW+sp;
  let g=`<defs><clipPath id="obszar"><rect x="${ox}" y="${oy}" width="${(dl*100*k).toFixed(1)}" height="${(sz*100*k).toFixed(1)}"/></clipPath></defs><g clip-path="url(#obszar)">`;
  let i=0;
  for(let r=0,y=0;y<sz*100;r++,y+=pitchY){
    const off=(uklad==="polowki"&&r%2)?-pitchX/2:0;
    for(let x=off;x<dl*100;x+=pitchX,i++){
      g+=`<rect class="beton pop" style="animation-delay:${(i%80)*8}ms" x="${(ox+x*k).toFixed(1)}" y="${(oy+y*k).toFixed(1)}" width="${(elL*k).toFixed(1)}" height="${(elW*k).toFixed(1)}" rx="1"/>`;
    }
  }
  g+=`</g><rect x="${ox}" y="${oy}" width="${(dl*100*k).toFixed(1)}" height="${(sz*100*k).toFixed(1)}" fill="none" class="dim"/>`;
  g+=`<text class="tm" x="${ox}" y="${(oy+sz*100*k+20).toFixed(1)}">${f(dl)} m × ${f(sz)} m, element ${elL} × ${elW} cm</text>`;
  document.getElementById("plan").innerHTML=g;
}
document.querySelectorAll("input,select").forEach(e=>e.addEventListener("input",licz));licz();''')

CALC['ogrodzenie']=dict(title='Ogrodzenie: ile słupków, przęseł i betonu',
 desc='Policz przęsła, słupki i beton pod fundamenty dla ogrodzenia o zadanej długości. Przekrój fragmentu pokazuje proporcje słupków i przęseł.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Ogrodzenie: ile słupków, przęseł i betonu</h1>
<p class="lead">Podaj długość granicy, rozstaw słupków i wysokość. Zobaczysz liczbę przęseł, słupków i beton pod fundamenty.</p>
<section class="calc"><div class="panel"><div class="grid">
<div><label for="dl">Długość ogrodzenia (m)</label><input id="dl" type="number" value="40" step="0.5"></div>
<div><label for="rozst">Rozstaw słupków, szerokość przęsła (m)</label><input id="rozst" type="number" value="2.5" step="0.05"></div>
<div><label for="wys">Wysokość przęsła (m)</label><input id="wys" type="number" value="1.8" step="0.1"></div>
<div><label for="zag">Zagłębienie słupka (m)</label><input id="zag" type="number" value="0.9" step="0.1"></div>
<div><label for="bok">Fundament pod słupek: bok (cm)</label><input id="bok" type="number" value="40" step="5"></div>
</div></div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<figure class="panel fig"><figcaption>Fragment ogrodzenia <span>trzy przęsła w skali</span></figcaption><svg id="elewacja" viewBox="0 0 640 240" role="img" aria-label="Fragment ogrodzenia: słupki z fundamentem i przęsła między nimi"></svg><p class="note">Pokazany jest fragment, nie całe ogrodzenie. Przęsła i słupki to schemat, system zależy od wybranego producenta.</p></figure>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Granica musi być pewna.</b> Sprawdź ją na mapie geodezyjnej przed postawieniem słupka. Przesunięcie o kilkanaście centymetrów kończy się sporem z sąsiadem.</div>
<div class="tip"><b>Słupek sięga poniżej przemarzania.</b> Zagłębienie to nie tylko stabilność. Słupek musi być osadzony w gruncie tak, jak wskazuje projekt lub producent.</div>
<div class="tip"><b>Przy spadku terenu przęsło się nie dopasuje.</b> Na pochyłym terenie przęsła trzeba ustawić schodkowo albo z przerwą. Płaskie przęsło na spadku wygląda źle i obciąża słupki.</div>
<div class="tip"><b>Bramy i furtki liczy się osobno.</b> Kalkulator zakłada same przęsła pełne. Brama ma własne słupki i fundamenty.</div>
<details><summary>Jak liczymy</summary>
<p>Liczba przęseł to długość ogrodzenia podzielona przez rozstaw słupków, zaokrąglona w górę. Słupków jest o jeden więcej, bo ogrodzenie zaczyna się i kończy słupkiem.</p>
<p>Długość słupka to wysokość przęsła plus zagłębienie. Beton pod każdy słupek to kwadrat fundamentu razy zagłębienie, pomnożone przez liczbę słupków.</p>
</details>
</main>''',
 script='''const v=id=>parseFloat(document.getElementById(id).value)||0;
const f=(n,d=1)=>n.toLocaleString("pl-PL",{maximumFractionDigits:d});
function licz(){
  const L=v("dl"), rs=Math.max(0.5,v("rozst")), wys=v("wys"), zag=v("zag"), bok=v("bok")/100;
  const przesla=Math.ceil(L/rs), slupki=przesla+1, dlS=wys+zag, mbS=slupki*dlS, beton=slupki*bok*bok*zag, pole=L*wys;
  document.getElementById("wynik").innerHTML=
    `Przęsła: <b>${przesla} szt.</b> po ${f(rs,2)} m<br>`+
    `Słupki: <b>${slupki} szt.</b>, każdy ${f(dlS,2)} m (razem ${f(mbS,0)} mb)<br>`+
    `Beton pod słupki: <b>${f(beton,2)} m³</b><br>`+
    `Pole ogrodzenia: <b>${f(pole,1)} m²</b>`+
    `<p class="mut">Bez bram i furtek. Wymiar fundamentu wpisz z projektu lub z karty systemu.</p>`;
  rysuj(rs,wys,zag);
}
function rysuj(rs,wys,zag){
  const bays=3, ground=200, k=Math.min(560/(bays*rs),170/(wys+zag)), x0=40;
  let g=`<rect class="grunt" x="0" y="${ground}" width="640" height="40"/><rect class="grunt2" x="0" y="${ground}" width="640" height="5"/>`;
  for(let i=0;i<bays;i++){
    const x=x0+i*rs*k+4, w=rs*k-8, top=ground-wys*k;
    g+=`<rect class="eps pop" x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${w.toFixed(1)}" height="${(wys*k).toFixed(1)}"/>`;
    for(let j=1;j<=3;j++){const yy=top+j*wys*k/4; g+=`<path class="dim" d="M${x.toFixed(1)} ${yy.toFixed(1)}H${(x+w).toFixed(1)}"/>`;}
  }
  for(let i=0;i<=bays;i++){
    const x=x0+i*rs*k;
    g+=`<rect class="beton" x="${(x-4).toFixed(1)}" y="${(ground-wys*k).toFixed(1)}" width="8" height="${((wys+zag)*k).toFixed(1)}"/>`;
  }
  g+=`<text class="tm" x="${x0}" y="${(ground+zag*k+22).toFixed(1)}">przęsło ${f(rs,2)} m, wysokość ${f(wys,1)} m, zagłębienie ${f(zag,1)} m</text>`;
  document.getElementById("elewacja").innerHTML=g;
}
document.querySelectorAll("input").forEach(e=>e.addEventListener("input",licz));licz();''')
