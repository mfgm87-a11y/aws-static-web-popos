# -*- coding: utf-8 -*-
"""Genera las paginas HTML de la rutina a partir de los datos."""
import os, json, html, re
import dibujos, fichas, secciones

OUT = "/home/user/aws-static-web-popos/ejercicio-fisico/web"
os.makedirs(OUT, exist_ok=True)

DIAS = [
 ("dia-1","Lunes","L"),("dia-2","Martes","M"),("dia-3","Miércoles","M"),
 ("dia-4","Jueves","J"),("dia-5","Viernes","V"),("dia-6","Sábado","S"),
 ("dia-7","Domingo","D"),
]

# ---------------------------------------------------------------- CSS

CSS = """
:root{
  color-scheme: light;
  --bg:#f4f2ef; --surface:#fffefc; --surface-2:#eceae6;
  --ink:#1b1917; --ink-2:#6d655e; --ink-3:#9a918a;
  --line:#dcd6cf; --line-strong:#c4bcb3;
  --accent:#cf4526; --accent-soft:#f7e3dc; --on-accent:#fffefc;
  --steel:#33697d; --steel-soft:#e0eaee;
  --shadow:0 1px 2px rgba(27,25,23,.06), 0 8px 24px -16px rgba(27,25,23,.3);
  --fig-bg:#faf8f5;
  --r:10px;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme: dark;
    --bg:#141311; --surface:#1e1c1a; --surface-2:#272421;
    --ink:#f2eee9; --ink-2:#a79d94; --ink-3:#7b726a;
    --line:#332f2b; --line-strong:#463f39;
    --accent:#ff6b45; --accent-soft:#3a201a; --on-accent:#171310;
    --steel:#79b3c8; --steel-soft:#1d2c32;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.8);
    --fig-bg:#191715;
  }
}
:root[data-theme="dark"]{
  color-scheme: dark;
  --bg:#141311; --surface:#1e1c1a; --surface-2:#272421;
  --ink:#f2eee9; --ink-2:#a79d94; --ink-3:#7b726a;
  --line:#332f2b; --line-strong:#463f39;
  --accent:#ff6b45; --accent-soft:#3a201a; --on-accent:#171310;
  --steel:#79b3c8; --steel-soft:#1d2c32;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.8);
    --fig-bg:#191715;
}

*{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"Source Sans 3", ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif;
  font-size:16px; line-height:1.55; -webkit-text-size-adjust:100%;
}
h1,h2,h3,.disp{font-family:Oswald, "Source Sans 3", ui-sans-serif, system-ui, sans-serif; font-weight:600; letter-spacing:.01em;}
h1,h2,h3{text-wrap:balance; margin:0}
a{color:var(--accent)}
.num{font-variant-numeric:tabular-nums}

/* ---------- barra superior ---------- */
.top{
  position:sticky; top:env(safe-area-inset-top,0px); z-index:40;
  background:color-mix(in srgb, var(--bg) 92%, transparent);
  backdrop-filter:saturate(150%) blur(10px);
  border-bottom:1px solid var(--line);
}
.top-in{max-width:760px; margin:0 auto; padding:8px 16px; display:flex; align-items:center; gap:10px}
.home{
  font-family:Oswald,sans-serif; font-size:12px; text-transform:uppercase; letter-spacing:.14em;
  color:var(--ink-2); text-decoration:none; white-space:nowrap; padding:6px 0;
}
.home:hover{color:var(--accent)}
.days{display:flex; gap:3px; margin-left:auto; flex-wrap:nowrap}
.days a{
  width:30px; height:30px; display:grid; place-items:center; text-decoration:none;
  font-family:Oswald,sans-serif; font-size:13px; border-radius:7px;
  color:var(--ink-2); border:1px solid transparent;
}
.days a:hover{background:var(--surface-2); color:var(--ink)}
.days a[aria-current="page"]{background:var(--accent); color:var(--on-accent); border-color:var(--accent)}
.days .sec-chip{
  width:auto; min-width:0; padding:0 8px; height:28px; font-size:12px;
  letter-spacing:.02em; border:1px solid var(--line);
}
.days .dado{font-size:19px; line-height:1; margin-left:5px; border-left:1px solid var(--line); border-radius:0 7px 7px 0; padding-left:7px; width:auto; min-width:30px}

/* ---------- estructura ---------- */
.wrap{max-width:760px; margin:0 auto; padding-inline:16px; padding-block:0 120px}
.hero{padding-block:26px 20px; border-bottom:2px solid var(--ink)}
.eyebrow{
  font-family:Oswald,sans-serif; font-size:12px; letter-spacing:.18em; text-transform:uppercase;
  color:var(--accent); margin:0 0 6px;
}
.hero h1{font-size:clamp(30px,8vw,46px); line-height:1.02; text-transform:uppercase}
.hero .focus{margin:10px 0 0; color:var(--ink-2); font-size:16px; max-width:52ch}
.meta{display:flex; flex-wrap:wrap; gap:6px; margin-top:14px}
.chip{
  font-size:12.5px; padding:4px 9px; border-radius:99px; border:1px solid var(--line-strong);
  color:var(--ink-2); background:var(--surface);
}
.chip.load{border-color:var(--accent); color:var(--accent); background:var(--accent-soft)}

/* ---------- progreso ---------- */
.prog{display:flex; align-items:center; gap:10px; margin-top:16px}
.bar{flex:1; height:5px; border-radius:99px; background:var(--surface-2); overflow:hidden}
.bar i{display:block; height:100%; width:0%; background:var(--accent); transition:width .25s ease}
.prog .n{font-family:Oswald,sans-serif; font-size:13px; color:var(--ink-2)}
.reset{
  background:none; border:1px solid var(--line-strong); color:var(--ink-2);
  font:inherit; font-size:12.5px; padding:3px 10px; border-radius:99px; cursor:pointer;
}
.reset:hover{border-color:var(--accent); color:var(--accent)}

/* ---------- bloques ---------- */
.block{margin-top:26px}
.bhead{display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; padding-bottom:8px; border-bottom:1px solid var(--line)}
.bhead h2{font-size:21px; text-transform:uppercase; letter-spacing:.03em}
.bhead .t{font-family:Oswald,sans-serif; font-size:13px; color:var(--ink-3); margin-left:auto}
.bhead .kind{
  font-size:11px; font-family:Oswald,sans-serif; letter-spacing:.12em; text-transform:uppercase;
  color:var(--steel); background:var(--steel-soft); padding:2px 8px; border-radius:99px;
}
.bnote{color:var(--ink-2); font-size:14.5px; margin:10px 0 0}

/* rondas */
.rounds{display:flex; align-items:center; gap:8px; margin-top:12px; flex-wrap:wrap}
.rounds .lb{font-family:Oswald,sans-serif; font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3)}
.rd{
  width:36px; height:36px; border-radius:9px; border:1.5px solid var(--line-strong);
  background:var(--surface); color:var(--ink-2); font-family:Oswald,sans-serif; font-size:15px;
  cursor:pointer; transition:.15s;
}
.rd:hover{border-color:var(--accent)}
.rd[aria-pressed="true"]{background:var(--accent); border-color:var(--accent); color:var(--on-accent)}

/* ejercicios */
.ex{list-style:none; margin:12px 0 0; padding:0; display:flex; flex-direction:column; gap:6px}
.ex>li{
  background:var(--surface); border:1px solid var(--line); border-radius:var(--r);
  box-shadow:var(--shadow); overflow:hidden;
}
.row{display:flex; align-items:flex-start; gap:11px; padding:11px 13px; cursor:pointer}
.row input{
  appearance:none; -webkit-appearance:none; flex:none; margin:2px 0 0;
  width:21px; height:21px; border-radius:6px; border:1.5px solid var(--line-strong);
  background:var(--surface); cursor:pointer; position:relative; transition:.15s;
}
.row input:checked{background:var(--accent); border-color:var(--accent)}
.row input:checked::after{
  content:""; position:absolute; left:6px; top:2px; width:5px; height:10px;
  border:solid var(--on-accent); border-width:0 2px 2px 0; transform:rotate(42deg);
}
.row input:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
.txt{min-width:0; flex:1}
.nm{font-weight:600; font-size:15.5px; line-height:1.3}
.code{
  font-family:Oswald,sans-serif; color:var(--accent); font-size:13px; margin-right:6px;
  letter-spacing:.06em;
}
.sub{display:flex; flex-wrap:wrap; gap:4px 10px; margin-top:3px; font-size:13.5px; color:var(--ink-2)}
.sub .d{font-weight:600; color:var(--ink); font-variant-numeric:tabular-nums}
.row input:checked ~ .txt .nm{text-decoration:line-through; color:var(--ink-3)}
.row input:checked ~ .txt .sub{opacity:.5}
details.how{border-top:1px solid var(--line); background:var(--surface-2)}
details.how summary{
  cursor:pointer; padding:8px 13px; font-family:Oswald,sans-serif; font-size:12px;
  letter-spacing:.12em; text-transform:uppercase; color:var(--ink-2); list-style:none;
}
details.how summary::-webkit-details-marker{display:none}
details.how summary::before{content:"▸ "; color:var(--accent)}
details.how[open] summary::before{content:"▾ "}
details.how p{margin:0; padding:0 13px 12px; font-size:14.5px; color:var(--ink-2); max-width:62ch}
details.how strong{color:var(--ink)}

/* descanso */
.restbtn{
  margin-top:12px; width:100%; padding:11px; border-radius:var(--r); cursor:pointer;
  background:var(--ink); color:var(--bg); border:none;
  font-family:Oswald,sans-serif; font-size:14px; letter-spacing:.1em; text-transform:uppercase;
}
.restbtn:hover{background:var(--accent); color:var(--on-accent)}

/* notas */
.notes{
  margin-top:28px; padding:16px 18px; border-radius:var(--r);
  background:var(--surface); border:1px solid var(--line); border-left:3px solid var(--accent);
}
.notes h3{font-size:13px; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); margin-bottom:8px}
.notes ul{margin:0; padding-left:18px; display:flex; flex-direction:column; gap:8px}
.notes li{font-size:14.5px; color:var(--ink-2); max-width:62ch}
.notes strong{color:var(--ink)}

/* pie */
.pager{display:flex; gap:10px; margin-top:30px; padding-top:18px; border-top:1px solid var(--line)}
.pager a{
  flex:1; text-decoration:none; padding:12px 14px; border-radius:var(--r);
  background:var(--surface); border:1px solid var(--line); color:var(--ink);
}
.pager a:hover{border-color:var(--accent)}
.pager .k{
  display:block; font-family:Oswald,sans-serif; font-size:11px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3); margin-bottom:2px;
}
.pager .v{font-family:Oswald,sans-serif; font-size:16px}
.pager .next{text-align:right}

/* ---------- cronometro ---------- */
.timer{
  position:fixed; left:0; right:0; bottom:0; z-index:60;
  background:var(--ink); color:var(--bg);
  padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));
  transform:translateY(110%); transition:transform .22s ease;
}
.timer.on{transform:none}
.timer-in{max-width:760px; margin:0 auto; display:flex; align-items:center; gap:12px}
.timer .lb{font-family:Oswald,sans-serif; font-size:11px; letter-spacing:.16em; text-transform:uppercase; opacity:.6}
.timer .cd{font-family:Oswald,sans-serif; font-size:34px; line-height:1; font-variant-numeric:tabular-nums}
.timer .tbar{flex:1; height:4px; border-radius:99px; background:rgba(128,128,128,.35); overflow:hidden}
.timer .tbar i{display:block; height:100%; width:100%; background:var(--accent); transition:width 1s linear}
.timer button{
  background:none; border:1px solid rgba(128,128,128,.5); color:inherit; cursor:pointer;
  font-family:Oswald,sans-serif; font-size:12px; letter-spacing:.08em; text-transform:uppercase;
  padding:7px 11px; border-radius:8px;
}
.timer button:hover{border-color:var(--accent); color:var(--accent)}


/* ---------- monachos ---------- */
.figbox{border-top:1px solid var(--line); background:var(--fig-bg); padding:4px 8px 0}
svg.fig{width:100%; height:auto; display:block; max-width:300px; margin:0 auto}
@media (max-width:560px){ svg.fig{max-width:250px} }
.f-l{stroke:var(--ink); stroke-width:3.4; stroke-linecap:round; fill:none}
.f-lf{stroke:var(--ink-3); stroke-width:3; stroke-linecap:round; fill:none}
.f-h{stroke:var(--ink); stroke-width:2.6; fill:var(--fig-bg)}
.f-g{stroke:var(--line-strong); stroke-width:2}
.f-mat{fill:var(--surface-2)}
.f-box{fill:var(--surface-2); stroke:var(--line-strong); stroke-width:1.5}
.f-obj{stroke:var(--line-strong); stroke-width:2.4; fill:none; stroke-linecap:round}
.f-d{stroke:var(--accent); stroke-width:1.5; stroke-dasharray:4 4; fill:none}
.f-a{stroke:var(--accent); stroke-width:1.8; fill:none}
.f-am{fill:var(--accent)}
.f-e{fill:var(--accent)}
.f-eb{stroke:var(--accent); stroke-width:2.6; stroke-linecap:round}
.f-t{fill:var(--accent); font-family:"Source Sans 3",sans-serif; font-size:9px; font-weight:600}
.f-c{fill:var(--ink-3); font-family:Oswald,sans-serif; font-size:9px; letter-spacing:.08em}
:root.sin-fig .figbox{display:none}

/* ---------- pistas del ejercicio ---------- */
.cues{display:flex; flex-wrap:wrap; gap:5px; padding:9px 13px 0}
.cue{
  font-size:12px; line-height:1.3; padding:3px 8px; border-radius:6px;
  background:var(--surface-2); color:var(--ink-2); border:1px solid var(--line);
}
.cue b{
  color:var(--ink-3); font-family:Oswald,sans-serif; font-weight:500;
  font-size:10px; letter-spacing:.1em; text-transform:uppercase; margin-right:4px;
}
.cue.cad b{color:var(--steel)}
.cue.hasta{background:var(--accent-soft); border-color:var(--accent); color:var(--ink)}
.cue.hasta b{color:var(--accent)}
details.how p+p{margin-top:8px}
details.how .tag{
  font-family:Oswald,sans-serif; font-size:11px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--accent); margin-right:5px;
}
details.how .tag.err{color:var(--steel)}
.figtog{
  background:none; border:1px solid var(--line-strong); color:var(--ink-2);
  font:inherit; font-size:12.5px; padding:3px 10px; border-radius:99px; cursor:pointer;
}
.figtog:hover{border-color:var(--accent); color:var(--accent)}

@media (max-width:420px){
  .timer .cd{font-size:28px}
  .home{font-size:11px}
  .days a{width:27px; height:27px; font-size:12px}
}
@media (prefers-reduced-motion:reduce){
  *{transition:none !important; animation:none !important}
}
"""

# ---------------------------------------------------------------- JS

