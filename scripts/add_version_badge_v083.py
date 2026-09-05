from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('BOK War Room V0.8.2 — 2026','BOK War Room V0.8.3 — 2026',1)
old='<div class="status"><span class="pill orange">V3.0 OFFICIAL</span><span class="pill warn" id="lockState">WEEK 1 · PRELIMINARY</span></div>'
new='<div class="status"><span class="pill orange">V3.0 OFFICIAL</span><span class="pill" id="appVersion">APP V0.8.3</span><span class="pill warn" id="lockState">WEEK 1 · PRELIMINARY</span></div>'
if old not in s:
    raise SystemExit('status header anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('V0.8.3 version badge added')
