# -*- coding: utf-8 -*-
"""Un dibujo por ejercicio. DIB[clave] = svg listo para insertar."""
from figuras import (P, duo, solo, db, bar, plate, hline, vline, arc, arrow,
                     linea, nota, aviso, pie_nota, box, chair, wall, mat, GROUND)

DIB = {}
G = GROUND          # 130
PIE_H = (0, 86)     # cadera de pie
PIE_A = (0, 130)    # tobillo de pie


# ══════════════════════════════════════════════════ PIERNA · dominante rodilla

# --- sentadilla: sirve al aire y con goblet
sq_arr = P(PIE_H, 8, PIE_A, (14, 88))
sq_abj = P((0, 107), 45, (16, 129), (26, 88))

DIB["sentadilla_aire"] = duo(
    P(PIE_H, 8, PIE_A, (30, 84)), P((0, 107), 45, (16, 129), (34, 96)),
    "1 · De pie", "2 · Abajo",
    guides=lambda a, b: hline(b["hip"][1], "Cadera a la altura de la rodilla", 120, 244)
                        + arc(b["knee"], b["hip"], b["ankle"], "90°", 16),
    alt="Sentadilla al aire: de pie y posición abajo con el muslo paralelo al piso")

DIB["sentadilla_goblet"] = duo(
    sq_arr, sq_abj, "1 · De pie", "2 · Abajo",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    guides=lambda a, b: hline(b["hip"][1], "Muslo paralelo al piso", 120, 244)
                        + linea(b["knee"], (b["knee"][0], G), "rodilla sobre el pie", 16),
    alt="Sentadilla goblet con mancuerna al pecho, arriba y abajo")

# --- sentadilla sumo, vista de frente
DIB["sumo"] = duo(
    P((0, 88), 0, ((-22, G), (22, G)), (0, 112), knee=(-1, 1)),
    P((0, 109), 4, ((-24, G), (24, G)), (0, 122), knee=(-1, 1)),
    "1 · Pies abiertos", "2 · Abajo",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    guides=lambda a, b: aviso("Visto de frente · puntas hacia afuera")
                        + hline(b["hip"][1], "Baja recto", 128, 244),
    alt="Sentadilla sumo vista de frente, pies muy abiertos y puntas hacia afuera")

DIB["sumo_aire"] = DIB["sumo"].replace('<g class="f-e">', '<g class="f-e" opacity="0">')

# --- zancada inversa y sentadilla dividida
lunge_up = P(PIE_H, 6, PIE_A, (5, 92))
lunge_dn = P((0, 104), 9, ((18, G), (-33, 124)), (5, 110), knee=(1, -1),
             foot=(90, 20))

DIB["zancada_inversa"] = duo(
    lunge_up, lunge_dn, "1 · De pie", "2 · Paso atrás",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: arc(b["knee_n"], b["hip"], b["ankle_n"], "90°", 15)
                        + hline(b["knee_f"][1] + 3, "La rodilla de atrás casi toca", 120, 244),
    alt="Zancada inversa: de pie y abajo con la rodilla de atrás cerca del piso")

DIB["sentadilla_dividida"] = duo(
    P((0, 90), 6, ((14, G), (-28, 126)), (5, 96), knee=(1, -1), foot=(90, 25)),
    lunge_dn, "1 · Pies fijos", "2 · Abajo",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Los dos pies en el piso", 62, 24)
                        + hline(b["knee_f"][1] + 3, "Rodilla de atrás al piso", 120, 244),
    alt="Sentadilla dividida: los dos pies en el piso, se baja en el sitio")

DIB["zancada_rotacion"] = solo(
    P((0, 104), 9, ((18, G), (-33, 124)), ((30, 84), (-6, 80)), knee=(1, -1),
      foot=(90, 20)),
    "Abajo y giras el torso",
    guides=lambda j: arrow((150, 70), (186, 62), 10) + nota(196, 50, "gira"),
    alt="Zancada con rotación de torso hacia el lado de la pierna de adelante")

DIB["salto"] = duo(
    P((0, 104), 40, (14, 129), (-16, 104)),
    P((0, 70), 4, ((-4, 108), (4, 110)), ((8, 44), (-6, 46))),
    "1 · Carga abajo", "2 · Salta",
    guides=lambda a, b: nota(178, 30, "Cae suave, rodilla blanda"),
    piso=True, alt="Sentadilla con salto: se carga abajo y se despega del piso")


# ══════════════════════════════════════════════════ PIERNA · dominante cadera

hinge_up = P(PIE_H, 5, PIE_A, (7, 93))
hinge_dn = P((-6, 90), 74, (0, G), (26, 116))

DIB["peso_muerto_rumano"] = duo(
    hinge_up, hinge_dn, "1 · De pie", "2 · Cadera atrás",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: hline(119, "La barra baja a media canilla", 120, 244)
                        + linea(b["neck"], b["hip"], "espalda plana", -6)
                        + arrow((150, 96), (128, 96), 0),
    alt="Peso muerto rumano: de pie y con la cadera echada atrás, espalda plana")

DIB["bisagra"] = duo(
    hinge_up, hinge_dn, "1 · De pie", "2 · Cadera atrás",
    guides=lambda a, b: aviso("Rodillas casi rectas", 178, 24)
                        + linea(b["neck"], b["hip"], "espalda plana", -6),
    alt="Bisagra de cadera sin peso")

DIB["peso_muerto_1p"] = duo(
    P(PIE_H, 5, PIE_A, (7, 93)),
    P((-4, 92), 76, ((2, G), (-40, 88)), (24, 118), knee=(1, -1), foot=(95, 60)),
    "1 · Un pie", "2 · Baja",
    eq=lambda a, b: db(a["wrist_n"]) + db(b["wrist_n"]),
    guides=lambda a, b: linea(b["ankle_f"], b["neck"], "cuerpo en línea", -6)
                        + aviso("Cadera cuadrada, no se abre", 178, 24),
    alt="Peso muerto a una pierna: la pierna libre va atrás en línea con la espalda")

DIB["puente_gluteo"] = duo(
    P((0, 124), -90, (24, 128), (-20, 128)),
    P((-2, 106), -120, (24, 128), (-22, 126)),
    "1 · Cadera abajo", "2 · Cadera arriba",
    eq=lambda a, b: db(b["hip"]),
    guides=lambda a, b: linea(b["knee"], b["neck"], "línea recta rodilla–hombro", -6)
                        + aviso("Aprieta el glúteo 2 s arriba", 178, 24),
    alt="Puente de glúteo: subir la cadera hasta alinear rodillas y hombros")

