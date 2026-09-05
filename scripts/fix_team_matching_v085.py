from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.8.4 — 2026','BOK War Room V0.8.5 — 2026',1)
s=s.replace('APP V0.8.4','APP V0.8.5',1)
old="""const TEAM_ALIASES={
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
};"""
new="""const TEAM_ALIASES={
 'utep':['utep','texas el paso'],
 'oklahoma':['oklahoma','ou'],
 'texas state':['texas state','txst'],
 'texas':['texas','tex'],
 'boise state':['boise state','boise'],
 'oregon':['oregon','ore'],
 'baylor':['baylor','bay'],
 'auburn':['auburn','aub'],
 'missouri state':['missouri state','missouri st','most'],
 'texas a and m':['texas a and m','texas am','texas a m','texas aandm','tamu'],
 'clemson':['clemson','clem'],
 'lsu':['lsu','louisiana state'],
 'washington state':['washington state','washington st','wsu'],
 'washington':['washington','uw'],
 'wisconsin':['wisconsin','wis'],
 'notre dame':['notre dame','nd'],
 'louisville':['louisville','lou'],
 'ole miss':['ole miss','mississippi','miss'],
 'smu':['smu','southern methodist'],
 'florida state':['florida state','florida st','fsu']
};"""
if old not in s: raise SystemExit('TEAM_ALIASES anchor not found')
s=s.replace(old,new,1)
old2="""function teamMatchesBok(bokName,espnTeam){
  const bok=bokTeamAliases(bokName),espn=espnTeamAliases(espnTeam);
  for(const b of bok)for(const e of espn){
    if(b===e)return true;
    if(e.startsWith(b+' ')||b.startsWith(e+' '))return true;
  }
  return false;
}"""
new2="""function teamMatchesBok(bokName,espnTeam){
  const bok=bokTeamAliases(bokName),espn=espnTeamAliases(espnTeam);
  for(const b of bok)for(const e of espn){
    if(b===e)return true;
    // ESPN displayName often appends a mascot (e.g. \"Oklahoma Sooners\").
    // Only allow BOK alias -> ESPN prefix, never the reverse; this prevents
    // \"Texas\" from accidentally matching \"Texas State\".
    if(e.startsWith(b+' '))return true;
  }
  return false;
}
function eventMatchesGame(g,e){
  const c=e.competitions?.[0]?.competitors||[];
  const away=c.find(x=>x.homeAway==='away'),home=c.find(x=>x.homeAway==='home');
  if(away&&home){
    const direct=teamMatchesBok(g.Away,away.team)&&teamMatchesBok(g.Home,home.team);
    if(direct)return true;
    if(g['Neutral?']){
      const swapped=teamMatchesBok(g.Away,home.team)&&teamMatchesBok(g.Home,away.team);
      if(swapped)return true;
    }
    return false;
  }
  return c.length>=2 && c.some(x=>teamMatchesBok(g.Away,x.team)) && c.some(x=>teamMatchesBok(g.Home,x.team));
}"""
if old2 not in s: raise SystemExit('teamMatchesBok anchor not found')
s=s.replace(old2,new2,1)
old3="""      const ev=events.find(e=>{
        const c=e.competitions?.[0]?.competitors||[];
        return c.some(x=>teamMatchesBok(g.Away,x.team))&&c.some(x=>teamMatchesBok(g.Home,x.team));
      });"""
new3="""      const ev=events.find(e=>eventMatchesGame(g,e));"""
if old3 not in s: raise SystemExit('event finder anchor not found')
s=s.replace(old3,new3,1)
old4="""    status.textContent=`${finals} final${finals===1?'':'s'} imported · ${found}/${currentGames().length} slate games matched across ${events.length} ESPN events${missing.length?' · '+missing.length+' unmatched':''}.`;"""
new4="""    status.textContent=`${finals} final${finals===1?'':'s'} imported · ${found}/${currentGames().length} slate games matched across ${events.length} ESPN events${missing.length?' · unmatched: '+missing.join(' | '):''}.`;"""
if old4 not in s: raise SystemExit('status anchor not found')
s=s.replace(old4,new4,1)
p.write_text(s,encoding='utf-8')
print('V0.8.5 team matching hardening applied')
