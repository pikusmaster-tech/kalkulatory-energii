# Baza cen konfiguratora: dane/zrodla/RRRR-MM.json -> public/dane/ceny.json
# Każda cena to mediana źródeł przeliczonych na jednostkę z konfiguratora.
# Uruchomienie: python3 gen/ceny.py  (potem python3 gen/assemble2.py)
import json, os, re, glob, statistics, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZRD=os.path.join(ROOT,'dane','zrodla'); HIS=os.path.join(ROOT,'dane','historia')
OUT=os.path.join(ROOT,'public','dane','ceny.json')
KONF=os.path.join(ROOT,'public','js','konfigurator.js')
KINDS={'m','r','i','z'}

def wymagane_id():
    s=open(KONF,encoding='utf-8').read()
    return set(re.findall(r'"([mri]_[a-z_0-9]+|z_[a-z_0-9]+)"',s))

def ostatni(plik_glob):
    f=sorted(glob.glob(plik_glob))
    return f[-1] if f else None

def zbuduj(miesiac):
    src=json.load(open(os.path.join(ZRD,f'{miesiac}.json'),encoding='utf-8'))
    if src.get('miesiac')!=miesiac: sys.exit('zły miesiąc w pliku źródeł')
    p={}; bledy=[]
    for id_,poz in src['pozycje'].items():
        if poz.get('k') not in KINDS: bledy.append(f'{id_}: zły rodzaj'); continue
        vals=[]; zr=[]
        for z in poz.get('zrodla',[]):
            if not (z.get('url') and z.get('data')): bledy.append(f'{id_}: źródło bez adresu lub daty'); continue
            v=float(z['cena'])*float(z.get('przelicznik',1))
            vals.append(v); zr.append({'nazwa':z['nazwa'],'url':z['url'],'data':z['data']})
        if not vals: bledy.append(f'{id_}: brak źródeł'); continue
        c=statistics.median(vals)
        if len(vals)>=2: lo,hi=min(vals),max(vals)
        else: lo,hi=c*0.9,c*1.1   # jedno źródło: zakres ±10% (pokazany w cenniku)
        p[id_]={'n':poz['n'],'jm':poz['jm'],'k':poz['k'],'c':round(c,2),'lo':round(lo,2),'hi':round(hi,2),
                'zrodla':zr,'n_zr':len(vals)}
    brak=wymagane_id()-set(p)
    if brak: bledy.append('brak cen dla: '+', '.join(sorted(brak)))
    if bledy: sys.exit('BŁĘDY:\n- '+'\n- '.join(bledy))
    return src,p

if __name__=='__main__':
    miesiac=sys.argv[1] if len(sys.argv)>1 else os.path.basename(ostatni(os.path.join(ZRD,'*.json'))).replace('.json','')
    src,p=zbuduj(miesiac)
    prev=ostatni(os.path.join(HIS,'*.json'))
    old=json.load(open(prev,encoding='utf-8'))['p'] if prev and os.path.basename(prev)<f'{miesiac}.json' else {}
    for id_,x in p.items():
        o=old.get(id_)
        x['zmiana']=round((x['c']/o['c']-1)*100,1) if o and o.get('c') else None
    out={'miesiac':miesiac,'sprawdzone':src['sprawdzone'],
         'opis':"stan na "+".".join(reversed(src['sprawdzone'].split('-')))+", netto bez VAT",
         'p':p}
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    json.dump(out,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    json.dump({'miesiac':miesiac,'p':{k:{'c':v['c'],'lo':v['lo'],'hi':v['hi']} for k,v in p.items()}},
              open(os.path.join(HIS,f'{miesiac}.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('pozycji:',len(p),'miesiąc:',miesiac)
