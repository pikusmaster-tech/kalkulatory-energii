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