JS = """
(function(){
  var KEY = "rutina:" + (window.PAGE_KEY || "x");
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch(e){ state = {}; }
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(state)); } catch(e){} }

  var boxes = [], rds = [];
  var barEl = document.querySelector('.bar i');
  var nEl   = document.querySelector('.prog .n');

  function refresh(){
    var total = boxes.length + rds.length;
    var done  = boxes.filter(function(b){ return b.checked; }).length
              + rds.filter(function(r){ return r.getAttribute('aria-pressed') === 'true'; }).length;
    if (barEl) barEl.style.width = total ? Math.round(done/total*100) + '%' : '0%';
    if (nEl) nEl.textContent = done + ' / ' + total;
  }

  function ambito(){
    return document.querySelector('.rutina:not([hidden])') || document;
  }

  function enlaza(){
    var raiz = ambito();
    boxes = Array.prototype.slice.call(raiz.querySelectorAll('.row input[type=checkbox]'));
    rds   = Array.prototype.slice.call(raiz.querySelectorAll('.rd'));

    boxes.forEach(function(b){
      if (b.dataset.lig) return;
      b.dataset.lig = '1';
      if (state[b.id]) b.checked = true;
      b.addEventListener('change', function(){
        if (b.checked) state[b.id] = 1; else delete state[b.id];
        save(); refresh();
      });
    });

    rds.forEach(function(r){
      if (r.dataset.lig) return;
      r.dataset.lig = '1';
      if (state[r.id]) r.setAttribute('aria-pressed','true');
      r.addEventListener('click', function(){
        var on = r.getAttribute('aria-pressed') === 'true';
        r.setAttribute('aria-pressed', on ? 'false' : 'true');
        if (on) delete state[r.id]; else state[r.id] = 1;
        save(); refresh();
      });
    });

    document.querySelectorAll('.restbtn').forEach(function(b){
      if (b.dataset.lig) return;
      b.dataset.lig = '1';
      b.addEventListener('click', function(){ start(parseInt(b.dataset.sec,10) || 60, b.dataset.label); });
    });

    refresh();
  }

  var rs = document.querySelector('.reset');
  if (rs) rs.addEventListener('click', function(){
    boxes.forEach(function(b){ b.checked = false; delete state[b.id]; });
    rds.forEach(function(r){ r.setAttribute('aria-pressed','false'); delete state[r.id]; });
    save(); refresh();
  });

  /* ---- cronometro de descanso ---- */
  var t    = document.querySelector('.timer');
  var cd   = t && t.querySelector('.cd');
  var tbar = t && t.querySelector('.tbar i');
  var tlb  = t && t.querySelector('.lb');
  var iv = null, left = 0, span = 0, lock = null;

  function fmt(s){
    var m = Math.floor(s/60), r = s%60;
    return m > 0 ? m + ':' + (r<10?'0':'') + r : String(r);
  }
  function paint(){
    if (cd) cd.textContent = fmt(left);
    if (tbar) tbar.style.width = span ? (left/span*100) + '%' : '0%';
  }
  function beep(){
    try {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      var c = new AC(), o = c.createOscillator(), g = c.createGain();
      o.type = 'sine'; o.frequency.value = 660;
      g.gain.setValueAtTime(.001, c.currentTime);
      g.gain.exponentialRampToValueAtTime(.3, c.currentTime + .02);
      g.gain.exponentialRampToValueAtTime(.001, c.currentTime + .55);
      o.connect(g); g.connect(c.destination);
      o.start(); o.stop(c.currentTime + .6);
      setTimeout(function(){ try{ c.close(); }catch(e){} }, 900);
    } catch(e){}
  }
  function stop(){
    if (iv) clearInterval(iv);
    iv = null;
    if (t) t.classList.remove('on');
    if (lock) { try { lock.release(); } catch(e){} lock = null; }
  }
  function start(sec, label){
    if (!t) return;
    if (iv) clearInterval(iv);
    span = left = sec;
    if (tlb) tlb.textContent = label || 'Descanso';
    t.classList.add('on');
    paint();
    iv = setInterval(function(){
      left--;
      paint();
      if (left <= 0){ clearInterval(iv); iv = null; beep(); setTimeout(stop, 1600); }
    }, 1000);
  }

  var plus = t && t.querySelector('[data-add]');
  if (plus) plus.addEventListener('click', function(){ left += 15; span = Math.max(span, left); paint(); });
  var sk = t && t.querySelector('[data-stop]');
  if (sk) sk.addEventListener('click', stop);

  /* la pantalla no se apaga mientras entrenas */
  if ('wakeLock' in navigator){
    var req = function(){
      navigator.wakeLock.request('screen').then(function(l){ lock = l; }).catch(function(){});
    };
    document.addEventListener('click', function once(){
      document.removeEventListener('click', once); req();
    });
    document.addEventListener('visibilitychange', function(){
      if (document.visibilityState === 'visible' && !lock) req();
    });
  }

  var ft = document.querySelector('.figtog');
  if (ft) {
    var R = document.documentElement, KF = 'rutina:sinfig';
    var off = false;
    try { off = localStorage.getItem(KF) === '1'; } catch(e){}
    var pinta = function(){
      R.classList.toggle('sin-fig', off);
      ft.textContent = off ? 'Mostrar dibujos' : 'Ocultar dibujos';
    };
    pinta();
    ft.addEventListener('click', function(){
      off = !off;
      try { localStorage.setItem(KF, off ? '1' : '0'); } catch(e){}
      pinta();
    });
  }

  window.RUTINA_ENLAZA = function(){
    try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch(e){ state = {}; }
    enlaza();
  };
  enlaza();
})();
"""

# ---------------------------------------------------------------- datos

E = html.escape

def dia(n, nombre, focus, carga, dur, blocks, notes):
    return dict(n=n, nombre=nombre, focus=focus, carga=carga, dur=dur, blocks=blocks, notes=notes)

def warm(name, mins, note, items):
    return dict(kind="warm", name=name, mins=mins, note=note, items=items, tag="Seguido")

def work(name, mins, rounds, rest, tag, note, items):
    return dict(kind="work", name=name, mins=mins, rounds=rounds, rest=rest, tag=tag, note=note, items=items)

def cool(name, mins, note, items):
    return dict(kind="cool", name=name, mins=mins, note=note, items=items, tag="Sostenido")

def it(n, d, load=None, how=None, code=None):
    return dict(n=n, d=d, load=load, how=how, code=code)

DATA = {}

# ---- DIA 1
DATA["dia-1"] = dia(1, "Lunes",
  "Cuádriceps · Pecho medio · Dorsal ancho · Bíceps",
  "Mancuernas en Actual — 7,5 kg c/u", 30,
  [
    warm("Calentamiento", 4, "Uno detrás de otro, sin peso y sin descanso.", [
      it("Sentadilla al aire", "15 reps"),
      it("Círculos de brazos", "15 por sentido"),
      it("Gato–camello", "10 reps"),
      it("Zancada en el sitio con rotación", "6 por pierna"),
      it("Flexiones de rodillas", "8 reps"),
    ]),
    work("Bloque A", 13, 3, 75, "Tri-serie",
      "A1 → A2 → A3 seguidos. Al terminar los tres, descansas y vuelves a empezar.", [
      it("Sentadilla goblet", "12 reps", "1 mancuerna · 7,5 kg", code="A1",
         how="Abraza la mancuerna contra el pecho, agarrándola por el disco de arriba. Pies al ancho de los hombros, puntas un poco hacia afuera. Baja hasta que los muslos queden paralelos al piso, rodillas siguiendo la línea de los pies. Sube empujando con el medio del pie. <strong>El espejo es tu juez:</strong> la espalda no se redondea."),
      it("Press de pecho en el piso", "10 reps", "2 mancuernas · 7,5 kg", code="A2",
         how="Acostado boca arriba en el tapete, rodillas dobladas. Mancuernas a la altura del pecho, codos a unos 45° del cuerpo. Sube hasta estirar los brazos. El piso frena el recorrido y de paso te cuida el hombro."),
      it("Pullover con mancuerna", "12 reps", "1 mancuerna · 7,5 kg", code="A3",
         how="Acostado en el tapete, sostén <strong>una</strong> mancuerna con las dos manos sobre el pecho. Con los brazos casi rectos, llévala por detrás de la cabeza hasta sentir el estirón en las costillas y el dorsal. Regresa. La espalda baja pegada al piso todo el tiempo."),
    ]),
    work("Bloque B", 9, 3, 60, "Tri-serie", None, [
      it("Zancada inversa", "10 por pierna", "2 mancuernas · 7,5 kg", code="B1",
         how="De pie con las mancuernas colgando. Da un paso largo <strong>hacia atrás</strong> y baja hasta que la rodilla de atrás casi toque el tapete. Empuja con el talón de adelante para volver. Todo el peso vive en la pierna de adelante; la de atrás solo hace equilibrio."),
      it("Curl de bíceps con la vara", "12 reps", "Barra · ~19 kg", code="B2",
         how="De pie, agarre supinado (palmas al frente) al ancho de los hombros. Codos pegados a las costillas y quietos. Sube la barra hasta el pecho sin balancear la espalda. Si te queda liviana, baja el ritmo: 3 segundos para bajar."),
      it("Plancha abdominal", "40 s", None, code="B3",
         how="Antebrazos y puntas de los pies. Cuerpo en línea recta desde los talones hasta la cabeza. Aprieta glúteos y abdomen. Si la cadera se hunde, paras: mejor 25 segundos bien que 40 mal."),
    ]),
    cool("Estiramiento", 4, None, [
      it("Cuádriceps de pie, talón al glúteo", "40 s por pierna"),
      it("Pecho en el marco de la puerta", "40 s"),
      it("Dorsal: brazo arriba, inclínate al lado contrario", "30 s por lado"),
      it("Isquios sentado, pierna estirada al frente", "30 s por pierna"),
    ]),
  ],
  ["Este es el día más pesado de piernas de la semana. Si el martes amaneces adolorido, tranquilo: el Día 2 es de isquios y glúteo, músculos distintos.",
   "Anota cuántas reps completaste en la <strong>tercera ronda</strong> de la sentadilla goblet. Ese es tu número de referencia para saber cuándo subir peso."])

# ---- DIA 2
DATA["dia-2"] = dia(2, "Martes",
  "Isquios y glúteo · Pecho superior y hombro anterior · Espalda media · Tríceps largo",
  "Barra ~19 kg + mancuernas en Actual", 30,
  [
    warm("Calentamiento", 4, "Uno detrás de otro, sin peso.", [
      it("Bisagra de cadera sin peso", "15 reps"),
      it("Puente de glúteo en el tapete", "15 reps"),
      it("Y–T–W boca abajo", "8 de cada letra"),
      it("Balanceo de pierna al frente y atrás", "10 por pierna"),
      it("Rotación de hombros con brazos estirados", "15 reps"),
    ]),
    work("Bloque A", 13, 3, 75, "Tri-serie", None, [
      it("Peso muerto rumano con barra", "12 reps", "Barra · ~19 kg", code="A1",
         how="De pie, barra al frente de los muslos, agarre prono. <strong>Rodillas casi rectas, apenas suaves.</strong> Empuja la cadera hacia atrás como si cerraras un cajón con la cola. La barra baja rozando las piernas. Para cuando sientas el estirón fuerte atrás del muslo, que suele ser a media canilla. Sube apretando el glúteo. La espalda nunca se redondea: si se redondea, bajaste demasiado."),
      it("Press de hombro sentado", "10 reps", "2 mancuernas · 7,5 kg", code="A2",
         how="Sentado normal en la silla, espalda apoyada en el espaldar. Mancuernas a la altura de los hombros, palmas al frente. Empuja recto hacia arriba. Sentado y con el espaldar detrás no hay forma de arquear la espalda, que es el error de siempre en este ejercicio. Trabaja el hombro anterior y la parte de arriba del pecho."),
      it("Remo inclinado con barra", "12 reps", "Barra · ~19 kg", code="A3",
         how="Bisagra de cadera hasta que el torso quede a unos 45°, espalda plana, barra colgando. Jala la barra al ombligo llevando los codos hacia atrás. <strong>Aprieta los omóplatos</strong> un segundo arriba. Baja controlado hasta estirar los brazos."),
    ]),
    work("Bloque B", 9, 3, 60, "Tri-serie", None, [
      it("Puente de glúteo con peso", "15 reps", "1 mancuerna sobre la cadera", code="B1",
         how="Acostado, rodillas dobladas, pies planos. Mancuerna atravesada sobre los huesos de la cadera, sujétala con las dos manos. Sube hasta formar una línea recta de rodillas a hombros. <strong>Aprieta el glúteo arriba 2 segundos.</strong> Baja sin tocar el piso."),
      it("Extensión de tríceps sobre la cabeza", "12 reps", "1 mancuerna · 7,5 kg", code="B2",
         how="Sentado o de pie. Una mancuerna con las dos manos, agarrada por el disco de arriba, sostenida detrás de la cabeza. Codos apuntando al techo y <strong>quietos</strong>: solo se mueve el antebrazo. Esto pega en la porción larga del tríceps, la que le da grosor al brazo por detrás."),
      it("Muerto bicho (dead bug)", "10 por lado", None, code="B3",
         how="Boca arriba, brazos al techo, rodillas y caderas a 90°. Estira el brazo derecho hacia atrás y la pierna izquierda al frente al mismo tiempo, sin que la espalda baja se despegue del tapete. Regresa y cambia. Lento. Si la espalda se arquea, no estires tanto la pierna."),
    ]),
    cool("Estiramiento", 4, None, [
      it("Isquios: pie adelante, talón clavado, punta arriba, inclínate", "40 s por pierna"),
      it("Glúteo sentado en el piso, figura 4", "40 s por lado"),
      it("Tríceps: codo arriba, mano a la espalda", "30 s por brazo"),
      it("Pecho en el marco de la puerta, brazo alto", "30 s por lado"),
    ]),
  ],
  ["El peso muerto rumano es el ejercicio más valioso de la semana y el más fácil de hacer mal. <strong>El primer día hazlo sin peso frente al espejo</strong> hasta que el movimiento salga solo: cadera atrás, espalda plana.",
   "Si lo sientes en la espalda baja en vez de atrás del muslo, estás doblando la espalda en lugar de la cadera. Menos recorrido y más control."])

