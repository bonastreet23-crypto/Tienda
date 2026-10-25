"""Genera stock.json a partir de los productos de la app Bona Gestión (carpeta con un JSON por SKU).
Uso: python3 sync_stock.py CARPETA_PRODUCTOS salida/stock.json"""
import json,glob,sys,os,datetime
src,out=sys.argv[1],sys.argv[2]
s={}
for f in sorted(glob.glob(os.path.join(src,"*.json"))):
    d=json.load(open(f)); p=d.get("data",d)
    for t,q in (p.get("stock") or {}).items(): s[f'{p["sku"]}|{t}']=max(0,int(q))
old=json.load(open(out))["s"] if os.path.exists(out) else None
if old==s: print("sin cambios"); sys.exit(0)
json.dump({"updated":datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat()+"Z","s":s},open(out,"w"),separators=(",",":"))
print("stock.json actualizado:",len(s),"variantes")
