GUIDE={}
_short=["Projekt","Wykop","Fundamenty","Ściany","Mury","Dach","Stolarka","Instalacje","Tynki","Odbiór"]
_steps=[("Projekt i formalności","Projekt architektoniczno-budowlany i konstrukcyjny, badanie gruntu, uzgodnienia. Tryb pozwolenia albo zgłoszenia zależy od rodzaju budowy i lokalizacji, więc sprawdź go w urzędzie przed wyborem.",None),
("Tyczenie i wykop","Geodeta wyznacza kontur budynku względem granic działki. Potem wykop. Objętość i liczbę kursów policzysz w kalkulatorze ziemi.","/wykop"),
("Fundamenty i izolacja","Ławy albo płyta, izolacja przeciwwilgociowa i termiczna. Fundament to etap, którego nie da się nadrobić później.","/beton"),
("Ściany fundamentowe i strop","Ściany fundamentowe, potem strop nad piwnicą lub parterem. Rodzaj stropu wybierany jest już w projekcie.","/strop"),
("Mury i nadproża","Ściany z pustaków albo bloczków. Nad otworami nadproża, których nie zastępuje się przypadkowym elementem.","/nadproza"),
("Dach","Więźba albo konstrukcja, pokrycie, membrana i rynny. Dach zamyka budynek przed deszczem, więc robi się go szybko po murach.","/dach"),
("Stolarka i zamknięcie budynku","Okna i drzwi zewnętrzne. Kolejność montażu wynika z projektu i wykonawcy. Nie ma jednej, właściwej dla każdego domu.",None),
("Instalacje pod tynkami","Woda, kanalizacja, prąd i ogrzewanie wykonywane przed tynkami i wylewkami. Poprawki po tynku kosztują więcej niż robota wykonana dobrze za pierwszym razem.",None),
("Ocieplenie, tynki i wylewki","Ocieplenie ścian i tynki zewnętrzne, wylewka wewnątrz. Wylewka schnie długo i nie kładzie się na niej podłogi przed sprawdzeniem wilgotności.","/ocieplenie"),
("Wykończenie i odbiór","Podłogi, łazienki, malowanie, schody. Na końcu odbiór techniczny i komplet dokumentów, bez których trudno sprzedać albo zmienić dom.","/schody")]
def _timeline():
    n=len(_steps); x0=40; x1=600; y=64; out=[]
    out.append(f'<path class="strzem draw" pathLength="1" d="M{x0} {y}H{x1}"/>')
    for i,(t,_,_) in enumerate(_steps):
        cx=x0+i*(x1-x0)/(n-1)
        out.append(f'<circle class="rura pop" style="animation-delay:{i*60}ms" cx="{cx:.1f}" cy="{y}" r="14"/>')
        out.append(f'<text x="{cx:.1f}" y="{y+4}" text-anchor="middle" style="fill:#fff;font:700 12px Inter,sans-serif">{i+1}</text>')
        ly=y-30 if i%2==0 else y+40
        out.append(f'<text class="tm" x="{cx:.1f}" y="{ly}" text-anchor="middle">{_short[i]}</text>')
    return ''.join(out)
_li=''
for i,(t,txt,link) in enumerate(_steps):
    _nazwy={'/wykop':'ziemia z wykopu','/beton':'beton i stal','/strop':'strop','/nadproza':'nadproża','/dach':'dach','/ocieplenie':'ocieplenie ścian','/schody':'schody'}
    _rola='Poradnik' if link=='/nadproza' else 'Kalkulator'
    lk=f' {_rola}: <a href="{link}">{_nazwy.get(link,link.strip("/"))}</a>.' if link else ''
    _li+=f'<li><b>{t}.</b> {txt}{lk}</li>\n'
