KONF={}
KONF['konfigurator-domu']=dict(title='Konfigurator domu 3D: koszt budowy elementów, materiał i robocizna',
 desc='Ustaw wymiary, dach, ściany i fundament. Model 3D rośnie etap po etapie, a kalkulator wycenia każdy element osobno: materiał i robocizna, z cenami aktualizowanymi co miesiąc.',
 main=r'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Kalkulatory</div>
<h1>Konfigurator domu: model 3D i koszt budowy</h1>
<p class="lead">Ustaw wymiary, dach, ściany i fundament. Model rośnie etap po etapie, a pod nim widzisz, ile kosztuje każdy element, osobno materiał i robocizna. Ceny jednostkowe pochodzą z naszej bazy, którą aktualizujemy co miesiąc.</p>
<section class="kfg">
<div class="panel" id="par">
<div class="grid">
<div><label for="dl">Długość domu (m)</label><input id="dl" type="number" min="6" max="30" step="0.1" value="12"></div>
<div><label for="sz">Szerokość domu (m)</label><input id="sz" type="number" min="5" max="18" step="0.1" value="9.5"></div>
<div><label for="kond">Kondygnacje</label><select id="kond"><option value="poddasze">Parter + poddasze</option><option value="parter">Parterowy</option><option value="pietro">Parter + piętro</option></select></div>
<div><label for="h">Wysokość kondygnacji (m)</label><input id="h" type="number" min="2.6" max="3.6" step="0.05" value="3"></div>
<div id="wKol"><label for="kol">Ścianka kolankowa (m)</label><input id="kol" type="number" min="0" max="2" step="0.1" value="1.2"></div>
<div><label for="dach">Dach</label><select id="dach"><option value="2">Dwuspadowy</option><option value="4">Czterospadowy</option></select></div>
<div><label for="kat">Kąt dachu (°)</label><input id="kat" type="number" min="15" max="50" step="1" value="38"></div>
<div><label for="okap">Okap (m)</label><input id="okap" type="number" min="0" max="1.2" step="0.1" value="0.6"></div>
<div><label for="pokr">Pokrycie</label><select id="pokr"><option value="blacho">Blachodachówka</option><option value="dachowka">Dachówka ceramiczna</option></select></div>
<div><label for="fund">Fundament</label><select id="fund"><option value="lawy">Ławy</option><option value="plyta">Płyta</option></select></div>
<div id="wHz"><label for="hz">Głębokość posadowienia (m)</label><input id="hz" type="number" min="0.8" max="1.6" step="0.1" value="1"></div>
<div><label for="sc">Ściany zewnętrzne</label><select id="sc"><option value="cer">Pustak 25 cm</option><option value="bk">Beton kom. 24 cm</option></select></div>
<div><label for="eps">Styropian na ścianach (cm)</label><input id="eps" type="number" min="5" max="30" step="1" value="15"></div>
<div><label for="okna">Okna (m², z projektu)</label><input id="okna" type="number" min="0" step="0.5" value="24"></div>
<div><label for="drzwi">Drzwi zewnętrzne (szt.)</label><input id="drzwi" type="number" min="0" max="6" step="1" value="1"></div>
<div><label for="wew">Ściany nośne wewnątrz (m na kondygnację)</label><input id="wew" type="number" min="0" step="0.5" placeholder="auto"></div>
<div><label for="zak">Zakres wyceny</label><select id="zak"><option value="sd">Stan deweloperski</option><option value="ssz">Surowy zamknięty</option><option value="sso">Surowy otwarty</option></select></div>
</div>
<p class="mut" id="ilosci"></p>
</div>
<figure class="panel fig model"><figcaption>Model budowy <span id="etapTxt"></span></figcaption>
<canvas id="model3d" aria-label="Model 3D domu budowanego etapami: fundamenty, ściany, stropy, więźba, pokrycie, okna i elewacja"></canvas>
<p id="brak3d" class="mut" hidden>Twoja przeglądarka nie wyświetla grafiki 3D. Wycena poniżej działa bez modelu.</p>
<div class="etapy noprint"><input id="etap" type="range" min="0" max="8" step="1" value="8" aria-label="Etap budowy"><button class="btn" id="graj" type="button">Pokaż budowę od początku</button></div>
<p class="note">Przeciągnij, żeby obrócić. Najedź na wiersz tabeli, żeby podświetlić element. Model pokazuje proporcje i kolejność prac, bez detali.</p>
</figure>
</section>
<div class="out" id="wynik" aria-live="polite">Wczytuję ceny…</div>
<h2>Koszt elementów</h2>
<div id="tab" class="scrollx"></div>
<details id="cenyD"><summary>Ceny jednostkowe: wpisz swoje</summary><p class="mut">Ceny z bazy Budlicz: <span id="baza"></span>. Pełna lista ze źródłami jest w <a href="/ceny-budowlane">cenniku materiałów i robocizny</a>. Zmiany działają tylko w Twojej przeglądarce.</p><div id="cenyTab"></div></details>
<h2>Czego konfigurator nie liczy</h2>
<ul>
<li>Projektu, adaptacji, pozwoleń, geodety i kierownika budowy.</li>
<li>Przyłączy: prądu, wody, kanalizacji lub szamba, gazu.</li>
<li>Schodów, kominów, ścianek działowych na poddaszu, parapetów, obróbek blacharskich i okien dachowych.</li>
<li>Wykończenia: podłóg, łazienek, drzwi wewnętrznych, malowania i kuchni.</li>
<li>Zagospodarowania działki: ogrodzenia, podjazdu, tarasu.</li>
</ul>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Cena za metr z internetu to nie cena Twojego domu.</b> Liczba podawana „za m²” ukrywa kształt, dach i zakres prac. Dom o tej samej powierzchni z piętrem ma mniejszy dach i fundament, ale więcej ścian i drugi strop. Zmień kondygnacje w konfiguratorze i zobacz, co się przesuwa.</div>
<div class="tip"><b>Stan deweloperski to nie koniec wydatków.</b> Po nim zostają podłogi, łazienki, drzwi wewnętrzne, malowanie i kuchnia. Policz je osobno, zanim ustalisz kwotę kredytu.</div>
<div class="tip"><b>Prosta bryła jest tańsza.</b> Każdy narożnik, wykusz i lukarna to dodatkowe ściany, obróbki i godziny pracy dekarza. Konfigurator liczy prostokąt, więc przy bardziej złożonej bryle koszt będzie wyższy.</div>
<div class="tip"><b>Ceny się zmieniają.</b> Dlatego baza ma datę i źródła, a my odświeżamy ją co miesiąc. Do decyzji weź oferty z Twojej okolicy i wpisz je w tabeli cen.</div>
<details><summary>Jak liczymy</summary>
<p>Ilości liczymy z wymiarów zewnętrznych ścian. Powierzchnia podłóg to wnętrze ścian zewnętrznych na każdej kondygnacji. Na poddaszu pokazujemy dodatkowo, ile podłogi ma wysokość co najmniej 2,2 m i od 1,4 do 2,2 m, licząc od ścianki kolankowej i kąta dachu, bez grubości ocieplenia.</p>
<p>Przyjęte założenia, które zmieni dopiero projekt: ławy 60 × 40 cm pod ścianami zewnętrznymi i jedną ścianą wewnętrzną, ściana fundamentowa do 30 cm nad terenem, wykop o szerokości 1 m. Płyta ma 25 cm betonu na 20 cm polistyrenu XPS. Stal: 70 kg na m³ ław i 90 kg na m³ płyty, jak w <a href="/beton">kalkulatorze betonu i stali</a>. Wieńce 25 × 25 cm z czterema prętami Ø12 i strzemionami Ø6 co 25 cm, czyli 4,35 kg stali na metr. Nadproża to dwie belki po 1,75 m na każdy otwór, a liczbę okien liczymy przy średnim oknie 1,6 m². Podłoga na gruncie: 10 cm chudego betonu i 15 cm styropianu. Poddasze: 25 cm wełny i zabudowa z płyt GK. Strop pod nieużytkowym dachem: 30 cm wełny.</p>
<p>Zapas pokrycia to 7% na dachu dwuspadowym i 12% na czterospadowym, a membrany 10%, jak w <a href="/dach">kalkulatorze dachu</a>. Do styropianu na ściany doliczamy 5% na docinki. Instalacje liczymy według powierzchni podłóg, z cen podawanych razem z materiałem, więc nie dzielimy ich na materiał i robociznę.</p>
<p>Każda cena w bazie to mediana z kilku źródeł z podanej daty. Zakres w wyniku liczymy z najniższych i najwyższych cen w bazie. Szczegóły i źródła są w <a href="/ceny-budowlane">cenniku</a>.</p>
</details>
<p>Powiązane: <a href="/etapy-budowy">etapy budowy krok po kroku</a>, <a href="/harmonogram">harmonogram budowy</a>, <a href="/kredyt">kredyt na budowę</a>, <a href="/vat-budowa">VAT 8% czy 23%</a>.</p>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="/js/konfigurator.js" defer></script>
</main>''',
 script='')
