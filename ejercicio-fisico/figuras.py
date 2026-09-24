# -*- coding: utf-8 -*-
"""Monachos: dibuja figuras de palo en SVG para ilustrar cada ejercicio.

Sistema de angulos: 0 = hacia abajo, 90 = hacia la derecha, 180 = hacia
arriba, 270 = hacia la izquierda. La figura mira a la derecha.

Una pose se define con:
    hip   (x, y) de la cadera
    t     inclinacion del torso: 0 = vertical, + = se inclina al frente
    th    angulo del muslo    (cerca, lejos)
    sh    angulo de la canilla (cerca, lejos)
    ua    angulo del brazo     (cerca, lejos)
    fa    angulo del antebrazo (cerca, lejos)
    foot  angulo del pie (90 = apunta al frente)
    head  inclinacion extra de la cabeza
"""
import math

TORSO, UA, FA, TH, SH, HEAD, FOOT = 32.0, 18.0, 17.0, 22.0, 22.0, 6.5, 9.0
GROUND = 130.0
VB_W, VB_H = 250.0, 188.0


def polar(p, ang, d):
    a = math.radians(ang)
    return (p[0] + d * math.sin(a), p[1] + d * math.cos(a))


def _pair(v):
    return v if isinstance(v, (tuple, list)) else (v, v)


def pose(hip, t=0.0, th=0.0, sh=0.0, ua=0.0, fa=0.0, foot=90.0, head=0.0):
    return dict(hip=tuple(hip), t=t, th=_pair(th), sh=_pair(sh),
                ua=_pair(ua), fa=_pair(fa), foot=_pair(foot), head=head)


def joints(p):
    """Calcula todos los puntos de una pose."""
    hip = p["hip"]
    neck = polar(hip, 180 - p["t"], TORSO)
    hd = polar(neck, 180 - p["t"] + p["head"], HEAD + 3.2)
    out = dict(hip=hip, neck=neck, head=hd, sho=neck)
    for i, side in enumerate(("n", "f")):
        kn = polar(hip, p["th"][i], TH)
        an = polar(kn, p["sh"][i], SH)
        to = polar(an, p["foot"][i], FOOT)
        el = polar(neck, p["ua"][i], UA)
        wr = polar(el, p["fa"][i], FA)
        out["knee_" + side] = kn
        out["ankle_" + side] = an
        out["toe_" + side] = to
        out["elbow_" + side] = el
        out["wrist_" + side] = wr
    out["knee"], out["ankle"] = out["knee_n"], out["ankle_n"]
    out["elbow"], out["wrist"] = out["elbow_n"], out["wrist_n"]
    return out


def _f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def _wrap(texto, ancho):
    """Parte un texto en lineas de a lo sumo `ancho` caracteres."""
    if len(texto) <= ancho:
        return [texto]
    lineas, act = [], ""
    for w in texto.split():
        if act and len(act) + 1 + len(w) > ancho:
            lineas.append(act); act = w
        else:
            act = (act + " " + w).strip()
    if act:
        lineas.append(act)
    return lineas[:3]


def _ln(a, b, cls):
    return '<line class="%s" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (
        cls, _f(a[0]), _f(a[1]), _f(b[0]), _f(b[1]))