DIB["almeja"] = solo(
    P((0, 116), -90, ((26, 128), (22, 106)), (-24, 118), knee=(1, 1)),
    "Acostado de lado, abre la rodilla",
    guides=lambda j: arrow((150, 96), (164, 78), 6) + nota(178, 68, "abre"),
    alt="Almeja: acostado de lado con las rodillas dobladas, se abre la de arriba")

DIB["balanceo_pierna"] = solo(
    P(PIE_H, 4, ((30, 112), (0, G)), (6, 92), knee=(1, 1)),
    "Balancea al frente y atrás",
    guides=lambda j: arrow((175, 112), (140, 116), -8) + nota(125, 30, "Suelto, sin forzar"),
    alt="Balanceo de pierna al frente y atrás, apoyándose en algo")


# ══════════════════════════════════════════════════ PIERNA · pantorrilla

DIB["talones"] = duo(
    P(PIE_H, 3, (0, G), (8, 92)),
    P((0, 75), 3, (0, 119), (8, 81), foot=48),
    "1 · Talón abajo", "2 · Lo más alto",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: vline(214, "sube", 84, 118)
                        + aviso("1 s arriba, baja lento", 178, 24),
    alt="Elevación de talones: se sube hasta el tope sobre las puntas de los pies")


# ══════════════════════════════════════════════════ EMPUJE

# --- press de pecho en el piso
DIB["press_piso"] = duo(
    P((0, 122), -90, (22, 128), (-22, 112)),
    P((0, 122), -90, (22, 128), (-32, 88)),
    "1 · Codos en el piso", "2 · Brazos estirados",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: hline(a["elbow"][1] + 3, "El codo toca el piso, ahí paras", 10, 108, "start")
                        + arc(a["elbow"], a["neck"], a["wrist"], "90°", 13),
    fondo=mat(14, 236), piso=False,
    alt="Press de pecho en el piso: se baja hasta que el codo toca y se empuja arriba")

DIB["press_cerrado"] = duo(
    P((0, 122), -90, (22, 128), (-26, 108)),
    P((0, 122), -90, (22, 128), (-32, 90)),
    "1 · Codos pegados", "2 · Estira",
    eq=lambda a, b: db(a["wrist_n"]) + db(b["wrist_n"]),
    guides=lambda a, b: aviso("Codos pegados a las costillas", 62, 24)
                        + aviso("Mancuernas juntas", 178, 24),
    fondo=mat(14, 236), piso=False,
    alt="Press cerrado en el piso con las mancuernas juntas y los codos pegados")

# --- aperturas, vista desde arriba
DIB["aperturas"] = duo(
    P((0, 108), 0, ((-9, G), (9, G)), ((-36, 84), (36, 84))),
    P((0, 108), 0, ((-9, G), (9, G)), ((-5, 60), (5, 60))),
    "1 · Brazos abiertos", "2 · Junta arriba",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Visto desde arriba · acostado en el tapete")
                        + pie_nota("codos tocan el piso", 62),
    piso=False, alt="Aperturas en el piso vistas desde arriba: brazos abiertos y juntos")

DIB["pullover"] = duo(
    P((0, 122), -90, (22, 128), (-30, 88)),
    P((0, 122), -90, (22, 128), (-58, 106)),
    "1 · Sobre el pecho", "2 · Atrás de la cabeza",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    guides=lambda a, b: hline(126, "La espalda baja no se despega", 128, 244)
                        + aviso("Hasta sentir el estirón", 178, 24),
    fondo=mat(14, 236), piso=False,
    alt="Pullover: la mancuerna va del pecho a detrás de la cabeza")

# --- flexiones
DIB["flexion"] = duo(
    P((0, 96), 90, (-42, 126), (34, 129), elbow=-1, foot=200),
    P((0, 110), 90, (-42, 126), (34, 129), elbow=-1, foot=200),
    "1 · Arriba", "2 · Abajo",
    guides=lambda a, b: linea(a["ankle"], a["head"], "línea recta", -6)
                        + arc(b["elbow"], b["neck"], b["wrist"], "90°", 13),
    alt="Flexión de pecho: el cuerpo baja en línea recta hasta que el codo hace 90 grados")

DIB["flexion_rodillas"] = duo(
    P((0, 100), 90, (-30, 124), (34, 129), elbow=-1, foot=200),
    P((0, 112), 90, (-30, 124), (34, 129), elbow=-1, foot=200),
    "1 · Arriba", "2 · Abajo",
    guides=lambda a, b: aviso("Versión fácil: rodillas en el piso")
                        + linea(a["knee"], a["head"], "línea recta", -6),
    alt="Flexión apoyando las rodillas en el piso")

DIB["flexion_manos_altas"] = duo(
    P((0, 84), 90, (-44, 126), (36, 104), elbow=-1, foot=200),
    P((0, 96), 90, (-44, 126), (36, 104), elbow=-1, foot=200),
    "1 · Arriba", "2 · Pecho al borde",
    fondo=box(198, 104, 46, 26, "sofá"),
    guides=lambda a, b: linea(a["ankle"], a["head"], "línea recta", -6)
                        + aviso("Entre más lejos los pies, más difícil", 62, 24),
    alt="Flexión con las manos en el borde del sofá, cuerpo en línea recta")

# --- press de hombro sentado
DIB["press_hombro"] = duo(
    P((0, 104), 3, (21, 128), (17, 78)),
    P((0, 104), 3, (21, 128), (6, 42)),
    "1 · A la altura del hombro", "2 · Estira arriba",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    fondo=chair(30, 140) + chair(146, 140),
    guides=lambda a, b: arc(a["elbow"], a["neck"], a["wrist"], "90°", 13)
                        + aviso("Espalda pegada al espaldar", 178, 24),
    alt="Press de hombro sentado en la silla con la espalda apoyada")

DIB["press_militar"] = DIB["press_hombro"]


# ══════════════════════════════════════════════════ JALÓN

row_dn = P((-6, 90), 72, (0, G), (25, 117))
row_up = P((-6, 90), 72, (0, G), (9, 98))

DIB["remo_barra"] = duo(
    row_dn, row_up, "1 · Brazos estirados", "2 · Al ombligo",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: linea(b["neck"], b["hip"], "torso a 45°", -6)
                        + arrow((196, 112), (196, 96), 0)
                        + nota(214, 88, "codo atrás"),
    alt="Remo inclinado con barra: se jala hasta el ombligo con los codos hacia atrás")

DIB["remo_1brazo"] = duo(
    P((-6, 90), 72, (0, G), ((25, 117), (14, 104))),
    P((-6, 90), 72, (0, G), ((10, 100), (14, 104))),
    "1 · Cuelga", "2 · Jala a la cadera",
    eq=lambda a, b: db(a["wrist_n"]) + db(b["wrist_n"]),
    guides=lambda a, b: aviso("El otro antebrazo sobre tu muslo", 62, 24)
                        + linea(b["neck"], b["hip"], "espalda plana", -6),
    alt="Remo a un brazo apoyando el antebrazo libre sobre el propio muslo")

