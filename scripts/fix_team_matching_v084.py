from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.8.3 — 2026','BOK War Room V0.8.4 — 2026',1)
s=s.replace('APP V0.8.3','APP V0.8.4',1)
old="""function normTeamName(s){return String(s||'').toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,' ').replace(/\\b(state|st)\\b/g,'state').trim();}"""
new="""function normTeamName(s){return String(s||'').toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,' ').replace(/\\b(state|st)\\b/g,'state').trim();}
const TEAM_ALIASES={
 'ole miss':['ole miss','mississippi'],
 'utep':['utep','texas el paso'],
 'smu':['smu','southern methodist'],
 'lsu':['lsu','louisiana state'],
 'texas a and m':['texas a and m','texas am','texas a m'],
 'boise state':['boise state'],
 'missouri state':['missouri state'],
 'washington state':['washington state'],
 'florida state':['florida state'],
 'texas state':['texas state'],
 'notre dame':['notre dame']
};
function bokTeamAliases(name){
  const n=normTeamName(name),out=new Set([n]);
  (TEAM_ALIASES[n]||[]).forEach(x=>out.add(normTeamName(x)));
  return out;
}
function espnTeamAliases(team){
  const vals=[team?.displayName,team?.shortDisplayName,team?.name,team?.location,team?.abbreviation];
  const out=new Set(vals.filter(Boolean).map(normTeamName));
  return out;
}
function teamMatchesBok(bokName,espnTeam){
  const bok=bokTeamAliases(bokName),espn=espnTeamAliases(espnTeam);
  for(const b of bok)for(const e of espn){
    if(b===e)return true;
    if(e.startsWith(b+' ')||b.startsWith(e+' '))return true;
  }
  return false;
}"""
if old not in s: raise SystemExit('normTeamName anchor not found')
s=s.replace(old,new,1)
old2="""      const a=normTeamName(g.Away),h=normTeamName(g.Home);
      const ev=events.find(e=>{
        const c=e.competitions?.[0]?.competitors||[]; const names=c.map(x=>normTeamName(x.team?.displayName||x.team?.shortDisplayName||x.team?.name));
        return names.includes(a)&&names.includes(h);
      });"""
new2="""      const ev=events.find(e=>{
        const c=e.competitions?.[0]?.competitors||[];
        return c.some(x=>teamMatchesBok(g.Away,x.team))&&c.some(x=>teamMatchesBok(g.Home,x.team));
      });"""
if old2 not in s: raise SystemExit('results match anchor not found')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('V0.8.4 team-name matching fix applied')
