# Baza cen konfiguratora.
# Wejście: dane/zrodla/RRRR-MM.json (każde źródło: min, max, vat, przelicznik).
# Wyjście: public/dane/ceny.json oraz archiwum dane/historia/RRRR-MM.json.
# Każde źródło przeliczamy na netto (brutto 8% dzielimy przez 1,08, brutto 23% przez 1,23),
# potem bierzemy medianę środków przedziałów, medianę dolnych i medianę górnych granic.
# Uruchomienie: python3 gen/ceny.py RRRR-MM   (potem python3 gen/assemble2.py)
import json, os, re, glob, statistics, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZRD=os.path.join(ROOT,'dane','zrodla'); HIS=os.path.join(ROOT,'dane','historia')
OUT=os.path.join(ROOT,'public','dane','ceny.json')
KONF=os.path.join(ROOT,'public','js','konfigurator.js')
KINDS={'m','r','i','z'}
DZIEL={'netto':1.0,'?':1.0,'brutto8':1.08,'brutto23':1.23}

def wymagane_id():
    s=open(KONF,encoding='utf-8').read()
    return set(re.findall(r'"([mri]_[a-z_0-9]+|z_[a-z_0-9]+)"',s))

def zbuduj(miesiac):
    src=json.load(open(os.path.join(ZRD,f'{miesiac}.json'),encoding='utf-8'))
    if src.get('miesiac')!=miesiac: sys.exit('zły miesiąc w pliku źródeł')
    p={}; bledy=[]
    for id_,poz in src['pozycje'].items():
        if poz.get('k') not in KINDS: bledy.append(f'{id_}: zły rodzaj'); continue
        para=[]; zr=[]
        for z in poz.get('zrodla',[]):
            if not (z.get('url') and z.get('data_zrodla')): bledy.append(f'{id_}: źródło bez adresu lub daty'); continue
            if z.get('vat') not in DZIEL: bledy.append(f'{id_}: nieznany VAT {z.get("vat")}'); continue
            przel=float(z.get('przelicznik',1)); dziel=DZIEL[z['vat']]
            a=float(z['min'])*przel/dziel; b=float(z['max'])*przel/dziel
            para.append((a,b))
            zr.append({'nazwa':z['nazwa'],'url':z['url'],'data_zrodla':z['data_zrodla'],'vat':z['vat']})
        if not para: bledy.append(f'{id_}: brak źródeł'); continue
        c=statistics.median([(a+b)/2 for a,b in para])
        lo=min(statistics.median([a for a,_ in para]),c)
        hi=max(statistics.median([b for _,b in para]),c)
        p[id_]={'n':poz['n'],'jm':poz['jm'],'k':poz['k'],'c':round(c,2),'lo':round(lo,2),'hi':round(hi,2),
                'zrodla':zr,'n_zr':len(para),'uwaga':poz.get('uwaga','')}
    brak=wymagane_id()-set(p)
    if brak: bledy.append('brak cen dla: '+', '.join(sorted(brak)))
    if bledy: sys.exit('BŁĘDY:\n- '+'\n- '.join(bledy))
    return src,p

def ostatni(glob_):
    f=sorted(glob.glob(glob_))
    return f[-1] if f else None

if __name__=='__main__':
    miesiac=sys.argv[1] if len(sys.argv)>1 else os.path.basename(ostatni(os.path.join(ZRD,'*.json'))).replace('.json','')
    src,p=zbuduj(miesiac)
    prev=ostatni(os.path.join(HIS,'*.json'))
    old=json.load(open(prev,encoding='utf-8'))['p'] if prev and os.path.basename(prev)<f'{miesiac}.json' else {}
    for id_,x in p.items():
        o=old.get(id_)
        x['zmiana']=round((x['c']/o['c']-1)*100,1) if o and o.get('c') else None
    dz='.'.join(reversed(src['sprawdzone'].split('-')))
    out={'miesiac':miesiac,'sprawdzone':src['sprawdzone'],'opis':f'stan na {dz}, netto bez VAT','p':p}
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    json.dump(out,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    os.makedirs(HIS,exist_ok=True)
    json.dump({'miesiac':miesiac,'p':{k:{'c':v['c'],'lo':v['lo'],'hi':v['hi']} for k,v in p.items()}},
              open(os.path.join(HIS,f'{miesiac}.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('pozycji:',len(p),'miesiąc:',miesiac)