# pájaro: vista desde arriba, igual que las aperturas pero al revés
DIB["pajaro"] = duo(
    P((0, 108), 0, ((-9, G), (9, G)), ((-6, 128), (6, 128))),
    P((0, 108), 0, ((-9, G), (9, G)), ((-36, 96), (36, 96))),
    "1 · Cuelgan juntas", "2 · Abre como alas",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Visto desde arriba · inclinado al frente")
                        + pie_nota("aprieta los omóplatos", 178),
    piso=False, alt="Pájaro visto desde arriba: se abren los brazos como alas")

DIB["encogimiento"] = duo(
    P((0, 88), 3, (0, G), (8, 94)),
    P((0, 82), 3, (0, 124), (8, 88)),
    "1 · Hombros sueltos", "2 · A las orejas",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: vline(214, "derecho arriba", 48, 72)
                        + aviso("Sin rodar el hombro", 178, 24),
    alt="Encogimiento de hombros: suben derecho hacia las orejas")

DIB["ytw"] = solo(
    P((0, 122), -92, (34, 126), ((-52, 100), (-40, 96)), bow=-3),
    "Boca abajo: brazos en Y, T y W",
    guides=lambda j: aviso("Solo despega los brazos del piso"),
    fondo=mat(60, 194), piso=False,
    alt="Ejercicio Y T W boca abajo en el tapete")


# ══════════════════════════════════════════════════ BRAZO

DIB["curl"] = duo(
    P(PIE_H, 4, PIE_A, (6, 89)),
    P(PIE_H, 4, PIE_A, (21, 63)),
    "1 · Brazos estirados", "2 · Sube al pecho",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: arc(b["elbow"], b["neck"], b["wrist"], "cierra", 14)
                        + aviso("El codo pegado y quieto", 178, 24),
    alt="Curl de bíceps con barra: solo se mueve el antebrazo")

DIB["martillo"] = duo(
    P(PIE_H, 4, PIE_A, (7, 89)),
    P(PIE_H, 4, PIE_A, (20, 64)),
    "1 · Palmas enfrentadas", "2 · Sube",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Como si sostuvieras dos martillos: la muñeca no gira"),
    alt="Curl martillo con las palmas enfrentadas")

DIB["frances"] = duo(
    P((0, 104), 3, (21, 128), (4, 24)),
    P((0, 104), 3, (21, 128), (-15, 46)),
    "1 · Brazos estirados", "2 · Detrás de la cabeza",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    fondo=chair(30, 140) + chair(146, 140),
    guides=lambda a, b: vline(214, "codos al techo", 30, 58)
                        + aviso("Solo se mueve el antebrazo", 62, 24),
    alt="Extensión de tríceps sobre la cabeza, sentado")

DIB["patada_triceps"] = duo(
    P((-6, 90), 70, (0, G), ((16, 104), (14, 106))),
    P((-6, 90), 70, (0, G), ((4, 118), (14, 106))),
    "1 · Codo arriba", "2 · Estira atrás",
    eq=lambda a, b: db(a["wrist_n"]) + db(b["wrist_n"]),
    guides=lambda a, b: aviso("El codo pegado al costado, quieto"),
    alt="Patada de tríceps inclinado hacia adelante")

DIB["lateral"] = duo(
    P((0, 88), 0, ((-8, G), (8, G)), ((-11, 118), (11, 118))),
    P((0, 88), 0, ((-8, G), (8, G)), ((-35, 57), (35, 57))),
    "1 · A los lados", "2 · Altura del hombro",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: hline(b["neck"][1], "No más alto que el hombro", 128, 244)
                        + pie_nota("meñique un pelo más alto", 178),
    alt="Elevación lateral vista de frente, hasta la altura del hombro")

DIB["rot_externa"] = solo(
    P((0, 88), 0, ((-8, G), (8, G)), ((-31, 84), (31, 84))),
    "Codos pegados, abre los antebrazos",
    guides=lambda j: aviso("Visto de frente · sin peso, para calentar"),
    alt="Rotación externa de hombro con los codos pegados al costado")


# ══════════════════════════════════════════════════ CORE

DIB["plancha"] = solo(
    P((0, 104), 90, (-42, 126), (48, 128), elbow=1, foot=200),
    "Antebrazos y puntas de los pies",
    guides=lambda j: linea(j["ankle"], j["head"], "línea recta talón–cabeza", -6)
                     + aviso("Aprieta glúteo y abdomen"),
    alt="Plancha sobre los antebrazos con el cuerpo en línea recta")

DIB["plancha_lateral"] = solo(
    P((0, 112), 62, (-40, 128), (42, 128), elbow=1, foot=170),
    "Antebrazo y canto del pie",
    guides=lambda j: linea(j["ankle"], j["head"], "cadera arriba", -6)
                     + aviso("Fácil: apoya la rodilla de abajo"),
    alt="Plancha lateral apoyando el antebrazo y el canto del pie")

DIB["plancha_toque"] = duo(
    P((0, 96), 90, (-42, 126), (34, 129), foot=200),
    P((0, 96), 90, (-42, 126), ((34, 129), (26, 88)), foot=200),
    "1 · Plancha alta", "2 · Toca el hombro",
    guides=lambda a, b: aviso("La cadera no se mueve ni un centímetro", 178, 24)
                        + linea(a["ankle"], a["head"], "", 0),
    alt="Plancha alta tocando el hombro contrario sin mover la cadera")

DIB["escalador"] = duo(
    P((0, 96), 90, (-42, 126), (34, 129), foot=200),
    P((0, 96), 90, ((-42, 126), (12, 118)), (34, 129), knee=(-1, 1), foot=200),
    "1 · Plancha alta", "2 · Rodilla al pecho",
    guides=lambda a, b: aviso("Rápido, alternando · la cadera no rebota"),
    alt="Escaladores: en plancha alta se llevan las rodillas al pecho alternando")

DIB["muerto_bicho"] = duo(
    P((0, 122), -90, ((24, 102), (44, 122)), ((-32, 88), (-32, 88)), knee=(1, 1)),
    P((0, 122), -90, ((24, 102), (44, 122)), ((-32, 88), (-60, 108)), knee=(1, 1)),
    "1 · Todo a 90°", "2 · Brazo y pierna contrarios",
    fondo=mat(14, 236), piso=False,
    guides=lambda a, b: hline(126, "La espalda baja no se despega del piso", 128, 244)
                        + aviso("Rodillas y caderas a 90°", 62, 24),
    alt="Muerto bicho: se estiran brazo y pierna contrarios sin arquear la espalda")

