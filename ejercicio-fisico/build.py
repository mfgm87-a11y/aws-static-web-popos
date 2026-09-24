# -*- coding: utf-8 -*-
"""Genera las paginas HTML de la rutina a partir de los datos."""
import os, json, html

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

  var boxes = Array.prototype.slice.call(document.querySelectorAll('.row input[type=checkbox]'));
  var rds   = Array.prototype.slice.call(document.querySelectorAll('.rd'));
  var barEl = document.querySelector('.bar i');
  var nEl   = document.querySelector('.prog .n');

  function refresh(){
    var total = boxes.length + rds.length;
    var done  = boxes.filter(function(b){ return b.checked; }).length
              + rds.filter(function(r){ return r.getAttribute('aria-pressed') === 'true'; }).length;
    if (barEl) barEl.style.width = total ? Math.round(done/total*100) + '%' : '0%';
    if (nEl) nEl.textContent = done + ' / ' + total;
  }

  boxes.forEach(function(b){
    if (state[b.id]) b.checked = true;
    b.addEventListener('change', function(){
      if (b.checked) state[b.id] = 1; else delete state[b.id];
      save(); refresh();
    });
  });

  rds.forEach(function(r){
    if (state[r.id]) r.setAttribute('aria-pressed','true');
    r.addEventListener('click', function(){
      var on = r.getAttribute('aria-pressed') === 'true';
      r.setAttribute('aria-pressed', on ? 'false' : 'true');
      if (on) delete state[r.id]; else state[r.id] = 1;
      save(); refresh();
    });
  });

  var rs = document.querySelector('.reset');
  if (rs) rs.addEventListener('click', function(){
    state = {}; save();
    boxes.forEach(function(b){ b.checked = false; });
    rds.forEach(function(r){ r.setAttribute('aria-pressed','false'); });
    refresh();
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

  document.querySelectorAll('.restbtn').forEach(function(b){
    b.addEventListener('click', function(){ start(parseInt(b.dataset.sec,10) || 60, b.dataset.label); });
  });
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

  refresh();
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

def topbar(active):
    chips = []
    for slug, nombre, letra in DIAS:
        cur = ' aria-current="page"' if slug == active else ''
        chips.append('<a href="%s.html"%s title="%s">%s</a>' % (slug, cur, nombre, letra))
    return ('<header class="top"><div class="top-in">'
            '<a class="home" href="index.html">&larr; Índice</a>'
            '<nav class="days" aria-label="Días de la semana">%s</nav>'
            '</div></header>') % ("".join(chips))

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
    how = ''
    if x.get("how"):
        how = ('<details class="how"><summary>Cómo se hace</summary><p>%s</p></details>' % x["how"])
    return (
      '<li>'
      '<label class="row" for="%s">'
      '<input type="checkbox" id="%s">'
      '<span class="txt"><span class="nm">%s%s</span>'
      '<span class="sub"><span class="d">%s</span>%s</span></span>'
      '</label>%s</li>'
    ) % (ident, ident, code, E(x["n"]), E(x["d"]), load, how)

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
    if b.get("rest"):
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
        pager += '<a href="index.html"><span class="k">Volver</span><span class="v">Índice</span></a>'
    if nxt:
        pager += '<a class="next" href="%s.html"><span class="k">Siguiente</span><span class="v">%s</span></a>' % (nxt[0], nxt[1])
    else:
        pager += '<a class="next" href="progresion.html"><span class="k">Siguiente</span><span class="v">Progresión</span></a>'
    pager += '</nav>'

    body = (
      '<div class="wrap">'
      '<header class="hero">'
      '<p class="eyebrow">Día %d de 7</p>'
      '<h1>%s</h1>'
      '<p class="focus">%s</p>'
      '<div class="meta"><span class="chip">%d minutos</span><span class="chip load">%s</span></div>'
      '<div class="prog"><span class="bar"><i></i></span><span class="n num">0 / 0</span>'
      '<button type="button" class="reset">Reiniciar</button></div>'
      '</header>'
      '%s%s%s</div>%s'
    ) % (d["n"], E(d["nombre"]), E(d["focus"]), d["dur"], E(d["carga"]),
         blocks, notes, pager, TIMER)

    title = "Día %d · %s — Rutina del tapete" % (d["n"], d["nombre"])
    return (HEAD.format(title=E(title), css=CSS)
            + topbar(slug)
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

def render_index():
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
      '<section class="sec"><h2>Tu equipo</h2><div class="tw"><table>'
      '<tbody>%s</tbody></table></div></section>'
      '<section class="sec"><h2>Configuraciones de carga</h2>'
      '<p class="bnote">Cambiar discos toma 30 segundos. Cada rutina te dice cuál usar.</p>'
      '<div class="tw"><table><thead><tr><th>Nombre</th><th>Cómo se arma</th><th>Peso</th></tr></thead>'
      '<tbody>%s</tbody></table></div></section>'
      '<section class="sec"><h2>La rotación</h2><div class="tw"><table>'
      '<thead><tr><th>Día</th><th>Pierna</th><th>Pecho</th><th>Espalda</th><th>Brazo</th></tr></thead>'
      '<tbody>%s</tbody></table></div>'
      '<p class="bnote">El domingo es suave a propósito. Entrenas los siete días, pero uno deja que '
      'el cuerpo se reconstruya. Sin ese día, a las tres semanas se te cae el rendimiento.</p></section>'
      '<section class="sec"><h2>Reglas de la casa</h2><ul class="rules">%s</ul></section>'
      '<section class="sec"><h2>Progresión</h2>'
      '<p class="bnote">Cuándo subir de peso, qué hacer cuando se acaben los discos y dónde anotar tus números.</p>'
      '<div class="grid" style="margin-top:12px"><a class="card rest" href="progresion.html">'
      '<span class="d">Referencia</span><h3>Progresión</h3>'
      '<p>La regla de las dos rondas, qué esperar mes a mes y la tabla de registro.</p>'
      '<div class="load">Abrir &rarr;</div></a></div></section>'
      '<p class="fine">Esto es una rutina general para alguien sano que entrena en casa y no sustituye '
      'a un profesional. Si tienes una lesión, una condición cardíaca o llevas mucho tiempo sin moverte, '
      'habla con un médico o un fisioterapeuta antes de arrancar.</p>'
      '</div>'
    ) % (cards, eq, cg, rt, rl)

    return (HEAD.format(title="Rutina del tapete", css=CSS + INDEX_CSS_EXTRA)
            + '<header class="top"><div class="top-in">'
            + '<span class="home">Rutina del tapete</span>'
            + '<nav class="days" aria-label="Días de la semana">'
            + "".join('<a href="%s.html" title="%s">%s</a>' % (s, n, l) for s, n, l in DIAS)
            + '</nav></div></header>'
            + body)

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(render_index())


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
      '<nav class="pager"><a href="index.html"><span class="k">Volver</span><span class="v">Índice</span></a>'
      '<a class="next" href="dia-1.html"><span class="k">Empezar</span><span class="v">Lunes</span></a></nav>'
      '</div>'
    ) % (ps, sn, ini, sem_tables, esp)

    return (HEAD.format(title="Progresión — Rutina del tapete", css=CSS + PROG_CSS)
            + topbar("progresion")
            + body
            + '<script>%s</script>' % REG_JS)

with open(os.path.join(OUT, "progresion.html"), "w", encoding="utf-8") as f:
    f.write(render_prog())

print("ok:", sorted(os.listdir(OUT)))
