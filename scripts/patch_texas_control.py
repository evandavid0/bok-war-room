from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.6 — 2026','BOK War Room V0.7 — 2026',1)
s=s.replace('<button data-view="lab">Model Lab</button>','<button data-view="texas">Texas Control</button>\n    <button data-view="lab">Model Lab</button>',1)
css='''.texasHero{background:linear-gradient(135deg,#fff8f1,#fff);border:1px solid var(--line);border-radius:16px;padding:20px}.texasMatch{display:grid;grid-template-columns:1fr auto 1fr;gap:16px;align-items:center}.texasTeam{font-size:clamp(24px,4vw,40px);font-weight:950}.texasTeam.right{text-align:right;color:var(--burnt)}.texasAt{font-weight:950;color:var(--muted)}.texasCall{margin-top:18px;padding-top:16px;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.texasMetric{background:white;border:1px solid var(--line);border-radius:12px;padding:12px}.texasMetric .tlabel{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:900}.texasMetric .tvalue{font-size:22px;font-weight:950;margin-top:4px}.driverGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.driverCard{border:1px solid var(--line);border-radius:12px;padding:14px;background:white}.driverCard .dval{font-size:24px;font-weight:950;margin-top:4px}.publishBox{white-space:pre-wrap;line-height:1.55;background:#fff8f1;border:1px solid var(--line);border-radius:12px;padding:14px;font-size:13px}@media(max-width:700px){.texasCall,.driverGrid{grid-template-columns:1fr}.texasTeam{font-size:24px}}
'''
s=s.replace('.scoregrid{display:grid;',css+'.scoregrid{display:grid;',1)
anchor='<section id="lab" class="view">'
texas='''<section id="texas" class="view">
  <div class="hero"><div class="panel"><div class="panelhead orange"><h2>Texas Control Panel</h2><span id="texasWeekTag">Week —</span></div><div class="pad" id="texasControl"></div></div><div class="panel"><div class="panelhead"><h3>Texas Snapshot</h3></div><div class="pad" id="texasSnapshot"></div></div></div>
  <div class="staffgrid"><div class="panel"><div class="panelhead"><h3>Margin Drivers</h3><span>V3.0 decomposition</span></div><div class="pad"><div class="driverGrid" id="texasDrivers"></div></div></div><div class="panel"><div class="panelhead"><h3>Publishing Copy</h3><span>Data-only</span></div><div class="pad"><div class="publishBox" id="texasPublish"></div></div></div></div>
  <div class="footerNote">Texas Control is a presentation layer only. It does not add subjective matchup adjustments, projected totals, or win probability to V3.0.</div>
</section>

'''
if '<section id="texas"' not in s:s=s.replace(anchor,texas+anchor,1)
# improve market wording
s=s.replace('${side} ${Math.abs(marketGap).toFixed(1)} pts</div>','${Math.abs(marketGap).toFixed(1)} pts toward ${side}</div>',1)
# insert function before openIntel
fn=r'''function renderTexasControl(){
  const games=currentGames(),g=games.find(x=>x.Away==='Texas'||x.Home==='Texas');
  const control=document.getElementById('texasControl'),snap=document.getElementById('texasSnapshot'),drivers=document.getElementById('texasDrivers'),pub=document.getElementById('texasPublish');
  if(!control)return;
  document.getElementById('texasWeekTag').textContent='Week '+currentWeek().week;
  if(!g){control.innerHTML='<div class="mini">Texas is not on the active BOK slate.</div>';snap.innerHTML=drivers.innerHTML=pub.innerHTML='—';return;}
  const tr=ratings.find(r=>r.Team==='Texas')||{},oppName=g.Away==='Texas'?g.Home:g.Away,or=ratings.find(r=>r.Team===oppName)||{};
  const texasHome=g.Home==='Texas',homeMargin=Number(g['Home Projected Margin']),texasMargin=texasHome?homeMargin:-homeMargin;
  const vals=ratings.map(r=>Number(r['SP+ Rating'])).filter(Number.isFinite),mean=vals.reduce((a,b)=>a+b,0)/vals.length,sd=Math.sqrt(vals.reduce((a,b)=>a+(b-mean)**2,0)/Math.max(1,vals.length-1));
  const spHome=.8*(Number((ratings.find(r=>r.Team===g.Home)||{})['SP+ Z'])-Number((ratings.find(r=>r.Team===g.Away)||{})['SP+ Z']))*sd;
  const talHome=.2*(Number((ratings.find(r=>r.Team===g.Home)||{})['Talent Z'])-Number((ratings.find(r=>r.Team===g.Away)||{})['Talent Z']))*sd;
  const sign=texasHome?1:-1,sp=spHome*sign,tal=talHome*sign,hfa=Number(g['HFA to Home'])*sign;
  const res=(currentWeek().results||{})[gameId(g)];
  control.innerHTML=`<div class="texasHero"><div class="texasMatch"><div><div class="texasTeam">${oppName}</div><div class="mini">V3 #${or['V3 Rank']} · ${Number(or['V3 Rating']).toFixed(1)}</div></div><div class="texasAt">${g['Neutral?']?'VS':'AT'}</div><div><div class="texasTeam right">Texas</div><div class="mini" style="text-align:right">V3 #${tr['V3 Rank']} · ${Number(tr['V3 Rating']).toFixed(1)}</div></div></div><div class="texasCall"><div class="texasMetric"><div class="tlabel">BOK Fair Line</div><div class="tvalue">${g['BOK Fair Line']}</div></div><div class="texasMetric"><div class="tlabel">Official ATS Pick</div><div class="tvalue" style="color:var(--burnt)">${g['ATS Pick']}</div></div><div class="texasMetric"><div class="tlabel">Model Edge</div><div class="tvalue">${Number(g['Model Edge']).toFixed(1)}</div></div></div></div>`;
  snap.innerHTML=`<div class="intelgrid"><div class="intelbox"><div class="label">Texas V3 Rank</div><div class="v">#${tr['V3 Rank']}</div></div><div class="intelbox"><div class="label">Opponent V3 Rank</div><div class="v">#${or['V3 Rank']}</div></div><div class="intelbox"><div class="label">Frozen Splash</div><div class="v">${splashText(g)}</div></div><div class="intelbox"><div class="label">Projected Margin</div><div class="v">Texas ${texasMargin>=0?'+':''}${texasMargin.toFixed(1)}</div></div><div class="intelbox"><div class="label">Site</div><div class="v">${g['Neutral?']?'Neutral':(texasHome?'Home':'Away')}</div></div><div class="intelbox"><div class="label">Status</div><div class="v">${res?res.grade:(currentWeek().locked?'LOCKED':'PRELIM')}</div></div></div>`;
  const dc=(name,val,sub)=>`<div class="driverCard"><div class="mini">${name}</div><div class="dval">${val>=0?'+':''}${val.toFixed(1)}</div><div class="mini">${sub}</div></div>`;
  drivers.innerHTML=dc('80% SP+',sp,'Texas-side margin contribution')+dc('20% Talent',tal,'Texas-side margin contribution')+dc('HFA',hfa,g['Neutral?']?'Neutral site':(texasHome?'Texas home field':'Opponent home field'));
  const direction=Number(g['Model Edge'])<0.05?'essentially in line with':(String(g['ATS Pick']).startsWith('Texas ')?'more favorable to Texas than':'less favorable to Texas than');
  pub.textContent=`BOK Model V3.0: ${g['BOK Fair Line']}. Frozen Splash line: ${splashText(g)}. Official ATS pick: ${g['ATS Pick']} (${Number(g['Model Edge']).toFixed(1)}-point edge). Texas enters Week ${currentWeek().week} at V3 #${tr['V3 Rank']} (${Number(tr['V3 Rating']).toFixed(1)}), with ${oppName} at #${or['V3 Rank']} (${Number(or['V3 Rating']).toFixed(1)}). The model is ${direction} the frozen market. Margin components from the Texas perspective: SP+ ${sp>=0?'+':''}${sp.toFixed(1)}, talent ${tal>=0?'+':''}${tal.toFixed(1)}, HFA ${hfa>=0?'+':''}${hfa.toFixed(1)}.`;
}

'''
if 'function renderTexasControl()' not in s:s=s.replace('function openIntel(id){',fn+'function openIntel(id){',1)
# make nav render Texas when selected
s=s.replace("if(b.dataset.view==='autopsy')renderAutopsy(); if(b.dataset.view==='results')renderResults();","if(b.dataset.view==='autopsy')renderAutopsy(); if(b.dataset.view==='results')renderResults(); if(b.dataset.view==='texas')renderTexasControl();",1)
# ensure renderAll includes it by adding to updateLock render sequence (safe active refresh)
s=s.replace('renderWar();renderWeekSelector();','renderWar();renderWeekSelector();renderTexasControl();',1)
p.write_text(s,encoding='utf-8')
print('Texas Control V0.7 patch applied')
'''
p.write_text(s,encoding='utf-8')
print('Texas Control V0.7 patch applied')