def body(p, dx=0.0):
    """Dibuja una figura completa desplazada dx en x."""
    j = joints(p)
    if dx:
        j = {k: (v[0] + dx, v[1]) for k, v in j.items()}
    s = []
    # extremidades lejanas primero, mas claras
    s.append(_ln(j["hip"], j["knee_f"], "f-lf"))
    s.append(_ln(j["knee_f"], j["ankle_f"], "f-lf"))
    s.append(_ln(j["ankle_f"], j["toe_f"], "f-lf"))
    s.append(_ln(j["sho"], j["elbow_f"], "f-lf"))
    s.append(_ln(j["elbow_f"], j["wrist_f"], "f-lf"))
    # tronco y cabeza
    bow = p.get("bow", 0.0)
    if bow:
        h, n = j["hip"], j["neck"]
        mx, my = (h[0] + n[0]) / 2.0, (h[1] + n[1]) / 2.0
        dx, dy = n[0] - h[0], n[1] - h[1]
        L = math.hypot(dx, dy) or 1.0
        cx, cy = mx - dy / L * bow, my + dx / L * bow
        s.append('<path class="f-l" fill="none" d="M %s %s Q %s %s %s %s"/>' % (
            _f(h[0]), _f(h[1]), _f(cx), _f(cy), _f(n[0]), _f(n[1])))
    else:
        s.append(_ln(j["hip"], j["neck"], "f-l"))
    s.append('<circle class="f-h" cx="%s" cy="%s" r="%s"/>' % (
        _f(j["head"][0]), _f(j["head"][1]), _f(HEAD)))
    # extremidades cercanas
    s.append(_ln(j["hip"], j["knee_n"], "f-l"))
    s.append(_ln(j["knee_n"], j["ankle_n"], "f-l"))
    s.append(_ln(j["ankle_n"], j["toe_n"], "f-l"))
    s.append(_ln(j["sho"], j["elbow_n"], "f-l"))
    s.append(_ln(j["elbow_n"], j["wrist_n"], "f-l"))
    return "".join(s), j


# ------------------------------------------------------------------ equipo

def db(p):
    """Una mancuerna en el punto p."""
    x, y = p
    return ('<g class="f-e"><rect x="%s" y="%s" width="13" height="2.6" rx="1.3"/>'
            '<rect x="%s" y="%s" width="4" height="11" rx="1.4"/>'
            '<rect x="%s" y="%s" width="4" height="11" rx="1.4"/></g>') % (
        _f(x - 6.5), _f(y - 1.3), _f(x - 8.5), _f(y - 5.5), _f(x + 4.5), _f(y - 5.5))


def bar(a, b=None):
    """La vara larga. Si b es None, dibuja una barra horizontal centrada en a."""
    if b is None:
        b = (a[0] + 34, a[1])
        a = (a[0] - 34, a[1])
    s = ['<line class="f-eb" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (
        _f(a[0]), _f(a[1]), _f(b[0]), _f(b[1]))]
    for q in (a, b):
        s.append('<rect class="f-e" x="%s" y="%s" width="4.4" height="15" rx="1.6"/>'
                 % (_f(q[0] - 2.2), _f(q[1] - 7.5)))
    return "".join(s)


def plate(p):
    x, y = p
    return '<circle class="f-e" cx="%s" cy="%s" r="6"/>' % (_f(x), _f(y))


def ground(y=GROUND, x1=6, x2=VB_W - 6):
    return '<line class="f-g" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (_f(x1), _f(y), _f(x2), _f(y))


def mat(x1, x2, y=GROUND):
    return ('<rect class="f-mat" x="%s" y="%s" width="%s" height="4" rx="2"/>'
            % (_f(x1), _f(y - 2), _f(x2 - x1)))


def chair(x, y=GROUND, w=30):
    """Silla de perfil: asiento, espaldar y patas."""
    seat = y - 34
    return ('<g class="f-obj">'
            '<line x1="%s" y1="%s" x2="%s" y2="%s"/>'
            '<line x1="%s" y1="%s" x2="%s" y2="%s"/>'
            '<line x1="%s" y1="%s" x2="%s" y2="%s"/>'
            '<line x1="%s" y1="%s" x2="%s" y2="%s"/></g>') % (
        _f(x), _f(seat), _f(x + w), _f(seat),
        _f(x + w), _f(seat), _f(x + w), _f(seat - 30),
        _f(x + 2), _f(seat), _f(x + 2), _f(y),
        _f(x + w - 2), _f(seat), _f(x + w - 2), _f(y))


def box(x, y, w, h, label=None):
    """Un bloque solido: sofa, escalon, cajon."""
    s = ['<rect class="f-box" x="%s" y="%s" width="%s" height="%s" rx="2.5"/>'
         % (_f(x), _f(y), _f(w), _f(h))]
    if label:
        s.append('<text class="f-c" x="%s" y="%s" text-anchor="middle">%s</text>'
                 % (_f(x + w / 2.0), _f(y + h / 2.0 + 3.5), label))
    return "".join(s)