GUIDE['etapy-budowy']=dict(title='Etapy budowy domu krok po kroku',
 desc='Dziesięć etapów budowy domu w typowej kolejności, od projektu do odbioru. Przy każdym etapie wskazuję, który kalkulator policzy materiały.',
 main=f'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Poradniki</div>
<h1>Etapy budowy domu krok po kroku</h1>
<p class="lead">Dziesięć etapów w typowej kolejności, od projektu do odbioru. Przy każdym etapie wskazuję, który kalkulator policzy materiały dla tej części.</p>
<figure class="panel fig"><figcaption>Oś czasu <span>kolejność jest typowa, etapy się nakładają</span></figcaption>
<svg viewBox="0 0 640 120" role="img" aria-label="Oś czasu budowy domu: dziesięć etapów od projektu do odbioru">{_timeline()}</svg>
<p class="note">Przy każdym etapie kolejność może się przesunąć, zależnie od pogody, dostaw i wykonawcy.</p></figure>
<h2>Kolejność i co w niej ważne</h2>
<ol class="kroki">
{_li}</ol>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Płać za odebrany etap, nie za obietnicę.</b> Zaliczka na początku jest zwykła, ale większa część pieniędzy powinna iść za wykonaną i sprawdzoną pracę.</div>
<div class="tip"><b>Instalacje zanim tynki.</b> Bruzdy i przejścia wykonane po tynku są widoczne i kosztowne. Zdjęcia zakrytych instalacji zrób przed zamknięciem.</div>
<div class="tip"><b>Wilgoć w wylewce.</b> Nie zamawiaj wszystkiego naraz. Materiały stojące w wilgoci i przy świeżym tynku tracą jakość, a wylewka wymaga czasu na wyschnięcie.</div>
<div class="tip"><b>Dokumenty też są etapem.</b> Dziennik budowy, protokoły odbiorów i karty materiałów wracają do ciebie przy sprzedaży albo zmianie domu.</div>
<p>Materiały policzysz w kalkulatorach z menu: <a href="/beton">beton i stal</a>, <a href="/sciany">ściany</a>, <a href="/dach">dach</a>, <a href="/wylewka">wylewka</a>. Kiedy który etap wypadnie w kalendarzu i do kiedy zamówić okna, pokaże <a href="/harmonogram">harmonogram budowy</a>.</p>
</main>''')

GUIDE['hydroizolacja-fundamentow']=dict(title='Hydroizolacja fundamentów: wilgoć czy woda',
 desc='Różnica między izolacją przeciwwilgociową a przeciwwodną, izolacja pozioma pod ścianą i drenaż opaskowy. Co sprawdzić przed zamówieniem.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Poradniki</div>
<h1>Hydroizolacja fundamentów: wilgoć czy woda gruntowa</h1>
<p class="lead">To dwa różne problemy i dwie różne izolacje. Zanim zamówisz materiał, ustal, z którym masz do czynienia.</p>
<figure class="panel fig"><figcaption>Ściana fundamentowa <span>schemat przekroju</span></figcaption>
<svg viewBox="0 0 640 300" role="img" aria-label="Przekrój ściany fundamentowej: izolacja pionowa i pozioma, termoizolacja, drenaż i opaska">
<rect class="grunt" x="0" y="90" width="640" height="210"/><rect class="grunt2" x="0" y="90" width="640" height="5"/>
<rect class="mur" x="250" y="40" width="66" height="170"/>
<rect class="beton" x="230" y="210" width="106" height="32" rx="2"/>
<rect class="xps" x="318" y="90" width="12" height="118"/>
<rect class="jastrych" x="332" y="84" width="58" height="6"/>
<rect class="chudy" x="332" y="214" width="36" height="28"/>
<circle cx="350" cy="228" r="7" fill="#495057"/>
<path class="hydro draw" pathLength="1" d="M316 90V210"/>
<path class="hydro draw" pathLength="1" d="M250 210H316"/>
<text class="tm" x="20" y="84">teren</text>
<text class="tm" x="20" y="196">izolacja pozioma pod ścianą</text><path class="dim" d="M150 200L246 209"/>
<text class="tm" x="20" y="262">ława</text><path class="dim" d="M80 258H228"/>
<text class="tm" x="410" y="66">opaska</text><path class="dim" d="M392 84L404 72"/>
<text class="tm" x="410" y="132">termoizolacja</text><path class="dim" d="M330 128H402"/>
<text class="tm" x="410" y="162">izolacja pionowa</text><path class="dim" d="M332 158H402"/>
<text class="tm" x="410" y="262">drenaż w żwirze</text><path class="dim" d="M357 236L402 256"/>
</svg>
<p class="note">Schemat poglądowy. Układ warstw, grubości i rodzaje mat określa projekt i karta producenta.</p></figure>
<h2>Dwa przypadki</h2>
<div class="tip"><b>Wilgoć z gruntu.</b> Grunt jest wilgotny, ale woda nie stoi przy ścianie. Wystarcza izolacja przeciwwilgociowa, zwykle bitumiczna albo polimerowa, nałożona na ścianę fundamentową od zewnątrz.</div>
<div class="tip"><b>Woda gruntowa albo woda stojąca przy domu.</b> Woda naciska na ścianę, więc potrzebna jest izolacja przeciwwodna i drenaż. O tym, która wersja jest potrzebna, decyduje badanie gruntu i poziom wód.</div>
<h2>Co zawsze robi się przy ścianie fundamentowej</h2>
<ul>
<li><b>Izolacja pozioma pod ścianą.</b> Warstwa, która odcina podciąganie wilgoci z ławy do muru. Ściana stoi na niej, nie bezpośrednio na betonie.</li>
<li><b>Izolacja pionowa na zewnątrz.</b> Ciągła, bez przerw, doprowadzona do poziomu gruntu i połączona z izolacją poziomą.</li>
<li><b>Ochrona izolacji przy zasypce.</b> Płyta drenażowa albo geowłóknina chroni izolację przed kamieniami i sprzętem podczas zasypywania.</li>
<li><b>Drenaż opaskowy.</b> Rura perforowana w żwirze, z odpływem grawitacyjnym albo do studzienki. Drenaż bez odpływu tylko gromadzi wodę.</li>
</ul>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Izolacja pozioma i pionowa to dwie różne rzeczy.</b> Jedna nie zastępuje drugiej. Pionowa bez poziomej zostawia drogę dla wilgoci w murze.</div>
<div class="tip"><b>Drenaż bez spadku nie działa.</b> Rura musi mieć spadek i miejsce, w którym woda może odpłynąć. Zakopana bez odpływu tylko się zapycha.</div>
<div class="tip"><b>Jeden odwiert to nie cała działka.</b> Grunt zmienia się na niewielkich odległościach. Badanie geotechniczne przed projektem to standard, którego warto się trzymać.</div>
<p>Powiązane kalkulatory: <a href="/beton">beton i stal na ławy</a>, <a href="/lawy-czy-plyta">ławy czy płyta</a>, <a href="/wykop">ziemia z wykopu</a>.</p>
</main>''')