# ---- DIA 3
DATA["dia-3"] = dia(3, "Miércoles",
  "Pierna unilateral y equilibrio · Pecho externo · Dorsal unilateral · Braquial y antebrazo",
  "Aperturas con 5 kg · el resto en Actual", 30,
  [
    warm("Calentamiento", 4, None, [
      it("Marcha en el sitio con rodilla alta", "30 s"),
      it("Parado en un pie", "30 s por pierna"),
      it("Círculos de cadera", "10 por lado"),
      it("Abrazo y abre (apertura de pecho)", "15 reps"),
      it("Muñecas: círculos y flexión-extensión", "30 s"),
    ]),
    work("Bloque A", 13, 3, 75, "Tri-serie", None, [
      it("Sentadilla dividida", "10 por pierna", "2 mancuernas · 7,5 kg", code="A1",
         how="Un pie adelante y uno atrás, a un paso largo, <strong>los dos en el piso</strong>. No caminas: bajas y subes en el mismo sitio. La rodilla de atrás baja hasta casi tocar el tapete. Termina las 10 de una pierna y cambias. Mancuernas colgando a los lados."),
      it("Aperturas en el piso", "12 reps", "2 mancuernas · 5 kg", code="A2",
         how="Acostado en el tapete. Mancuernas arriba del pecho, palmas enfrentadas, <strong>codos con una curva suave que no cambia</strong>. Abre los brazos en arco hasta que los codos toquen el piso. Sube juntando como si abrazaras un barril. El peso es liviano a propósito: este ejercicio estira la fibra externa del pecho, no busca carga."),
      it("Remo a un brazo sin apoyo", "10 por lado", "1 mancuerna · 7,5 kg", code="A3",
         how="Pies al ancho de la cadera, bisagra de cadera hasta que el torso quede casi paralelo al piso. <strong>Apoya el antebrazo libre sobre tu propio muslo</strong> para sostener la espalda. Jala el codo hacia la cadera trasera, con la palma mirando al cuerpo. Ese ángulo carga el dorsal ancho y deja quieto el trapecio."),
    ]),
    work("Bloque B", 9, 3, 60, "Tri-serie", None, [
      it("Peso muerto a una pierna", "8 por pierna", "1 mancuerna · 7,5 kg", code="B1",
         how="Mancuerna en la mano <strong>contraria</strong> a la pierna que te sostiene. Bisagra de cadera sobre esa pierna mientras la otra se va hacia atrás formando una línea recta con la espalda. Baja hasta donde controles. La cadera queda cuadrada, sin abrirse al lado. Si te tambaleas, roza la pared con los dedos de la otra mano."),
      it("Curl martillo", "12 reps", "2 mancuernas · 7,5 kg", code="B2",
         how="De pie, palmas enfrentadas como si sostuvieras dos martillos. Sube sin girar la muñeca. Trabaja el braquial, que está debajo del bíceps, y el antebrazo. Es lo que hace que el brazo se vea más lleno visto de lado."),
      it("Plancha lateral", "30 s por lado", None, code="B3",
         how="Antebrazo y canto del pie. Cadera arriba, cuerpo en línea. Si es mucho, apoya la rodilla de abajo en el tapete."),
    ]),
    cool("Estiramiento", 4, None, [
      it("Flexor de cadera en zancada, rodilla en el tapete", "40 s por lado"),
      it("Pecho en el piso: brazo estirado y gira el cuerpo", "40 s por lado"),
      it("Antebrazo: palma arriba y palma abajo, tira los dedos", "20 s cada una"),
      it("Costado: brazo arriba, inclínate", "30 s por lado"),
    ]),
  ],
  ["Hoy todo es a una pierna o a un brazo. Vas a descubrir que un lado es más fuerte que el otro, cosa normal en todo el mundo. <strong>Empieza siempre por el lado débil</strong> y haz en el fuerte las mismas reps que te salieron en el débil. En dos meses se empareja.",
   "Las aperturas con 5 kg pueden saberte a poco. No subas el peso: el hombro en esa posición es frágil y no vale la pena el riesgo."])

# ---- DIA 4
DATA["dia-4"] = dia(4, "Jueves",
  "Glúteo medio y abductores · Pecho inferior · Trapecio y hombro posterior · Tríceps lateral",
  "Pájaro con 2,5 kg · el resto en Actual", 30,
  [
    warm("Calentamiento", 4, None, [
      it("Sentadilla sumo al aire", "15 reps"),
      it("Almeja acostado de lado", "12 por lado"),
      it("Encogimiento de hombros sin peso", "15 reps"),
      it("Flexiones de rodillas", "10 reps"),
      it("Rotación externa de hombro sin peso", "15 por lado"),
    ]),
    work("Bloque A", 13, 3, 75, "Tri-serie", None, [
      it("Sentadilla sumo con mancuerna", "15 reps", "1 mancuerna · 7,5 kg", code="A1",
         how="Pies bien abiertos, más que los hombros, puntas apuntando hacia afuera unos 45°. Mancuerna colgando con las dos manos entre las piernas. Baja recto, <strong>rodillas abriéndose hacia donde apuntan los pies</strong>. Esa apertura es lo que mete al glúteo medio y a los abductores."),
      it("Flexión con manos elevadas", "12 reps", "Manos en el borde del sofá", code="A2",
         how="De pie en el piso, manos en el borde del sofá un poco más abiertas que los hombros. Cuerpo en línea recta de talones a cabeza. Baja el pecho al borde y empuja. Con las manos arriba el trabajo baja a la parte inferior del pecho. El sofá es pesado y ancho: no se mueve. Si te queda fácil, aléjate más con los pies."),
      it("Pájaro (apertura posterior)", "15 reps", "2 mancuernas · 2,5 kg", code="A3",
         how="Inclinado hacia adelante desde la cadera, espalda plana, torso casi paralelo al piso. Mancuernas colgando. Abre los brazos hacia los lados como alas, apretando los omóplatos. <strong>Peso liviano de verdad:</strong> si puedes usar más de 2,5 kg, estás jalando con la espalda en vez del hombro posterior. Este es el músculo que corrige la postura de estar en el computador."),
    ]),
    work("Bloque B", 9, 3, 60, "Tri-serie", None, [
      it("Encogimiento de hombros con barra", "15 reps", "Barra · ~19 kg", code="B1",
         how="Barra colgando al frente de los muslos, brazos rectos. Sube los hombros <strong>derecho hacia las orejas</strong>, sin rodarlos. Aprieta arriba un segundo, baja completo. Nada de girar los hombros en círculo."),
      it("Press cerrado en el piso", "12 reps", "2 mancuernas · 7,5 kg", code="B2",
         how="Acostado en el tapete. Mancuernas juntas sobre el pecho, palmas enfrentadas, <strong>codos pegados a las costillas</strong>. Baja hasta que los tríceps toquen el piso y empuja. Los codos cerrados mandan el trabajo a la cabeza lateral del tríceps, la que se ve por fuera del brazo."),
      it("Plancha con toque de hombro", "10 por lado", None, code="B3",
         how="En plancha alta con los brazos estirados, pies un poco abiertos. Toca el hombro contrario con una mano sin que la cadera se mueva ni un centímetro. Ese <strong>no moverse</strong> es el ejercicio."),
    ]),
    cool("Estiramiento", 4, None, [
      it("Aductor: mariposa sentado o abierto en V", "45 s"),
      it("Glúteo medio: rodilla cruzada, acostado", "40 s por lado"),
      it("Cuello y trapecio: oreja al hombro, la mano ayuda", "30 s por lado"),
      it("Hombro: brazo cruzado al pecho", "30 s por brazo"),
    ]),
  ],
  ["El pájaro con 2,5 kg se siente ridículo los primeros días y al tercero te arde. Es de los ejercicios que más se agradecen si pasas horas sentado.",
   "Si el sofá te queda muy bajo para las flexiones, cualquier borde firme a la altura de la rodilla sirve. Lo único que importa es que <strong>no se mueva</strong>."])

# ---- DIA 5
DATA["dia-5"] = dia(5, "Viernes",
  "Cuerpo completo en complejo · Acondicionamiento metabólico",
  "Barra ~19 kg. Si es mucho, quita los discos de 1 kg", 30,
  [
    warm("Calentamiento", 5, "Hazlo completo. Hoy más que nunca.", [
      it("Marcha en el sitio", "45 s"),
      it("Sentadilla al aire", "15 reps"),
      it("Bisagra de cadera", "15 reps"),
      it("Círculos de brazos grandes", "15 por sentido"),
      it("El complejo entero con la vara sola, sin discos", "1 ronda de 5 reps"),
    ]),
    work("El complejo", 15, 4, 90, "Sin soltar la barra",
      "Seis ejercicios encadenados, 6 reps de cada uno, en este orden y sin soltar la barra. Al terminar los seis, sueltas y descansas.", [
      it("Peso muerto", "6 reps", None, code="1",
         how="Barra en el piso, pies al ancho de la cadera. Cadera atrás, pecho arriba, levanta empujando el piso con los pies hasta quedar parado derecho."),
      it("Remo inclinado", "6 reps", None, code="2",
         how="Desde parado, inclínate hasta que el torso quede a unos 45°. Jala la barra al ombligo, codos hacia atrás. Baja controlado."),
      it("Cargada al pecho", "6 reps", None, code="3",
         how="Desde la posición inclinada, jala la barra hacia arriba con fuerza de cadera y métete debajo: la barra termina apoyada al frente de los hombros, codos apuntando adelante. Es el movimiento más técnico del complejo. <strong>Los primeros días hazlo despacio y en dos tiempos.</strong>"),
      it("Press de hombro", "6 reps", None, code="4",
         how="Con la barra al frente de los hombros, empújala recto sobre la cabeza hasta estirar los brazos. Aprieta glúteo y abdomen para no arquear la espalda."),
      it("Sentadilla frontal", "6 reps", None, code="5",
         how="Baja la barra de nuevo al frente de los hombros y haz sentadilla con ella ahí. <strong>Codos arriba:</strong> si los codos caen, la barra se te va hacia adelante."),
      it("Buenos días (good morning)", "6 reps", None, code="6",
         how="Pasa la barra atrás de la nuca, sobre los trapecios. Con las rodillas apenas suaves, empuja la cadera atrás y baja el torso hasta la horizontal. Sube. Recorrido corto, control total. Al terminar, deja la barra en el piso."),
    ]),
    work("Finisher · AMRAP 6 min", 6, 1, 0, "Tantas rondas como puedas",
      "Seis minutos de reloj. Sin peso. Descansas cuando lo necesites y sigues. Apunta cuántas rondas hiciste.", [
      it("Flexiones", "8 reps", None, code="—"),
      it("Escaladores (mountain climbers)", "20 (10 por pierna)", None, code="—"),
      it("Sentadilla con salto", "10 reps", None, code="—"),
      it("Plancha", "20 s", None, code="—"),
    ]),
    cool("Estiramiento", 4, None, [
      it("Respiración: 5 inhalaciones lentas boca arriba, rodillas dobladas", "1 min"),
      it("Cuádriceps de pie", "30 s por pierna"),
      it("Isquios sentado", "30 s por pierna"),
      it("Pecho en el marco de la puerta", "30 s"),
      it("Torsión de columna acostado", "30 s por lado"),
    ]),
  ],
  ["<strong>La primera vez, haz 2 rondas, no 4.</strong> El complejo se ve inofensivo en el papel. En la ronda 3 vas a entender por qué.",
   "Si en alguna ronda se te daña la técnica, para esa ronda. Con la barra encima de la cabeza y la espalda cansada es cuando pasan las cosas.",
   "¿No te sale la cargada al pecho? Cámbiala por <strong>remo alto</strong>: jala la barra pegada al cuerpo hasta la altura del pecho, codos altos. Mismo efecto, menos técnica.",
   "¿19 kg es mucho para el press de hombro? Es normal, el press es el eslabón débil del complejo. <strong>El peso lo decide el ejercicio más débil:</strong> quita los discos de 1 kg y trabaja con ~15 kg."])

# ---- DIA 6
DATA["dia-6"] = dia(6, "Sábado",
  "Pantorrilla · Hombro medial · Erectores y espalda baja · Core completo",
  "Pantorrilla en Pesada 9,5 kg · hombro en 2,5 kg", 30,
  [
    warm("Calentamiento", 4, None, [
      it("Elevación de talones sin peso", "20 reps"),
      it("Círculos de tobillo", "10 por sentido, cada pie"),
      it("Superman lento en el tapete", "10 reps"),
      it("Círculos de brazos y rotación de hombro", "30 s"),
      it("Gato–camello", "10 reps"),
    ]),
    work("Bloque A", 12, 3, 60, "Tri-serie", None, [
      it("Elevación de talones de pie", "20 reps", "2 mancuernas · 9,5 kg", code="A1",
         how="De pie, mancuernas colgando a los lados. Sube lo más alto que puedas sobre las puntas, <strong>aprieta 1 segundo arriba</strong> y baja lento hasta abajo del todo. La pantorrilla aguanta mucho volumen: por eso son 20 reps con el peso más alto de la semana. Para más recorrido, párate con la mitad delantera del pie sobre un escalón o un libro grueso y deja caer el talón."),
      it("Elevación lateral", "12 reps", "2 mancuernas · 2,5 kg", code="A2",
         how="De pie, mancuernas a los lados, codos con una curva suave. Sube los brazos hacia los lados hasta la altura de los hombros, ni un centímetro más. <strong>Sube como si derramaras agua de una jarra</strong>, meñique un poco más alto que el pulgar. Este es el músculo que da el ancho de los hombros y no se trabaja con ningún press."),
      it("Superman", "15 reps", "Peso corporal", code="A3",
         how="Boca abajo en el tapete, brazos estirados adelante. Sube al tiempo brazos, pecho y piernas unos centímetros. Aguanta 2 segundos arriba y baja. Trabaja los erectores de la columna, los que te sostienen la espalda todo el día."),
    ]),
    work("Bloque B · Circuito de core", 10, 3, 45, "Los cuatro seguidos", None, [
      it("Plancha", "45 s", None, code="B1"),
      it("Bicicleta", "30 s", None, code="B2",
         how="Acostado, manos en las sienes. Codo derecho hacia rodilla izquierda mientras la otra pierna se estira. Alterna con ritmo, sin jalarte el cuello."),
      it("Elevación de piernas", "12 reps", None, code="B3",
         how="Acostado, manos debajo de la cola para proteger la espalda. Piernas rectas suben hasta la vertical y bajan <strong>sin tocar el piso</strong>. Si la espalda se arquea, dobla las rodillas."),
      it("Giro ruso con disco", "20 (10 por lado)", "1 disco · 1 kg", code="B4",
         how="Sentado, tronco inclinado atrás unos 45°, pies levantados o apoyados. Un disco con las dos manos. Gira el torso de lado a lado tocando el piso al lado de la cadera. El giro sale del torso, no de los brazos."),
    ]),
    cool("Estiramiento", 4, None, [
      it("Pantorrilla contra la pared: pie atrás, talón abajo, rodilla recta", "45 s por pierna"),
      it("Sóleo: igual pero con la rodilla doblada", "30 s por pierna"),
      it("Espalda baja: rodillas al pecho, acostado", "45 s"),
      it("Hombro: brazo cruzado al pecho", "30 s por lado"),
      it("Postura del niño", "45 s"),
    ]),
  ],
  ["<strong>Los dos estiramientos de pantorrilla son distintos.</strong> Con la rodilla recta estiras el gemelo; con la rodilla doblada estiras el sóleo, que está debajo. Los dos se acortan de estar sentado.",
   "Hoy es el día menos exigente de piernas grandes, a propósito: el viernes fue duro y mañana toca recuperación."])

