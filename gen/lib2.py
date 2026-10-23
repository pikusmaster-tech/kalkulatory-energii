import re
import os
BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','public')+os.sep
_src=open(BASE+'beton.html',encoding='utf-8').read()
HEAD=_src[:_src.index('<body>')+len('<body>')]
HEADER_TMPL=_src[_src.index('<header class="top">'):_src.index('</header>')+len('</header>')]
FOOTER=_src[_src.index('<footer>'):_src.index('</footer>')+len('</footer>')].replace(
 '<span><a href="/">Wszystkie kalkulatory</a></span>',
 '<span><a href="/polityka-prywatnosci">Prywatność</a> · <a href="/o-serwisie">O serwisie</a> · <a href="/">Wszystkie kalkulatory</a></span>')
GROUPS=[
 ("Fundamenty",[("/beton","Beton i stal"),("/lawy-czy-plyta","Ławy czy płyta"),("/hydroizolacja-fundamentow","Hydroizolacja"),("/wykop","Ziemia z wykopu")]),
 ("Konstrukcja",[("/strop","Strop"),("/schody","Schody"),("/nadproza","Nadproża"),("/dylatacje","Dylatacje")]),
 ("Ściany i dach",[("/sciany","Pustaki na ściany"),("/ocieplenie","Ocieplenie ścian"),("/wspolczynnik-u","Współczynnik U"),("/sciana-dzialowa","Ścianka z płyt GK"),("/dach","Dach")]),
 ("Wykończenie i teren",[("/wylewka","Wylewka"),("/kostka","Kostka i płytki"),("/ogrodzenie","Ogrodzenie"),("/taras","Taras"),("/malowanie","Malowanie")]),
 ("Energia",[("/fotowoltaika","Fotowoltaika"),("/pompa-ciepla","Pompa ciepła"),("/pompa-ciepla-stary-dom","Pompa w starym domu"),("/moc-grzewcza","Moc grzewcza"),("/ogrzewanie-podlogowe","Ogrzewanie podłogowe")]),
 ("Plan budowy",[("/koszt-budowy","Koszt budowy domu"),("/konfigurator-domu","Konfigurator domu 3D"),("/ceny-budowlane","Ceny materiałów"),("/etapy-budowy","Etapy budowy"),("/harmonogram","Harmonogram"),("/kredyt","Kredyt na budowę"),("/vat-budowa","VAT 8% czy 23%"),("/dzialka-zabudowa","Wskaźnik zabudowy"),("/przylacza","Przyłącza")]),
 ("Dla firm",[("/kosztorys","Kosztorys ofertowy"),("/rozkroj-pretow","Rozkrój prętów")]),
]
def nav(cur):
    parts=[]
    for gname,items in GROUPS:
        inside=any(h==cur for h,_ in items)
        links=''.join(f'<a href="{h}"'+(' aria-current="page"' if h==cur else '')+f'>{t}</a>' for h,t in items)
        parts.append(f'<details class="grp{" cur" if inside else ""}"><summary>{gname}</summary><div class="dd">{links}</div></details>')
    return '<nav aria-label="Kalkulatory i poradniki">'+''.join(parts)+'</nav>'
def header(cur):
    return re.sub(r'<nav[^>]*>.*?</nav>',lambda m:nav(cur),HEADER_TMPL,count=1,flags=re.S)
CLOSE_JS='document.addEventListener("click",e=>{document.querySelectorAll(".grp[open]").forEach(d=>{if(!d.contains(e.target))d.open=false})});'
def page(cur,title,desc,main,script=''):
    h=re.sub(r'<title>.*?</title>',lambda m:f'<title>{title}</title>',HEAD,count=1)
    h=re.sub(r'<meta name="description" content="[^"]*">',lambda m:f'<meta name="description" content="{desc}">',h,count=1)
    return h+'\n'+header(cur)+'\n'+main+'\n'+FOOTER+'\n<script>\n'+script+'\n'+CLOSE_JS+'\n</script>\n</body>\n</html>\n'