GUIDE['nadproza']=dict(title='Nadproża: co je nosi i jak je dobrać',
 desc='Jak działa nadproże nad oknem i drzwiami, jakie są typy i co sprawdzić przed zamówieniem: rozpiętość, obciążenie i oparcie.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Poradniki</div>
<h1>Nadproża nad oknami i drzwiami</h1>
<p class="lead">Nadproże przenosi obciążenie ze ściany nad otworem na ściany po bokach. Typ dobiera się do rozpiętości, obciążenia i systemu murowania.</p>
<figure class="panel fig"><figcaption>Otwór w ścianie <span>schemat</span></figcaption>
<svg viewBox="0 0 640 300" role="img" aria-label="Schemat: ciężar z góry przechodzi łukiem nad otworem na ściany po bokach, a nadproże opiera się na ścianach po obu stronach otworu">
<rect class="mur" x="120" y="40" width="400" height="220"/>
<path class="lukob draw" pathLength="1" d="M200 96Q320 6 440 96"/>
<rect class="otwor" x="240" y="122" width="160" height="138"/>
<text class="tm" x="320" y="196" text-anchor="middle">okno lub drzwi</text>
<rect class="beton" x="220" y="100" width="200" height="22" rx="2"/>
<path class="sila" d="M190 4V34M184 28L190 36L196 28M320 4V34M314 28L320 36L326 28M450 4V34M444 28L450 36L456 28"/>
<text class="t" x="470" y="20">ciężar z góry</text>
<text class="tm halo" x="528" y="70">łuk przenosi</text>
<text class="tm halo" x="528" y="84">ciężar na ściany</text>
<text class="tm halo" x="528" y="98">po bokach</text>
<path class="dim" d="M526 92L446 94"/>
<text class="tm halo" x="20" y="116">nadproże</text><path class="dim" d="M110 112H218"/>
<path class="dim" d="M220 136H240M220 132V140M240 132V140M400 136H420M400 132V140M420 132V140"/>
<text class="tm halo" x="216" y="152" text-anchor="end">oparcie</text>
<text class="tm halo" x="424" y="152">oparcie</text>
<text class="tm halo" x="446" y="206">ściana</text>
<path class="dim" d="M240 268H400M240 262V274M400 262V274"/>
<text class="tm" x="320" y="290" text-anchor="middle">światło otworu</text>
</svg>
<p class="note">Schemat poglądowy. Strzałki to ciężar z góry, granatna linia to łuk, który przenosi go na ściany po bokach. Szare linie z opisem to wymiary. Wymiary i typ nadproża wpisuje projekt konstrukcyjny.</p></figure>
<h2>Jak działa nadproże</h2>
<p>Nad otworem ściana nie wisi cała na nadprożu. Dzięki wiązaniu cegieł ciężar muru przechodzi łukowo na słupy po bokach otworu, czyli na granatną linię na schemacie. Nadproże bierze na siebie to, co leży bezpośrednio na nim, na przykład belkę stropu opartą na ścianie nad oknem. Dlatego jego oparcie musi być solidne, a długość oparcia podaje projekt.</p>
<h2>Typy</h2>
<ul>
<li><b>Prefabrykowane belki.</b> Szybki montaż, a nośność i wymiary podaje karta producenta. Montuje się je dokładnie tak, jak opisano.</li>
<li><b>Wylewane na miejscu.</b> Żelbetowe, na deskowaniu, zbrojone według projektu. Wymagają czasu na związanie przed obciążeniem.</li>
<li><b>Nadproże w wieńcu.</b> W systemach, gdzie wieniec żelbetowy obejmuje cały obwód budynku, nadproże jest jego częścią.</li>
</ul>
<h2>Co sprawdzić przed zamówieniem</h2>
<ul>
<li>Rozpiętość światła otworu i obciążenie nad nim: strop, dach, inne ściany.</li>
<li>Długość oparcia po obu stronach. Wartość bierze się z karty producenta albo z projektu, nie z wyczucia.</li>
<li>Czy nadproże jest w projekcie. Dobór „na oko” prowadzi do błędu, którego na budowie zwykle nie widać od razu.</li>
</ul>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Nie skracaj oparcia na budowie.</b> Jeśli brakuje kilku centymetrów, nie kombinuj na miejscu. Zmianę elementu albo wymiaru otworu uzgodnij z projektantem.</div>
<div class="tip"><b>Sama wysokość muru to za mało.</b> Liczy się szerokość otworu i obciążenie z góry: strop, dach, belki, które się na tym opierają. Wysoki mur nad otworem nie wystarcza do doboru nadproża.</div>
<div class="tip"><b>Ocieplenie nad nadprożem.</b> Nadproże bywa mostkiem termicznym. Projekt energetyczny często wymaga dodatkowej izolacji w tym miejscu.</div>
<p>Powiązane: <a href="/sciany">kalkulator pustaków na ściany</a>, <a href="/strop">strop: monolit czy gęstożebrowy</a>.</p>
</main>''')

GUIDE['dylatacje']=dict(title='Dylatacje w ścianach i posadzkach: gdzie je robić',
 desc='Po co robi się dylatacje, gdzie są potrzebne w ścianach i posadzkach i czym różnią się od przypadkowych pęknięć. Schematy dla obu przypadków.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Poradniki</div>
<h1>Dylatacje: po co je robić i gdzie</h1>
<p class="lead">Dylatacja to celowo zostawiona przerwa, w której konstrukcja może pracować. Bez niej beton, mur i posadzka pękają w przypadkowych miejscach.</p>
<figure class="panel fig"><figcaption>Dwa przypadki <span>schematy poglądowe</span></figcaption>
<div class="figs2">
<div><svg viewBox="0 0 320 220" role="img" aria-label="Długa ściana z przerwami dylatacyjnymi"><rect class="mur" x="20" y="100" width="280" height="40"/><rect class="eps" x="118" y="88" width="6" height="64"/><rect class="eps" x="218" y="88" width="6" height="64"/><text class="tm" x="20" y="78">ściana z dylatacjami</text><text class="tm" x="20" y="170">odcinki ścian między przerwami</text></svg></div>
<div><svg viewBox="0 0 320 220" role="img" aria-label="Plan posadzki z polami dylatacyjnymi i taśmą przy ścianach"><rect class="jastrych" x="20" y="30" width="280" height="170"/><path d="M160 30V200M20 115H300" stroke="#8f8a80" stroke-width="2" stroke-dasharray="6 4" fill="none"/><rect x="20" y="30" width="280" height="4" fill="#7950f2"/><rect x="20" y="30" width="4" height="170" fill="#7950f2"/><text class="tm halo" x="170" y="70">pole dylatacyjne</text><text class="tm halo" x="26" y="222">taśma przy ścianie</text></svg></div>
</div>
<p class="note">Schematy poglądowe. Rozstaw i położenie dylatacji wpisuje projekt konstrukcyjny lub karta systemu posadzki.</p></figure>
<h2>Gdzie dylatujemy</h2>
<ul>
<li><b>Długie ściany.</b> Przerwa dzieli ścianę na krótsze odcinki, a projekt podaje ich maksymalną długość.</li>
<li><b>Narożniki i zmiany wysokości.</b> Ściana wyższa obok niższej pracuje inaczej, więc w miejscu zmiany robi się przerwę.</li>
<li><b>Połączenia różnych materiałów.</b> Beton z murem, mur z drewnem, ściana z kominem. Każdy materiał ma inną pracę pod temperaturą i wilgocią.</li>
<li><b>Posadzki.</b> Szczeliny przy ścianach i słupach, a na dużych polach dodatkowe przerwy według projektu wylewki.</li>
</ul>
<h2>Co z taśmą przy wylewce</h2>
<p>Taśma dylatacyjna przy ścianach odcina wylewkę od muru i pozwala jej pracować. Montuje się ją przed wylewaniem. Przycina się ją dopiero po położeniu wykończenia, zgodnie z kartą systemu.</p>
<h2>Na czym ludzie się mylą</h2>
<div class="tip"><b>Dylatacja to przerwa zaplanowana w projekcie. Pęknięcie to przypadek, dylatacja to plan.</b> Nie zalewaj jej sztywnym materiałem, jeśli projekt wymaga elastycznego wypełnienia. Sztywne wypełnienie przenosi naprężenia i pęka obok.</div>
<div class="tip"><b>Nie każde pęknięcie to brak dylatacji.</b> Drobne rysy włoskowate w tynku są zwykle skurczowe. Pęknięcie na całą grubość trzeba sprawdzić i ocenić, zanim cokolwiek zamalujesz.</div>
<p>Powiązane: <a href="/wylewka">kalkulator wylewki</a>, <a href="/sciany">ściany z pustaków</a>, <a href="/beton">beton i stal</a>.</p>
</main>''')

