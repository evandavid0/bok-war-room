from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.8.6 — 2026','BOK War Room V0.8.7 — 2026',1)
s=s.replace('APP V0.8.6','APP V0.8.7',1)
old="""    const days=Array.from({length:7},(_,i)=>new Date(start.getTime()+i*86400000));"""
new="""    // Week 1 spans the full Labor Day opening slate, including Sunday Sep 6
    // and Monday Sep 7. Later BOK weeks use the standard seven-day window.
    const dayCount=wk.week===1?9:7;
    const days=Array.from({length:dayCount},(_,i)=>new Date(start.getTime()+i*86400000));"""
if old not in s: raise SystemExit('day range anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('V0.8.7 Week 1 extended date window applied')