DIB["elev_piernas"] = duo(
    P((0, 122), -90, (43, 124), (-14, 126)),
    P((0, 122), -90, (2, 80), (-14, 126)),
    "1 · Abajo, sin tocar", "2 · Piernas arriba",
    fondo=mat(14, 236), piso=False,
    guides=lambda a, b: hline(126, "No tocan el piso", 10, 108, "start")
                        + aviso("Manos debajo de la cola", 178, 24),
    alt="Elevación de piernas acostado, sin tocar el piso abajo")

DIB["giro_ruso"] = solo(
    P((0, 120), -38, (32, 126), (6, 102)),
    "Sentado, tronco atrás",
    eq=lambda j: plate(j["wrist"]),
    guides=lambda j: arrow((96, 86), (154, 86), 14) + nota(125, 60, "gira el torso, no los brazos"),
    alt="Giro ruso sentado con el tronco inclinado atrás y un disco en las manos")

DIB["bicicleta"] = solo(
    P((0, 122), -88, ((18, 104), (46, 120)), ((-26, 100), (-30, 104)), knee=(1, 1)),
    "Codo hacia la rodilla contraria",
    fondo=mat(30, 220), piso=False,
    guides=lambda j: aviso("Alterna con ritmo, sin jalarte el cuello"),
    alt="Bicicleta abdominal: codo hacia la rodilla contraria")

DIB["superman"] = duo(
    P((0, 124), -90, (38, 126), (-58, 122), bow=-2),
    P((0, 124), -85, (38, 112), (-60, 104), bow=-5),
    "1 · Boca abajo", "2 · Sube brazos y piernas",
    fondo=mat(14, 118) + mat(130, 236), piso=False,
    guides=lambda a, b: aviso("2 s arriba, baja lento", 178, 24),
    alt="Superman: boca abajo se suben brazos, pecho y piernas a la vez")

DIB["perro_pajaro"] = solo(
    P((0, 104), 90, ((-26, 126), (-48, 102)), ((34, 130), (66, 100)),
      knee=(-1, -1), elbow=(1, -1)),
    "Brazo y pierna contrarios",
    guides=lambda j: linea(j["ankle_f"], j["wrist_f"], "una sola línea", -6)
                     + aviso("2 s arriba, la cadera no se ladea"),
    alt="Perro-pájaro en cuatro apoyos estirando brazo y pierna contrarios")


# ══════════════════════════════════════════════════ CALENTAMIENTO

DIB["marcha"] = solo(
    P((0, 86), 3, ((24, 102), (0, G)), ((18, 78), (-10, 100)), knee=(1, 1)),
    "Rodilla a la altura de la cadera",
    guides=lambda j: hline(j["hip"][1], "rodilla arriba", 150, 244),
    alt="Marcha en el sitio levantando la rodilla hasta la cadera")

DIB["un_pie"] = solo(
    P((0, 86), 3, ((6, 104), (0, G)), ((-14, 96), (16, 96)), knee=(1, 1)),
    "30 s por pierna, sin agarrarte",
    guides=lambda j: aviso("Si es fácil, cierra los ojos"),
    alt="Equilibrio parado en un pie")

DIB["gato_camello"] = duo(
    P((0, 104), 90, (-26, 126), (36, 130), knee=-1, bow=-9),
    P((0, 104), 90, (-26, 126), (36, 130), knee=-1, bow=8),
    "1 · Gato: redondea", "2 · Camello: hunde",
    guides=lambda a, b: aviso("Lento, siguiendo la respiración"),
    alt="Gato y camello en cuatro apoyos: se redondea y se hunde la espalda")

DIB["circulos_cadera"] = solo(
    P((0, 104), 90, ((-26, 126), (-34, 112)), (36, 130), knee=(-1, -1)),
    "Círculos con la rodilla",
    guides=lambda j: arrow((88, 100), (72, 118), 12) + aviso("10 por lado"),
    alt="Círculos de cadera en cuatro apoyos")

DIB["abre_libro"] = solo(
    P((0, 120), -90, (18, 102), ((-30, 96), (-30, 96)), knee=1),
    "De lado, rodillas a 90°",
    fondo=mat(30, 220), piso=False,
    guides=lambda j: arrow((76, 84), (48, 108), 16)
                     + aviso("Abre el brazo de arriba y síguelo con la mirada"),
    alt="Abre el libro: rotación torácica acostado de lado")

DIB["perro_plancha"] = duo(
    P((0, 80), 120, (-24, 129), (46, 129), knee=-1, elbow=-1, foot=105),
    P((0, 100), 90, (-42, 127), (34, 129), foot=200),
    "1 · Perro boca abajo", "2 · Plancha",
    guides=lambda a, b: aviso("Pasa de una a otra, 8 veces"),
    alt="Perro boca abajo y plancha alta, alternando")


# ══════════════════════════════════════════════════ ESTIRAMIENTOS

DIB["est_cuadriceps"] = solo(
    P((0, 86), 3, ((0, G), (-15, 88)), ((10, 96), (-15, 88)), knee=(1, -1)),
    "Talón al glúteo",
    guides=lambda j: aviso("Rodillas juntas · apóyate en la pared"),
    alt="Estiramiento de cuádriceps de pie llevando el talón al glúteo")

DIB["est_pecho_puerta"] = solo(
    P((0, 88), 0, ((-8, G), (8, G)), ((-40, 58), (10, 114))),
    "Antebrazo en el marco, gira el cuerpo",
    fondo=wall(72, 30, G),
    guides=lambda j: aviso("Codo a la altura del hombro", 148, 28),
    alt="Estiramiento de pecho apoyando el antebrazo en el marco de la puerta")

DIB["est_isquios_pie"] = solo(
    P((-4, 90), 58, ((34, 128), (-8, G)), (28, 112), foot=(55, 90)),
    "Talón clavado, punta arriba",
    guides=lambda j: aviso("Espalda plana · el pecho va al frente, no abajo"),
    alt="Estiramiento de isquiotibiales de pie con el talón clavado y la punta arriba")

DIB["est_isquios_sentado"] = solo(
    P((0, 122), 52, (44, 124), (44, 116)),
    "Sentado, pierna estirada",
    fondo=mat(60, 220), piso=False,
    guides=lambda j: aviso("Dobla desde la cadera, no desde la espalda"),
    alt="Estiramiento de isquiotibiales sentado con la pierna estirada")

