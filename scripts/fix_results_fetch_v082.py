from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.8.1 — 2026','BOK War Room V0.8.2 — 2026',1)
old="""    // ESPN's undocumented scoreboard API does not reliably honor the `week=` parameter.
    // Build an explicit 2026 date window instead: Tue–Mon for each BOK week.
    const anchor=new Date(Date.UTC(2026,8,1));
    const start=new Date(anchor.getTime()+(wk.week-1)*7*86400000);
    const end=new Date(start.getTime()+6*86400000);
    const ymd=d=>d.toISOString().slice(0,10).replace(/-/g,'');
    const url=`https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=${ymd(start)}-${ymd(end)}&seasontype=2&groups=80&limit=400`;
    const res=await fetch(url,{cache:'no-store'}); if(!res.ok)throw new Error('Scoreboard request failed ('+res.status+').');
    const data=await res.json(), events=Array.isArray(data.events)?data.events:[];
    let found=0,finals=0,missing=[];"""
new="""    // Query ESPN one calendar day at a time. The scoreboard endpoint is much more
    // reliable with a single YYYYMMDD than with its undocumented week/range filters.
    // BOK Week 1 is Aug 30–Sep 5; subsequent BOK weeks advance seven days.
    const anchor=new Date(Date.UTC(2026,7,30));
    const start=new Date(anchor.getTime()+(wk.week-1)*7*86400000);
    const ymd=d=>d.toISOString().slice(0,10).replace(/-/g,'');
    const days=Array.from({length:7},(_,i)=>new Date(start.getTime()+i*86400000));
    const payloads=await Promise.all(days.map(async d=>{
      const url=`https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=${ymd(d)}&seasontype=2&groups=80&limit=400`;
      const res=await fetch(url,{cache:'no-store'});if(!res.ok)throw new Error(`Scoreboard request failed for ${ymd(d)} (${res.status}).`);
      return res.json();
    }));
    const eventMap=new Map();
    payloads.forEach(data=>(Array.isArray(data.events)?data.events:[]).forEach(e=>eventMap.set(String(e.id||Math.random()),e)));
    const events=[...eventMap.values()];
    let found=0,finals=0,missing=[];"""
if old not in s: raise SystemExit('V0.8.1 fetch block not found')
s=s.replace(old,new,1)
s=s.replace("status.textContent=`${finals} final${finals===1?'':'s'} imported · ${found}/${currentGames().length} slate games matched${missing.length?' · '+missing.length+' unmatched':''}.`;","status.textContent=`${finals} final${finals===1?'':'s'} imported · ${found}/${currentGames().length} slate games matched across ${events.length} ESPN events${missing.length?' · '+missing.length+' unmatched':''}.`;",1)
p.write_text(s,encoding='utf-8')
print('V0.8.2 daily ESPN results fetch applied')