# ---- DIA 7
DATA["dia-7"] = dia(7, "Domingo",
  "Movilidad, respiración y core suave — recuperación activa",
  "Ninguna. Hoy no se tocan las mancuernas", 30,
  [
    warm("Parte 1 · Despertar el cuerpo", 6, "Dos vueltas al circuito, sin descanso.", [
      it("Gato–camello", "10 lentos"),
      it("Perro boca abajo a plancha", "8 reps"),
      it("Zancada con rotación de torso", "6 por lado"),
      it("Círculos de cadera en cuatro apoyos", "8 por lado"),
      it("Abre el libro (rotación torácica de lado)", "8 por lado",
         how="Acostado de lado, rodillas dobladas a 90°, brazos estirados juntos al frente. Abre el brazo de arriba siguiéndolo con la mirada hasta que la espalda toque el piso del otro lado. Es lo mejor que le puedes hacer a una espalda que pasa el día en una silla."),
    ]),
    cool("Parte 2 · Movilidad sostenida", 12,
      "Aquí te quedas quieto en cada posición. Respira lento: 4 segundos entrando, 6 saliendo. El estiramiento cede cuando exhalas.", [
      it("Sentadilla profunda sostenida", "90 s",
         how="Talones abajo, codos abriendo las rodillas desde adentro. Si no puedes bajar con los talones pegados al piso, agárrate del marco de una puerta y deja que el peso te baje."),
      it("Flexor de cadera en zancada, rodilla en el tapete", "90 s por lado"),
      it("Paloma o figura 4 para el glúteo", "90 s por lado"),
      it("Mariposa (aductores)", "90 s"),
      it("Pecho en el marco de la puerta", "60 s por lado"),
      it("Postura del niño con brazos largos", "90 s"),
    ]),
    warm("Parte 3 · Core suave", 7, "Sin llegar al fallo. Movimiento controlado, nada de ardor.", [
      it("Muerto bicho lento", "10 por lado"),
      it("Puente de glúteo sin peso, 2 s arriba", "15 reps"),
      it("Plancha", "30 s × 2"),
      it("Muerto bicho solo con brazos", "12 por lado"),
      it("Perro-pájaro", "10 por lado",
         how="En cuatro apoyos, estira el brazo derecho y la pierna izquierda hasta la horizontal. Aguanta 2 segundos sin que la cadera se ladee. Pon un vaso vacío en la espalda baja si quieres el reto de verdad."),
    ]),
    cool("Parte 4 · Respiración", 5,
      "Acostado boca arriba, rodillas dobladas, una mano en el pecho y otra en la barriga.", [
      it("Inhala por la nariz", "4 s — solo se mueve la mano de la barriga"),
      it("Aguanta", "2 s"),
      it("Exhala por la boca, despacio", "6 s"),
      it("Repite el ciclo", "20 veces"),
    ]),
  ],
  ["<strong>No te saltes este día pensando que no cuenta.</strong> Es el que más gente se salta y el que explica por qué a la cuarta semana ya no rinden. El músculo no crece entrenando: crece cuando lo dejas reconstruirse.",
   "Si algún día de la semana quedaste molido, puedes cambiar ese día por este y correr la rutina un día. La rotación se mantiene.",
   "¿Quieres hacer algo más hoy? Camina 30 minutos afuera. Eso sí suma."])

# ---------------------------------------------------------------- plantilla

HEAD = """<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>{css}</style>
"""

SECS = [("dias", "Días"), ("aleatoria", "Azar"),
        ("abdominales", "Abdomen"), ("pecho", "Pecho")]


def topbar(active, modo="sec"):
    if modo in ("dia", "dias"):
        chips = "".join(
            '<a href="%s.html"%s title="%s">%s</a>'
            % (slug, ' aria-current="page"' if slug == active else '', nombre, letra)
            for slug, nombre, letra in DIAS)
        home = ("dias.html", "&larr; Días") if modo == "dia" else ("index.html", "&larr; Menú")
        nav = '<nav class="days" aria-label="Días de la semana">%s</nav>' % chips
    else:
        chips = "".join(
            '<a class="sec-chip" href="%s.html"%s>%s</a>'
            % (slug, ' aria-current="page"' if slug == active else '', nombre)
            for slug, nombre in SECS)
        home = ("index.html", "&larr; Menú")
        nav = '<nav class="days" aria-label="Secciones">%s</nav>' % chips
    return ('<header class="top"><div class="top-in">'
            '<a class="home" href="%s">%s</a>%s</div></header>') % (home[0], home[1], nav)

TIMER = """<div class="timer" role="status" aria-live="polite">
  <div class="timer-in">
    <div>
      <div class="lb">Descanso</div>
      <div class="cd num">0</div>
    </div>
    <div class="tbar"><i></i></div>
    <button type="button" data-add>+15 s</button>
    <button type="button" data-stop>Listo</button>
  </div>
</div>"""

def render_item(bi, ii, x, checkbox=True):
    ident = "b%d-i%d" % (bi, ii)
    code = ('<span class="code">%s</span>' % E(x["code"])) if x.get("code") else ''
    load = ('<span>%s</span>' % E(x["load"])) if x.get("load") else ''
    fi = fichas.buscar(x["n"]) or {}

    figura = ''
    if fi.get("fig") and fi["fig"] in dibujos.DIB:
        figura = '<div class="figbox">%s</div>' % dibujos.DIB[fi["fig"]]

    cues = []
    if fi.get("cad"):
        cues.append('<span class="cue cad"><b>Cadencia</b>%s</span>' % E(fi["cad"]))
    if fi.get("hasta"):
        cues.append('<span class="cue hasta"><b>Hasta dónde</b>%s</span>' % E(fi["hasta"]))
    cues = '<div class="cues">%s</div>' % "".join(cues) if cues else ''

    partes = []
    if x.get("how"):
        partes.append('<p>%s</p>' % x["how"])
    if fi.get("facil"):
        partes.append('<p><span class="tag">Más fácil</span>%s</p>' % E(fi["facil"]))
    if fi.get("error"):
        partes.append('<p><span class="tag err">Error común</span>%s</p>' % E(fi["error"]))
    how = ('<details class="how"><summary>Cómo se hace</summary>%s</details>'
           % "".join(partes)) if partes else ''

    return (
      '<li>'
      '<label class="row" for="%s">'
      '<input type="checkbox" id="%s">'
      '<span class="txt"><span class="nm">%s%s</span>'
      '<span class="sub"><span class="d">%s</span>%s</span></span>'
      '</label>%s%s%s</li>'
    ) % (ident, ident, code, E(x["n"]), E(x["d"]), load, figura, cues, how)

def render_block(bi, b):
    tag = '<span class="kind">%s</span>' % E(b["tag"]) if b.get("tag") else ''
    head = ('<div class="bhead"><h2>%s</h2>%s<span class="t">%d min</span></div>'
            % (E(b["name"]), tag, b["mins"]))
    note = '<p class="bnote">%s</p>' % E(b["note"]) if b.get("note") else ''
    rounds = ''
    if b["kind"] == "work" and b.get("rounds", 0) > 1:
        pills = "".join('<button type="button" class="rd" id="b%d-r%d" aria-pressed="false">%d</button>'
                        % (bi, k, k) for k in range(1, b["rounds"] + 1))
        rounds = '<div class="rounds"><span class="lb">Rondas</span>%s</div>' % pills
    items = "".join(render_item(bi, i, x) for i, x in enumerate(b["items"]))
    rest = ''
    if b.get("timers"):
        botones = "".join(
            '<button type="button" class="restbtn %s" data-sec="%d" data-label="%s">%s %d s</button>'
            % ("trabajo" if i == 0 else "", sec, E(lb), E(lb), sec)
            for i, (sec, lb) in enumerate(b["timers"]))
        rest = '<div class="timers">%s</div>' % botones
    elif b.get("rest"):
        rest = ('<button type="button" class="restbtn" data-sec="%d" data-label="Descanso entre rondas">'
                'Descanso %d s</button>') % (b["rest"], b["rest"])
    return '<section class="block">%s%s%s<ul class="ex">%s</ul>%s</section>' % (head, note, rounds, items, rest)

def render_day(slug, d):
    i = [s for s, _, _ in DIAS].index(slug)
    prev = DIAS[i - 1] if i > 0 else None
    nxt = DIAS[i + 1] if i < len(DIAS) - 1 else None
    blocks = "".join(render_block(bi, b) for bi, b in enumerate(d["blocks"]))
    notes = ''
    if d["notes"]:
        lis = "".join("<li>%s</li>" % n for n in d["notes"])
        notes = '<section class="notes"><h3>Notas del día</h3><ul>%s</ul></section>' % lis
    pager = '<nav class="pager">'
    if prev:
        pager += '<a href="%s.html"><span class="k">Anterior</span><span class="v">%s</span></a>' % (prev[0], prev[1])
    else:
        pager += '<a href="dias.html"><span class="k">Volver</span><span class="v">Días</span></a>'
    if nxt:
        pager += '<a class="next" href="%s.html"><span class="k">Siguiente</span><span class="v">%s</span></a>' % (nxt[0], nxt[1])
    else:
        pager += '<a class="next" href="dias.html"><span class="k">Volver</span><span class="v">Días</span></a>'
    pager += '</nav>'

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">Día %d de 7</p>'
      '<h1>%s</h1>'
      '<p class="focus">%s</p>'
      '<div class="meta"><span class="chip">%d minutos</span><span class="chip load">%s</span></div>'
      '<div class="prog"><span class="bar"><i></i></span><span class="n num">0 / 0</span>'
      '<button type="button" class="figtog">Ocultar dibujos</button>'
      '<button type="button" class="reset">Reiniciar</button></div>'
      '</header>'
      '%s%s%s</div>%s'
    ) % (d["n"], E(d["nombre"]), E(d["focus"]), d["dur"], E(d["carga"]),
         blocks, notes, pager, TIMER)

    title = "Día %d · %s — Rutina del tapete" % (d["n"], d["nombre"])
    return (HEAD.format(title=E(title), css=CSS)
            + topbar(slug, "dia")
            + body
            + '<script>window.PAGE_KEY="%s";</script>' % slug
            + '<script>%s</script>' % JS)

for slug, nombre, letra in DIAS:
    with open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8") as f:
        f.write(render_day(slug, DATA[slug]))


# ---------------------------------------------------------------- índice

INDEX_CSS_EXTRA = """
.grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:10px; margin-top:14px}
.card{
  display:block; text-decoration:none; color:inherit; background:var(--surface);
  border:1px solid var(--line); border-radius:var(--r); padding:14px 15px;
  box-shadow:var(--shadow); border-top:3px solid var(--accent); transition:.15s;
}
.card:hover{border-color:var(--accent); transform:translateY(-1px)}
.card.rest{border-top-color:var(--steel)}
.card.alea{border-top-color:var(--steel); border-style:dashed; border-top-style:solid}
.card.alea .load{color:var(--steel)}
.card .d{font-family:Oswald,sans-serif; font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3)}
.card h3{font-size:20px; text-transform:uppercase; margin:2px 0 6px}
.card p{margin:0; font-size:13.5px; color:var(--ink-2); line-height:1.4}
.card .load{margin-top:9px; font-size:12px; color:var(--accent); font-family:Oswald,sans-serif; letter-spacing:.04em}
.card.rest .load{color:var(--steel)}
.sec{margin-top:34px}
.sec>h2{font-size:22px; text-transform:uppercase; padding-bottom:8px; border-bottom:2px solid var(--ink)}
.tw{overflow-x:auto; margin-top:12px; border:1px solid var(--line); border-radius:var(--r); background:var(--surface)}
table{border-collapse:collapse; width:100%; font-size:14px; min-width:460px}
th,td{padding:9px 12px; text-align:left; border-bottom:1px solid var(--line)}
th{
  font-family:Oswald,sans-serif; font-size:11px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--ink-2); background:var(--surface-2); font-weight:500;
}
tr:last-child td{border-bottom:none}
td strong{color:var(--ink)}
td.k{font-family:Oswald,sans-serif; color:var(--accent); white-space:nowrap}
.rules{margin:14px 0 0; padding:0; list-style:none; display:flex; flex-direction:column; gap:10px}
.rules li{
  background:var(--surface); border:1px solid var(--line); border-left:3px solid var(--steel);
  border-radius:var(--r); padding:12px 14px; font-size:14.5px; color:var(--ink-2); max-width:64ch;
}
.rules strong{color:var(--ink)}
.lede{font-size:17px; color:var(--ink-2); max-width:56ch; margin:12px 0 0}
.fine{margin-top:34px; padding-top:16px; border-top:1px solid var(--line); font-size:13px; color:var(--ink-3); max-width:62ch}
"""

DAY_CARDS = [
 ("dia-1","Lunes","Cuádriceps · pecho medio · dorsal ancho · bíceps","Actual — 7,5 kg", False),
 ("dia-2","Martes","Isquios y glúteo · pecho superior · espalda media · tríceps","Barra + Actual", False),
 ("dia-3","Miércoles","Unilateral · aperturas · dorsal · antebrazo","5 kg y Actual", False),
 ("dia-4","Jueves","Glúteo medio · pecho inferior · trapecio · tríceps lateral","2,5 kg y Actual", False),
 ("dia-5","Viernes","Complejo de barra + AMRAP metabólico","Barra — ~19 kg", False),
 ("dia-6","Sábado","Pantorrilla · hombro medial · lumbares · core","Pesada — 9,5 kg", False),
 ("dia-7","Domingo","Movilidad, respiración y core suave","Sin peso", True),
]