DIB["est_gluteo"] = solo(
    P((0, 124), -90, ((22, 102), (8, 98)), (-6, 100), knee=(1, 1)),
    "Tobillo sobre la rodilla, jala",
    fondo=mat(20, 200), piso=False,
    guides=lambda j: aviso("Figura 4 · jala el muslo hacia el pecho"),
    alt="Estiramiento de glúteo en figura 4 acostado")

DIB["est_triceps"] = solo(
    P((0, 86), 3, PIE_A, ((-11, 43), (5, 31))),
    "Codo arriba, la otra mano empuja",
    guides=lambda j: aviso("Sin arquear la espalda"),
    alt="Estiramiento de tríceps con el codo arriba y la mano en la espalda")

DIB["est_flexor"] = solo(
    P((0, 104), -6, ((24, 129), (-26, 128)), ((14, 108), (-10, 106)),
      knee=(1, -1), foot=(90, 15)),
    "Rodilla en el tapete, cadera al frente",
    guides=lambda j: arrow((150, 104), (176, 104), 0) + nota(190, 92, "empuja")
                     + aviso("Aprieta el glúteo de atrás"),
    alt="Estiramiento del flexor de cadera en zancada con la rodilla en el tapete")

DIB["est_pantorrilla"] = solo(
    P((0, 92), 14, ((24, G), (-32, G)), (50, 74)),
    "Pie atrás, talón pegado al piso",
    fondo=wall(178, 26, G),
    guides=lambda j: aviso("Rodilla recta: gemelo · rodilla doblada: sóleo"),
    alt="Estiramiento de pantorrilla contra la pared con el pie atrás")

DIB["est_rodillas_pecho"] = solo(
    P((0, 124), -90, (14, 98), (-4, 100)),
    "Rodillas al pecho",
    fondo=mat(20, 200), piso=False,
    guides=lambda j: aviso("Suelta la espalda baja, respira lento"),
    alt="Estiramiento de espalda baja abrazando las rodillas al pecho")

DIB["est_torsion"] = solo(
    P((0, 108), 0, ((28, 120), (34, 112)), ((-34, 88), (34, 88)), knee=(1, 1)),
    "Rodillas a un lado, brazos abiertos",
    guides=lambda j: aviso("Visto desde arriba · los dos hombros en el piso"),
    piso=False, alt="Torsión de columna acostado con las rodillas hacia un lado")

DIB["est_mariposa"] = solo(
    P((0, 110), 8, ((-3, 127), (3, 127)), ((-10, 122), (10, 122)), knee=(-1, 1)),
    "Plantas juntas, rodillas afuera",
    fondo=mat(60, 194), piso=False,
    guides=lambda j: aviso("Visto de frente · no rebotes"),
    alt="Estiramiento de aductores en mariposa")

DIB["est_nino"] = solo(
    P((0, 116), 100, ((20, 128), (-2, 128)), (60, 129), knee=1, foot=(95, 95)),
    "Postura del niño",
    fondo=mat(40, 236), piso=False,
    guides=lambda j: aviso("Frente al tapete, brazos largos"),
    alt="Postura del niño con los brazos estirados al frente")

DIB["est_paloma"] = solo(
    P((0, 112), 34, ((26, 124), (-44, 128)), (34, 112), knee=(-1, -1), foot=(60, 30)),
    "Pierna de adelante cruzada",
    fondo=mat(30, 236), piso=False,
    guides=lambda j: aviso("Si molesta la rodilla, usa la figura 4 acostado"),
    alt="Postura de la paloma para el glúteo")

DIB["sentadilla_profunda"] = solo(
    P((0, 115), 38, (16, 129), (26, 102)),
    "Talones abajo, codos abriendo",
    guides=lambda j: aviso("Si no bajas, agárrate del marco de una puerta"),
    alt="Sentadilla profunda sostenida con los codos abriendo las rodillas")

DIB["est_costado"] = solo(
    P((0, 88), 22, ((-10, G), (6, G)), ((14, 44), (-14, 112))),
    "Brazo arriba, inclínate",
    guides=lambda j: aviso("Visto de frente · la cadera no se va al lado"),
    alt="Estiramiento del costado con el brazo arriba")

DIB["est_hombro"] = solo(
    P((0, 88), 0, ((-8, G), (8, G)), ((-24, 72), (-14, 76))),
    "Brazo cruzado al pecho",
    guides=lambda j: aviso("Visto de frente · el hombro no sube"),
    alt="Estiramiento de hombro con el brazo cruzado al pecho")

DIB["est_cuello"] = solo(
    P((0, 88), 0, ((-8, G), (8, G)), ((13, 46), (-11, 116)), head=24),
    "Oreja al hombro, la mano ayuda",
    guides=lambda j: aviso("Visto de frente · suave, sin jalones"),
    alt="Estiramiento de cuello y trapecio llevando la oreja al hombro")

DIB["respiracion"] = solo(
    P((0, 124), -90, (22, 128), (-18, 118)),
    "Una mano en el pecho, otra en la barriga",
    fondo=mat(20, 220), piso=False,
    guides=lambda j: aviso("Inhala 4 · aguanta 2 · exhala 6"),
    alt="Respiración acostado boca arriba con las rodillas dobladas")


# ══════════════════════════════════════════════════ correcciones de lectura
# Se redefinen los dibujos que no leian bien en la hoja de contacto.

DIB["aperturas"] = duo(
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-35, 60), (35, 60))),
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-6, 66), (6, 66))),
    "1 · Brazos abiertos", "2 · Junta arriba",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Estás acostado en el tapete. Los codos tocan el piso abajo."),
    piso=False, alt="Aperturas en el piso: los brazos abren y se juntan arriba")

DIB["pajaro"] = duo(
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-6, 74), (6, 74))),
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-36, 66), (36, 66))),
    "1 · Cuelgan juntas", "2 · Abre como alas",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Estás inclinado al frente con la espalda plana. Aprieta los omóplatos."),
    piso=False, alt="Pájaro: inclinado al frente se abren los brazos como alas")

DIB["curl"] = duo(
    P(PIE_H, 4, PIE_A, (6, 89)),
    P(PIE_H, 4, PIE_A, (22, 71)),
    "1 · Brazos estirados", "2 · Sube al pecho",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: aviso("El codo pegado a las costillas y quieto: solo sube el antebrazo"),
    alt="Curl de bíceps con barra: solo se mueve el antebrazo")

DIB["martillo"] = duo(
    P(PIE_H, 4, PIE_A, (7, 89)),
    P(PIE_H, 4, PIE_A, (21, 72)),
    "1 · Palmas enfrentadas", "2 · Sube",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Como si sostuvieras dos martillos: la muñeca no gira"),
    alt="Curl martillo con las palmas enfrentadas")

