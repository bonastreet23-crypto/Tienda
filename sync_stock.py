"""Sincroniza la web con la app Bona Gestión.
Uso: python3 sync_stock.py CARPETA_PRODUCTOS salida/stock.json   (catalogo.json debe estar al lado de stock.json)
- s: stock por SKU|talle (la web oculta lo agotado y muestra lo repuesto)
- pr: precios que cambiaron en la app desde que se armó la web (precio unitario de la app; la web calcula el de tarjeta)
- nuevos: SKUs con stock en la app que todavía no están publicados -> requieren regenerar la web (ver COMO-REGENERAR.md)"""
import json,glob,sys,os,datetime
src,out=sys.argv[1],sys.argv[2]
cat=json.load(open(os.path.join(os.path.dirname(os.path.abspath(out)),"catalogo.json")))
EXCLUIR={"DIA-015"}   # 27/10/2026 Luchi: duplicado del negro con detalles flúor (DIA-004)
pub,base=set(cat["publicados"]),cat["precios"]
s,pr,nuevos={},{},[]
for f in sorted(glob.glob(os.path.join(src,"*.json"))):
    d=json.load(open(f)); p=d.get("data",d); k=p["sku"]
    st=p.get("stock") or {}
    for t,q in st.items(): s[f"{k}|{t}"]=max(0,int(q))
    if k in pub:
        if k in base and p.get("precio") and p["precio"]!=base[k]: pr[k]=p["precio"]
    elif k not in EXCLUIR and sum(max(0,int(q)) for q in st.values())>0 and p.get("activo",True): nuevos.append(k)
new={"s":s,"pr":pr,"nuevos":nuevos}
old=json.load(open(out)) if os.path.exists(out) else {}
if all(old.get(k)==v for k,v in new.items()): print("sin cambios"); sys.exit(0)
new["updated"]=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
json.dump(new,open(out,"w"),separators=(",",":"))
print(f"stock.json actualizado: {len(s)} variantes · {len(pr)} precios cambiados · nuevos sin publicar: {nuevos or 'ninguno'}")