def render_dias():
    cards = ""
    for slug, nombre, desc, load, rest in DAY_CARDS:
        n = [s for s,_,_ in DIAS].index(slug) + 1
        cards += ('<a class="card%s" href="%s.html">'
                  '<span class="d">Día %d</span><h3>%s</h3><p>%s</p>'
                  '<div class="load">%s</div></a>') % (
                  " rest" if rest else "", slug, n, E(nombre), E(desc), E(load))

    equipo = [
      ("2 mancuernas ajustables", "Cargadas hoy a <strong>7,5 kg cada una</strong>: 2 discos de 2,5 kg y 2 de 1,25 kg por mancuerna."),
      ("4 discos sueltos", "1 kg cada uno. Son los que te dan la carga Pesada."),
      ("Vara larga", "Une las dos mancuernas en una barra de ~19 kg con todos los discos."),
      ("Silla", "Solo para sentarte. No te subes en ella ni la empujas contra la pared."),
      ("Sofá", "Borde firme para las flexiones con manos elevadas. Pesado y ancho: no se mueve."),
      ("Tapete", "Tu zona de trabajo de suelo. La baldosa es resbalosa."),
      ("Espejo", "Revisa la técnica, sobre todo en sentadilla y peso muerto."),
    ]
    eq = "".join('<tr><td class="k">%s</td><td>%s</td></tr>' % (E(a), b) for a, b in equipo)

    cargas = [
      ("Ligera", "Solo los discos de 1,25 kg", "2,5 kg por mancuerna"),
      ("Media", "Solo los discos de 2,5 kg", "5 kg por mancuerna"),
      ("Actual", "Como las tienes ahora", "7,5 kg por mancuerna"),
      ("Pesada", "Actual + 1 disco de 1 kg por lado", "9,5 kg por mancuerna"),
      ("Barra", "Todos los discos en la vara", "~19 kg en total"),
    ]
    cg = "".join('<tr><td class="k">%s</td><td>%s</td><td><strong>%s</strong></td></tr>' % (E(a), E(b), E(c))
                 for a, b, c in cargas)

    rot = [
      ("1 · Lun","Cuádriceps","Medio","Dorsal ancho","Bíceps"),
      ("2 · Mar","Isquios, glúteo","Superior","Media, romboides","Tríceps largo"),
      ("3 · Mié","Unilateral","Externo","Dorsal unilateral","Braquial"),
      ("4 · Jue","Glúteo medio","Inferior","Trapecio, hombro post.","Tríceps lateral"),
      ("5 · Vie","Complejo","Complejo","Complejo","Complejo"),
      ("6 · Sáb","Pantorrilla","—","Erectores","Hombro medial"),
      ("7 · Dom","Movilidad","Movilidad","Movilidad","Movilidad"),
    ]
    rt = "".join('<tr><td class="k">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                 % tuple(E(x) for x in r) for r in rot)

    leer_filas = [
      ("Cadencia", "Tres números: segundos para <strong>bajar</strong>, segundos de "
                   "<strong>pausa</strong> abajo y segundos para <strong>subir</strong>. "
                   "<strong>3-1-1</strong> es bajar en tres, parar uno, subir en uno. "
                   "Bajar lento es la mitad del trabajo y casi nadie lo hace."),
      ("Hasta dónde", "El punto exacto donde termina el recorrido. Más abajo no siempre "
                      "es mejor: en varios ejercicios pasarse es justo lo que lesiona."),
      ("El dibujo", "Posición 1 y posición 2. La línea punteada roja marca la altura o la "
                    "alineación que tienes que buscar."),
      ("Cuántas veces", "Cada músculo se trabaja una vez por semana en su día fuerte y "
                        "aparece de refilón en otros dos. Por eso puedes entrenar a diario "
                        "sin quemarte."),
    ]
    leer = "".join('<tr><td class="k">%s</td><td>%s</td></tr>' % (E(a), b) for a, b in leer_filas)

    reglas = [
      "<strong>Tri-serie</strong> quiere decir que haces A1, A2 y A3 seguidos, sin descanso entre ellos. Al terminar los tres, descansas. Eso es una ronda.",
      "<strong>Ritmo:</strong> baja el peso en 2 segundos, súbelo en 1. Sin rebotes.",
      "<strong>Piso:</strong> el tapete para todo lo de suelo. La baldosa es resbalosa, así que entrena descalzo o con tenis, nunca en medias.",
      "<strong>La silla es solo para sentarse.</strong> Si se desliza en la baldosa cuando te sientas, ponla sobre el tapete.",
      "<strong>Espacio:</strong> todo es en el sitio. No hay zancadas caminando en esta casa.",
      "<strong>Si algo duele</strong> con dolor puntual en una articulación, no el ardor del músculo, para ese ejercicio y sigue con el resto.",
      "<strong>Descanso real entre rondas.</strong> Mirar el celular 75 segundos no es descanso. Usa el cronómetro de cada bloque.",
    ]
    rl = "".join("<li>%s</li>" % r for r in reglas)

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">Entrenamiento en casa</p>'
      '<h1>Rutina del tapete</h1>'
      '<p class="lede">Siete rutinas de 30 minutos, una para cada día. Todos los días trabajas '
      'pierna, pecho, espalda, brazo y core, pero cada día le toca una parte distinta de cada área.</p>'
      '</header>'
      '<div class="grid">%s</div>'
      '<section class="sec"><h2>La rotación</h2><div class="tw"><table>'
      '<thead><tr><th>Día</th><th>Pierna</th><th>Pecho</th><th>Espalda</th><th>Brazo</th></tr></thead>'
      '<tbody>%s</tbody></table></div>'
      '<p class="bnote">El domingo es suave a propósito. Entrenas los siete días, pero uno deja que '
      'el cuerpo se reconstruya. Sin ese día, a las tres semanas se te cae el rendimiento.</p></section>'
      '<nav class="pager"><a href="index.html"><span class="k">Volver</span>'
      '<span class="v">Menú</span></a>'
      '<a class="next" href="guia.html"><span class="k">Ver</span>'
      '<span class="v">Cómo funciona</span></a></nav>'
      '</div>'
    ) % (cards, rt)

    return (HEAD.format(title="Rutinas por día — Rutina del tapete",
                        css=CSS + INDEX_CSS_EXTRA)
            + topbar("dias", "dias") + body)


with open(os.path.join(OUT, "dias.html"), "w", encoding="utf-8") as f:
    f.write(render_dias())


# ---------------------------------------------------------------- progresión

REG_JS = """
(function(){
  var KEY = "rutina:registro";
  var data = {};
  try { data = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch(e){ data = {}; }
  document.querySelectorAll('.reg input').forEach(function(i){
    if (data[i.id] != null) i.value = data[i.id];
    i.addEventListener('input', function(){
      data[i.id] = i.value;
      try { localStorage.setItem(KEY, JSON.stringify(data)); } catch(e){}
    });
  });
  var b = document.querySelector('.clearreg');
  if (b) b.addEventListener('click', function(){
    data = {};
    try { localStorage.removeItem(KEY); } catch(e){}
    document.querySelectorAll('.reg input').forEach(function(i){ i.value = ''; });
  });
})();
"""

PROG_CSS = INDEX_CSS_EXTRA + """
.reg input{
  width:100%; min-width:78px; font:inherit; font-size:14px; padding:6px 8px;
  border:1px solid var(--line); border-radius:7px; background:var(--bg); color:var(--ink);
  font-variant-numeric:tabular-nums;
}
.reg input:focus{outline:2px solid var(--accent); outline-offset:1px; border-color:var(--accent)}
.reg table{min-width:600px}
.reg td:first-child{font-family:Oswald,sans-serif; color:var(--accent); white-space:nowrap}
.clearreg{
  margin-top:10px; background:none; border:1px solid var(--line-strong); color:var(--ink-2);
  font:inherit; font-size:13px; padding:6px 13px; border-radius:99px; cursor:pointer;
}
.clearreg:hover{border-color:var(--accent); color:var(--accent)}
.wk{
  font-family:Oswald,sans-serif; font-size:12px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--ink-3); margin:20px 0 0;
}
.steps{counter-reset:s; margin:14px 0 0; padding:0; list-style:none; display:flex; flex-direction:column; gap:10px}
.steps li{
  counter-increment:s; position:relative; padding:13px 15px 13px 48px;
  background:var(--surface); border:1px solid var(--line); border-radius:var(--r);
  font-size:14.5px; color:var(--ink-2); max-width:64ch;
}
.steps li::before{
  content:counter(s); position:absolute; left:14px; top:12px;
  font-family:Oswald,sans-serif; font-size:17px; color:var(--accent);
}
.steps strong{color:var(--ink)}
"""

def render_prog():
    pasos = [
      "<strong>Sube reps.</strong> Agrega 2 reps por serie y quédate ahí una o dos semanas.",
      "<strong>Sube el tiempo bajo tensión.</strong> Baja el peso en 4 segundos en vez de 2. Es brutal y no cuesta un disco más.",
      "<strong>Sube la carga.</strong> Pasa a la siguiente configuración y vuelve a las reps originales.",
      "<strong>Sube la dificultad.</strong> Cuando ya no haya más discos: a una pierna, a un brazo, pies elevados, pausa de 2 segundos en el punto más difícil.",
    ]
    ps = "".join("<li>%s</li>" % p for p in pasos)

    sin = [
      ("A una pierna","La sentadilla dividida con 7,5 kg es más dura que la sentadilla con 19 kg."),
      ("Pausas","3 segundos abajo en la sentadilla, quieto, y subes."),
      ("Excéntricas lentas","5 segundos para bajar el peso."),
      ("Más rondas","De 3 a 4, recortando el descanso a 45 s."),
      ("Dos discos más","Dos de 5 kg cuestan poco y te dan otro año de progresión. Es la mejor inversión cuando llegues a ese punto."),
    ]
    sn = "".join('<tr><td class="k">%s</td><td>%s</td></tr>' % (E(a), E(b)) for a, b in sin)

    ejer = ["Sentadilla goblet","Peso muerto rumano","Sentadilla dividida","Sentadilla sumo",
            "Complejo (rondas)","Elevación de talones"]
    dias_lbl = ["Lun","Mar","Mié","Jue","Vie","Sáb"]
    sem_tables = ""
    for w in range(1, 5):
        rows = ""
        for i, (dl, ex) in enumerate(zip(dias_lbl, ejer)):
            rows += ('<tr><td>%s</td><td>%s</td>'
                     '<td><input id="w%d-d%d-p" inputmode="decimal" aria-label="Peso"></td>'
                     '<td><input id="w%d-d%d-r" inputmode="numeric" aria-label="Reps última ronda"></td>'
                     '<td><input id="w%d-d%d-n" aria-label="Cómo se sintió"></td></tr>'
                     ) % (dl, E(ex), w, i, w, i, w, i)
        sem_tables += (
          '<h3 class="wk">Semana %d</h3>'
          '<div class="reg"><div class="tw"><table>'
          '<thead><tr><th>Día</th><th>Ejercicio principal</th><th>Peso</th>'
          '<th>Reps última ronda</th><th>¿Cómo se sintió?</th></tr></thead>'
          '<tbody>%s</tbody></table></div></div>') % (w, rows)

    inicio = [
      ("Semana 1","Todo con carga <strong>Ligera</strong> o <strong>Media</strong>, aunque te sepa a poco. Estás enseñándole el patrón al cuerpo."),
      ("Semana 2","Sube a <strong>Actual</strong> en lo que se sintió fácil."),
      ("Semana 3 en adelante","Ahí sí, la regla de las dos rondas."),
    ]
    ini = "".join('<tr><td class="k">%s</td><td>%s</td></tr>' % (E(a), b) for a, b in inicio)

    esperar = [
      ("Semanas 1–3","Todo mejora rápido. Es el sistema nervioso aprendiendo, no músculo nuevo. Disfrútalo, es la parte más motivante."),
      ("Semanas 4–8","El progreso se vuelve lento y es donde la gente abandona. Aquí el registro salva: los números te muestran que sí estás avanzando aunque el espejo no lo grite."),
      ("Mes 3 en adelante","Cambios visibles, si la comida y el sueño acompañan. El entrenamiento es un tercio del asunto."),
    ]
    esp = "".join('<tr><td class="k">%s</td><td>%s</td></tr>' % (E(a), E(b)) for a, b in esperar)

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">Referencia</p><h1>Progresión</h1>'
      '<p class="lede">Hacer la misma rutina con el mismo peso durante tres meses no sirve de nada. '
      'El cuerpo se adapta a lo que le exiges: si la exigencia no sube, la adaptación se detiene.</p>'
      '</header>'
      '<section class="sec"><h2>La regla de las dos rondas</h2>'
      '<p class="bnote">Cuando puedas completar todas las reps de las tres rondas con buena técnica '
      '<strong>y te sobre fuerza</strong>, ese ejercicio ya te quedó corto. Súbelo, en este orden:</p>'
      '<ol class="steps">%s</ol>'
      '<p class="bnote">Tus saltos por mancuerna son <strong>2,5 → 5 → 7,5 → 9,5 kg</strong>. Son saltos '
      'grandes, y por eso los pasos 1 y 2 importan tanto: son tu forma de progresar entre salto y salto.</p>'
      '</section>'
      '<section class="sec"><h2>Cuando ya no haya más peso</h2>'
      '<p class="bnote">Vas a llegar. Los 9,5 kg por mancuerna se quedan cortos en sentadilla y peso muerto '
      'antes de lo que crees. Opciones, de la más barata a la menos:</p>'
      '<div class="tw"><table><tbody>%s</tbody></table></div></section>'
      '<section class="sec"><h2>Las primeras dos semanas</h2>'
      '<p class="bnote">No busques peso. Busca que el movimiento salga bien.</p>'
      '<div class="tw"><table><tbody>%s</tbody></table></div>'
      '<p class="bnote">El dolor muscular de los primeros días es normal, se llama agujetas, se pasa en '
      '48 horas y baja mucho desde la segunda semana. El dolor <strong>articular</strong> (rodilla, hombro, '
      'espalda baja) no es normal: eso es técnica o exceso de peso.</p></section>'
      '<section class="sec"><h2>Registro</h2>'
      '<p class="bnote">Anota solo dos cosas por sesión: el peso y las reps de la última ronda. '
      'Esa última ronda es la que te dice la verdad. Lo que escribas se guarda en este teléfono.</p>'
      '%s'
      '<button type="button" class="clearreg">Borrar todo el registro</button>'
      '</section>'
      '<section class="sec"><h2>Cada 8 semanas: una semana suave</h2>'
      '<p class="bnote">Haz las mismas rutinas con <strong>la mitad del peso y 2 rondas en vez de 3</strong>. '
      'No es perder el tiempo: es cuando el cuerpo termina de consolidar lo que ganaste. Vuelves la semana '
      'siguiente más fuerte que cuando paraste.</p></section>'
      '<section class="sec"><h2>Qué esperar, honestamente</h2>'
      '<div class="tw"><table><tbody>%s</tbody></table></div></section>'
      '<nav class="pager"><a href="index.html"><span class="k">Volver</span><span class="v">Menú</span></a>'
      '<a class="next" href="dias.html"><span class="k">Ir a</span><span class="v">Rutinas por día</span></a></nav>'
      '</div>'
    ) % (ps, sn, ini, sem_tables, esp)

    return (HEAD.format(title="Progresión — Rutina del tapete", css=CSS + PROG_CSS)
            + topbar("progresion")
            + body
            + '<script>%s</script>' % REG_JS)

with open(os.path.join(OUT, "progresion.html"), "w", encoding="utf-8") as f:
    f.write(render_prog())

print("ok:", sorted(os.listdir(OUT)))



# ---------------------------------------------------------------- aleatoria

CAT = fichas.catalogo()
CATALOGO = {}
for cat, lista in CAT.items():
    CATALOGO[cat] = [dict(n=d["nombre"], d=d["reps"] or "", carga=d["carga"] or "",
                          cad=d["cad"] or "", hasta=d["hasta"] or "",
                          facil=d["facil"] or "", error=d["error"] or "",
                          fig=dibujos.DIB.get(d["fig"], ""))
                     for d in lista]

