# Strona /ceny-budowlane: tabela cen z public/dane/ceny.json (wygenerowanego przez gen/ceny.py).
import json, os, html
from lib2 import BASE
_fn=os.path.join(BASE,'dane','ceny.json')
_d=json.load(open(_fn,encoding='utf-8')) if os.path.exists(_fn) else None
_P=_d['p'] if _d else {}
_KIND=[('m','Materiały','Cena materiału netto, z dostawą na budowę według źródła.'),
       ('r','Robocizna','Stawki za pracę ekipy, netto. Mediana z ogłoszeń i cenników firm budowlanych.'),
       ('i','Instalacje (z materiałem i montażem)','Stawka za m² lub sztukę, w której zawarty jest materiał i montaż.'),
       ('z','Zużycie według producentów','Ilości na jednostkę, nie ceny. Konfigurator mnoży je przez wymiary.')]
def _e(x): return html.escape(str(x),quote=True)
VAT={'netto':'netto','brutto8':'brutto, VAT 8%','brutto23':'brutto, VAT 23%','?':'VAT nieokreślony, przyjęto netto'}
def _liczba(x,d=2):
    return f"{x:,.{d}f}".replace(',',' ').replace('.',',') if d else f"{x:,.0f}".replace(',',' ')
def _zakres(p):
    return f"{_liczba(p['lo'],2)} do {_liczba(p['hi'],2)}"
def _zmiana(p):
    z=p.get('zmiana')
    if z is None: return '<span class="mut">pierwszy miesiąc</span>'
    return f'{"+" if z>0 else ""}{_liczba(z,1)}%'
def _wiersze(k):
    rows=[]
    for id_,p in sorted(_P.items(),key=lambda kv:kv[1]['n']):
        if p['k']!=k: continue
        zr='<br>'.join(f'<a href="{_e(z["url"])}" rel="nofollow noopener">{_e(z["nazwa"])}</a> <span class="mut">({_e(z["data_zrodla"])}, {_e(VAT[z["vat"]])})</span>' for z in p['zrodla'])
        uw=f'<br><span class="mut">{_e(p["uwaga"])}</span>' if p.get('uwaga') else ''
        rows.append(f'<tr><td>{_e(p["n"])}{uw}</td><td>{_e(p["jm"])}</td><td class="num"><b>{_liczba(p["c"])}</b></td><td class="num">{_zakres(p)}</td><td class="num">{_zmiana(p)}</td><td class="src">{zr}</td></tr>')
    return rows
def _tabela():
    out=[]
    for k,t,opis in _KIND:
        rows=_wiersze(k)
        if not rows: continue
        out.append(f'<h2>{t}</h2><p class="mut">{opis}</p>'
                   '<div class="tablewrap"><table class="cennik"><thead><tr><th>Pozycja</th><th>Jednostka</th><th class="num">Mediana</th><th class="num">Zakres</th><th class="num">Zmiana m/m</th><th>Źródła</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>')
    return '\n'.join(out)
_main=f'''<main class="wrap">
<div class="crumbs"><a href="/">Budlicz</a> › <a href="/konfigurator-domu">Konfigurator</a> › Ceny</div>
<h1>Ceny materiałów i robocizny</h1>
<p class="lead">Ceny jednostkowe, z których liczy się <a href="/konfigurator-domu">konfigurator domu</a>. Każda cena ma datę, źródła i zakres. Aktualizujemy je raz w miesiącu, a poprzedni stan zostaje w archiwum.</p>
<div class="tip"><b>Stan na {_e(".".join(reversed(_d["sprawdzone"].split("-")))) if _d else "brak danych"}.</b> Wszystkie ceny netto, bez VAT. Stawkę VAT na budowę domu (8% albo 23%) liczymy osobno w <a href="/vat-budowa">kalkulatorze VAT</a>.</div>
{_tabela()}
<h2>Jak liczymy cenę</h2>
<ul>
<li><b>Mediana, nie średnia.</b> Cena to środek przedziału z każdego źródła, a z nich środkowa wartość. Jedna skrajna oferta jej nie przesuwa.</li>
<li><b>Netto.</b> Źródła podające cenę brutto przeliczamy na netto: brutto 8% dzielimy przez 1,08, brutto 23% przez 1,23. Źródła bez podanego VAT traktujemy jako netto. Ta część może zawyżać cenę najwyżej o 8%.</li>
<li><b>Zakres.</b> Od najniższej do najwyższej wartości z źródeł. Konfigurator pokazuje go obok wyniku, żeby było widać rozrzut cen.</li>
<li><b>Przeliczenia.</b> Jeśli źródło podaje cenę w innej jednostce, przeliczamy ją na jednostkę konfiguratora (np. cenę za metr obwodu okna na sztukę, przy obwodzie 5,06 m). Przelicznik jest zapisany w danych źródłowych.</li>
<li><b>Zmiana m/m.</b> Różnica względem poprzedniej aktualizacji. Pokazuje tylko, czy rynek idzie w górę, czy w dół.</li>
<li><b>Robocizna.</b> To stawki za pracę ekipy, a nie wynagrodzenia pracowników. Źródło każdej stawki jest podane w tabeli.</li>
</ul>
<h2>Czego te ceny nie pokazują</h2>
<ul>
<li>Cen w Twoim regionie. Różnica między miastem a wsią potrafi być wyraźna, dlatego zawsze porównaj oferty.</li>
<li>Cen usług, których nie ma w konfiguratorze: projektu, przyłączy, schodów, wykończenia.</li>
<li>Rabatów, promocji i warunków płatności. Wiążąca jest oferta wykonawcy.</li>
</ul>
<p class="mut">Ceny mogą zawierać błędy albo być nieaktualne w Twojej okolicy. Jeśli zauważysz nieścisłość, napisz przez stronę <a href="/o-serwisie">O serwisie</a>.</p>
</main>'''
CENNIK={} if _d is None else {'ceny-budowlane':dict(title='Ceny materiałów i robocizny: baza z datą i źródłami',
  desc='Ceny jednostkowe materiałów i robocizny do szacowania budowy domu. Każda cena ma datę, źródła, zakres i zmianę z poprzedniego miesiąca.',
  main=_main,script='')}
