import re, glob, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import lib2, calc2, guides2, calc3, calc4, calc5, konfigurator, cennik
from lib2 import BASE, page, CLOSE_JS, header
NEW={}
for k,p in calc2.CALC.items(): NEW[k]=(p['title'],p['desc'],p['main'],p['script'])
for k,p in calc3.CALC3.items(): NEW[k]=(p['title'],p['desc'],p['main'],p['script'])
for k,p in calc4.CALC4.items(): NEW[k]=(p['title'],p['desc'],p['main'],p['script'])
for k,p in calc5.CALC5.items(): NEW[k]=(p['title'],p['desc'],p['main'],p['script'])
for k,p in guides2.GUIDE.items(): NEW[k]=(p['title'],p['desc'],p['main'],'')
for k,p in konfigurator.KONF.items(): NEW[k]=(p['title'],p['desc'],p['main'],p['script'])
for k,p in cennik.CENNIK.items(): NEW[k]=(p['title'],p['desc'],p['main'],p['script'])
for k,(t,d,m,sc) in NEW.items():
    open(BASE+k+'.html','w',encoding='utf-8').write(page('/'+k,t,d,m,sc))
print('new pages', len(NEW))
# existing pages: nav, footer, close-js
EXIST=['beton','sciany','dach','wylewka','lawy-czy-plyta','fotowoltaika','pompa-ciepla','pompa-ciepla-stary-dom','strop','kredyt']
for name in EXIST:
    p=BASE+name+'.html'; s=open(p,encoding='utf-8').read()
    s=re.sub(r'<header class="top">.*?</header>',lambda m:header('/'+name),s,count=1,flags=re.S)
    if 'o-serwisie' not in s:
        s=s.replace('<span><a href="/">Wszystkie kalkulatory</a></span>','<span><a href="/o-serwisie">O serwisie</a> · <a href="/">Wszystkie kalkulatory</a></span>',1)
    if 'grp[open]' not in s:
        s=s.replace('</script>\n</body>', CLOSE_JS+'\n</script>\n</body>',1)
    open(p,'w',encoding='utf-8').write(s); print('updated', name)
