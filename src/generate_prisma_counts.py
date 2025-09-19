import sqlite3, yaml, pathlib, csv, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
cfg = yaml.safe_load(open(ROOT/'src'/'config.yaml','r',encoding='utf-8'))
con = sqlite3.connect(str(ROOT/cfg['db_path'])); con.execute('PRAGMA foreign_keys=ON;')
cur = con.cursor()
cur.execute("SELECT decision_stage, include_flag, reason_code FROM eligibility")
rows = cur.fetchall()
from collections import Counter
stage_counts=Counter(); reasons=Counter()
for stage, inc, reason in rows:
    if stage: stage_counts[stage]+=1
    if inc==0 and reason: reasons[reason]+=1
os.makedirs(ROOT/'exports', exist_ok=True)
with open(ROOT/'exports'/'prisma_stage_counts.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['stage','count'])
    for k,v in stage_counts.items(): w.writerow([k,v])
with open(ROOT/'exports'/'exclusion_reasons.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['reason','count'])
    for k,v in reasons.items(): w.writerow([k,v])
print("[OK] generate_prisma_counts gerado")
