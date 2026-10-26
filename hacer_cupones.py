"""Genera cupones.json (público, con los códigos como hash SHA-256) desde cupones-fuente.json (privado).
Campos por cupón: codigo, t ("pct" o "monto"), v (porcentaje o pesos), min (compra mínima en $, opcional),
vence ("AAAA-MM-DD", opcional), acum (true: el % se multiplica con la escala 3/10/20; false: rige el mayor), activo.
Uso: python3 hacer_cupones.py [carpeta_de_salida]"""
import json,hashlib,sys,os
src=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"cupones-fuente.json")))
out=[]
for c in src["cupones"]:
    d={k:c[k] for k in ("t","v","min","vence","acum","activo") if k in c}
    d["h"]=hashlib.sha256(c["codigo"].strip().upper().encode()).hexdigest(); out.append(d)
dest=(sys.argv[1] if len(sys.argv)>1 else ".")+"/cupones.json"
json.dump({"c":out},open(dest,"w"),separators=(",",":")); print(len(out),"cupones ->",dest)
