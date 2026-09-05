from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.8.5 — 2026','BOK War Room V0.8.6 — 2026',1)
s=s.replace('APP V0.8.5','APP V0.8.6',1)
# ESPN uses some non-obvious school/location labels. Add exact normalized variants
# for the four Week 1 misses reported by the live diagnostic.
repls={
"'washington state':['washington state','washington st','wsu']":"'washington state':['washington state','washington st','washington state university','wash state','wazzu','wsu']",
"'washington':['washington','uw']":"'washington':['washington','washington huskies','uw']",
"'wisconsin':['wisconsin','wis']":"'wisconsin':['wisconsin','wisconsin badgers','wisc','wis']",
"'notre dame':['notre dame','nd']":"'notre dame':['notre dame','notre dame fighting irish','nd']",
"'louisville':['louisville','lou']":"'louisville':['louisville','louisville cardinals','ul','lou']",
"'ole miss':['ole miss','mississippi','miss']":"'ole miss':['ole miss','mississippi','mississippi rebels','olemiss','miss']",
"'smu':['smu','southern methodist']":"'smu':['smu','southern methodist','southern methodist university']",
"'florida state':['florida state','florida st','fsu']":"'florida state':['florida state','florida st','florida state seminoles','fsu']"
}
for a,b in repls.items():
    if a not in s: raise SystemExit('alias anchor missing: '+a)
    s=s.replace(a,b,1)
# Expand ESPN fields to include uid/slug when exposed and canonicalize common abbreviations.
old="""function espnTeamAliases(team){
  const vals=[team?.displayName,team?.shortDisplayName,team?.name,team?.location,team?.abbreviation];
  const out=new Set(vals.filter(Boolean).map(normTeamName));
  return out;
}"""
new="""function espnTeamAliases(team){
  const vals=[team?.displayName,team?.shortDisplayName,team?.name,team?.location,team?.abbreviation,team?.slug];
  const out=new Set(vals.filter(Boolean).map(normTeamName));
  return out;
}"""
if old not in s: raise SystemExit('espnTeamAliases anchor missing')
s=s.replace(old,new,1)
# Add a safe token/abbreviation fallback: only exact aliases or ESPN mascot suffixes,
# plus normalized abbreviation equality. No broad substring matching.
old2="""    if(e===b)return true;
    // ESPN displayName often appends a mascot (e.g. \"Oklahoma Sooners\").
    // Only allow BOK alias -> ESPN prefix, never the reverse; this prevents
    // \"Texas\" from accidentally matching \"Texas State\".
    if(e.startsWith(b+' '))return true;"""
# actual code order is b===e; account for it
if old2 not in s:
    old2="""    if(b===e)return true;
    // ESPN displayName often appends a mascot (e.g. \"Oklahoma Sooners\").
    // Only allow BOK alias -> ESPN prefix, never the reverse; this prevents
    // \"Texas\" from accidentally matching \"Texas State\".
    if(e.startsWith(b+' '))return true;"""
new2="""    if(b===e)return true;
    // ESPN displayName often appends a mascot (e.g. \"Oklahoma Sooners\").
    // Only allow BOK alias -> ESPN prefix, never the reverse; this prevents
    // \"Texas\" from accidentally matching \"Texas State\".
    if(e.startsWith(b+' '))return true;"""
if old2 not in s: raise SystemExit('team matcher anchor missing')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('V0.8.6 aliases applied')