DIB["frances"] = duo(
    P((0, 104), 3, (21, 128), (2, 26)),
    P((0, 104), 3, (21, 128), (-21, 58)),
    "1 · Brazos estirados", "2 · Detrás de la cabeza",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    fondo=chair(30, 140) + chair(146, 140),
    guides=lambda a, b: aviso("Codos apuntando al techo y quietos: solo se mueve el antebrazo"),
    alt="Extensión de tríceps sobre la cabeza, sentado")

DIB["lateral"] = duo(
    P((0, 88), 0, ((-8, G), (8, G)), ((-11, 118), (11, 118))),
    P((0, 88), 0, ((-8, G), (8, G)), ((-35, 57), (35, 57))),
    "1 · A los lados", "2 · Altura del hombro",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Ni un centímetro más alto que el hombro. Sube como si derramaras agua."),
    alt="Elevación lateral vista de frente, hasta la altura del hombro")

DIB["elev_piernas"] = duo(
    P((0, 122), -90, (43, 124), (-14, 126)),
    P((0, 122), -90, (2, 80), (-14, 126)),
    "1 · Abajo, sin tocar", "2 · Piernas arriba",
    fondo=mat(14, 236), piso=False,
    guides=lambda a, b: aviso("Manos debajo de la cola. Abajo las piernas no tocan el piso."),
    alt="Elevación de piernas acostado, sin tocar el piso abajo")

DIB["encogimiento"] = duo(
    P((0, 88), 3, (0, G), (8, 94)),
    P((0, 82), 3, (0, 124), (8, 88)),
    "1 · Hombros sueltos", "2 · A las orejas",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: vline(206, "sube", 46, 70)
                        + aviso("Derecho hacia las orejas, sin rodar el hombro"),
    alt="Encogimiento de hombros: suben derecho hacia las orejas")

DIB["gato_camello"] = duo(
    P((0, 104), 90, (-26, 126), (36, 130), knee=-1, bow=-13),
    P((0, 104), 90, (-26, 126), (36, 130), knee=-1, bow=11),
    "1 · Gato: redondea", "2 · Camello: hunde",
    guides=lambda a, b: aviso("Lento, siguiendo la respiración"),
    alt="Gato y camello en cuatro apoyos: se redondea y se hunde la espalda")

DIB["flexion"] = duo(
    P((0, 96), 90, (-42, 126), (34, 129), elbow=-1, foot=200),
    P((0, 110), 90, (-42, 126), (34, 129), elbow=-1, foot=200),
    "1 · Arriba", "2 · Abajo",
    guides=lambda a, b: linea(a["ankle"], a["head"], "línea recta", 13)
                        + arc(b["elbow"], b["neck"], b["wrist"], "90°", 12),
    alt="Flexión de pecho: el cuerpo baja en línea recta hasta que el codo hace 90 grados")

DIB["flexion_rodillas"] = duo(
    P((0, 100), 90, (-30, 124), (34, 129), elbow=-1, foot=200),
    P((0, 112), 90, (-30, 124), (34, 129), elbow=-1, foot=200),
    "1 · Arriba", "2 · Abajo",
    guides=lambda a, b: aviso("Versión fácil: las rodillas en el piso, el cuerpo sigue recto")
                        + linea(a["knee"], a["head"], "", 0),
    alt="Flexión apoyando las rodillas en el piso")

DIB["est_triceps"] = solo(
    P((0, 86), 3, PIE_A, ((-13, 50), (-3, 33))), "Codo arriba, la otra mano empuja",
    guides=lambda j: aviso("El codo apunta al techo. Sin arquear la espalda."),
    alt="Estiramiento de tríceps con el codo arriba y la mano en la espalda")

DIB["est_mariposa"] = solo(
    P((0, 112), 8, ((-2, 126), (2, 126)), ((-9, 120), (9, 120)), knee=(-1, 1)),
    "Plantas juntas, rodillas afuera",
    fondo=mat(60, 194), piso=False,
    guides=lambda j: aviso("Visto de frente · deja caer las rodillas, no rebotes"),
    alt="Estiramiento de aductores en mariposa")

DIB["est_torsion"] = solo(
    P((0, 100), 0, ((30, 118), (36, 110)), ((-36, 70), (36, 70)), knee=(1, 1)),
    "Rodillas a un lado, brazos abiertos",
    guides=lambda j: aviso("Visto desde arriba · los dos hombros pegados al piso"),
    piso=False, alt="Torsión de columna acostado con las rodillas hacia un lado")

DIB["est_nino"] = solo(
    P((0, 116), 98, ((22, 128), (18, 128)), (62, 129), knee=1, foot=(95, 95)),
    "Postura del niño",
    fondo=mat(40, 236), piso=False,
    guides=lambda j: aviso("La frente al tapete, los brazos largos al frente"),
    alt="Postura del niño con los brazos estirados al frente")

DIB["sumo_aire"] = duo(
    P((0, 88), 0, ((-22, G), (22, G)), (0, 112), knee=(-1, 1)),
    P((0, 109), 4, ((-24, G), (24, G)), (0, 122), knee=(-1, 1)),
    "1 · Pies abiertos", "2 · Abajo",
    guides=lambda a, b: aviso("Visto de frente · puntas hacia afuera, rodillas siguen a los pies"),
    alt="Sentadilla sumo al aire vista de frente")

DIB["peso_muerto_rumano"] = duo(
    hinge_up, hinge_dn, "1 · De pie", "2 · Cadera atrás",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: hline(119, "la barra baja a media canilla", 120, 242)
                        + linea(b["neck"], b["hip"], "espalda plana", 15)
                        + arrow((152, 92), (130, 92), 0),
    alt="Peso muerto rumano: de pie y con la cadera echada atrás, espalda plana")

DIB["bisagra"] = duo(
    hinge_up, hinge_dn, "1 · De pie", "2 · Cadera atrás",
    guides=lambda a, b: aviso("Rodillas casi rectas. La cadera va atrás, no bajas doblando la espalda.")
                        + linea(b["neck"], b["hip"], "", 0),
    alt="Bisagra de cadera sin peso")

DIB["remo_barra"] = duo(
    row_dn, row_up, "1 · Brazos estirados", "2 · Al ombligo",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: linea(b["neck"], b["hip"], "torso a 45°", 15)
                        + arrow((198, 114), (198, 98), 0)
                        + aviso("El codo va hacia atrás, no hacia afuera"),
    alt="Remo inclinado con barra: se jala hasta el ombligo con los codos hacia atrás")


# ── segunda ronda de correcciones: etiquetas que se montaban entre si ──