ALEA_CSS = INDEX_CSS_EXTRA + """
.dados{display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-top:18px}
.bigbtn{
  flex:1; min-width:190px; padding:14px 18px; border-radius:var(--r); cursor:pointer;
  background:var(--accent); color:var(--on-accent); border:none;
  font-family:Oswald,sans-serif; font-size:16px; letter-spacing:.08em; text-transform:uppercase;
}
.bigbtn:hover{filter:brightness(1.08)}
.opt{display:flex; align-items:center; gap:8px; font-size:14px; color:var(--ink-2); cursor:pointer}
.opt input{width:19px; height:19px; accent-color:var(--accent); cursor:pointer}
#salida:empty::after{
  content:"Dale a generar y te armo una rutina de 30 minutos con lo que tienes en casa.";
  display:block; margin-top:22px; padding:22px; text-align:center; color:var(--ink-3);
  border:1.5px dashed var(--line-strong); border-radius:var(--r); font-size:15px;
}
"""

ALEA_JS = """
var CAT = __CATALOGO__;
function raizSalida(){ return document.querySelector('.salida'); }

function elige(cat, n, usados){
  var pool = (CAT[cat] || []).filter(function(x){ return usados.indexOf(x.n) < 0; });
  var out = [];
  for (var i = 0; i < n && pool.length; i++){
    var k = Math.floor(Math.random() * pool.length);
    out.push(pool[k]); usados.push(pool[k].n); pool.splice(k, 1);
  }
  return out;
}

function arma(conHiit){
  var u = [], piernaA = Math.random() < 0.5 ? 'pierna_rodilla' : 'pierna_cadera';
  var b = [];
  b.push({ nombre:'Calentamiento', tag:'Seguido', mins:4, rondas:0, rest:0,
           nota:'Uno detrás de otro, sin peso y sin descanso.',
           ej: elige('calent', 5, u) });
  b.push({ nombre:'Bloque A', tag:'Tri-serie', mins: conHiit ? 11 : 13, rondas:3, rest:75,
           nota:'A1 → A2 → A3 seguidos. Al terminar los tres, descansas y repites.',
           ej: elige(piernaA,1,u).concat(elige('empuje',1,u), elige('jalon',1,u)) });
  b.push({ nombre:'Bloque B', tag:'Tri-serie', mins: conHiit ? 7 : 9, rondas:3, rest:60,
           nota:'', ej: elige('pierna_acc',1,u).concat(elige('brazo',1,u), elige('core',1,u)) });
  if (conHiit){
    b.push({ nombre:'HIIT · AMRAP 5 min', tag:'Tantas rondas como puedas', mins:5,
             rondas:0, rest:0,
             nota:'Cinco minutos de reloj. Descansas cuando lo necesites y sigues.',
             ej: elige('hiit', 3, u) });
  }
  b.push({ nombre:'Estiramiento', tag:'Sostenido', mins: conHiit ? 3 : 4, rondas:0, rest:0,
           nota:'', ej: elige('estiram', conHiit ? 3 : 4, u) });
  return b;
}

function esc(t){
  return String(t == null ? '' : t).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];
  });
}

function pinta(bloques){
  var h = '', bi = 0;
  bloques.forEach(function(b){
    h += '<section class="block"><div class="bhead"><h2>' + esc(b.nombre) + '</h2>' +
         '<span class="kind">' + esc(b.tag) + '</span>' +
         '<span class="t">' + b.mins + ' min</span></div>';
    if (b.nota) h += '<p class="bnote">' + esc(b.nota) + '</p>';
    if (b.rondas > 1){
      h += '<div class="rounds"><span class="lb">Rondas</span>';
      for (var r = 1; r <= b.rondas; r++)
        h += '<button type="button" class="rd" id="a' + bi + '-r' + r + '" aria-pressed="false">' + r + '</button>';
      h += '</div>';
    }
    h += '<ul class="ex">';
    b.ej.forEach(function(x, ii){
      var id = 'a' + bi + '-i' + ii;
      var codigo = b.rondas > 1 ? String.fromCharCode(64 + bi) + (ii + 1) : '';
      h += '<li><label class="row" for="' + id + '"><input type="checkbox" id="' + id + '">' +
           '<span class="txt"><span class="nm">' +
           (codigo ? '<span class="code">' + codigo + '</span>' : '') + esc(x.n) + '</span>' +
           '<span class="sub"><span class="d">' + esc(x.d) + '</span>' +
           (x.carga ? '<span>' + esc(x.carga) + '</span>' : '') + '</span></span></label>';
      if (x.fig) h += '<div class="figbox">' + x.fig + '</div>';
      var cues = '';
      if (x.cad)   cues += '<span class="cue cad"><b>Cadencia</b>' + esc(x.cad) + '</span>';
      if (x.hasta) cues += '<span class="cue hasta"><b>Hasta dónde</b>' + esc(x.hasta) + '</span>';
      if (cues) h += '<div class="cues">' + cues + '</div>';
      var det = '';
      if (x.facil) det += '<p><span class="tag">Más fácil</span>' + esc(x.facil) + '</p>';
      if (x.error) det += '<p><span class="tag err">Error común</span>' + esc(x.error) + '</p>';
      if (det) h += '<details class="how"><summary>Cómo se hace</summary>' + det + '</details>';
      h += '</li>';
    });
    h += '</ul>';
    if (b.rest) h += '<button type="button" class="restbtn" data-sec="' + b.rest +
                     '" data-label="Descanso entre rondas">Descanso ' + b.rest + ' s</button>';
    h += '</section>';
    bi++;
  });
  raizSalida().innerHTML = h;
  if (window.RUTINA_ENLAZA) window.RUTINA_ENLAZA();
  window.scrollTo({ top: raizSalida().offsetTop - 70, behavior: 'smooth' });
}

(function(){
  var hiit = document.getElementById('con-hiit');
  var KEY = 'rutina:aleatoria';
  try {
    var g = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (g && g.bloques){ pinta(g.bloques); if (hiit) hiit.checked = !!g.hiit; }
  } catch(e){}

  document.getElementById('generar').addEventListener('click', function(){
    var conHiit = hiit && hiit.checked;
    var b = arma(conHiit);
    pinta(b);
    try { localStorage.setItem(KEY, JSON.stringify({ bloques: b, hiit: conHiit })); } catch(e){}
    try { localStorage.removeItem('rutina:aleatoria-estado'); } catch(e){}
  });
})();
"""


def render_alea():
    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">Para no aburrirte</p><h1>Rutina aleatoria</h1>'
      '<p class="lede">Treinta minutos armados al azar con los mismos ejercicios de la '
      'semana. Respeta la estructura: una pierna, un empuje, un jalón, un brazo y core. '
      'Nunca te va a salir dos veces la misma.</p>'
      '<div class="dados">'
      '<button type="button" class="bigbtn" id="generar">Generar rutina</button>'
      '<label class="opt" for="con-hiit"><input type="checkbox" id="con-hiit">'
      'Con HIIT al final</label>'
      '</div>'
      '<div class="prog"><span class="bar"><i></i></span><span class="n num">0 / 0</span>'
      '<button type="button" class="figtog">Ocultar dibujos</button>'
      '<button type="button" class="reset">Reiniciar</button></div>'
      '</header>'
      '<div id="salida" class="salida"></div>'
      '<nav class="pager"><a href="index.html"><span class="k">Volver</span>'
      '<span class="v">Menú</span></a>'
      '<a class="next" href="banco.html"><span class="k">Ver</span>'
      '<span class="v">Banco de ejercicios</span></a></nav>'
      '</div>' + TIMER
    )
    js = ALEA_JS.replace("__CATALOGO__", json.dumps(CATALOGO, ensure_ascii=False).replace("</", "<\\/"))
    return (HEAD.format(title="Rutina aleatoria — Rutina del tapete", css=CSS + ALEA_CSS)
            + topbar("aleatoria") + body
            + '<script>window.PAGE_KEY="aleatoria-estado";</script>'
            + '<script>%s</script>' % JS
            + '<script>%s</script>' % js)


with open(os.path.join(OUT, "aleatoria.html"), "w", encoding="utf-8") as f:
    f.write(render_alea())

print("aleatoria ok ·", sum(len(v) for v in CATALOGO.values()), "ejercicios en el catálogo")


# ---------------------------------------------------------------- menú

MENU_CSS = INDEX_CSS_EXTRA + """
.tiles{display:flex; flex-direction:column; gap:12px; margin-top:22px}
.tile{
  display:grid; grid-template-columns:1fr 118px; align-items:center; gap:10px;
  text-decoration:none; color:inherit; background:var(--surface);
  border:1px solid var(--line); border-left:4px solid var(--accent);
  border-radius:var(--r); padding:16px 14px 16px 18px; box-shadow:var(--shadow);
  transition:.15s;
}
.tile:hover{border-color:var(--accent); border-left-color:var(--accent); transform:translateY(-1px)}
.tile .tn{
  font-family:Oswald,sans-serif; font-size:11px; letter-spacing:.18em;
  text-transform:uppercase; color:var(--ink-3); display:block; margin-bottom:3px;
}
.tile h2{font-size:clamp(21px,5.5vw,26px); text-transform:uppercase; line-height:1.05; margin:0}
.tile p{margin:6px 0 0; font-size:14.5px; color:var(--ink-2); line-height:1.4; max-width:40ch}
.tile .go{
  display:inline-block; margin-top:10px; font-family:Oswald,sans-serif; font-size:13px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--accent);
}
.tile .tfig{opacity:.85}
.tile .tfig .f-t, .tile .tfig .f-c{display:none}
.tile .tfig svg{width:100%; height:auto; display:block}
.tile.t2{border-left-color:var(--steel)} .tile.t2 .go{color:var(--steel)}
.mini{display:flex; flex-wrap:wrap; gap:8px; margin-top:26px}
.mini a{
  flex:1; min-width:150px; text-decoration:none; text-align:center;
  background:var(--surface-2); border:1px solid var(--line); border-radius:var(--r);
  padding:13px 12px; color:var(--ink-2); font-size:14px;
}
.mini a:hover{border-color:var(--accent); color:var(--accent)}
.mini b{display:block; font-family:Oswald,sans-serif; font-size:15px; color:var(--ink);
        text-transform:uppercase; letter-spacing:.03em; margin-bottom:2px}
.mini a:hover b{color:var(--accent)}
@media (max-width:430px){
  .tile{grid-template-columns:1fr 92px; padding:14px 12px 14px 14px}
  .tile p{font-size:13.5px}
}
"""

TILES = [
  ("dias.html", "1", "Rutinas por día", "t1", "sentadilla_goblet",
   "Lunes a domingo, ya armadas. Cada día trabaja una parte distinta del cuerpo. "
   "Entras y escoges el día de hoy.", "Escoger el día"),
  ("aleatoria.html", "2", "Rutina aleatoria", "t2", "salto",
   "Treinta minutos armados al azar con los mismos ejercicios, para los días en "
   "que la rutina fija aburre. Le das a un botón y te la pone en pantalla.", "Generar una"),
  ("abdominales.html", "3", "Abdominales", "t1", "plancha",
   "Abdomen, costados y espalda baja, más bloques de quema. Cuatro rutinas para "
   "escoger según el día.", "Ver las rutinas"),
  ("pecho.html", "4", "Pecho", "t2", "press_piso",
   "Tres rutinas de pectoral: con flexiones, solo con mancuernas, o mezclado con "
   "intervalos de quema.", "Ver las rutinas"),
]


def render_index():
    tiles = ""
    for href, n, titulo, cls, figk, desc, go in TILES:
        tiles += (
          '<a class="tile %s" href="%s">'
          '<div><span class="tn">%s</span><h2>%s</h2><p>%s</p>'
          '<span class="go">%s &rarr;</span></div>'
          '<div class="tfig" aria-hidden="true">%s</div></a>'
        ) % (cls, href, n, E(titulo), E(desc), E(go), dibujos.DIB.get(figk, ""))

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">Entrenamiento en casa</p>'
      '<h1>Rutina del tapete</h1>'
      '<p class="lede">Todo lo que necesitas son las mancuernas, la vara y el tapete. '
      'Escoge por dónde quieres empezar.</p>'
      '</header>'
      '<nav class="tiles">%s</nav>'
      '<div class="mini">'
      '<a href="banco.html"><b>Banco de ejercicios</b>Todos, con su dibujo</a>'
      '<a href="guia.html"><b>Cómo funciona</b>Equipo, cargas y cómo leer</a>'
      '<a href="progresion.html"><b>Progresión</b>Cuándo subir peso</a>'
      '</div>'
      '<p class="fine">Esto es una rutina general para alguien sano que entrena en casa y no '
      'sustituye a un profesional. Si tienes una lesión, una condición cardíaca o llevas mucho '
      'tiempo sin moverte, habla con un médico o un fisioterapeuta antes de arrancar.</p>'
      '</div>'
    ) % tiles

    return (HEAD.format(title="Rutina del tapete", css=CSS + MENU_CSS)
            + '<header class="top"><div class="top-in">'
            + '<span class="home">Menú</span>'
            + '<nav class="days" aria-label="Secciones">'
            + "".join('<a class="sec-chip" href="%s.html">%s</a>' % (sl, nm) for sl, nm in SECS)
            + '</nav></div></header>' + body)


with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(render_index())


# ---------------------------------------------------------------- secciones

SEC_CSS = INDEX_CSS_EXTRA + """
.verdad{margin-top:20px; border:1px solid var(--line); border-radius:var(--r);
        background:var(--surface-2)}
.verdad > summary{
  cursor:pointer; padding:13px 16px; list-style:none; color:var(--ink);
  font-family:Oswald,sans-serif; font-size:14px; letter-spacing:.06em; text-transform:uppercase;
}
.verdad > summary::-webkit-details-marker{display:none}
.verdad > summary::before{content:"▸ "; color:var(--steel)}
.verdad[open] > summary::before{content:"▾ "}
.verdad > summary:hover{color:var(--steel)}
.verdad .vin{display:flex; flex-direction:column; gap:10px; padding:0 10px 10px}
.verdad > div{
  background:var(--surface); border:1px solid var(--line);
  border-left:3px solid var(--steel); border-radius:var(--r); padding:14px 16px;
}
.verdad h3{
  font-size:15.5px; margin:0 0 5px; color:var(--ink); text-transform:none;
  letter-spacing:0; line-height:1.3;
}
.verdad p{margin:0; font-size:14.5px; color:var(--ink-2); line-height:1.5; max-width:62ch}
.verdad strong{color:var(--ink)}
.picker{display:flex; flex-wrap:wrap; gap:7px; margin-top:24px}
.picker button{
  flex:1 1 auto; min-width:120px; cursor:pointer; text-align:left;
  background:var(--surface); border:1.5px solid var(--line); border-radius:var(--r);
  padding:10px 13px; color:var(--ink-2); font:inherit; transition:.15s;
}
.picker button:hover{border-color:var(--accent)}
.picker button[aria-pressed="true"]{
  border-color:var(--accent); background:var(--accent-soft); color:var(--ink);
}
.picker .pn{
  display:block; font-family:Oswald,sans-serif; font-size:15px; color:var(--ink);
  text-transform:uppercase; letter-spacing:.03em;
}
.picker button[aria-pressed="true"] .pn{color:var(--accent)}
.picker .pm{display:block; font-size:12.5px; margin-top:1px}
.rdesc{margin:16px 0 0; font-size:15px; color:var(--ink-2); max-width:58ch}
.timers{display:flex; gap:8px; margin-top:12px}
.timers .restbtn{margin-top:0}
.timers .trabajo{background:var(--accent); color:var(--on-accent)}
.timers .trabajo:hover{background:var(--ink); color:var(--bg)}
"""

