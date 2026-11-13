# -*- coding: utf-8 -*-
# Kalkulator kosztu budowy domu (kolejka automatu, 2026-10-20).
from calc3 import _H

CALC5={}
CALC5['koszt-budowy']=dict(title='Koszt budowy domu: stan surowy, deweloperski, pod klucz',
 desc='Policz koszt budowy domu dla stanu surowego, deweloperskiego i pod klucz. Wpisz metraż i własne stawki z ofert, a kalkulator pokaże różnicę.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Koszt budowy domu: stan surowy, deweloperski czy pod klucz</h1>
<p class="lead">Podaj metraż i stawkę za metr z ofert wykonawców. Kalkulator pokaże koszt dla każdego standardu i różnicę między nimi. Stawki w polach są przykładowe, zamień je na własne.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="m2">Powierzchnia użytkowa (m²)</label><input id="m2" type="number" value="120" min="0" step="1"></div>
<div><label for="std">Standard, który liczysz</label><select id="std"><option value="0">stan surowy zamknięty</option><option value="1" selected>stan deweloperski</option><option value="2">pod klucz</option></select></div>
<div><label for="kor">Korekta regionalna (%)</label><input id="kor" type="number" value="0" step="1"></div>
<div><label for="zap">Zapas na nieprzewidziane (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
</div>
<h3>Stawki netto za m² (przykładowe, wpisz z ofert)</h3>
<div class="grid">
<div><label for="s0">Stan surowy zamknięty (zł/m²)</label><input id="s0" type="number" value="1800" min="0" step="10"></div>
<div><label for="s1">Stan deweloperski (zł/m²)</label><input id="s1" type="number" value="3000" min="0" step="10"></div>
<div><label for="s2">Pod klucz (zł/m²)</label><input id="s2" type="number" value="4200" min="0" step="10"></div>
</div>
<p class="mut">Stawki i zapas to przykłady, nie dane rynkowe. Korekta regionalna to różnica między Twoim regionem a ofertami, 0 oznacza bez korekty. Bazę cen jednostkowych znajdziesz na <a href="/ceny-budowlane">stronie cen</a>.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Koszt netto to metraż razy stawka za metr wybranego standardu. Potem dolicza się korektę regionalną i zapas na nieprzewidziane. VAT nie jest wliczony. Jego stawka zależy od umowy i warunków, więc sprawdź ją na <a href="/vat-budowa">stronie o VAT 8% czy 23%</a>.</p>
<h2>Co zwykle jest w każdym standardzie</h2>
<table><thead><tr><th>Standard</th><th>Zwykle w cenie</th></tr></thead><tbody>
<tr><td>Stan surowy zamknięty</td><td>Fundamenty, ściany, strop, dach z pokryciem, okna i drzwi zewnętrzne.</td></tr>
<tr><td>Stan deweloperski</td><td>To samo co wyżej, plus tynki, wylewki i instalacje doprowadzone do punktów. Podłóg i łazienek zwykle nie ma.</td></tr>
<tr><td>Pod klucz</td><td>Wykończenie gotowe do mieszkania: podłogi, łazienki, kuchnia i malowanie.</td></tr>
</tbody></table>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Stan deweloperski to nie pod klucz.</b> Różnica często wychodzi dopiero przy odbiorze. Sprawdź w specyfikacji, czy tynki, wylewki i instalacje są w cenie.</div>
<div class="tip"><b>Najniższa stawka może nie mieć wszystkiego.</b> Oferta bez instalacji albo bez ogrzewania wygląda tanio tylko na papierze. Porównuj oferty z tym samym zakresem.</div>
<div class="tip"><b>Poza stawką za m² zostają przyłącza, projekt i zagospodarowanie działki.</b> Liczy się je osobno. Zobacz <a href="/przylacza">przyłącza do domu</a>.</div>
<h2>Finansowanie</h2>
<p>Jeśli budujesz na kredyt, porównaj oferty przed podpisaniem umowy. Sprawdzaj RRSO i całkowity koszt kredytu, a nie tylko wysokość raty.</p>
<a class="cta" href="#" rel="sponsored nofollow">Porównaj oferty kredytu hipotecznego</a>
<p class="mut">To link partnerski. Kalkulator raty znajdziesz na <a href="/kredyt">stronie kredytu</a>.</p>
<p>Powiązane: <a href="/konfigurator-domu">konfigurator domu z kosztem elementów</a>, <a href="/harmonogram">harmonogram budowy</a>, <a href="/ceny-budowlane">ceny materiałów i robocizny</a>.</p>
</main>''',
 script=_H+r'''const STD=["stan surowy zamknięty","stan deweloperski","pod klucz"];
function kosztCalc(m2,st,kor,zap){return m2*st*(1+kor/100)*(1+zap/100);}
function licz(){
  const m2=v("m2"), kor=v("kor"), zap=v("zap"), sel=+$("std").value;
  const r=[v("s0"),v("s1"),v("s2")];
  const tot=r.map(st=>kosztCalc(m2,st,kor,zap));
  const d1=tot[1]-tot[0], d2=tot[2]-tot[1];
  $("wynik").innerHTML=`Koszt netto, ${STD[sel]}: <b>${f(tot[sel],0)} zł</b><br>Dla tego samego metrażu:<br>${STD.map((n,i)=>`${n}: <b>${f(tot[i],0)} zł</b>`).join("<br>")}<br>Z surowego do deweloperskiego dopłacasz <b>${f(d1,0)} zł</b>, z deweloperskiego do pod klucz <b>${f(d2,0)} zł</b>.<div class="mut">Metraż ${f(m2,0)} m², zapas ${f(zap,0)} %, korekta regionalna ${f(kor,0)} %. Stawki są przykładowe. Wynik to szacunek, nie wycena. VAT nie jest wliczony.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)

CALC5['malowanie']=dict(title='Malowanie: ile farby na ściany i sufit',
 desc='Policz litry farby na ściany i sufit pokoju z odjęciem okien i drzwi. Wpisz wydajność z karty produktu, a kalkulator doliczy zapas i opakowania.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Malowanie: ile farby na ściany i sufit</h1>
<p class="lead">Podaj wymiary pokoju, powierzchnię okien i drzwi oraz wydajność farby z karty produktu. Kalkulator policzy litry i liczbę opakowań z zapasem.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość pokoju (m)</label><input id="dl" type="number" value="4" min="0" step="0.1"></div>
<div><label for="sz">Szerokość pokoju (m)</label><input id="sz" type="number" value="3" min="0" step="0.1"></div>
<div><label for="wy">Wysokość ścian (m)</label><input id="wy" type="number" value="2.6" min="0" step="0.1"></div>
<div><label for="otw">Okna i drzwi (m²)</label><input id="otw" type="number" value="3" min="0" step="0.1"></div>
<div><label for="suf">Malujemy sufit</label><select id="suf"><option value="1" selected>tak</option><option value="0">nie</option></select></div>
<div><label for="war">Liczba warstw</label><select id="war"><option value="1">1</option><option value="2" selected>2</option><option value="3">3</option></select></div>
<div><label for="wyd">Wydajność farby (m² z 1 l na warstwę)</label><input id="wyd" type="number" value="10" min="0" step="0.5"></div>
<div><label for="poj">Pojemność opakowania (l)</label><select id="poj"><option value="2.5">2,5</option><option value="5" selected>5</option><option value="10">10</option></select></div>
<div><label for="zap">Zapas (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
</div>
<p class="mut">Wydajność 10 m² z litra to przykład. Wpisz wartość z karty swojej farby, bo zależy ona od podłoża i producenta.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Ściany to obwód pokoju razy wysokość, minus okna i drzwi. Sufit to długość razy szerokość, jeśli go malujesz. Powierzchnię mnożymy przez liczbę warstw, dzielimy przez wydajność z karty i dodajemy zapas. Opakowania liczymy w górę, bo farby nie kupisz na sztuki.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Okna i drzwi odejmij, ale nie zapominaj o ościeżach.</b> Boki otworu i ościeżnice też się maluje. Przy dużych otworach dolicz trochę farby, zamiast odejmować je co do centymetra.</div>
<div class="tip"><b>Sufit to osobna pozycja.</b> Jeśli go nie malujesz, wybierz „nie”, bo inaczej farby kupisz za dużo.</div>
<div class="tip"><b>Wydajność z etykiety to wartość idealna.</b> Na chłonnym tynku i przy dwóch warstwach zużycie rośnie. Zostaw zapas.</div>
<div class="tip"><b>Odcienie z różnych partii bywają różne.</b> Kup całą ilość naraz, nawet z zapasem, żeby ściana nie miała dwóch kolorów.</div>
<p>Powiązane: <a href="/wylewka">wylewka</a>, <a href="/ocieplenie">ocieplenie ścian</a>, <a href="/kostka">kostka i płytki</a>.</p>
</main>''',
 script=_H+r'''function malCalc(dl,sz,wy,otw,suf,war,wyd,zap,poj){
  const sc=Math.max(0,2*(dl+sz)*wy-otw);
  const sf=suf?dl*sz:0;
  const m2=(sc+sf)*war;
  const litry=m2/wyd*(1+zap/100);
  const opak=Math.ceil(litry/poj-1e-9);
  return {sc,sf,m2,litry,opak};
}
function licz(){
  const wyd=v("wyd");
  if(!(wyd>0)){$("wynik").innerHTML="Wpisz wydajność farby z karty produktu, większą od zera.";return;}
  const r=malCalc(v("dl"),v("sz"),v("wy"),v("otw"),$("suf").value==="1",+$("war").value,wyd,v("zap"),+$("poj").value);
  $("wynik").innerHTML=`Pole do malowania: <b>${f(r.m2,1)} m²</b><br>Ściany: ${f(r.sc,1)} m², sufit: ${f(r.sf,1)} m²<br>Farby z zapasem: <b>${f(r.litry,1)} l</b><br>Opakowania po ${f(+$("poj").value,1)} l: <b>${r.opak} szt.</b><div class="mut">Wynik to szacunek. Wydajność sprawdź w karcie produktu, a przy zakupie weź zapas z tej samej partii.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)

CALC5['tynk']=dict(title='Tynk na ściany: ile worków kupić',
 desc='Policz, ile worków tynku na ściany pokoju, z odjęciem okien i drzwi. Grubość i zużycie wpisz z karty produktu, a kalkulator doda zapas.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Tynk na ściany: ile worków kupić</h1>
<p class="lead">Podaj wymiary pokoju, okna i drzwi, grubość warstwy oraz zużycie z karty produktu. Kalkulator policzy kilogramy tynku i liczbę worków z zapasem.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość pokoju (m)</label><input id="dl" type="number" value="4" min="0" step="0.1"></div>
<div><label for="sz">Szerokość pokoju (m)</label><input id="sz" type="number" value="3" min="0" step="0.1"></div>
<div><label for="wy">Wysokość ścian (m)</label><input id="wy" type="number" value="2.6" min="0" step="0.1"></div>
<div><label for="otw">Okna i drzwi (m²)</label><input id="otw" type="number" value="3" min="0" step="0.1"></div>
<div><label for="gr">Grubość warstwy (mm)</label><input id="gr" type="number" value="10" min="0" step="1"></div>
<div><label for="zuz">Zużycie z karty (kg na m² na 1 mm)</label><input id="zuz" type="number" value="1.5" min="0" step="0.05"></div>
<div><label for="wrk">Pojemność worka (kg)</label><select id="wrk"><option value="20">20</option><option value="25" selected>25</option><option value="30">30</option></select></div>
<div><label for="zap">Zapas (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
</div>
<p class="mut">Grubość 10 mm i zużycie 1,5 kg na m² na 1 mm to przykłady. Wpisz wartości z karty swojego tynku, bo zależą od rodzaju tynku i podłoża. Pole sufitu kalkulator nie liczy.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Powierzchnia ścian to obwód pokoju razy wysokość, minus okna i drzwi. Zużycie z karty podaje, ile kilogramów tynku idzie na 1 m² przy grubości 1 mm. Mnożymy to przez grubość warstwy i powierzchnię, dodajemy zapas, a worki liczymy w górę.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Grubość na ścianie to nie zawsze grubość z karty.</b> Nierówna ściana wymaga grubszej warstwy w miejscach ubytków. Przy większej grubości zużycie rośnie, więc zostaw zapas.</div>
<div class="tip"><b>Zużycie zależy od podłoża.</b> Na mocno chłonnym bloczku tynk wsiąka szybciej, a zużycie rośnie. Sprawdź warunki na karcie produktu.</div>
<div class="tip"><b>Otwarty albo zawilgocony worek traci jakość.</b> Kupuj tyle, ile zużyjesz w ciągu kilku dni, a resztę dokupuj w razie potrzeby.</div>
<div class="tip"><b>Sufit to osobna pozycja.</b> Ten kalkulator liczy same ściany. Sufit policz osobno, bo grubość i zużycie bywają inne.</div>
<p>Powiązane: <a href="/malowanie">malowanie: ile farby</a>, <a href="/wylewka">wylewka</a>, <a href="/ocieplenie">ocieplenie ścian</a>.</p>
</main>''',
 script=_H+r'''function tynkCalc(dl,sz,wy,otw,gr,zuz,wrk,zap){
  const sc=Math.max(0,2*(dl+sz)*wy-otw);
  const kg=sc*gr*zuz*(1+zap/100);
  const worki=Math.ceil(kg/wrk-1e-9);
  return {sc,kg,worki};
}
function licz(){
  const gr=v("gr"), zuz=v("zuz");
  if(!(gr>0)||!(zuz>0)){$("wynik").innerHTML="Wpisz grubość warstwy i zużycie z karty produktu, większe od zera.";return;}
  const r=tynkCalc(v("dl"),v("sz"),v("wy"),v("otw"),gr,zuz,+$("wrk").value,v("zap"));
  $("wynik").innerHTML=`Powierzchnia ścian: <b>${f(r.sc,1)} m²</b><br>Tynku z zapasem: <b>${f(r.kg,0)} kg</b><br>Worki po ${f(+$("wrk").value,0)} kg: <b>${r.worki} szt.</b><div class="mut">Wynik to szacunek. Zużycie i grubość sprawdź w karcie produktu. Sufit nie jest wliczony.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)

CALC5['sufit-gk']=dict(title='Sufit z płyt GK: ile płyt i profili',
 desc='Policz płyty GK i profile nośne na sufit podwieszany. Podaj wymiary pomieszczenia, rozstaw i długość profilu z karty systemu, a kalkulator doda zapas.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Sufit z płyt GK: ile płyt i profili kupić</h1>
<p class="lead">Podaj wymiary pomieszczenia, wielkość płyty i rozstaw profili z karty systemu. Kalkulator policzy płyty i metry profili z zapasem.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość pomieszczenia (m)</label><input id="dl" type="number" value="4" min="0" step="0.1"></div>
<div><label for="sz">Szerokość pomieszczenia (m)</label><input id="sz" type="number" value="3" min="0" step="0.1"></div>
<div><label for="pl">Płyta GK, długość</label><select id="pl"><option value="2" selected>1200 × 2000 mm</option><option value="2.5">1200 × 2500 mm</option></select></div>
<div><label for="roz">Rozstaw profili nośnych (cm)</label><select id="roz"><option value="40">40</option><option value="50">50</option><option value="60" selected>60</option></select></div>
<div><label for="osi">Profile biegną wzdłuż</label><select id="osi"><option value="L" selected>długości pomieszczenia</option><option value="W">szerokości pomieszczenia</option></select></div>
<div><label for="dp">Długość profilu (m)</label><select id="dp"><option value="3">3,0</option><option value="3.6" selected>3,6</option><option value="4">4,0</option></select></div>
<div><label for="zap">Zapas (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
</div>
<p class="mut">Zapas 10 % to założenie, zmień je wg uznania. Rozstaw i długość profilu podaj z karty systemu, bo zależą od obciążenia i producenta.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Powierzchnia to długość razy szerokość pomieszczenia. Płyty liczymy z powierzchni z zapasem, dzieląc ją przez powierzchnię jednej płyty: 1,2 m szerokości razy jej długość. Wynik zaokrąglamy w górę. Profile nośne: liczba rzędów to odległość między ścianami podzielona przez rozstaw, plus rząd przy ścianie. Każdy rząd ma długość wybranej osi pomieszczenia. Metry bieżące mnożymy przez zapas i dzielimy na profile po wybranej długości.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Rozstaw zależy od systemu, a nie od wygody montażu.</b> Płyta cięższa albo lampa w suficie wymaga gęstszego rozstawu. Wpisz wartość z karty systemu, zanim kupisz profile.</div>
<div class="tip"><b>Profile obwodowe i wieszaki to osobna pozycja.</b> Kalkulator liczy profile nośne i płyty. Wieszaki, wkręty i profile przy ścianach policz wg systemu producenta.</div>
<div class="tip"><b>W wilgotnych pomieszczeniach materiał jest inny.</b> W łazience i kuchni stosuje się płyty odporne na wilgoć. Wymiary te same, ale cena i zalecenia już inne.</div>
<p>Powiązane: <a href="/malowanie">malowanie: ile farby</a>, <a href="/tynk">tynk na ściany</a>, <a href="/sciana-dzialowa">ścianka z płyt GK</a>.</p>
</main>''',
 script=_H+r'''function gkCalc(L,W,plDl,roz,osi,zap,dp){
  const A=L*W;
  const plA=1.2*plDl;
  const plyty=Math.ceil(A*(1+zap/100)/plA-1e-9);
  const across=osi==="L"?W:L;
  const along=osi==="L"?L:W;
  const rzedy=Math.floor(across*100/roz+1e-9)+1;
  const mb=rzedy*along*(1+zap/100);
  const sztuk=Math.ceil(mb/dp-1e-9);
  return {A,plyty,rzedy,mb,sztuk};
}
function licz(){
  const r=gkCalc(v("dl"),v("sz"),+$("pl").value,+$("roz").value,$("osi").value,v("zap"),+$("dp").value);
  $("wynik").innerHTML=`Powierzchnia sufitu: <b>${f(r.A,1)} m²</b><br>Płyty GK z zapasem: <b>${r.plyty} szt.</b><br>Profile nośne: <b>${f(r.mb,1)} mb</b>, czyli <b>${r.sztuk} szt.</b> po ${f(+$("dp").value,1)} m<div class="mut">Rzędów profili: ${r.rzedy}. Wieszaki, wkręty i profile obwodowe liczy się osobno. Wynik to szacunek, nie projekt.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)

CALC5['panele-podlogowe']=dict(title='Panele podłogowe: ile paczek kupić',
 desc='Ile paczek paneli kupić na podłogę. Podaj wymiary pokoju, zapas na docinki i m² w paczce z karty produktu, a kalkulator policzy resztę.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Panele podłogowe: ile paczek kupić</h1>
<p class="lead">Podaj wymiary pokoju, zapas na docinki i ilość m² w paczce z karty produktu. Kalkulator policzy liczbę paczek i ile zostanie z nich na zapas.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość pokoju (m)</label><input id="dl" type="number" value="4" min="0" step="0.1"></div>
<div><label for="sz">Szerokość pokoju (m)</label><input id="sz" type="number" value="3" min="0" step="0.1"></div>
<div><label for="zap">Zapas na docinki (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
<div><label for="m2p">m² w paczce (z karty produktu)</label><input id="m2p" type="number" value="2" min="0" step="0.01"></div>
</div>
<p class="mut">Zapas 10 % to założenie, zmień je wg układu. Ilość m² w paczce podaj z karty swojego produktu, bo różni się między producentami. Wartość 2 m² to przykład.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Powierzchnia to długość razy szerokość pokoju. Dodajemy zapas na docinki przy ścianach i progach, a wynik dzielimy przez m² w paczce. Liczbę paczek zaokrąglamy w górę, bo panelu nie kupisz na sztuki.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Układ na skos i wąski pokój zjadają więcej docinków.</b> Przy 10 % zapasu proste układy się mieszczą, ale przy skosie warto dać więcej.</div>
<div class="tip"><b>Paczki z różnych partii mogą różnić się odcieniem.</b> Kupuj komplet z jednej partii, a zapas zostaw w tej samej.</div>
<div class="tip"><b>Panele nie wybaczą nierównego podłoża.</b> Na krzywej wylewce zaczną skrzypieć i odstawać. To kwestia podłoża, nie ilości paczek.</div>
<div class="tip"><b>Podkład i listwy to osobna pozycja.</b> Kalkulator liczy same panele. Podkład, listwy i profile dylatacyjne kupuj osobno.</div>
<p>Powiązane: <a href="/wylewka">wylewka pod podłogę</a>, <a href="/kostka">kostka i płytki</a>, <a href="/malowanie">malowanie ścian</a>.</p>
</main>''',
 script=_H+r'''function paneleCalc(dl,sz,zap,m2p){
  const A=dl*sz;
  const potrzeba=A*(1+zap/100);
  const paczki=Math.ceil(potrzeba/m2p-1e-9);
  const razem=paczki*m2p;
  return {A,potrzeba,paczki,razem,nadwyzka:razem-A};
}
function licz(){
  const m2p=v("m2p");
  if(!(m2p>0)){$("wynik").innerHTML="Wpisz ilość m² w paczce z karty produktu, większą od zera.";return;}
  const r=paneleCalc(v("dl"),v("sz"),v("zap"),m2p);
  $("wynik").innerHTML=`Powierzchnia pokoju: <b>${f(r.A,2)} m²</b><br>Z zapasem na docinki: <b>${f(r.potrzeba,2)} m²</b><br>Paczek do kupienia: <b>${r.paczki} szt.</b><br>Razem w paczkach: ${f(r.razem,2)} m², nadwyżka ${f(r.nadwyzka,2)} m²<div class="mut">Wynik to szacunek. Podkład i listwy liczy się osobno. Sprawdź m² w paczce w karcie produktu.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)

CALC5['welna-strop']=dict(title='Wełna na strop poddasza: ile opakowań kupić',
 desc='Ile opakowań wełny na strop poddasza. Podaj wymiary stropu, grubość z projektu i m² w opakowaniu z karty produktu, a kalkulator doliczy zapas.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Wełna na strop poddasza: ile opakowań kupić</h1>
<p class="lead">Podaj wymiary stropu, grubość warstwy z projektu oraz m² w opakowaniu z karty produktu. Kalkulator policzy opakowania z zapasem i objętość wełny.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość stropu (m)</label><input id="dl" type="number" value="6" min="0" step="0.1"></div>
<div><label for="sz">Szerokość stropu (m)</label><input id="sz" type="number" value="5" min="0" step="0.1"></div>
<div><label for="prz">Odejmij przeszkody (m²)</label><input id="prz" type="number" value="0" min="0" step="0.1"></div>
<div><label for="gr">Grubość warstwy z projektu (cm)</label><input id="gr" type="number" value="20" min="0" step="1"></div>
<div><label for="m2o">m² w opakowaniu (z karty produktu)</label><input id="m2o" type="number" value="3.6" min="0" step="0.01"></div>
<div><label for="zap">Zapas na docinki (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
</div>
<p class="mut">Grubość 20 cm i 3,6 m² w opakowaniu to przykłady. Grubość bierz z projektu, a m² z karty produktu. Zapas 10 % to założenie.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Powierzchnia stropu to długość razy szerokość, minus przeszkody, na przykład komin albo właz. Dodajemy zapas na docinki przy belkach i krawędziach. Opakowania liczymy w górę. Objętość wełny to powierzchnia z zapasem razy grubość warstwy, bo tyle materiału realnie się układa.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Grubość bierze się z projektu, nie z oferty sprzedawcy.</b> Wymagany współczynnik U wynika z przepisów. Sprawdź go na stronie o <a href="/wspolczynnik-u">współczynniku U</a>, zanim kupisz wełnę.</div>
<div class="tip"><b>Wełny nie ściskaj na siłę.</b> Wciśnięta między belki traci grubość i część izolacyjności. Lepiej dobrać wełnę na rozstaw belek niż ją wciskać.</div>
<div class="tip"><b>Od strony ciepłej potrzebna jest paroizolacja.</b> Bez niej para z domu skrapla się w wełnie, a ona przestaje izolować. Folię kupujesz osobno.</div>
<div class="tip"><b>Docinki przy belkach zjadają zapas.</b> Rozstaw belek rzadko jest idealnie równy. Zostaw zapas, a nie kupuj na styk.</div>
<p>Powiązane: <a href="/ocieplenie">ocieplenie ścian</a>, <a href="/dach">dach</a>, <a href="/wspolczynnik-u">współczynnik U ściany i dachu</a>.</p>
</main>''',
 script=_H+r'''function welnaCalc(dl,sz,prz,gr,m2o,zap){
  const A=Math.max(0,dl*sz-prz);
  const potrzeba=A*(1+zap/100);
  const opak=Math.ceil(potrzeba/m2o-1e-9);
  const razem=opak*m2o;
  const obj=potrzeba*gr/100;
  return {A,potrzeba,opak,razem,obj};
}
function licz(){
  const m2o=v("m2o");
  if(!(m2o>0)){$("wynik").innerHTML="Wpisz ilość m² w opakowaniu z karty produktu, większą od zera.";return;}
  const r=welnaCalc(v("dl"),v("sz"),v("prz"),v("gr"),m2o,v("zap"));
  $("wynik").innerHTML=`Powierzchnia stropu: <b>${f(r.A,2)} m²</b><br>Z zapasem na docinki: <b>${f(r.potrzeba,2)} m²</b><br>Opakowań do kupienia: <b>${r.opak} szt.</b><br>Razem w opakowaniach: ${f(r.razem,2)} m²<br>Objętość wełny z zapasem: <b>${f(r.obj,2)} m³</b><div class="mut">Wynik to szacunek. Grubość i współczynnik U sprawdź w projekcie. Paroizolacji nie wliczono.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)

CALC5['listwy-przypodlogowe']=dict(title='Listwy przypodłogowe: ile metrów kupić',
 desc='Ile metrów bieżących listew przypodłogowych kupić. Podaj wymiary pokoju, szerokość drzwi i długość listwy z karty produktu, a kalkulator doliczy zapas.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Listwy przypodłogowe: ile metrów kupić</h1>
<p class="lead">Podaj wymiary pokoju, liczbę drzwi i ich szerokość oraz długość listwy z karty produktu. Kalkulator policzy metry bieżące i liczbę sztuk z zapasem.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="dl">Długość pokoju (m)</label><input id="dl" type="number" value="4" min="0" step="0.1"></div>
<div><label for="sz">Szerokość pokoju (m)</label><input id="sz" type="number" value="3" min="0" step="0.1"></div>
<div><label for="nd">Liczba drzwi w obwodzie</label><input id="nd" type="number" value="1" min="0" step="1"></div>
<div><label for="szd">Szerokość jednych drzwi (m)</label><input id="szd" type="number" value="0.9" min="0" step="0.05"></div>
<div><label for="ld">Długość listwy z karty (m)</label><select id="ld"><option value="2">2,0</option><option value="2.5" selected>2,5</option><option value="3">3,0</option></select></div>
<div><label for="zap">Zapas na cięcia i narożniki (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
</div>
<p class="mut">Szerokość drzwi 0,9 m to przykład, wpisz wymiar swoich drzwi. Zapas 10 % to założenie, zwiększ go przy wielu narożnikach.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Obwód pokoju to dwa razy suma długości i szerokości. Od obwodu odejmujemy szerokości drzwi, bo tam listwy nie ma. Do wyniku dodajemy zapas na cięcia pod kątem 45 stopni w narożnikach. Liczbę listew zaokrąglamy w górę, według długości z karty.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Odejmij przejścia i drzwi, ale nie okna.</b> Pod oknem ściana zwykle też stoi przy podłodze, więc listwa biegnie dalej.</div>
<div class="tip"><b>Narożniki zjadają materiał.</b> Każde cięcie pod kątem 45 stopni coś kosztuje. Przy wielu narożnikach zostaw większy zapas.</div>
<div class="tip"><b>Listwa z tej samej kolekcji co podłoga.</b> Kolor i wykończenie bywają różne między kolekcjami, więc zamawiaj razem z panelami.</div>
<p>Powiązane: <a href="/panele-podlogowe">panele podłogowe: ile paczek</a>, <a href="/malowanie">malowanie ścian</a>, <a href="/wylewka">wylewka pod podłogę</a>.</p>
</main>''',
 script=_H+r'''function listwyCalc(dl,sz,nd,szd,ld,zap){
  const obw=2*(dl+sz);
  const mb=Math.max(0,obw-nd*szd);
  const zm=mb*(1+zap/100);
  const sztuk=Math.ceil(zm/ld-1e-9);
  return {obw,mb,zm,sztuk,razem:sztuk*ld};
}
function licz(){
  const ld=+$("ld").value;
  const r=listwyCalc(v("dl"),v("sz"),v("nd"),v("szd"),ld,v("zap"));
  $("wynik").innerHTML=`Obwód pokoju: <b>${f(r.obw,2)} m</b><br>Listwa bez drzwi: <b>${f(r.mb,2)} mb</b><br>Z zapasem: <b>${f(r.zm,2)} mb</b><br>Listew do kupienia: <b>${r.sztuk} szt.</b> po ${f(ld,1)} m, razem ${f(r.razem,1)} m<div class="mut">Wynik to szacunek. Długość listwy i zapas sprawdź w karcie produktu i na swoim rzucie.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)

CALC5['rynny']=dict(title='Rynny i rury spustowe: ile metrów kupić',
 desc='Ile rynny i rur spustowych kupić. Podaj długość okapu, rozstaw rur i wysokość pionów, a kalkulator policzy odcinki z zapasem na łączniki.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Rynny i rury spustowe: ile metrów kupić</h1>
<p class="lead">Podaj długość okapu, rozstaw rur spustowych i wysokość pionów. Kalkulator policzy odcinki rynny i rur z zapasem na łączniki.</p>
<section class="calc"><div class="panel">
<div class="grid">
<div><label for="ok">Długość okapu, czyli rynny (m)</label><input id="ok" type="number" value="12" min="0" step="0.1"></div>
<div><label for="roz">Rozstaw rur spustowych (m)</label><input id="roz" type="number" value="10" min="0.5" step="0.5"></div>
<div><label for="h">Wysokość pionu od rynny do gruntu (m)</label><input id="h" type="number" value="6" min="0" step="0.1"></div>
<div><label for="dlr">Długość odcinka rynny z karty (m)</label><select id="dlr"><option value="3">3,0</option><option value="4" selected>4,0</option></select></div>
<div><label for="dlp">Długość odcinka rury z karty (m)</label><select id="dlp"><option value="2">2,0</option><option value="3" selected>3,0</option></select></div>
<div><label for="zap">Zapas na łączniki i narożniki (%)</label><input id="zap" type="number" value="10" min="0" step="1"></div>
</div>
<p class="mut">Okap 12 m, rozstaw rur 10 m i wysokość 6 m to przykłady. Wpisz wymiary ze swojego rzutu i z projektu. Zapas 10 % to założenie.</p>
</div>
<div class="out" id="wynik" aria-live="polite"></div></section>
<h2>Jak liczymy</h2>
<p>Liczba pionów to okap podzielony przez rozstaw rur, zaokrąglony w górę, ale nie mniej niż jeden. Rynnę liczymy z zapasem na łączniki i narożniki, a potem dzielimy na odcinki z karty. Każdy pion to wysokość podzielona przez długość odcinka rury, w górę. Pionów mnożymy przez liczbę odcinków.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Rynna musi mieć spadek w stronę rury.</b> Bez spadku woda stoi w rynnie, zalega w łączeniach i z czasem przecieka.</div>
<div class="tip"><b>Piony trzeba postawić też w narożnikach.</b> Dodaj je tam, gdzie woda spływa z dwóch połaci, nawet jeśli wypadają blisko siebie.</div>
<div class="tip"><b>Woda z dachu musi odpłynąć od fundamentów.</b> Rury kończą się nad opaską albo odprowadzeniem. Zobacz <a href="/hydroizolacja-fundamentow">hydroizolację fundamentów</a>.</div>
<div class="tip"><b>Systemy PVC i metalowe mają inne odcinki i łączniki.</b> Sprawdź kartę wybranego systemu, zanim policzysz.</div>
<p>Powiązane: <a href="/dach">dach</a>, <a href="/ocieplenie">ocieplenie ścian</a>.</p>
</main>''',
 script=_H+r'''function rynnyCalc(ok,roz,h,dlr,dlp,zap){
  const n=ok>0?Math.max(1,Math.ceil(ok/roz-1e-9)):0;
  const rynnaMb=ok*(1+zap/100);
  const rynnaSzt=ok>0?Math.ceil(rynnaMb/dlr-1e-9):0;
  const pionSzt=h>0?Math.ceil(h/dlp-1e-9):0;
  const rurySzt=n*pionSzt;
  return {n,rynnaMb,rynnaSzt,pionSzt,rurySzt,ruryMb:n*h};
}
function licz(){
  const roz=v("roz");
  if(!(roz>0)){$("wynik").innerHTML="Wpisz rozstaw rur spustowych większy od zera.";return;}
  const dlr=+$("dlr").value, dlp=+$("dlp").value;
  const r=rynnyCalc(v("ok"),roz,v("h"),dlr,dlp,v("zap"));
  $("wynik").innerHTML=`Rynna z zapasem: <b>${f(r.rynnaMb,2)} mb</b>, czyli <b>${r.rynnaSzt} szt.</b> po ${f(dlr,1)} m<br>Piony rur spustowych: <b>${r.n} szt.</b><br>Rury: <b>${r.rurySzt} szt.</b> (na pion: ${r.pionSzt}, odcinki po ${f(dlp,1)} m), łącznie ${f(r.ruryMb,1)} mb<div class="mut">Wynik to szacunek. Rozstaw rur i spadek sprawdź w projekcie. Narożniki, uchwyty i denka liczy się osobno.</div>`;
}
document.querySelector("section.calc").addEventListener("input",licz);
document.querySelector("section.calc").addEventListener("change",licz);
licz();'''
)