# index
old=open(BASE+'index.html',encoding='utf-8').read()
i0=old.index('<section class="hero">'); i1=old.index('</section>',i0)+len('</section>')
hero=old[i0:i1]
tiles={}
for full,href in re.findall(r'(<a class="tile" href="(/[^"]+)">.*?</a>)',old,flags=re.S): tiles[href]=full
NEWTILES={
 '/schody':('Konstrukcja','Schody: ile stopni','Liczba stopni, wysokość i szerokość stopnia, długość biegu, reguła 2h + s.','<path d="M3 19h4v-4h4v-4h4V7h4"/>'),
 '/wykop':('Fundamenty','Ziemia z wykopu','Objętość wykopu, ilość ziemi po spulchnieniu i liczba kursów wywozu.','<path d="M3 6h18M5 6l3 12h8l3-12"/>'),
 '/ocieplenie':('Ściany i dach','Ocieplenie ścian','Płyty styropianu z zapasem, klej, dyble i przekrój warstw ściany.','<path d="M3 7h18M3 12h18M3 17h18"/>'),
 '/sciana-dzialowa':('Ściany i dach','Ścianka z płyt GK','Płyty, słupki, prowadnice i wełna na ściankę działową.','<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M9 4v16M15 4v16"/>'),
 '/kostka':('Wykończenie i teren','Kostka i płytki','Metry kwadratowe z zapasem, liczba elementów, podbudowa i plan układu.','<path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/>'),
 '/ogrodzenie':('Wykończenie i teren','Ogrodzenie','Przęsła, słupki i beton pod fundamenty dla zadanej długości granicy.','<path d="M5 5v15M12 5v15M19 5v15M3 10h18M3 16h18"/>'),
 '/etapy-budowy':('Plan budowy','Etapy budowy krok po kroku','Dziesięć etapów w typowej kolejności, od projektu do odbioru.','<circle cx="6" cy="12" r="2.5"/><circle cx="12" cy="12" r="2.5"/><circle cx="18" cy="12" r="2.5"/><path d="M8.5 12h1M14.5 12h1"/>'),
 '/hydroizolacja-fundamentow':('Fundamenty','Hydroizolacja fundamentów','Wilgoć czy woda gruntowa, izolacja pozioma, drenaż opaskowy.','<path d="M12 3c3 4 6 7 6 11a6 6 0 0 1-12 0c0-4 3-7 6-11z"/>'),
 '/nadproza':('Konstrukcja','Nadproża','Jak działa nadproże, typy i co sprawdzić: rozpiętość, obciążenie, oparcie.','<path d="M3 7h18M5 7v12M19 7v12"/>'),
 '/wspolczynnik-u':('Ściany i dach','Współczynnik U ściany i dachu','Ułóż warstwy przegrody i sprawdź U, wymaganie WT 2021 i spadek temperatury w ścianie.','<path d="M10 14V5a2 2 0 0 1 4 0v9a4 4 0 1 1-4 0z"/><path d="M12 11v6"/>'),
 '/harmonogram':('Plan budowy','Harmonogram budowy','Etapy na osi czasu od wybranego miesiąca, termin zamówienia okien i prace mokre zimą.','<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M7 14h5M10 17h6"/>'),
 '/vat-budowa':('Plan budowy','VAT 8% czy 23%','Stawka VAT na budowę domu, limit 300 m² i ile kosztuje kupowanie materiałów samemu.','<path d="M19 5 5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>'),
 '/kosztorys':('Dla firm','Kosztorys ofertowy','Pozycje z nakładami, stawka r-g, narzuty, zysk i VAT. Tabela do oferty, do Excela i do druku.','<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>'),
 '/rozkroj-pretow':('Dla firm','Rozkrój prętów','Zestawienie stali według średnic, ile prętów 12 m zamówić i plan cięcia z małym odpadem.','<path d="M3 8h18M3 16h18M9 5v6M15 13v6"/>'),
 '/konfigurator-domu':('Plan budowy','Konfigurator domu 3D','Model domu rośnie etapami, a obok koszt każdego elementu: materiał i robocizna.','<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
 '/ceny-budowlane':('Plan budowy','Ceny materiałów i robocizny','Baza cen jednostkowych z datą i źródłami, odświeżana co miesiąc.','<path d="M4 4h10l6 6-10 10-6-6z"/><circle cx="9" cy="9" r="1.5"/>'),
 '/dylatacje':('Konstrukcja','Dylatacje','Gdzie robić dylatacje w ścianach i posadzkach i czym różnią się od pęknięć.','<path d="M12 3v4M12 17v4M8 7h8M8 17h8"/>'),
 '/dzialka-zabudowa':('Plan budowy','Wskaźnik zabudowy działki','Wskaźnik zabudowy, intensywność i powierzchnia biologicznie czynna, porównane z planem.','<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M7 15V9h4v6M13 15h4"/>'),
 '/moc-grzewcza':('Energia','Moc grzewcza domu','Straty ciepła przez przegrody i wentylację. Wynik w kW do doboru pompy lub kotła.','<rect x="4" y="5" width="16" height="11" rx="2"/><path d="M8 20h8M9 9v3M12 9v3M15 9v3"/>'),
 '/ogrzewanie-podlogowe':('Energia','Ogrzewanie podłogowe','Długość rury, liczba pętli i obiegów rozdzielacza przy zadanym rozstawie.','<path d="M3 17h18M3 13c2 0 2-2 4-2s2 2 4 2 2-2 4-2 2 2 4 2"/>'),
 '/taras':('Wykończenie i teren','Taras: deski i legary','Deski, legary i stopy z zapasem na docinki, dla drewna i kompozytu.','<path d="M3 8h18M3 12h18M3 16h18"/><path d="M6 16v4M18 16v4"/>'),
 '/koszt-budowy':('Plan budowy','Koszt budowy domu','Stan surowy, deweloperski czy pod klucz: koszt z metrażu i stawek z ofert, z różnicą między standardami.','<path d="M4 19h16"/><path d="M6 19V9l6-4 6 4v10"/><path d="M10 14h4"/>'),
 '/malowanie':('Wykończenie i teren','Malowanie: ile farby','Litry farby na ściany i sufit z odjęciem okien i drzwi, zapasem i liczbą opakowań.','<rect x="4" y="3" width="13" height="6" rx="1"/><path d="M17 6h3v5h-3M10 9v4M9 13h5v7H9z"/>'),
 '/przylacza':('Plan budowy','Przyłącza do domu','Porównaj oferty na prąd, wodę, kanalizację i gaz: suma i koszt każdych 10 m.','<path d="M9 3v5M15 3v5M7 8h10v4a5 5 0 0 1-10 0z"/><path d="M12 17v4"/>'),
}
FEAT='<a class="feat" href="/konfigurator-domu"><span class="tag">Nowość</span><b>Konfigurator domu 3D</b><span>Ustaw wymiary, dach i ściany. Model rośnie od fundamentów do elewacji, a pod nim widzisz koszt każdego elementu, osobno materiał i robocizna.</span><span class="go">Otwórz konfigurator</span></a>'
def tile(href):
    if href in NEWTILES:
        _,title,desc,path=NEWTILES[href]; tag=NEWTILES[href][0].upper()
        return f'<a class="tile" href="{href}"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{path}</svg></div><span class="tag">{tag}</span><b>{title}</b><span>{desc}</span></a>'
    return tiles[href]
GROUPS_IDX=[
 ('Fundamenty',['/beton','/lawy-czy-plyta','/hydroizolacja-fundamentow','/wykop']),
 ('Konstrukcja',['/strop','/schody','/nadproza','/dylatacje']),
 ('Ściany i dach',['/sciany','/ocieplenie','/wspolczynnik-u','/sciana-dzialowa','/dach']),
 ('Wykończenie i teren',['/wylewka','/kostka','/ogrodzenie','/taras','/malowanie']),
 ('Energia',['/fotowoltaika','/pompa-ciepla','/pompa-ciepla-stary-dom','/moc-grzewcza','/ogrzewanie-podlogowe']),
 ('Plan budowy',['/koszt-budowy','/konfigurator-domu','/ceny-budowlane','/etapy-budowy','/harmonogram','/kredyt','/vat-budowa','/dzialka-zabudowa','/przylacza']),
 ('Dla firm',['/kosztorys','/rozkroj-pretow']),
]
main='<main class="wrap">\n'+hero+'\n'+FEAT+'\n'
for g,hrefs in GROUPS_IDX:
    main+=f'<h2>{g}</h2>\n<div class="tiles">\n'+'\n'.join(tile(h) for h in hrefs)+'\n</div>\n'
main+='<p class="mut">Nowe kalkulatory dochodzą co kilka dni. Wyniki to szacunki, a przy konstrukcji wiążący jest zawsze projekt.</p>\n</main>'
desc=re.search(r'<meta name="description" content="([^"]*)">',old).group(1)
open(BASE+'index.html','w',encoding='utf-8').write(page('/','Budlicz: kalkulatory budowlane online',desc,main))
print('index written, tiles:', len(re.findall('class="tile"', main)))
# sitemap
pages=['/']+sorted('/'+os.path.basename(p)[:-5] for p in glob.glob(BASE+'*.html') if os.path.basename(p)!='index.html')
urls=''.join(f'<url><loc>https://budlicz.pl{"/" if p=="/" else p}</loc><lastmod>2026-10-17</lastmod></url>\n' for p in pages)
open(BASE+'sitemap.xml','w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
print('sitemap urls', len(pages))
