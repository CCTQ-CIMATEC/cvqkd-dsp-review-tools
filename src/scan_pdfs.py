import os, sqlite3, yaml, pathlib, hashlib, re
from pypdf import PdfReader
ROOT = pathlib.Path(__file__).resolve().parents[1]
cfg = yaml.safe_load(open(ROOT/'src'/'config.yaml','r',encoding='utf-8'))
def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for ch in iter(lambda:f.read(8192), b''): h.update(ch)
    return h.hexdigest()
def norm_title_from_filename(fn):
    base=os.path.splitext(os.path.basename(fn))[0]
    return re.sub(r'[_\-\s]+',' ',base).strip()
con = sqlite3.connect(str(ROOT/cfg['db_path'])); con.execute('PRAGMA foreign_keys=ON;')
cur = con.cursor()
pdf_dir = (ROOT/cfg['pdfs_dir']).resolve(); pdf_dir.mkdir(exist_ok=True, parents=True)
count=0
for r,_,fs in os.walk(pdf_dir):
    for f in fs:
        if not f.lower().endswith('.pdf'): continue
        p = pathlib.Path(r)/f
        s = sha256(p)
        cur.execute("SELECT id FROM publications WHERE pdf_sha256=?",(s,)); row=cur.fetchone()
        if row: continue
        title_meta=None
        try:
            info=(PdfReader(str(p)).metadata or {})
            title_meta=(getattr(info,'title',None) or "").strip()
        except Exception: pass
        pid=None
        if title_meta:
            cur.execute("SELECT id FROM publications WHERE lower(title)=lower(?)",(title_meta,)); stub=cur.fetchone()
            if stub: pid=stub[0]
        if pid is None:
            guess=norm_title_from_filename(f)
            cur.execute("SELECT id FROM publications WHERE lower(title)=lower(?)",(guess,)); stub=cur.fetchone()
            if stub: pid=stub[0]
        if pid is None:
            t = title_meta or guess
            cur.execute("INSERT INTO publications(title) VALUES (?)",(t,)); pid=cur.lastrowid
        cur.execute("UPDATE publications SET pdf_path=?, pdf_sha256=? WHERE id=?", (str(p), s, pid))
        count+=1
con.commit()
print(f"[OK] scan_pdfs: {count} PDFs vinculados/atualizados")