DIB["aperturas"] = duo(
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-35, 60), (35, 60))),
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-14, 44), (14, 44))),
    "1 · Abiertos", "2 · Junta arriba",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Estás acostado en el tapete. Abajo los codos tocan el piso."),
    piso=False, alt="Aperturas en el piso: los brazos abren y se juntan arriba")

DIB["pajaro"] = duo(
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-11, 82), (11, 82))),
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-36, 66), (36, 66))),
    "1 · Cuelgan", "2 · Abre como alas",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Estás inclinado al frente con la espalda plana. Aprieta los omóplatos."),
    piso=False, alt="Pájaro: inclinado al frente se abren los brazos como alas")

DIB["frances"] = duo(
    P((0, 104), 3, (21, 128), (2, 26)),
    P((0, 104), 3, (21, 128), (-24, 62)),
    "1 · Estirado", "2 · Atrás de la cabeza",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    fondo=chair(30, 140) + chair(146, 140),
    guides=lambda a, b: aviso("Codos apuntando al techo y quietos: solo se mueve el antebrazo"),
    alt="Extensión de tríceps sobre la cabeza, sentado")

DIB["est_mariposa"] = solo(
    P((0, 106), 8, ((-3, 128), (3, 128)), ((-9, 124), (9, 124)), knee=(-1, 1)),
    "Plantas juntas",
    fondo=mat(60, 194), piso=False,
    guides=lambda j: aviso("Visto de frente · deja caer las rodillas, no rebotes"),
    alt="Estiramiento de aductores en mariposa")

DIB["est_torsion"] = solo(
    P((0, 100), 0, ((32, 112), (37, 104)), ((-36, 70), (36, 70)), knee=(1, 1)),
    "Rodillas a un lado",
    fondo=mat(88, 162), piso=False,
    guides=lambda j: aviso("Acostado, visto desde arriba · los dos hombros pegados al piso"),
    alt="Torsión de columna acostado con las rodillas hacia un lado")

DIB["est_nino"] = solo(
    P((0, 114), 92, ((24, 128), (20, 128)), (64, 128), knee=1, foot=(95, 95)),
    "Postura del niño",
    fondo=mat(40, 236), piso=False,
    guides=lambda j: aviso("La frente al tapete, los brazos largos al frente"),
    alt="Postura del niño con los brazos estirados al frente")

DIB["peso_muerto_rumano"] = duo(
    hinge_up, hinge_dn, "1 · De pie", "2 · Cadera atrás",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: hline(119, "media canilla", 150, 244)
                        + aviso("Rodillas casi rectas · la espalda queda plana todo el rato")
                        + arrow((152, 90), (130, 90), 0),
    alt="Peso muerto rumano: de pie y con la cadera echada atrás, espalda plana")

DIB["remo_barra"] = duo(
    row_dn, row_up, "1 · Estirados", "2 · Al ombligo",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: aviso("Torso a 45°, espalda plana. El codo va hacia atrás, no hacia afuera.")
                        + arrow((214, 116), (214, 100), 0),
    alt="Remo inclinado con barra: se jala hasta el ombligo con los codos hacia atrás")

DIB["press_piso"] = duo(
    P((0, 122), -90, (22, 128), (-22, 112)),
    P((0, 122), -90, (22, 128), (-32, 88)),
    "1 · Codo en el piso", "2 · Estira",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("El piso frena el recorrido: cuando el codo toca, empujas. Cuida el hombro."),
    fondo=mat(14, 236), piso=False,
    alt="Press de pecho en el piso: se baja hasta que el codo toca y se empuja arriba")

DIB["press_hombro"] = duo(
    P((0, 104), 3, (21, 128), (17, 78)),
    P((0, 104), 3, (21, 128), (6, 42)),
    "1 · Al hombro", "2 · Estira arriba",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    fondo=chair(30, 140) + chair(146, 140),
    guides=lambda a, b: aviso("Sentado, espalda pegada al espaldar: así no arqueas la lumbar"),
    alt="Press de hombro sentado en la silla con la espalda apoyada")

DIB["remo_1brazo"] = duo(
    P((-6, 90), 72, (0, G), ((25, 117), (14, 104))),
    P((-6, 90), 72, (0, G), ((10, 100), (14, 104))),
    "1 · Cuelga", "2 · A la cadera",
    eq=lambda a, b: db(a["wrist_n"]) + db(b["wrist_n"]),
    guides=lambda a, b: aviso("El antebrazo libre se apoya sobre tu propio muslo y sostiene la espalda"),
    alt="Remo a un brazo apoyando el antebrazo libre sobre el propio muslo")

DIB["zancada_inversa"] = duo(
    lunge_up, lunge_dn, "1 · De pie", "2 · Paso atrás",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: arc(b["knee_n"], b["hip"], b["ankle_n"], "90°", 14)
                        + aviso("La rodilla de atrás casi toca el piso. El peso vive en la pierna de adelante."),
    alt="Zancada inversa: de pie y abajo con la rodilla de atrás cerca del piso")

DIB["sentadilla_dividida"] = duo(
    P((0, 90), 6, ((14, G), (-28, 126)), (5, 96), knee=(1, -1), foot=(90, 25)),
    lunge_dn, "1 · Pies fijos", "2 · Abajo",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Los dos pies en el piso, no caminas: bajas y subes en el mismo sitio"),
    alt="Sentadilla dividida: los dos pies en el piso, se baja en el sitio")

DIB["sentadilla_goblet"] = duo(
    sq_arr, sq_abj, "1 · De pie", "2 · Abajo",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    guides=lambda a, b: hline(b["hip"][1], "muslo paralelo", 152, 244)
                        + aviso("La rodilla sigue la línea del pie. La espalda no se redondea."),
    alt="Sentadilla goblet con mancuerna al pecho, arriba y abajo")

DIB["sentadilla_aire"] = duo(
    P(PIE_H, 8, PIE_A, (30, 84)), P((0, 107), 45, (16, 129), (34, 96)),
    "1 · De pie", "2 · Abajo",
    guides=lambda a, b: hline(b["hip"][1], "muslo paralelo", 152, 244)
                        + aviso("Baja hasta que el muslo quede paralelo al piso"),
    alt="Sentadilla al aire: de pie y posición abajo con el muslo paralelo al piso")

DIB["muerto_bicho"] = duo(
    P((0, 122), -90, ((24, 102), (44, 122)), ((-32, 88), (-32, 88)), knee=(1, 1)),
    P((0, 122), -90, ((24, 102), (44, 122)), ((-32, 88), (-60, 108)), knee=(1, 1)),
    "1 · Todo a 90°", "2 · Contrarios",
    fondo=mat(14, 236), piso=False,
    guides=lambda a, b: aviso("La espalda baja no se despega del piso. Si se arquea, estira menos."),
    alt="Muerto bicho: se estiran brazo y pierna contrarios sin arquear la espalda")