def wall(x, y1=24, y2=GROUND):
    return ('<line class="f-obj" x1="%s" y1="%s" x2="%s" y2="%s"/>'
            % (_f(x), _f(y1), _f(x), _f(y2)))


# ------------------------------------------------------------- anotaciones

def hline(y, label, x1=10, x2=VB_W - 10, anchor="end"):
    """Linea punteada horizontal: 'hasta aqui'."""
    tx = x2 - 2 if anchor == "end" else x1 + 2
    return ('<line class="f-d" x1="%s" y1="%s" x2="%s" y2="%s"/>'
            '<text class="f-t" x="%s" y="%s" text-anchor="%s">%s</text>') % (
        _f(x1), _f(y), _f(x2), _f(y), _f(tx), _f(y - 4), anchor, label)


def vline(x, label, y1, y2):
    return ('<line class="f-d" x1="%s" y1="%s" x2="%s" y2="%s"/>'
            '<text class="f-t" x="%s" y="%s" text-anchor="middle">%s</text>') % (
        _f(x), _f(y1), _f(x), _f(y2), _f(x), _f(y1 - 4), label)


def arc(v, a, b, label, r=15):
    """Arco de angulo con vertice en v, entre las direcciones a y b."""
    def ang(p):
        return math.atan2(p[1] - v[1], p[0] - v[0])
    a0, a1 = ang(a), ang(b)
    d = (a1 - a0) % (2 * math.pi)
    sweep = 1
    if d > math.pi:
        d = 2 * math.pi - d
        a0, a1 = a1, a0
    p0 = (v[0] + r * math.cos(a0), v[1] + r * math.sin(a0))
    p1 = (v[0] + r * math.cos(a1), v[1] + r * math.sin(a1))
    mid = a0 + d / 2.0
    lx = v[0] + (r + 10) * math.cos(mid)
    ly = v[1] + (r + 10) * math.sin(mid) + 3.5
    return ('<path class="f-d" d="M %s %s A %s %s 0 0 %d %s %s" fill="none"/>'
            '<text class="f-t" x="%s" y="%s" text-anchor="middle">%s</text>') % (
        _f(p0[0]), _f(p0[1]), _f(r), _f(r), sweep, _f(p1[0]), _f(p1[1]),
        _f(lx), _f(ly), label)


def arrow(a, b, bend=16):
    """Flecha curva de a hacia b."""
    mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0 - bend
    return ('<path class="f-a" d="M %s %s Q %s %s %s %s" marker-end="url(#ah)"/>'
            % (_f(a[0]), _f(a[1]), _f(mx), _f(my), _f(b[0]), _f(b[1])))


def caption(x, text):
    ls = _wrap(text, 19)
    y0 = VB_H - 20 if len(ls) > 1 else VB_H - 14
    return "".join('<text class="f-c" x="%s" y="%s" text-anchor="middle">%s</text>'
                   % (_f(x), _f(y0 + i * 11), l) for i, l in enumerate(ls))


DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        '<path d="M 0 1 L 9 5 L 0 9 z" class="f-am"/></marker></defs>')


def scene(parts, alt=""):
    """Envuelve el dibujo en un <svg> listo para insertar en la pagina."""
    return ('<svg class="fig" viewBox="0 0 %s %s" role="img" aria-label="%s" '
            'preserveAspectRatio="xMidYMid meet">%s%s</svg>'
            % (_f(VB_W), _f(VB_H), alt, DEFS, "".join(parts)))


# --------------------------------------------------- poses por coordenadas

def ang_of(v):
    return math.degrees(math.atan2(v[0], v[1]))


