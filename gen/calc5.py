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