DIB["superman"] = duo(
    P((0, 124), -90, (38, 126), (-58, 122), bow=-2),
    P((0, 122), -82, (40, 106), (-62, 98), bow=-7),
    "1 · Boca abajo", "2 · Sube todo",
    fondo=mat(14, 118) + mat(130, 236), piso=False,
    guides=lambda a, b: aviso("Suben brazos, pecho y piernas a la vez · 2 s arriba, baja lento"),
    alt="Superman: boca abajo se suben brazos, pecho y piernas a la vez")

DIB["salto"] = duo(
    P((0, 106), 38, (14, 129), (-18, 106)),
    P((0, 68), 4, ((-3, 106), (4, 108)), ((10, 40), (-8, 42))),
    "1 · Carga abajo", "2 · Salta",
    guides=lambda a, b: aviso("Cae suave, la rodilla blanda · si molesta, cámbialo por sentadilla rápida"),
    alt="Sentadilla con salto: se carga abajo y se despega del piso")

DIB["est_triceps"] = solo(
    P((0, 86), 3, PIE_A, ((-15, 52), (-5, 34)), elbow=(1, -1)),
    "Codo arriba",
    guides=lambda j: aviso("El codo apunta al techo, la otra mano empuja. Sin arquear la espalda."),
    alt="Estiramiento de tríceps con el codo arriba y la mano en la espalda")

DIB["sumo"] = duo(
    P((0, 88), 0, ((-22, G), (22, G)), (0, 112), knee=(-1, 1)),
    P((0, 106), 4, ((-24, G), (24, G)), (0, 120), knee=(-1, 1)),
    "1 · Pies abiertos", "2 · Abajo",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    guides=lambda a, b: aviso("Visto de frente · puntas hacia afuera y las rodillas se abren hacia ellas"),
    alt="Sentadilla sumo vista de frente, pies muy abiertos y puntas hacia afuera")

DIB["sumo_aire"] = duo(
    P((0, 88), 0, ((-22, G), (22, G)), (0, 112), knee=(-1, 1)),
    P((0, 106), 4, ((-24, G), (24, G)), (0, 120), knee=(-1, 1)),
    "1 · Pies abiertos", "2 · Abajo",
    guides=lambda a, b: aviso("Visto de frente · puntas hacia afuera, las rodillas siguen a los pies"),
    alt="Sentadilla sumo al aire vista de frente")

DIB["press_militar"] = DIB["press_hombro"]


# ── tercera ronda: superposiciones finas ──

DIB["aperturas"] = duo(
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-35, 60), (35, 60))),
    P((0, 92), 0, ((-8, 136), (8, 136)), ((-21, 40), (21, 40))),
    "1 · Abiertos", "2 · Junta arriba",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("Estás acostado en el tapete. Abajo los codos tocan el piso."),
    piso=False, alt="Aperturas en el piso: los brazos abren y se juntan arriba")

DIB["est_mariposa"] = solo(
    P((0, 100), 8, ((-6, 132), (6, 132)), ((-13, 124), (13, 124)), knee=(-1, 1)),
    "Plantas juntas",
    fondo=mat(66, 188, 134), piso=False,
    guides=lambda j: aviso("Visto de frente · deja caer las rodillas, no rebotes"),
    alt="Estiramiento de aductores en mariposa")

DIB["est_torsion"] = solo(
    P((0, 122), -90, ((28, 126), (32, 118)), ((-30, 98), (-36, 128))),
    "Rodillas a un lado",
    fondo=mat(20, 220), piso=False,
    guides=lambda j: arrow((168, 112), (192, 124), -8)
                     + aviso("Las rodillas caen a un lado y los dos hombros siguen pegados al piso"),
    alt="Torsión de columna acostado con las rodillas hacia un lado")

DIB["salto"] = duo(
    P((0, 106), 38, (14, 129), (-18, 106)),
    P((0, 72), 3, ((0, 114), (3, 116)), ((9, 41), (-5, 43))),
    "1 · Carga abajo", "2 · Salta",
    guides=lambda a, b: aviso("Cae suave, la rodilla blanda · si molesta, hazla sin salto"),
    alt="Sentadilla con salto: se carga abajo y se despega del piso")

DIB["sentadilla_goblet"] = duo(
    sq_arr, sq_abj, "1 · De pie", "2 · Abajo",
    eq=lambda a, b: db(a["wrist"]) + db(b["wrist"]),
    guides=lambda a, b: hline(b["hip"][1], "paralelo", 196, 244)
                        + aviso("La rodilla sigue la línea del pie. La espalda no se redondea."),
    alt="Sentadilla goblet con mancuerna al pecho, arriba y abajo")

DIB["sentadilla_aire"] = duo(
    P(PIE_H, 8, PIE_A, (30, 84)), P((0, 107), 45, (16, 129), (34, 96)),
    "1 · De pie", "2 · Abajo",
    guides=lambda a, b: hline(b["hip"][1], "paralelo", 196, 244)
                        + aviso("Baja hasta que el muslo quede paralelo al piso"),
    alt="Sentadilla al aire: de pie y posición abajo con el muslo paralelo al piso")

DIB["zancada_inversa"] = duo(
    lunge_up, lunge_dn, "1 · De pie", "2 · Paso atrás",
    eq=lambda a, b: db(a["wrist_n"]) + db(a["wrist_f"]) + db(b["wrist_n"]) + db(b["wrist_f"]),
    guides=lambda a, b: aviso("La rodilla de atrás casi toca el piso. El peso vive en la pierna de adelante."),
    alt="Zancada inversa: de pie y abajo con la rodilla de atrás cerca del piso")


DIB["talones_aire"] = duo(
    P(PIE_H, 3, (0, G), (8, 92)),
    P((0, 75), 3, (0, 119), (8, 81), foot=48),
    "1 · Talón abajo", "2 · Lo más alto",
    guides=lambda a, b: vline(206, "sube", 82, 116)
                        + aviso("Sin peso, para calentar · 1 s arriba, baja lento"),
    alt="Elevación de talones sin peso")


DIB["peso_muerto_rumano"] = duo(
    hinge_up, hinge_dn, "1 · De pie", "2 · Cadera atrás",
    eq=lambda a, b: bar(a["wrist"]) + bar(b["wrist"]),
    guides=lambda a, b: hline(119, "", 150, 244)
                        + aviso("Rodillas casi rectas · la cadera va atrás y la espalda queda plana")
                        + arrow((152, 90), (130, 90), 0),
    alt="Peso muerto rumano: de pie y con la cadera echada atrás, espalda plana")