PICKER_JS = """
(function(){
  var v = document.querySelector('details.verdad');
  if (v){
    var KV = 'rutina:verdad:' + (window.PAGE_KEY || 'x');
    try { if (localStorage.getItem(KV) === '0') v.open = false; } catch(e){}
    v.addEventListener('toggle', function(){
      try { localStorage.setItem(KV, v.open ? '1' : '0'); } catch(e){}
    });
  }
})();

(function(){
  var K = 'rutina:sel:' + (window.PAGE_KEY || 'x');
  var bs = Array.prototype.slice.call(document.querySelectorAll('.picker button'));
  if (!bs.length) return;

  function muestra(id, guarda){
    document.querySelectorAll('.rutina').forEach(function(r){ r.hidden = (r.dataset.rid !== id); });
    bs.forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.rid === id ? 'true' : 'false'); });
    if (guarda) { try { localStorage.setItem(K, id); } catch(e){} }
    if (window.RUTINA_ENLAZA) window.RUTINA_ENLAZA();
  }

  var ini = bs[0].dataset.rid;
  try {
    var g = localStorage.getItem(K);
    if (g && document.querySelector('.rutina[data-rid="' + g + '"]')) ini = g;
  } catch(e){}
  muestra(ini, false);

  bs.forEach(function(b){
    b.addEventListener('click', function(){
      muestra(b.dataset.rid, true);
      var r = document.querySelector('.rutina:not([hidden])');
      if (r) window.scrollTo({ top: r.offsetTop - 70, behavior: 'smooth' });
    });
  });
})();
"""


def render_seccion(slug, eyebrow, titulo, lede, verdad, rutinas, resumen):
    vs = "".join('<div><h3>%s</h3><p>%s</p></div>' % (E(t), p) for t, p in verdad)

    pick = "".join(
        '<button type="button" data-rid="%s" aria-pressed="false">'
        '<span class="pn">%s</span><span class="pm">%d min</span></button>'
        % (r["id"], E(r["nombre"]), r["mins"]) for r in rutinas)

    cuerpo = ""
    for ri, r in enumerate(rutinas):
        bloques = "".join(render_block(ri * 10 + bi, b) for bi, b in enumerate(r["blocks"]))
        cuerpo += ('<div class="rutina" data-rid="%s" hidden>'
                   '<p class="rdesc">%s</p>%s</div>') % (r["id"], E(r["desc"]), bloques)

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">%s</p><h1>%s</h1>'
      '<p class="lede">%s</p>'
      '<div class="prog"><span class="bar"><i></i></span><span class="n num">0 / 0</span>'
      '<button type="button" class="figtog">Ocultar dibujos</button>'
      '<button type="button" class="reset">Reiniciar</button></div>'
      '</header>'
      '<details class="verdad" open><summary>%s</summary><div class="vin">%s</div></details>'
      '<div class="picker" role="group" aria-label="Escoge la rutina">%s</div>'
      '%s'
      '<nav class="pager"><a href="index.html"><span class="k">Volver</span>'
      '<span class="v">Menú</span></a>'
      '<a class="next" href="banco.html"><span class="k">Ver</span>'
      '<span class="v">Banco de ejercicios</span></a></nav>'
      '</div>'
    ) % (E(eyebrow), E(titulo), E(lede), E(resumen), vs, pick, cuerpo) + TIMER

    return (HEAD.format(title=E(titulo + " — Rutina del tapete"), css=CSS + SEC_CSS)
            + topbar(slug) + body
            + '<script>window.PAGE_KEY="%s";</script>' % slug
            + '<script>%s</script>' % JS
            + '<script>%s</script>' % PICKER_JS)


with open(os.path.join(OUT, "abdominales.html"), "w", encoding="utf-8") as f:
    f.write(render_seccion(
        "abdominales", "Abdomen y quema", "Abdominales",
        "Cuatro rutinas: tres de abdomen y una de quema. Escoge una y arranca. "
        "Antes de eso, léete lo de abajo una vez.",
        secciones.ABD_VERDAD, secciones.ABDOMINALES,
        "Antes de empezar · qué quema grasa de verdad"))

with open(os.path.join(OUT, "pecho.html"), "w", encoding="utf-8") as f:
    f.write(render_seccion(
        "pecho", "Pectoral", "Pecho",
        "Tres rutinas de pecho para escoger según el día y según cómo tengas el hombro.",
        secciones.PECHO_VERDAD, secciones.PECHO,
        "Antes de empezar · qué cambia la forma del pecho"))

print("secciones ok")


# ---------------------------------------------------------------- guía

def render_guia():
    equipo = [
      ("2 mancuernas ajustables", "Cargadas hoy a <strong>7,5 kg cada una</strong>: 2 discos de 2,5 kg y 2 de 1,25 kg por mancuerna."),
      ("4 discos sueltos", "1 kg cada uno. Son los que te dan la carga Pesada."),
      ("Vara larga", "Une las dos mancuernas en una barra de ~19 kg con todos los discos."),
      ("Silla", "Solo para sentarte. No te subes en ella ni la empujas contra la pared."),
      ("Sofá", "Borde firme para las flexiones con manos elevadas. Pesado y ancho: no se mueve."),
      ("Tapete", "Tu zona de trabajo de suelo. La baldosa es resbalosa."),
      ("Espejo", "Revisa la técnica, sobre todo en sentadilla y peso muerto."),
    ]
    eq = "".join('<tr><td class="k">%s</td><td>%s</td></tr>' % (E(a), b) for a, b in equipo)

    cargas = [
      ("Ligera", "Solo los discos de 1,25 kg", "2,5 kg por mancuerna"),
      ("Media", "Solo los discos de 2,5 kg", "5 kg por mancuerna"),
      ("Actual", "Como las tienes ahora", "7,5 kg por mancuerna"),
      ("Pesada", "Actual + 1 disco de 1 kg por lado", "9,5 kg por mancuerna"),
      ("Barra", "Todos los discos en la vara", "~19 kg en total"),
    ]
    cg = "".join('<tr><td class="k">%s</td><td>%s</td><td><strong>%s</strong></td></tr>'
                 % (E(a), E(b), E(c)) for a, b, c in cargas)

    leer_filas = [
      ("Cadencia", "Tres números: segundos para <strong>bajar</strong>, segundos de "
                   "<strong>pausa</strong> abajo y segundos para <strong>subir</strong>. "
                   "<strong>3-1-1</strong> es bajar en tres, parar uno, subir en uno. "
                   "Bajar lento es la mitad del trabajo y casi nadie lo hace."),
      ("Hasta dónde", "El punto exacto donde termina el recorrido. Más abajo no siempre "
                      "es mejor: en varios ejercicios pasarse es justo lo que lesiona."),
      ("El dibujo", "Posición 1 y posición 2. La línea punteada roja marca la altura o la "
                    "alineación que tienes que buscar."),
      ("Tri-serie", "Haces A1, A2 y A3 seguidos, sin descanso entre ellos. Al terminar los "
                    "tres, descansas. Eso es una ronda."),
      ("Cómo se hace", "Ábrelo y encuentras la técnica, la versión más fácil para arrancar "
                       "y el error que casi todo el mundo comete."),
    ]
    leer = "".join('<tr><td class="k">%s</td><td>%s</td></tr>' % (E(a), b) for a, b in leer_filas)

    reglas = [
      "<strong>Ritmo:</strong> baja el peso en 2 segundos, súbelo en 1. Sin rebotes.",
      "<strong>Piso:</strong> el tapete para todo lo de suelo. La baldosa es resbalosa, así que "
      "entrena descalzo o con tenis, nunca en medias.",
      "<strong>La silla es solo para sentarse.</strong> Si se desliza en la baldosa cuando te "
      "sientas, ponla sobre el tapete.",
      "<strong>Espacio:</strong> todo es en el sitio. No hay zancadas caminando en esta casa.",
      "<strong>Si algo duele</strong> con dolor puntual en una articulación, no el ardor del "
      "músculo, para ese ejercicio y sigue con el resto.",
      "<strong>Descanso real entre rondas.</strong> Mirar el celular 75 segundos no es descanso. "
      "Usa el cronómetro que trae cada bloque.",
      "<strong>Los botones de la esquina:</strong> las casillas se marcan al tocarlas y se "
      "guardan en el celular. <em>Reiniciar</em> las borra y <em>Ocultar dibujos</em> "
      "compacta la página cuando ya te sepas la rutina.",
    ]
    rl = "".join("<li>%s</li>" % r for r in reglas)

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">Antes de empezar</p><h1>Cómo funciona</h1>'
      '<p class="lede">Qué equipo suponen las rutinas, cómo se arman los pesos y cómo se '
      'lee cada ejercicio. Se lee una vez y ya.</p>'
      '</header>'
      '<section class="sec"><h2>Tu equipo</h2>'
      '<div class="tw"><table><tbody>%s</tbody></table></div></section>'
      '<section class="sec"><h2>Configuraciones de carga</h2>'
      '<p class="bnote">Cambiar discos toma 30 segundos. Cada rutina te dice cuál usar.</p>'
      '<div class="tw"><table><thead><tr><th>Nombre</th><th>Cómo se arma</th><th>Peso</th></tr>'
      '</thead><tbody>%s</tbody></table></div></section>'
      '<section class="sec"><h2>Cómo leer cada ejercicio</h2>'
      '<div class="tw"><table><tbody>%s</tbody></table></div></section>'
      '<section class="sec"><h2>Reglas de la casa</h2><ul class="rules">%s</ul></section>'
      '<nav class="pager"><a href="index.html"><span class="k">Volver</span>'
      '<span class="v">Menú</span></a>'
      '<a class="next" href="progresion.html"><span class="k">Ver</span>'
      '<span class="v">Progresión</span></a></nav>'
      '</div>'
    ) % (eq, cg, leer, rl)

    return (HEAD.format(title="Cómo funciona — Rutina del tapete", css=CSS + INDEX_CSS_EXTRA)
            + topbar("guia") + body)


with open(os.path.join(OUT, "guia.html"), "w", encoding="utf-8") as f:
    f.write(render_guia())


# ---------------------------------------------------------------- banco

GRUPOS = [
  ("pierna_rodilla", "Pierna · sentadilla y zancada"),
  ("pierna_cadera",  "Pierna · cadera y glúteo"),
  ("pierna_acc",     "Pierna · accesorios"),
  ("empuje",         "Empuje · pecho y hombro"),
  ("pecho",          "Pecho"),
  ("jalon",          "Jalón · espalda"),
  ("brazo",          "Brazo"),
  ("core",           "Abdomen"),
  ("core_obl",       "Abdomen · costados y oblicuos"),
  ("core_bajo",      "Abdomen · bajo"),
  ("hiit",           "Quema"),
  ("calent",         "Calentamiento y movilidad"),
  ("estiram",        "Estiramientos"),
]

BANCO_CSS = INDEX_CSS_EXTRA + """
.buscar{
  width:100%; margin-top:20px; padding:12px 14px; font:inherit; font-size:16px;
  border:1.5px solid var(--line-strong); border-radius:var(--r);
  background:var(--surface); color:var(--ink);
}
.buscar:focus{outline:none; border-color:var(--accent)}
.gr{margin-top:28px}
.gr > h2{
  font-size:15px; text-transform:uppercase; letter-spacing:.1em; color:var(--accent);
  padding-bottom:7px; border-bottom:1px solid var(--line);
}
.gr .ex{margin-top:10px}
.gr .ex > li .row{cursor:default}
.vacio{margin-top:26px; padding:22px; text-align:center; color:var(--ink-3);
       border:1.5px dashed var(--line-strong); border-radius:var(--r)}
"""

BANCO_JS = """
(function(){
  var inp = document.querySelector('.buscar');
  if (!inp) return;
  var sin = function(t){
    return t.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
  };
  inp.addEventListener('input', function(){
    var q = sin(inp.value.trim());
    var total = 0;
    document.querySelectorAll('.gr').forEach(function(g){
      var n = 0;
      var grupo = q && sin(g.querySelector('h2').textContent).indexOf(q) >= 0;
      g.querySelectorAll('li[data-nombre]').forEach(function(li){
        var ok = !q || grupo || sin(li.dataset.nombre).indexOf(q) >= 0;
        li.hidden = !ok;
        if (ok) n++;
      });
      g.hidden = n === 0;
      total += n;
    });
    document.querySelector('.vacio').hidden = total > 0;
  });
})();
"""


def render_banco():
    por_cat, vistos = {}, set()
    for pat, d in fichas.FICHAS:
        if not d["cat"] or not d["nombre"] or d["fig"] not in dibujos.DIB:
            continue
        if (d["cat"], d["nombre"]) in vistos:
            continue
        vistos.add((d["cat"], d["nombre"]))
        por_cat.setdefault(d["cat"], []).append(d)

    total, grupos = 0, ""
    for cat, titulo in GRUPOS:
        lista = por_cat.get(cat, [])
        if not lista:
            continue
        total += len(lista)
        items = ""
        for i, d in enumerate(lista):
            cues = ""
            if d.get("cad"):
                cues += '<span class="cue cad"><b>Cadencia</b>%s</span>' % E(d["cad"])
            if d.get("hasta"):
                cues += '<span class="cue hasta"><b>Hasta dónde</b>%s</span>' % E(d["hasta"])
            det = ""
            if d.get("facil"):
                det += '<p><span class="tag">Más fácil</span>%s</p>' % E(d["facil"])
            if d.get("error"):
                det += '<p><span class="tag err">Error común</span>%s</p>' % E(d["error"])
            items += (
              '<li data-nombre="%s">'
              '<div class="row"><span class="txt"><span class="nm">%s</span>'
              '<span class="sub"><span class="d">%s</span>%s</span></span></div>'
              '<div class="figbox">%s</div>%s%s</li>'
            ) % (E(d["nombre"]), E(d["nombre"]), E(d["reps"] or ""),
                 ('<span>%s</span>' % E(d["carga"])) if d.get("carga") else "",
                 dibujos.DIB[d["fig"]],
                 ('<div class="cues">%s</div>' % cues) if cues else "",
                 ('<details class="how"><summary>Cómo se hace</summary>%s</details>' % det) if det else "")
        grupos += '<section class="gr"><h2>%s</h2><ul class="ex">%s</ul></section>' % (E(titulo), items)

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">La base de todo</p><h1>Banco de ejercicios</h1>'
      '<p class="lede">Los %d ejercicios que usan todas las rutinas, con su dibujo. '
      'Busca uno por nombre si quieres revisar cómo se hace.</p>'
      '<button type="button" class="figtog">Ocultar dibujos</button>'
      '</header>'
      '<input class="buscar" type="search" id="q-banco" placeholder="Buscar: sentadilla, plancha, pecho…" '
      'aria-label="Buscar ejercicio">'
      '%s'
      '<p class="vacio" hidden>Ningún ejercicio con ese nombre.</p>'
      '<nav class="pager"><a href="index.html"><span class="k">Volver</span>'
      '<span class="v">Menú</span></a>'
      '<a class="next" href="guia.html"><span class="k">Ver</span>'
      '<span class="v">Cómo funciona</span></a></nav>'
      '</div>'
    ) % (total, grupos)

    return (HEAD.format(title="Banco de ejercicios — Rutina del tapete",
                        css=CSS + BANCO_CSS)
            + topbar("banco") + body
            + '<script>window.PAGE_KEY="banco";</script>'
            + '<script>%s</script>' % JS
            + '<script>%s</script>' % BANCO_JS)


