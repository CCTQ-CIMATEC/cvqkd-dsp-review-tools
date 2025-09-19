import sqlite3, pathlib, yaml, os, csv
ROOT = pathlib.Path(__file__).resolve().parents[1]
cfg = yaml.safe_load(open(ROOT/'src'/'config.yaml','r',encoding='utf-8'))
con = sqlite3.connect(str(ROOT/cfg['db_path'])); con.execute('PRAGMA foreign_keys=ON;')
cur = con.cursor()
os.makedirs(ROOT/'exports', exist_ok=True)
for table in ["publications","eligibility","rq_map","data_items"]:
    cur.execute(f"SELECT * FROM {table}")
    cols=[d[0] for d in cur.description]; rows=cur.fetchall()
    with open(ROOT/'exports'/f"{table}.csv",'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(cols)
        for row in rows: w.writerow(row)
print("[OK] export_csv gerado")
