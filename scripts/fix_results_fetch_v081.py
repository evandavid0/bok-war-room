from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.8 — 2026','BOK War Room V0.8.1 — 2026',1)
old="""    const url=`https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?week=${wk.week}&seasontype=2&groups=80&limit=400`;\n    const res=await fetch(url); if(!res.ok)throw new Error('Scoreboard request failed ('+res.status+').');"""
new="""    // ESPN's undocumented scoreboard API does not reliably honor the `week=` parameter.\n    // Build an explicit 2026 date window instead: Tue–Mon for each BOK week.\n    const anchor=new Date(Date.UTC(2026,8,1));\n    const start=new Date(anchor.getTime()+(wk.week-1)*7*86400000);\n    const end=new Date(start.getTime()+6*86400000);\n    const ymd=d=>d.toISOString().slice(0,10).replace(/-/g,'');\n    const url=`https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=${ymd(start)}-${ymd(end)}&seasontype=2&groups=80&limit=400`;\n    const res=await fetch(url,{cache:'no-store'}); if(!res.ok)throw new Error('Scoreboard request failed ('+res.status+').');"""
if old not in s: raise SystemExit('results fetch anchor not found')
s=s.replace(old,new,1)
s=s.replace("status.textContent='Fetching ESPN scoreboard…';","status.textContent='Fetching ESPN scoreboard for Week '+wk.week+'…';",1)
p.write_text(s,encoding='utf-8')
print('V0.8.1 results fetch fix applied')