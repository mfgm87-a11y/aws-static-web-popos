# -*- coding: utf-8 -*-
"""Ficha de cada ejercicio: dibujo, cadencia, versión fácil y error común.

Se enlaza con las rutinas por coincidencia de texto en el nombre, así que
el orden importa: lo más específico va primero.

  fig    clave del dibujo en dibujos.DIB
  cad    cadencia "baja-pausa-sube" en segundos
  hasta  hasta dónde llega el movimiento
  facil  cómo hacerlo más fácil
  error  el error que casi todo el mundo comete
  cat    categoría para el generador aleatorio
  reps   repeticiones por defecto cuando lo arma el generador
  carga  carga por defecto
"""

def f(pat, fig, cat=None, cad=None, hasta=None, facil=None, error=None,
      reps=None, carga=None, nombre=None):
    return (pat.lower(), dict(fig=fig, cat=cat, cad=cad, hasta=hasta, facil=facil,
                              error=error, reps=reps, carga=carga, nombre=nombre))


FICHAS = [

# ─────────────────────────────────────────── pierna · dominante de rodilla
f("sentadilla goblet", "sentadilla_goblet", "pierna_rodilla", "3-1-1",
  "Hasta que el muslo quede paralelo al piso",
  "Baja solo hasta media sentadilla, o hazla sin peso",
  "Dejar que la rodilla se meta hacia adentro al subir",
  "12 reps", "1 mancuerna · 7,5 kg", "Sentadilla goblet"),

f("sentadilla al aire", "sentadilla_aire", "calent", "2-0-1",
  "Muslo paralelo al piso", None, None, "15 reps", None, "Sentadilla al aire"),

f("sentadilla sumo con", "sumo", "pierna_rodilla", "2-1-1",
  "Hasta que el muslo quede paralelo",
  "Menos peso y pies un poco menos abiertos",
  "Dejar que las rodillas se cierren hacia adentro",
  "15 reps", "1 mancuerna · 7,5 kg", "Sentadilla sumo"),

f("sentadilla sumo al aire", "sumo_aire", "calent", "2-0-1",
  "Muslo paralelo", None, None, "15 reps", None, "Sentadilla sumo al aire"),

f("sentadilla dividida", "sentadilla_dividida", "pierna_rodilla", "3-0-1",
  "La rodilla de atrás casi toca el piso",
  "Sin peso, tocando la pared con una mano",
  "Dar un paso muy corto: la rodilla de adelante se pasa del pie",
  "10 por pierna", "2 mancuernas · 7,5 kg", "Sentadilla dividida"),

f("zancada inversa", "zancada_inversa", "pierna_rodilla", "2-0-1",
  "La rodilla de atrás casi toca el piso",
  "Sin peso, o agarrándote de algo firme",
  "Inclinar el torso al frente en vez de bajar recto",
  "10 por pierna", "2 mancuernas · 7,5 kg", "Zancada inversa"),

f("zancada en el sitio con rotación", "zancada_rotacion", "calent", None,
  None, None, None, "6 por pierna", None, "Zancada con rotación"),
f("zancada con rotación", "zancada_rotacion", "calent", None,
  None, None, None, "6 por lado", None, "Zancada con rotación"),

f("sentadilla con salto", "salto", "hiit", None,
  "Los pies despegan del piso",
  "Sentadilla rápida sin salto",
  "Caer con la rodilla rígida", "10 reps", None, "Sentadilla con salto"),

f("sentadilla frontal", "sentadilla_goblet", None, "2-0-1",
  "Muslo paralelo, codos arriba", None,
  "Dejar caer los codos: la barra se va al frente", "6 reps", None, "Sentadilla frontal"),

f("sentadilla profunda", "sentadilla_profunda", "estiram", None,
  "Lo más abajo que llegues con los talones pegados", None, None,
  "90 s", None, "Sentadilla profunda sostenida"),

# ─────────────────────────────────────────── pierna · dominante de cadera
f("peso muerto rumano", "peso_muerto_rumano", "pierna_cadera", "3-0-1",
  "A media canilla, o donde sientas el estirón atrás del muslo",
  "Sin peso frente al espejo hasta que salga solo",
  "Doblar la espalda en vez de la cadera",
  "12 reps", "Barra · ~19 kg", "Peso muerto rumano"),

f("peso muerto a una pierna", "peso_muerto_1p", "pierna_cadera", "3-0-1",
  "Hasta donde controles sin torcer la cadera",
  "Roza la pared con la mano libre",
  "Abrir la cadera hacia el lado al bajar",
  "8 por pierna", "1 mancuerna · 7,5 kg", "Peso muerto a una pierna"),

f("bisagra de cadera", "bisagra", "calent", "2-0-1",
  "Hasta sentir el estirón atrás del muslo", None, None,
  "15 reps", None, "Bisagra de cadera"),

f("peso muerto", "peso_muerto_rumano", None, "2-0-1",
  "La barra baja al piso", None,
  "Levantar con la espalda en vez de con las piernas", "6 reps", None, "Peso muerto"),

f("buenos días", "bisagra", None, "2-0-1",
  "Torso hasta la horizontal", None,
  "Bajar más de lo que la espalda aguanta plana", "6 reps", None, "Buenos días"),

f("puente de glúteo con peso", "puente_gluteo", "pierna_acc", "2-2-1",
  "Hasta alinear rodillas, cadera y hombros",
  "Sin peso", "Empujar con la espalda baja en vez del glúteo",
  "15 reps", "1 mancuerna sobre la cadera", "Puente de glúteo con peso"),

f("puente de glúteo", "puente_gluteo", "calent", "2-2-1",
  "Línea recta de rodillas a hombros", None, None, "15 reps", None, "Puente de glúteo"),

f("almeja", "almeja", "calent", None, None, None, None,
  "12 por lado", None, "Almeja"),

f("balanceo de pierna", "balanceo_pierna", "calent", None, None, None, None,
  "10 por pierna", None, "Balanceo de pierna"),

# ─────────────────────────────────────────── pantorrilla
f("elevación de talones de pie", "talones", "pierna_acc", "3-1-1",
  "Lo más alto que llegues sobre las puntas",
  "Sin peso", "Rebotar abajo en vez de subir hasta el tope",
  "20 reps", "2 mancuernas · 9,5 kg", "Elevación de talones"),

f("elevación de talones", "talones_aire", "calent", "2-1-1",
  "Hasta el tope", None, None, "20 reps", None, "Elevación de talones sin peso"),

# ─────────────────────────────────────────── empuje
f("press de pecho en el piso", "press_piso", "empuje", "3-0-1",
  "Hasta que el codo toque el piso",
  "Con una sola mancuerna a la vez, o sin peso",
  "Abrir los codos a 90°: eso castiga el hombro",
  "10 reps", "2 mancuernas · 7,5 kg", "Press de pecho en el piso"),

f("press cerrado en el piso", "press_cerrado", "empuje", "3-0-1",
  "Hasta que el tríceps toque el piso",
  "Menos peso: este pesa más de lo que parece",
  "Dejar que los codos se abran", "12 reps", "2 mancuernas · 7,5 kg",
  "Press cerrado en el piso"),

f("aperturas en el piso", "aperturas", "empuje", "3-0-2",
  "Hasta que los codos toquen el piso",
  "Menos peso todavía, nunca más de 5 kg",
  "Estirar el codo del todo: el hombro se lleva la carga",
  "12 reps", "2 mancuernas · 5 kg", "Aperturas en el piso"),

f("pullover", "pullover", "empuje", "3-0-2",
  "Hasta sentir el estirón en las costillas",
  "Menos recorrido",
  "Arquear la espalda baja para llegar más atrás",
  "12 reps", "1 mancuerna · 7,5 kg", "Pullover con mancuerna"),

f("flexión con manos elevadas", "flexion_manos_altas", "empuje", "3-0-1",
  "El pecho toca el borde",
  "Pon las manos en algo más alto",
  "Dejar caer la cadera", "12 reps", "Manos en el borde del sofá",
  "Flexión con manos elevadas"),

f("flexiones de rodillas", "flexion_rodillas", "calent", "2-0-1",
  "El pecho casi toca el piso", None, None, "10 reps", None, "Flexiones de rodillas"),

f("flexiones", "flexion", "hiit", "2-0-1",
  "El pecho casi toca el piso",
  "Apoya las rodillas en el piso",
  "Bajar solo la cabeza y dejar la cadera arriba", "8 reps", None, "Flexiones"),

f("flexión", "flexion", "empuje", "3-0-1",
  "El pecho casi toca el piso",
  "Apoya las rodillas, o pon las manos en el sofá",
  "Dejar caer la cadera o sacar el culo", "10 reps", None, "Flexión"),

f("press de hombro sentado", "press_hombro", "empuje", "2-0-1",
  "Hasta estirar los brazos arriba",
  "Menos peso, o una mancuerna a la vez",
  "Arquear la espalda baja para empujar",
  "10 reps", "2 mancuernas · 7,5 kg", "Press de hombro sentado"),

f("press militar", "press_militar", "empuje", "2-0-1",
  "Hasta estirar arriba", "Hazlo sentado con la espalda apoyada",
  "Arquear la lumbar", "10 reps", "2 mancuernas · 5 kg", "Press militar"),

f("press de hombro", "press_hombro", None, "2-0-1",
  "Hasta estirar arriba", None, "Arquear la espalda", "6 reps", None, "Press de hombro"),

# ─────────────────────────────────────────── jalón
f("remo inclinado con barra", "remo_barra", "jalon", "2-1-1",
  "La barra llega al ombligo",
  "Menos peso, torso un poco más alto",
  "Jalar con los brazos en vez de con la espalda",
  "12 reps", "Barra · ~19 kg", "Remo inclinado con barra"),

f("remo inclinado", "remo_barra", None, "2-1-1",
  "Al ombligo", None, "Redondear la espalda", "6 reps", None, "Remo inclinado"),

f("remo a un brazo", "remo_1brazo", "jalon", "2-1-1",
  "El codo llega a la cadera",
  "Menos peso y más apoyo en el muslo",
  "Girar el torso para jalar más", "10 por lado", "1 mancuerna · 7,5 kg",
  "Remo a un brazo"),

f("pájaro", "pajaro", "jalon", "2-1-2",
  "Hasta la altura del hombro, no más",
  "Sin peso las primeras semanas",
  "Usar tanto peso que lo jalas con la espalda",
  "15 reps", "2 mancuernas · 2,5 kg", "Pájaro"),

f("encogimiento de hombros con barra", "encogimiento", "jalon", "1-1-1",
  "Los hombros suben derecho hacia las orejas",
  "Con mancuernas en vez de barra",
  "Rodar el hombro en círculo", "15 reps", "Barra · ~19 kg",
  "Encogimiento de hombros"),

f("encogimiento de hombros", "encogimiento", "calent", None,
  None, None, None, "15 reps", None, "Encogimiento sin peso"),

f("cargada al pecho", "remo_barra", None, None,
  "La barra termina al frente de los hombros",
  "Cámbiala por remo alto", "Jalar con los brazos en vez de con la cadera",
  "6 reps", None, "Cargada al pecho"),

f("y–t–w", "ytw", "calent", None, None, None, None, "8 de cada letra", None, "Y–T–W"),

# ─────────────────────────────────────────── brazo
f("curl de bíceps", "curl", "brazo", "3-0-1",
  "Hasta el pecho, sin balancear",
  "Menos peso o solo con las mancuernas",
  "Balancear la espalda para subir la barra",
  "12 reps", "Barra · ~19 kg", "Curl de bíceps"),

f("curl martillo", "martillo", "brazo", "3-0-1",
  "Hasta el pecho",
  "Un brazo a la vez",
  "Girar la muñeca al subir", "12 reps", "2 mancuernas · 7,5 kg", "Curl martillo"),

f("extensión de tríceps sobre la cabeza", "frances", "brazo", "3-0-1",
  "Hasta sentir el estirón atrás del brazo",
  "Menos peso: el codo manda aquí",
  "Abrir los codos hacia afuera", "12 reps", "1 mancuerna · 7,5 kg",
  "Extensión de tríceps sobre la cabeza"),

f("patada de tríceps", "patada_triceps", "brazo", "2-1-1",
  "Hasta estirar el brazo del todo",
  "Menos peso", "Mover el codo en vez del antebrazo",
  "15 por brazo", "1 mancuerna · 7,5 kg", "Patada de tríceps"),

f("elevación lateral", "lateral", "brazo", "2-1-2",
  "Hasta la altura del hombro, ni un centímetro más",
  "Sin peso, solo con el brazo",
  "Subir por encima del hombro o ayudarse con un impulso",
  "12 reps", "2 mancuernas · 2,5 kg", "Elevación lateral"),

f("rotación externa de hombro", "rot_externa", "calent", None,
  None, None, None, "15 por lado", None, "Rotación externa de hombro"),

# ─────────────────────────────────────────── core
f("plancha con toque de hombro", "plancha_toque", "core", None,
  "Tocas el hombro sin que la cadera se mueva",
  "Abre más los pies",
  "Dejar que la cadera rote al tocar", "10 por lado", None,
  "Plancha con toque de hombro"),

f("plancha lateral", "plancha_lateral", "core", None,
  "Cadera arriba, cuerpo en línea",
  "Apoya la rodilla de abajo",
  "Dejar caer la cadera", "30 s por lado", None, "Plancha lateral"),

f("plancha", "plancha", "core", None,
  "Línea recta de talones a cabeza",
  "Apoya las rodillas, o menos tiempo",
  "Hundir la cadera o subir el culo", "40 s", None, "Plancha"),

f("muerto bicho", "muerto_bicho", "core", "3-0-3",
  "Hasta donde la espalda baja siga pegada al piso",
  "Mueve solo los brazos, o solo las piernas",
  "Dejar que la espalda se arquee", "10 por lado", None, "Muerto bicho"),

f("elevación de piernas", "elev_piernas", "core", "3-0-2",
  "Suben a la vertical, bajan sin tocar el piso",
  "Dobla las rodillas",
  "Arquear la espalda al bajar", "12 reps", None, "Elevación de piernas"),

f("giro ruso", "giro_ruso", "core", None,
  "Tocas el piso al lado de la cadera",
  "Apoya los pies en el piso", "Girar solo los brazos",
  "20 (10 por lado)", "1 disco · 1 kg", "Giro ruso"),

f("bicicleta", "bicicleta", "core", None,
  "Codo hacia la rodilla contraria",
  "Más lento", "Jalarse el cuello con las manos", "30 s", None, "Bicicleta"),

f("superman", "superman", "core", "1-2-1",
  "Unos centímetros, no más",
  "Sube solo los brazos, o solo las piernas",
  "Tirar la cabeza atrás", "15 reps", None, "Superman"),

f("perro-pájaro", "perro_pajaro", "core", "1-2-1",
  "Brazo y pierna a la horizontal",
  "Mueve solo un brazo o solo una pierna",
  "Ladear la cadera", "10 por lado", None, "Perro-pájaro"),

f("escaladores", "escalador", "hiit", None,
  "La rodilla llega al pecho", "Más lento",
  "Rebotar la cadera arriba y abajo", "20 (10 por pierna)", None, "Escaladores"),

f("hollow", "muerto_bicho", "core", None, None, None, None, "30 s", None, "Hollow"),

# ─────────────────────────────────────────── calentamiento y movilidad
f("marcha en el sitio", "marcha", "calent", None,
  "La rodilla llega a la altura de la cadera", None, None, "45 s", None,
  "Marcha en el sitio"),
f("marcha", "marcha", "calent", None, None, None, None, "30 s", None, "Marcha con rodilla alta"),
f("parado en un pie", "un_pie", "calent", None, None, None, None,
  "30 s por pierna", None, "Parado en un pie"),
f("gato–camello", "gato_camello", "calent", None, None, None, None, "10 reps", None, "Gato–camello"),
f("gato-camello", "gato_camello", "calent", None, None, None, None, "10 reps", None, "Gato–camello"),
f("círculos de cadera", "circulos_cadera", "calent", None, None, None, None,
  "10 por lado", None, "Círculos de cadera"),
f("abre el libro", "abre_libro", "calent", None, None, None, None, "8 por lado", None, "Abre el libro"),
f("rotación torácica", "abre_libro", "calent", None, None, None, None, "8 por lado", None, "Abre el libro"),
f("perro boca abajo a plancha", "perro_plancha", "calent", None, None, None, None,
  "8 reps", None, "Perro boca abajo a plancha"),

# ─────────────────────────────────────────── estiramientos
f("cuádriceps de pie", "est_cuadriceps", "estiram", None, None, None, None,
  "40 s por pierna", None, "Cuádriceps de pie"),
f("cuádriceps", "est_cuadriceps", "estiram", None, None, None, None,
  "40 s por pierna", None, "Cuádriceps de pie"),
f("pecho en el marco", "est_pecho_puerta", "estiram", None, None, None, None,
  "40 s por lado", None, "Pecho en el marco de la puerta"),
f("pecho en el piso", "est_pecho_puerta", "estiram", None, None, None, None,
  "40 s por lado", None, "Pecho estirado en el piso"),
f("isquios: pie adelante", "est_isquios_pie", "estiram", None, None, None, None,
  "40 s por pierna", None, "Isquios de pie"),
f("isquios de pie", "est_isquios_pie", "estiram", None, None, None, None,
  "40 s por pierna", None, "Isquios de pie"),
f("isquios sentado", "est_isquios_sentado", "estiram", None, None, None, None,
  "30 s por pierna", None, "Isquios sentado"),
f("isquios", "est_isquios_sentado", "estiram", None, None, None, None,
  "30 s por pierna", None, "Isquios sentado"),
f("glúteo sentado", "est_gluteo", "estiram", None, None, None, None,
  "40 s por lado", None, "Glúteo en figura 4"),
f("glúteo medio", "est_gluteo", "estiram", None, None, None, None,
  "40 s por lado", None, "Glúteo en figura 4"),
f("paloma", "est_paloma", "estiram", None, None, None, None,
  "90 s por lado", None, "Paloma"),
f("tríceps: codo arriba", "est_triceps", "estiram", None, None, None, None,
  "30 s por brazo", None, "Tríceps"),
f("tríceps y hombro", "est_hombro", "estiram", None, None, None, None,
  "30 s por brazo", None, "Hombro cruzado"),
f("flexor de cadera", "est_flexor", "estiram", None, None, None, None,
  "40 s por lado", None, "Flexor de cadera"),
f("pantorrilla contra la pared", "est_pantorrilla", "estiram", None, None, None, None,
  "45 s por pierna", None, "Pantorrilla contra la pared"),
f("sóleo", "est_pantorrilla", "estiram", None, None, None, None,
  "30 s por pierna", None, "Sóleo"),
f("espalda baja", "est_rodillas_pecho", "estiram", None, None, None, None,
  "45 s", None, "Rodillas al pecho"),
f("rodillas al pecho", "est_rodillas_pecho", "estiram", None, None, None, None,
  "45 s", None, "Rodillas al pecho"),
f("torsión de columna", "est_torsion", "estiram", None, None, None, None,
  "30 s por lado", None, "Torsión de columna"),
f("torsión", "est_torsion", "estiram", None, None, None, None,
  "30 s por lado", None, "Torsión de columna"),
f("aductor", "est_mariposa", "estiram", None, None, None, None, "45 s", None, "Mariposa"),
f("mariposa", "est_mariposa", "estiram", None, None, None, None, "45 s", None, "Mariposa"),
f("postura del niño", "est_nino", "estiram", None, None, None, None, "45 s", None, "Postura del niño"),
f("cuello y trapecio", "est_cuello", "estiram", None, None, None, None,
  "30 s por lado", None, "Cuello y trapecio"),
f("hombro: brazo cruzado", "est_hombro", "estiram", None, None, None, None,
  "30 s por lado", None, "Hombro cruzado"),
f("costado", "est_costado", "estiram", None, None, None, None,
  "30 s por lado", None, "Costado"),
f("dorsal", "est_costado", "estiram", None, None, None, None,
  "30 s por lado", None, "Dorsal"),
f("respiración", "respiracion", "estiram", None, None, None, None, "1 min", None, "Respiración"),
f("inhala", "respiracion", None, None, None, None, None, None, None, None),
]


def buscar(nombre):
    """Devuelve la ficha del ejercicio, o None."""
    n = (nombre or "").lower()
    for pat, datos in FICHAS:
        if pat in n:
            return datos
    return None


def catalogo():
    """Ejercicios que el generador aleatorio puede usar, por categoría."""
    vistos, out = set(), {}
    for pat, d in FICHAS:
        if not d["cat"] or not d["nombre"]:
            continue
        clave = (d["cat"], d["nombre"])
        if clave in vistos:
            continue
        vistos.add(clave)
        out.setdefault(d["cat"], []).append(d)
    return out