GUIDE['o-serwisie']=dict(title='O serwisie Budlicz',
 desc='Czym jest Budlicz, kto go prowadzi, jak powstają kalkulatory i poradniki oraz jak traktować wyniki.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › O serwisie</div>
<h1>O serwisie Budlicz</h1>
<p class="lead">Budlicz to zbiór kalkulatorów i poradników o budowie domu. Kalkulatory liczą materiały i koszty z wymiarów, które wpisujesz. Poradniki opisują kolejność prac i typowe błędy.</p>
<h2>Jak powstają treści</h2>
<p>Teksty i kalkulatory przygotowuje Claude, model AI firmy Anthropic, na podstawie publicznie dostępnych źródeł: norm, kart technicznych producentów i ogólnodostępnych poradników. Nie każdy wzór i każda liczba są sprawdzane przez inżyniera.</p>
<h2>Jak traktować wyniki</h2>
<p>Wyniki to szacunki do planowania i rozmowy z wykonawcą. Wiążący jest zawsze projekt konstrukcyjny i wycena wykonawcy. Ceny w kalkulatorach są przykładowe. Wpisz ceny z konkretnej oferty.</p>
<p>Przepisy, normy i stawki zmieniają się. Aktualizujemy treści, gdy zauważymy zmianę. Jeśli coś jest nieaktualne, to błąd i warto go zgłosić.</p>
<h2>Z czego serwis się utrzymuje</h2>
<p>Planujemy reklamy oraz linki partnerskie do ofert kredytów i sklepów z materiałami. Każdy taki link będzie oznaczony jako partnerski. Wyniki kalkulatorów nie zależą od tego, kto płaci.</p>
<h2>Dane operatora</h2>
<p>Serwis Budlicz prowadzi 3D Automation spółka z ograniczoną odpowiedzialnością z siedzibą w Nikielkowie, ul. Tęczowa 13, 10-376 Nikielkowo, wpisana do rejestru przedsiębiorców KRS pod numerem 0000632953, NIP 7393888019, REGON 365190756, kapitał zakładowy 5 000 zł.</p>
<p>Adres e-mail do kontaktu dodamy tutaj po uruchomieniu skrzynki. Do tego czasu napisz na adres siedziby spółki.</p>
</main>''')

GUIDE['polityka-prywatnosci']=dict(title='Polityka prywatności Budlicz',
 desc='Jakie dane zostają w przeglądarce, jakie trafiają do zewnętrznych usług Cloudflare i Google, kto jest administratorem i jakie masz prawa.',
 main='''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › Polityka prywatności</div>
<h1>Polityka prywatności</h1>
<p class="lead">Ta strona opisuje, jakie dane zostają w Twojej przeglądarce, jakie trafiają do zewnętrznych usług i co możesz z tym zrobić. Ostatnia aktualizacja: 17.10.2026.</p>

<h2>Kto odpowiada za dane</h2>
<p>Administratorem danych w serwisie Budlicz jest 3D Automation spółka z ograniczoną odpowiedzialnością z siedzibą w Nikielkowie, ul. Tęczowa 13, 10-376 Nikielkowo, wpisana do rejestru przedsiębiorców KRS pod numerem 0000632953, NIP 7393888019, REGON 365190756.</p>

<h2>Co zostaje w przeglądarce</h2>
<p>Serwis nie ma kont, formularzy ani logowania. Wartości wpisane w kalkulatorach nie są nigdzie wysyłane. Zostają w przeglądarce i znikają po odświeżeniu albo zamknięciu strony.</p>
<p>Kod serwisu nie ustawia własnych plików cookies i nie zapisuje niczego w pamięci przeglądarki (localStorage ani sessionStorage).</p>

<h2>Co dzieje się przy wejściu na stronę</h2>
<p>Strony są dostarczane przez Cloudflare, który obsługuje domenę. Cloudflare przetwarza adres IP i dane techniczne żądania, żeby dostarczyć stronę i chronić ją przed nadużyciami. Może też ustawić techniczne pliki cookies związane z bezpieczeństwem, na przykład __cf_bm. Są one niezbędne do działania i bezpieczeństwa usługi, dlatego nie wymagają zgody. Szczegóły znajdziesz w <a href="https://www.cloudflare.com/privacypolicy/">polityce prywatności Cloudflare</a>.</p>
<p>Operator nie prowadzi własnych logów odwiedzin i nie korzysta z narzędzi analitycznych.</p>

<h2>Czcionki Google</h2>
<p>Strony wczytują kroje pisma z Google Fonts (fonts.googleapis.com i fonts.gstatic.com). Przeglądarka wysyła wtedy do Google adres IP i dane o sobie. Zasady opisuje <a href="https://policies.google.com/privacy">polityka prywatności Google</a>.</p>

<h2>Model 3D na stronie o dachu</h2>
<p>Strona o dachu wczytuje bibliotekę do rysowania 3D z cdnjs.cloudflare.com. Zasady są takie same jak dla Cloudflare: przetwarzany jest adres IP potrzebny do pobrania pliku.</p>

<h2>Linki do innych stron</h2>
<p>Serwis zawiera linki do stron zewnętrznych. Po przejściu na nie obowiązują zasady tamtych serwisów. Przyciski „link partnerski” nie prowadzą jeszcze nigdzie. Gdy partner zostanie podłączony, jego strona może ustawić własne pliki cookies.</p>

<h2>Reklamy i linki partnerskie: plan</h2>
<p>Serwis nie wyświetla dziś reklam. Planowane są reklamy Google AdSense oraz linki partnerskie do ofert kredytów i sklepów z materiałami. Gdy je uruchomimy, zaktualizujemy tę stronę. Reklamowe pliki cookies będą ustawiane tylko po wyrażeniu zgody w banerze, a bez zgody nie zostaną włączone.</p>

<h2>Twoje prawa</h2>
<p>Masz prawo dostępu do swoich danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, sprzeciwu i przenoszenia. Masz też prawo złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych. Operator nie prowadzi własnych logów odwiedzin, więc większość danych technicznych opisanych wyżej przetwarzają Cloudflare i Google, a nie operator.</p>

<h2>Kontakt w sprawach danych</h2>
<p>Pytania o dane wyślij na adres: 3D Automation sp. z o.o., ul. Tęczowa 13, 10-376 Nikielkowo. Adres e-mail do tych spraw dodamy tutaj po uruchomieniu skrzynki. Odpowiadamy najpóźniej w ciągu miesiąca.</p>

<h2>Zmiany tej polityki</h2>
<p>Jeśli zmienimy sposób działania serwisu, zaktualizujemy tę stronę i datę na początku.</p>
</main>''')