with open(os.path.join(OUT, "banco.html"), "w", encoding="utf-8") as f:
    f.write(render_banco())

print("guía y banco ok")


# ---------------------------------------------------------------- un solo archivo
# Version de una sola pagina para descargar y usar sin internet.

PAGINAS = ["index", "dias", "dia-1", "dia-2", "dia-3", "dia-4", "dia-5", "dia-6",
           "dia-7", "aleatoria", "abdominales", "pecho", "banco", "guia", "progresion"]

# ids que hay que separar por seccion para que no choquen entre si
# (los de dentro de los SVG se dejan quietos: el marcador de flecha es el mismo)
RE_ID = re.compile(r'\b(id|for)="((?:b\d+-[ir]\d+|w\d+-d\d+-[prn]|salida|generar|con-hiit|q-banco))"')

UNICO_CSS = """
.pg[hidden]{display:none !important}
.volver{
  position:fixed; right:14px; bottom:calc(14px + env(safe-area-inset-bottom,0px)); z-index:55;
  width:46px; height:46px; border-radius:50%; border:1px solid var(--line-strong);
  background:var(--surface); color:var(--ink-2); box-shadow:var(--shadow);
  font-size:20px; line-height:1; cursor:pointer; display:none;
}
.volver:hover{border-color:var(--accent); color:var(--accent)}
.volver.on{display:block}
.cronometrando .volver{bottom:calc(96px + env(safe-area-inset-bottom,0px))}
"""

UNICO_JS = r"""
(function(){
  var secs = Array.prototype.slice.call(document.querySelectorAll('.pg'));
  var crono = document.querySelector('.timer');
  var volver = document.querySelector('.volver');

  /* ---------------- cronometro, uno para toda la pagina ---------------- */
  var cd = crono && crono.querySelector('.cd');
  var tb = crono && crono.querySelector('.tbar i');
  var tl = crono && crono.querySelector('.lb');
  var iv = null, left = 0, span = 0, lock = null;

  function fmt(s){ var m = Math.floor(s/60), r = s%60; return m ? m+':'+(r<10?'0':'')+r : ''+r; }
  function pinta(){ if(cd) cd.textContent = fmt(left); if(tb) tb.style.width = span ? (left/span*100)+'%' : '0%'; }
  function beep(){
    try{
      var AC = window.AudioContext || window.webkitAudioContext; if(!AC) return;
      var c = new AC(), o = c.createOscillator(), g = c.createGain();
      o.type='sine'; o.frequency.value=660;
      g.gain.setValueAtTime(.001,c.currentTime);
      g.gain.exponentialRampToValueAtTime(.3,c.currentTime+.02);
      g.gain.exponentialRampToValueAtTime(.001,c.currentTime+.55);
      o.connect(g); g.connect(c.destination); o.start(); o.stop(c.currentTime+.6);
      setTimeout(function(){ try{c.close();}catch(e){} }, 900);
    }catch(e){}
  }
  function parar(){ if(iv) clearInterval(iv); iv=null;
                    if(crono) crono.classList.remove('on');
                    document.documentElement.classList.remove('cronometrando');
                    if(lock){ try{lock.release();}catch(e){} lock=null; } }
  function arranca(seg, et){
    if(!crono) return;
    if(iv) clearInterval(iv);
    span = left = seg; if(tl) tl.textContent = et || 'Descanso';
    crono.classList.add('on');
    document.documentElement.classList.add('cronometrando'); pinta();
    iv = setInterval(function(){ left--; pinta();
      if(left<=0){ clearInterval(iv); iv=null; beep(); setTimeout(parar,1600); } }, 1000);
  }
  if (crono){
    var mas = crono.querySelector('[data-add]');
    if (mas) mas.addEventListener('click', function(){ left+=15; span=Math.max(span,left); pinta(); });
    var ya = crono.querySelector('[data-stop]');
    if (ya) ya.addEventListener('click', parar);
  }

  /* ---------------- progreso de la seccion visible ---------------- */
  var raiz = null, clave = 'x', st = {}, cajas = [], rondas = [];

  function guarda(){ try{ localStorage.setItem('rutina:'+clave, JSON.stringify(st)); }catch(e){} }
  function ambito(){ return (raiz && raiz.querySelector('.rutina:not([hidden])')) || raiz || document; }

  function refresca(){
    var tot = cajas.length + rondas.length, ok = 0;
    cajas.forEach(function(b){ if(b.checked) ok++; });
    rondas.forEach(function(r){ if(r.getAttribute('aria-pressed')==='true') ok++; });
    var bar = raiz && raiz.querySelector('.bar i'), n = raiz && raiz.querySelector('.prog .n');
    if (bar) bar.style.width = tot ? Math.round(ok/tot*100)+'%' : '0%';
    if (n) n.textContent = ok + ' / ' + tot;
  }

  function enlaza(){
    if (!raiz) return;
    var a = ambito();
    cajas  = Array.prototype.slice.call(a.querySelectorAll('.row input[type=checkbox]'));
    rondas = Array.prototype.slice.call(a.querySelectorAll('.rd'));

    cajas.forEach(function(b){
      if (st[b.id]) b.checked = true;
      if (b.dataset.lig) return;
      b.dataset.lig = '1';
      b.addEventListener('change', function(){
        if (b.checked) st[b.id] = 1; else delete st[b.id];
        guarda(); refresca();
      });
    });
    rondas.forEach(function(r){
      r.setAttribute('aria-pressed', st[r.id] ? 'true' : 'false');
      if (r.dataset.lig) return;
      r.dataset.lig = '1';
      r.addEventListener('click', function(){
        var on = r.getAttribute('aria-pressed')==='true';
        r.setAttribute('aria-pressed', on?'false':'true');
        if (on) delete st[r.id]; else st[r.id] = 1;
        guarda(); refresca();
      });
    });
    raiz.querySelectorAll('.restbtn').forEach(function(b){
      if (b.dataset.lig) return;
      b.dataset.lig = '1';
      b.addEventListener('click', function(){ arranca(parseInt(b.dataset.sec,10)||60, b.dataset.label); });
    });
    refresca();
  }
  window.RUTINA_ENLAZA = enlaza;

  /* ---------------- dibujos on/off, global ---------------- */
  var KF = 'rutina:sinfig', sinFig = false;
  try{ sinFig = localStorage.getItem(KF)==='1'; }catch(e){}
  function pintaFig(){
    document.documentElement.classList.toggle('sin-fig', sinFig);
    document.querySelectorAll('.figtog').forEach(function(b){
      b.textContent = sinFig ? 'Mostrar dibujos' : 'Ocultar dibujos';
    });
  }
  document.querySelectorAll('.figtog').forEach(function(b){
    b.addEventListener('click', function(){
      sinFig = !sinFig; try{ localStorage.setItem(KF, sinFig?'1':'0'); }catch(e){}
      pintaFig();
    });
  });
  pintaFig();

  /* ---------------- reiniciar, por seccion ---------------- */
  document.querySelectorAll('.reset').forEach(function(r){
    r.addEventListener('click', function(){
      cajas.forEach(function(b){ b.checked=false; delete st[b.id]; });
      rondas.forEach(function(x){ x.setAttribute('aria-pressed','false'); delete st[x.id]; });
      guarda(); refresca();
    });
  });

  /* ---------------- selector de rutina (abdominales y pecho) ---------------- */
  secs.forEach(function(sec){
    var bs = Array.prototype.slice.call(sec.querySelectorAll('.picker button'));
    if (!bs.length) return;
    var K = 'rutina:sel:' + sec.dataset.key;
    function muestra(id, g){
      sec.querySelectorAll('.rutina').forEach(function(r){ r.hidden = (r.dataset.rid !== id); });
      bs.forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.rid===id ? 'true':'false'); });
      if (g){ try{ localStorage.setItem(K, id); }catch(e){} }
      if (sec === raiz) enlaza();
    }
    var ini = bs[0].dataset.rid;
    try{ var g = localStorage.getItem(K);
         if (g && sec.querySelector('.rutina[data-rid="'+g+'"]')) ini = g; }catch(e){}
    muestra(ini, false);
    bs.forEach(function(b){
      b.addEventListener('click', function(){
        muestra(b.dataset.rid, true);
        var r = sec.querySelector('.rutina:not([hidden])');
        if (r) window.scrollTo({ top: r.offsetTop - 70, behavior:'smooth' });
      });
    });
    var v = sec.querySelector('details.verdad');
    if (v){
      var KV = 'rutina:verdad:' + sec.dataset.key;
      try{ if (localStorage.getItem(KV)==='0') v.open = false; }catch(e){}
      v.addEventListener('toggle', function(){
        try{ localStorage.setItem(KV, v.open?'1':'0'); }catch(e){}
      });
    }
  });

  /* ---------------- buscador del banco ---------------- */
  (function(){
    var sec = document.querySelector('.pg[data-key="banco"]');
    if (!sec) return;
    var inp = sec.querySelector('.buscar'); if (!inp) return;
    var sin = function(t){ return t.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase(); };
    inp.addEventListener('input', function(){
      var q = sin(inp.value.trim()), tot = 0;
      sec.querySelectorAll('.gr').forEach(function(g){
        var n = 0;
        var grupo = q && sin(g.querySelector('h2').textContent).indexOf(q) >= 0;
        g.querySelectorAll('li[data-nombre]').forEach(function(li){
          var ok = !q || grupo || sin(li.dataset.nombre).indexOf(q) >= 0;
          li.hidden = !ok; if (ok) n++;
        });
        g.hidden = n === 0; tot += n;
      });
      sec.querySelector('.vacio').hidden = tot > 0;
    });
  })();

  /* ---------------- registro de la progresion ---------------- */
  (function(){
    var sec = document.querySelector('.pg[data-key="progresion"]'); if (!sec) return;
    var K = 'rutina:registro', d = {};
    try{ d = JSON.parse(localStorage.getItem(K)||'{}')||{}; }catch(e){}
    sec.querySelectorAll('.reg input').forEach(function(i){
      if (d[i.id] != null) i.value = d[i.id];
      i.addEventListener('input', function(){
        d[i.id] = i.value;
        try{ localStorage.setItem(K, JSON.stringify(d)); }catch(e){}
      });
    });
    var b = sec.querySelector('.clearreg');
    if (b) b.addEventListener('click', function(){
      d = {}; try{ localStorage.removeItem(K); }catch(e){}
      sec.querySelectorAll('.reg input').forEach(function(i){ i.value=''; });
    });
  })();

  /* ---------------- navegacion entre secciones ---------------- */
  function ir(id, empujar){
    var sec = document.querySelector('.pg[data-key="'+id+'"]') || secs[0];
    secs.forEach(function(s){ s.hidden = (s !== sec); });
    raiz = sec; clave = sec.dataset.key;
    try{ st = JSON.parse(localStorage.getItem('rutina:'+clave)||'{}')||{}; }catch(e){ st = {}; }
    parar();
    enlaza();
    if (volver) volver.classList.toggle('on', clave !== 'index');
    if (empujar && location.hash !== '#'+clave){
      try{ history.pushState(null,'','#'+clave); }catch(e){ location.hash = clave; }
    }
    window.scrollTo(0, 0);
  }

  document.addEventListener('click', function(ev){
    var a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href').slice(1);
    if (!document.querySelector('.pg[data-key="'+id+'"]')) return;
    ev.preventDefault();
    ir(id, true);
  });
  window.addEventListener('popstate', function(){ ir((location.hash||'#index').slice(1), false); });
  if (volver) volver.addEventListener('click', function(){ ir('index', true); });

  ir((location.hash||'#index').slice(1), false);
})();
"""


def _cuerpo(archivo, clave):
    """Saca la barra y el contenido de una pagina ya generada."""
    txt = open(os.path.join(OUT, archivo), encoding="utf-8").read()
    ini = txt.index('<header class="top">')
    fin = txt.find("<script", ini)
    if fin < 0:
        fin = len(txt)
    html = txt[ini:fin]
    html = html.replace(TIMER, "")                       # el cronometro va aparte
    html = re.sub(r'href="([a-z0-9-]+)\.html"', r'href="#\1"', html)
    html = RE_ID.sub(lambda m: '%s="%s__%s"' % (m.group(1), clave, m.group(2)), html)
    return '<section class="pg" data-key="%s" hidden>%s</section>' % (clave, html)


TODO_CSS = (CSS + INDEX_CSS_EXTRA + MENU_CSS + SEC_CSS + BANCO_CSS + PROG_CSS
            + ALEA_CSS + UNICO_CSS)

alea_js = (ALEA_JS
           .replace("__CATALOGO__",
                    json.dumps(CATALOGO, ensure_ascii=False).replace("</", "<\\/"))
           .replace("document.getElementById('generar')", "document.querySelector('.bigbtn')")
           .replace("document.getElementById('con-hiit')", "document.querySelector('.opt input')"))

unico = (
    '<!doctype html><html lang="es"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
    '<title>Rutina del tapete</title>'
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Oswald:wght@400;500;600&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400'
    '&display=swap">'
    '<style>:root{padding-top:env(safe-area-inset-top,0px);'
    'padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:light}'
    'body{margin:0}img{max-width:100%}[hidden]{display:none!important}'
    + TODO_CSS + '</style></head><body>'
    + "".join(_cuerpo(("index" if p == "index" else p) + ".html", p) for p in PAGINAS)
    + TIMER
    + '<button type="button" class="volver" title="Volver al menú" aria-label="Volver al menú">&#9737;</button>'
    + '<script>' + alea_js + '</script>'
    + '<script>' + UNICO_JS + '</script>'
    + '</body></html>'
)

RUTA_UNICO = os.path.join(os.path.dirname(OUT), "rutina-del-tapete.html")
with open(RUTA_UNICO, "w", encoding="utf-8") as f:
    f.write(unico)

print("archivo unico: %.0f KB" % (len(unico.encode("utf-8")) / 1024))
