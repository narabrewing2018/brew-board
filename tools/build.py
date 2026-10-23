import re,sys
API_URL='https://script.google.com/macros/s/AKfycbxOxw4dyY9HO7KxVGBWpGfKXkaQfKB_oTkP73aohQD8dV-LDKR0ZP6QW-kk-x_hDzSHaQ/exec'
api_url=sys.argv[1] if len(sys.argv)>1 else API_URL
out=sys.argv[2] if len(sys.argv)>2 else 'app/index.html'
import datetime
VERSION=(sys.argv[3] if len(sys.argv)>3 else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y%m%d-%H%M'))
s=open('src/page.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,b)

rep('<html lang="ja"><head><meta charset="utf-8"><base target="_top">\n<title>醸造ボード</title>',
'''<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>醸造ボード</title>
<meta name="description" content="奈良醸造のタンク状況と今日のタスク">
<meta name="theme-color" content="#eceff0">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/favicon-64.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="醸造ボード">
<meta name="apple-mobile-web-app-status-bar-style" content="default">''')

# extra styles: lock screen + install banner
rep('</style>\n<link rel="stylesheet" href="https://fonts.googleapis.com','''
/* app: lock screen (合言葉) + install hint */
.lock{position:fixed;inset:0;z-index:50;background:var(--bg);display:flex;align-items:center;justify-content:center;padding:24px 16px calc(24px + env(safe-area-inset-bottom,0px))}
.lock form{width:100%;max-width:340px;display:flex;flex-direction:column;gap:14px}
.lock img{width:72px;height:72px;border-radius:16px}
.lock h2{font-family:var(--f-display);font-weight:900;font-size:24px;margin:0}
.lock p{margin:0;color:var(--muted);font-size:14px;line-height:1.6}
.lock input{font:inherit;font-size:18px;padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}
.lock .err{color:var(--today);font-weight:700}
.lock .btn{font-size:16px;padding:12px}
.install{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:12px 0 0;font-size:13px;color:var(--muted)}
.install b{color:var(--ink)}
.install .sp{margin-left:auto;display:flex;gap:8px}
.update{position:sticky;top:env(safe-area-inset-top,0px);z-index:30;display:flex;align-items:center;justify-content:center;gap:10px;width:100%;border:0;background:var(--accent);color:var(--accent-ink);font:inherit;font-weight:700;font-size:14px;padding:12px 16px;cursor:pointer}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com''')

rep('<div class="wrap">\n  <header class="top">','''<div class="lock" id="lock" hidden>
  <form id="lockForm" autocomplete="off">
    <img src="icons/icon-192.png" alt="">
    <h2>醸造ボード</h2>
    <p>合言葉を入力してください。この端末では次回から入力不要です。</p>
    <input id="lockInput" type="password" inputmode="text" autocomplete="current-password" aria-label="合言葉" required>
    <p class="err" id="lockErr" hidden>合言葉が違います</p>
    <button class="btn primary" id="lockBtn" type="submit">開く</button>
  </form>
</div>
<button class="update" id="updateBar" type="button" hidden>新しいバージョンがあります（タップで更新）</button>
<div class="wrap">
  <div class="install" id="installBar" hidden><span id="installText"></span><span class="sp"><button class="btn primary" id="installBtn" hidden>インストール</button><button class="btn" id="installClose">閉じる</button></span></div>
  <header class="top">''')

# backend: replace google.script.run with fetch
rep('''function gas(fn,arg){return new Promise((res,rej)=>{if(!window.google||!google.script){rej({code:'offline'});return;}
  google.script.run.withSuccessHandler(res).withFailureHandler(e=>rej({code:'server',message:String(e&&e.message||e)}))[fn](arg);});}''',
'''const API_URL='%s';
const KEY_STORE='brewboard.k';
function getKey(){try{return localStorage.getItem(KEY_STORE)||'';}catch(e){return S.key||'';}}
function setKey(k){S.key=k;try{if(k)localStorage.setItem(KEY_STORE,k);else localStorage.removeItem(KEY_STORE);}catch(e){}}
async function gas(fn,arg){
  const k=S.key||getKey();if(!k){showLock();throw {code:'auth'};}
  let r;
  try{r=await fetch(API_URL,{method:'POST',credentials:'omit',redirect:'follow',cache:'no-store',
      headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({k,fn:fn==='apiGetAll'?'getAll':fn==='apiWrite'?'write':fn,arg})});}
  catch(e){throw {code:'offline'};}
  let j;try{j=await r.json();}catch(e){throw {code:'server',message:'HTTP '+r.status};}
  if(j&&j.error==='auth'){setKey('');showLock(true);throw {code:'auth'};}
  if(!j||!j.ok)throw {code:'server',message:String(j&&j.message||'error')};
  return j.data;}
function showLock(wrong){const l=$('#lock');if(!l.hidden&&!wrong)return;l.hidden=false;$('#lockErr').hidden=!wrong;
  const i=$('#lockInput');i.value='';setTimeout(()=>i.focus(),50);}
$('#lockForm').addEventListener('submit',async ev=>{ev.preventDefault();const v=$('#lockInput').value.trim();if(!v)return;
  const b=$('#lockBtn');b.disabled=true;b.textContent='確認中…';
  try{const r=await fetch(API_URL,{method:'POST',credentials:'omit',redirect:'follow',cache:'no-store',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({k:v,fn:'ping'})});
    const j=await r.json();
    if(j&&j.ok){setKey(v);$('#lock').hidden=true;refresh(true);}
    else{$('#lockErr').textContent='合言葉が違います';$('#lockErr').hidden=false;$('#lockInput').select();}}
  catch(e){$('#lockErr').textContent='接続できません。電波を確認してください';$('#lockErr').hidden=false;}
  finally{b.disabled=false;b.textContent='開く';}});''' % api_url)

rep("function writeErr(e){toast(e&&e.code==='offline'?",
    "function writeErr(e){if(e&&e.code==='auth')return;toast(e&&e.code==='offline'?")
rep("  }catch(e){console.error('refresh failed',e&&(e.stack||e.message||e.code)||e);S.offline=true;",
    "  }catch(e){console.error('refresh failed',e&&(e.stack||e.message||e.code)||e);if(e&&e.code==='auth'){return;}S.offline=true;")

# install hint + service worker, before initial render
rep("render();refresh();\n</script>",'''/* ---------- app: install hint + offline shell ---------- */
(function(){
  const standalone=window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  let closed=false;try{closed=localStorage.getItem('brewboard.installClosed')==='1';}catch(e){}
  const bar=$('#installBar'),txt=$('#installText'),btn=$('#installBtn');
  let deferred=null;
  $('#installClose').onclick=()=>{bar.hidden=true;try{localStorage.setItem('brewboard.installClosed','1');}catch(e){}};
  if(standalone||closed)return;
  const ua=navigator.userAgent;
  if(/iPhone|iPad|iPod/.test(ua)){txt.innerHTML='<b>ホーム画面に追加</b>するとアプリとして使えます：Safari の共有ボタン（□↑）→「ホーム画面に追加」';bar.hidden=false;}
  window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferred=e;
    txt.innerHTML='<b>アプリとしてインストール</b>すると、ホーム画面やデスクトップから開けます';btn.hidden=false;bar.hidden=false;});
  btn.onclick=async()=>{if(!deferred)return;deferred.prompt();try{await deferred.userChoice;}catch(e){}deferred=null;bar.hidden=true;};
  window.addEventListener('appinstalled',()=>{bar.hidden=true;});
})();
/* ---------- app: new-version notice ---------- */
const APP_VERSION='%s';
let updateShown=false;
async function checkUpdate(){if(updateShown||!navigator.onLine)return;
  try{const r=await fetch('version.json?t='+Date.now(),{cache:'no-store'});if(!r.ok)return;const j=await r.json();
    if(j&&j.v&&j.v!==APP_VERSION){updateShown=true;$('#updateBar').hidden=false;}}catch(e){}}
$('#updateBar').onclick=async()=>{$('#updateBar').textContent='更新中…';
  try{const reg=await navigator.serviceWorker?.getRegistration();if(reg)await reg.update();}catch(e){}
  location.reload();};
setInterval(checkUpdate,5*60*1000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)checkUpdate();});
setTimeout(checkUpdate,5000);
if('serviceWorker' in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{});});}
S.key=getKey();
render();if(S.key)refresh();else showLock();
</script>''')
assert s.count("const APP_VERSION='%s';")==1
s=s.replace("const APP_VERSION='%s';","const APP_VERSION='"+VERSION+"';")
open(out,'w').write(s)
import os,json
json.dump({'v':VERSION},open(os.path.join(os.path.dirname(out) or '.','version.json'),'w'))
print('version',VERSION)
print('wrote',out,len(s))