def ik(root, target, l1, l2, bend=1):
    """Angulos de una cadena de dos segmentos que va de root a target."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    d = math.hypot(dx, dy)
    d = max(abs(l1 - l2) + 0.01, min(l1 + l2 - 0.01, d))
    phi = ang_of((dx, dy))
    c = (l1 * l1 + d * d - l2 * l2) / (2.0 * l1 * d)
    alpha = math.degrees(math.acos(max(-1.0, min(1.0, c))))
    a1 = phi + bend * alpha
    j = polar(root, a1, l1)
    a2 = ang_of((target[0] - j[0], target[1] - j[1]))
    return a1, a2


def P(hip, lean, ankles, wrists, knee=1, elbow=-1, foot=None, head=0.0, bow=0.0):
    """Arma una pose a partir de puntos: tobillos y munecas.

    ankles y wrists son (cerca, lejos); si se pasa un solo punto, vale
    para los dos lados. knee/elbow dan la direccion del doblez.
    """
    hip = tuple(hip)
    neck = polar(hip, 180 - lean, TORSO)
    an = ankles if isinstance(ankles, (tuple, list)) and isinstance(ankles[0], (tuple, list)) else (ankles, ankles)
    wr = wrists if isinstance(wrists, (tuple, list)) and isinstance(wrists[0], (tuple, list)) else (wrists, wrists)
    kb = _pair(knee)
    eb = _pair(elbow)
    th, sh, ua, fa = [], [], [], []
    for i in (0, 1):
        a, b = ik(hip, an[i], TH, SH, kb[i])
        th.append(a); sh.append(b)
        c, d = ik(neck, wr[i], UA, FA, eb[i])
        ua.append(c); fa.append(d)
    if foot is None:
        foot = tuple(sh[i] + 105 for i in (0, 1))
    return dict(hip=hip, t=lean, th=tuple(th), sh=tuple(sh),
                ua=tuple(ua), fa=tuple(fa), foot=_pair(foot), head=head, bow=bow)


LX, RX = 62.0, 178.0   # centros de las dos figuras


def duo(pa, pb, la, lb, eq=None, guides=None, flecha=None,
        piso=True, fondo=None, alt=""):
    """Dos poses lado a lado: inicio y final."""
    parts = []
    if fondo:
        parts.append(fondo)
    if piso:
        parts.append(ground())
    sa, ja = body(pa, LX)
    sb, jb = body(pb, RX)
    parts += [sa, sb]
    if eq:
        parts.append(eq(ja, jb))
    if guides:
        parts.append(guides(ja, jb))
    if flecha:
        parts.append(flecha(ja, jb))
    parts.append(caption(LX, la))
    parts.append(caption(RX, lb))
    return scene(parts, alt)


def solo(p, label, eq=None, guides=None, piso=True, fondo=None, alt=""):
    """Una sola pose, centrada."""
    parts = []
    if fondo:
        parts.append(fondo)
    if piso:
        parts.append(ground())
    s, j = body(p, 125.0)
    parts.append(s)
    if eq:
        parts.append(eq(j))
    if guides:
        parts.append(guides(j))
    parts.append(caption(125.0, label))
    return scene(parts, alt)


def linea(a, b, label=None, off=-5):
    """Linea punteada entre dos puntos: sirve para marcar alineacion."""
    out = ['<line class="f-d" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (
        _f(a[0]), _f(a[1]), _f(b[0]), _f(b[1]))]
    if label:
        out.append('<text class="f-t" x="%s" y="%s" text-anchor="middle">%s</text>' % (
            _f((a[0] + b[0]) / 2.0), _f((a[1] + b[1]) / 2.0 + off), label))
    return "".join(out)


def nota(x, y, texto, anchor="middle"):
    return '<text class="f-t" x="%s" y="%s" text-anchor="%s">%s</text>' % (
        _f(x), _f(y), anchor, texto)


def aviso(texto, x=125.0, ancho=48, y=18.0, cls="f-t"):
    """Texto de guia centrado en x, partido en varias lineas si hace falta."""
    ls = _wrap(texto, ancho)
    return "".join(
        '<text class="%s" x="%s" y="%s" text-anchor="middle">%s</text>'
        % (cls, _f(x), _f(y + i * 11), l) for i, l in enumerate(ls))


def pie_nota(texto, x=125.0, ancho=26):
    """Igual que aviso pero debajo de la figura."""
    return aviso(texto, x, ancho, y=145.0)
