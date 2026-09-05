from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.7 — 2026','BOK War Room V0.8 — 2026',1)
css='''.autopsyGrid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:18px}.sliceTable{width:100%;min-width:0}.sliceTable th{position:static}.sliceTable td,.sliceTable th{padding:9px 8px}.sliceName{font-weight:900}.sampleWarn{color:var(--gold);font-weight:800}.researchNote{background:#fff8f1;border:1px solid var(--line);border-radius:12px;padding:12px;line-height:1.5}.driverBadge{display:inline-block;border-radius:999px;padding:4px 8px;font-size:11px;font-weight:900;background:#eee5dc}.driverBadge.sp{background:#ffe0c6;color:#8a3500}.driverBadge.talent{background:#e9e3f5;color:#544477}@media(max-width:900px){.autopsyGrid{grid-template-columns:1fr}}
'''
s=s.replace('.scoregrid{display:grid;',css+'.scoregrid{display:grid;',1)
old='''<section id="autopsy" class="view">
  <div class="kpis">
    <div class="kpi"><div class="label">Graded Model Picks</div><div class="value" id="aGraded">0</div></div>
    <div class="kpi"><div class="label">Wins</div><div class="value" id="aWins">0</div></div>
    <div class="kpi"><div class="label">Losses</div><div class="value" id="aLosses">0</div></div>
    <div class="kpi"><div class="label">ATS Win Rate</div><div class="value" id="aRate">—</div></div>
  </div>
  <div class="staffgrid">
    <div class="panel"><div class="panelhead orange"><h2>Edge Distribution</h2></div><div class="pad"><canvas id="edgeChart" width="700" height="280"></canvas></div></div>
    <div class="panel"><div class="panelhead"><h2>Research Guardrail</h2></div><div class="pad rules"><b>V3.0 remains frozen.</b><br><br>Any change to weights, transforms, HFA, injury treatment or other methodology belongs in a separately versioned experimental model. Experimental versions are judged prospectively against future frozen lines—not retroactively optimized against known results.</div></div>
  </div>
</section>'''
new='''<section id="autopsy" class="view">
  <div class="kpis">
    <div class="kpi"><div class="label">Graded Model Picks</div><div class="value" id="aGraded">0</div><div class="sub" id="aWeeks">0 completed weeks</div></div>
    <div class="kpi"><div class="label">Wins</div><div class="value" id="aWins">0</div></div>
    <div class="kpi"><div class="label">Losses</div><div class="value" id="aLosses">0</div></div>
    <div class="kpi"><div class="label">ATS Win Rate</div><div class="value" id="aRate">—</div><div class="sub">Pushes excluded</div></div>
  </div>
  <div class="staffgrid">
    <div class="panel"><div class="panelhead orange"><h2>Season Edge Distribution</h2><span>All frozen cards</span></div><div class="pad"><canvas id="edgeChart" width="700" height="280"></canvas></div></div>
    <div class="panel"><div class="panelhead"><h2>Research Guardrail</h2></div><div class="pad rules"><b>V3.0 remains frozen.</b><br><br>These are descriptive out-of-sample diagnostics only. Small samples are explicitly flagged. No V3.0 weight, transform, HFA, or other methodology changes based on these results. Any candidate change belongs in a separately versioned model and must be judged prospectively.</div></div>
  </div>
  <div class="autopsyGrid">
    <div class="panel"><div class="panelhead"><h3>ATS by Edge Size</h3><span>Signal strength</span></div><div class="pad" id="edgeSlices"></div></div>
    <div class="panel"><div class="panelhead"><h3>ATS by Pick Type</h3><span>Favorite / underdog</span></div><div class="pad" id="pickSlices"></div></div>
    <div class="panel"><div class="panelhead"><h3>ATS by Site</h3><span>Home / away / neutral</span></div><div class="pad" id="siteSlices"></div></div>
    <div class="panel"><div class="panelhead"><h3>ATS by Spread</h3><span>Frozen Splash magnitude</span></div><div class="pad" id="spreadSlices"></div></div>
    <div class="panel"><div class="panelhead"><h3>Primary Rating Driver</h3><span>SP+ vs talent</span></div><div class="pad" id="driverSlices"></div></div>
    <div class="panel"><div class="panelhead"><h3>Projection Error</h3><span>Margin calibration</span></div><div class="pad" id="errorSlices"></div></div>
  </div>
  <div class="panel" style="margin-top:18px"><div class="panelhead orange"><h3>Autopsy Readout</h3><span id="autopsySample">No results yet</span></div><div class="pad"><div class="researchNote" id="autopsyReadout">Results will populate automatically as frozen games finish.</div></div></div>
</section>'''
if old not in s: raise SystemExit('autopsy section anchor not found')
s=s.replace(old,new,1)
start=s.index('function renderAutopsy(){')
end=s.index('function updateLock(){',start)
fn=r'''function autopsyDataset(){
 const rows=[];
 Object.values(state.weeks||{}).forEach(wk=>{
  const wr=Array.isArray(wk.snapshot?.ratings)?wk.snapshot.ratings:ratings;
  const by=Object.fromEntries(wr.map(r=>[r.Team,r]));
  (wk.games||[]).forEach(g=>{
   const r=(wk.results||{})[gameId(g)]; if(!r)return;
   const pickTeam=String(g['ATS Pick']||'').replace(/\s[+-].*$/,'').replace(/\sPK$/,'').trim();
   const pickFav=pickTeam===g['Splash Favorite'];
   const pickHome=pickTeam===g.Home;
   const spreadAbs=Math.abs(Number(g['Splash Fav Spread']));
   const actualHome=Number(r.homeScore)-Number(r.awayScore),err=Math.abs(actualHome-Number(g['Home Projected Margin']));
   const ar=by[g.Away]||{},hr=by[g.Home]||{};
   const spDiff=Math.abs(Number(hr['SP+ Z'])-Number(ar['SP+ Z']));
   const talentDiff=Math.abs(Number(hr['Talent Z'])-Number(ar['Talent Z']));
   const driver=(.8*spDiff)>=.2*talentDiff?'SP+':'Talent';
   const site=g['Neutral?']?'Neutral':(pickHome?'Home pick':'Away pick');
   rows.push({week:wk.week,g,r,grade:r.grade,edge:Number(g['Model Edge']),pickFav,site,spreadAbs,driver,err});
  });
 });
 return rows;
}
function sliceStats(rows,label,test){
 const a=rows.filter(test),w=a.filter(x=>x.grade==='WIN').length,l=a.filter(x=>x.grade==='LOSS').length,p=a.filter(x=>x.grade==='PUSH').length,n=w+l,rate=n?w/n:null;
 return {label,w,l,p,n:a.length,rate};
}
function sliceTable(stats){
 return `<table class="sliceTable"><thead><tr><th>Slice</th><th>W-L-P</th><th>ATS</th><th>N</th></tr></thead><tbody>${stats.map(x=>`<tr><td class="sliceName">${x.label}</td><td>${x.w}-${x.l}-${x.p}</td><td>${x.rate===null?'—':(x.rate*100).toFixed(1)+'%'}</td><td class="${x.n<10?'sampleWarn':''}">${x.n}${x.n<10?' *':''}</td></tr>`).join('')}</tbody></table><div class="mini" style="margin-top:8px">* fewer than 10 graded games — descriptive only.</div>`;
}
function renderAutopsy(){
 const rows=autopsyDataset(),w=rows.filter(x=>x.grade==='WIN').length,l=rows.filter(x=>x.grade==='LOSS').length,p=rows.filter(x=>x.grade==='PUSH').length,dec=w+l;
 document.getElementById('aGraded').textContent=rows.length;document.getElementById('aWins').textContent=w;document.getElementById('aLosses').textContent=l;document.getElementById('aRate').textContent=dec?(100*w/dec).toFixed(1)+'%':'—';
 const weeks=new Set(rows.map(x=>x.week));document.getElementById('aWeeks').textContent=`${weeks.size} week${weeks.size===1?'':'s'} with finals`;
 const allGames=Object.values(state.weeks||{}).flatMap(wk=>wk.games||[]),c=document.getElementById('edgeChart'),ctx=c.getContext('2d');ctx.clearRect(0,0,c.width,c.height);
 const buckets=[['0–1.49',allGames.filter(g=>g['Model Edge']<1.5).length],['1.5–2.99',allGames.filter(g=>g['Model Edge']>=1.5&&g['Model Edge']<3).length],['3–4.99',allGames.filter(g=>g['Model Edge']>=3&&g['Model Edge']<5).length],['5+',allGames.filter(g=>g['Model Edge']>=5).length]];
 const max=Math.max(...buckets.map(x=>x[1]),1);ctx.font='14px system-ui';buckets.forEach((b,i)=>{const x=70+i*150,y=230,h=160*b[1]/max;ctx.fillStyle='#BF5700';ctx.fillRect(x,y-h,80,h);ctx.fillStyle='#151515';ctx.fillText(b[0],x,y+24);ctx.fillText(String(b[1]),x+34,y-h-8);});
 document.getElementById('edgeSlices').innerHTML=sliceTable([sliceStats(rows,'0–1.49',x=>x.edge<1.5),sliceStats(rows,'1.5–2.99',x=>x.edge>=1.5&&x.edge<3),sliceStats(rows,'3–4.99',x=>x.edge>=3&&x.edge<5),sliceStats(rows,'5+',x=>x.edge>=5)]);
 document.getElementById('pickSlices').innerHTML=sliceTable([sliceStats(rows,'Favorite',x=>x.pickFav),sliceStats(rows,'Underdog',x=>!x.pickFav)]);
 document.getElementById('siteSlices').innerHTML=sliceTable([sliceStats(rows,'Home pick',x=>x.site==='Home pick'),sliceStats(rows,'Away pick',x=>x.site==='Away pick'),sliceStats(rows,'Neutral',x=>x.site==='Neutral')]);
 document.getElementById('spreadSlices').innerHTML=sliceTable([sliceStats(rows,'0–6.5',x=>x.spreadAbs<7),sliceStats(rows,'7–13.5',x=>x.spreadAbs>=7&&x.spreadAbs<14),sliceStats(rows,'14–27.5',x=>x.spreadAbs>=14&&x.spreadAbs<28),sliceStats(rows,'28+',x=>x.spreadAbs>=28)]);
 document.getElementById('driverSlices').innerHTML=sliceTable([sliceStats(rows,'SP+ driver',x=>x.driver==='SP+'),sliceStats(rows,'Talent driver',x=>x.driver==='Talent')]);
 const avgErr=rows.length?rows.reduce((a,x)=>a+x.err,0)/rows.length:null,medErr=rows.length?[...rows].sort((a,b)=>a.err-b.err)[Math.floor((rows.length-1)/2)].err:null;
 document.getElementById('errorSlices').innerHTML=`<div class="driverGrid"><div class="driverCard"><div class="mini">Mean Absolute Margin Error</div><div class="dval">${avgErr===null?'—':avgErr.toFixed(1)}</div></div><div class="driverCard"><div class="mini">Median Absolute Error</div><div class="dval">${medErr===null?'—':medErr.toFixed(1)}</div></div><div class="driverCard"><div class="mini">Pushes</div><div class="dval">${p}</div></div></div>`;
 const tag=document.getElementById('autopsySample'),read=document.getElementById('autopsyReadout');tag.textContent=rows.length?`${rows.length} graded games`:'No results yet';
 if(!rows.length){read.textContent='Results will populate automatically as frozen games finish. No conclusions are generated before games are graded.';return;}
 const edge5=sliceStats(rows,'5+',x=>x.edge>=5),dogs=sliceStats(rows,'Underdog',x=>!x.pickFav),favs=sliceStats(rows,'Favorite',x=>x.pickFav);
 const parts=[`Season ATS: ${w}-${l}${p?'-'+p+'P':''} (${dec?(100*w/dec).toFixed(1):'—'}% excluding pushes).`,`Mean absolute margin error: ${avgErr.toFixed(1)} points.`];
 if(edge5.n>=10)parts.push(`5+ point edges are ${edge5.w}-${edge5.l}-${edge5.p} (${edge5.rate===null?'—':(edge5.rate*100).toFixed(1)+'%'}).`);else parts.push(`The 5+ edge bucket has only ${edge5.n} graded game${edge5.n===1?'':'s'}; no inference yet.`);
 if(dogs.n>=10&&favs.n>=10)parts.push(`Favorite picks: ${(favs.rate*100).toFixed(1)}%; underdog picks: ${(dogs.rate*100).toFixed(1)}%.`);else parts.push('Favorite/underdog splits remain small-sample diagnostics until both groups have at least 10 graded games.');
 parts.push('These diagnostics do not alter V3.0. Any pattern worth testing becomes a separately versioned prospective experiment.');read.textContent=parts.join(' ');
}
'''
s=s[:start]+fn+s[end:]
p.write_text(s,encoding='utf-8')
print('V0.8 Autopsy analytics patch applied')