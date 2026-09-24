# -*- coding: utf-8 -*-
"""Contenido de las secciones de Abdominales y Pecho."""


def w(nombre, mins, note, items, tag="Seguido"):
    return dict(kind="warm", name=nombre, mins=mins, note=note, items=items, tag=tag)


def c(nombre, mins, rondas, rest, tag, note, items, timers=None):
    return dict(kind="work", name=nombre, mins=mins, rounds=rondas, rest=rest,
                tag=tag, note=note, items=items, timers=timers)


def s(nombre, mins, note, items):
    return dict(kind="cool", name=nombre, mins=mins, note=note, items=items,
                tag="Sostenido")


def e(n, d, load=None, code=None):
    return dict(n=n, d=d, load=load, code=code, how=None)


# ══════════════════════════════════════════════════════════ ABDOMINALES

ABD_VERDAD = [
  ("No se puede quemar grasa de un sitio en particular.",
   "Mil abdominales no quitan la barriga y los ejercicios de costado no quitan "
   "los rollos del lado. El cuerpo saca la grasa de donde le da la gana y el "
   "orden lo decide la genética. Cualquiera que te diga lo contrario te está "
   "vendiendo algo."),
  ("Lo que sí funciona, en orden de importancia.",
   "<strong>Uno:</strong> comer menos de lo que gastas. Es la mayor parte del "
   "asunto y no hay rutina que lo reemplace. <strong>Dos:</strong> mantener el "
   "músculo mientras bajas, con las rutinas de pesas de la semana, porque si no "
   "quedas igual pero más pequeño. <strong>Tres:</strong> gastar más, caminando "
   "y con los bloques de quema. <strong>Cuatro:</strong> entrenar el abdomen "
   "para que cuando la grasa se vaya haya algo debajo."),
  ("Esta sección hace el tres y el cuatro.",
   "El uno y el dos no los hace ninguna rutina, ni esta ni ninguna otra. Por eso "
   "el bloque de quema está acá al lado del de abdomen: el que mueve la aguja de "
   "la grasa es el de quema, no el de abdomen."),
]

ABDOMINALES = [

 dict(id="completo", nombre="Core completo", mins=15,
      desc="Todo el cilindro: adelante, costados y espalda baja.",
      blocks=[
   w("Calentamiento", 3, "Sin descanso entre uno y otro.", [
     e("Gato–camello", "10 reps"),
     e("Puente de glúteo", "12 reps"),
     e("Muerto bicho", "8 por lado"),
     e("Perro-pájaro", "8 por lado"),
   ]),
   c("Circuito", 10, 3, 45, "Los cinco seguidos",
     "Haces los cinco uno detrás de otro y al terminar descansas 45 segundos.", [
     e("Plancha", "45 s", code="1"),
     e("Encogimiento abdominal", "20 reps", code="2"),
     e("Elevación de piernas", "12 reps", code="3"),
     e("Giro ruso", "20 (10 por lado)", "1 disco · 1 kg", code="4"),
     e("Superman", "15 reps", code="5"),
   ]),
   s("Estiramiento", 2, None, [
     e("Rodillas al pecho", "45 s"),
     e("Torsión de columna", "30 s por lado"),
   ]),
 ]),

 dict(id="costados", nombre="Costados y oblicuos", mins=14,
      desc="Los músculos de los lados del tronco, que es lo que sostiene la cintura.",
      blocks=[
   w("Calentamiento", 3, None, [
     e("Abre el libro", "8 por lado"),
     e("Círculos de cadera", "10 por lado"),
     e("Gato–camello", "10 reps"),
   ]),
   c("Circuito", 9, 3, 45, "Los cinco seguidos", None, [
     e("Plancha lateral con cadera", "10 por lado", code="1"),
     e("Leñador", "12 por lado", "1 mancuerna · 5 kg", code="2"),
     e("Escalador cruzado", "20 (10 por lado)", code="3"),
     e("Toques de talón", "20 (10 por lado)", code="4"),
     e("Marcha con maleta", "40 s por lado", "1 mancuerna · 7,5 kg", code="5"),
   ]),
   s("Estiramiento", 2, None, [
     e("Costado", "30 s por lado"),
     e("Torsión de columna", "30 s por lado"),
   ]),
 ]),

 dict(id="bajo", nombre="Abdomen bajo", mins=12,
      desc="La parte de abajo del abdomen, la que casi nadie trabaja bien.",
      blocks=[
   w("Calentamiento", 2, None, [
     e("Muerto bicho", "10 por lado"),
     e("Puente de glúteo", "15 reps"),
   ]),
   c("Circuito", 8, 3, 40, "Los cuatro seguidos",
     "Si la espalda baja se despega del piso en cualquiera de estos, bajaste "
     "demasiado las piernas. Acorta el recorrido.", [
     e("Crunch inverso", "12 reps", code="1"),
     e("Tijeras", "30 s", code="2"),
     e("Rodillas al pecho sentado", "15 reps", code="3"),
     e("Hollow", "30 s", code="4"),
   ]),
   s("Estiramiento", 2, None, [
     e("Rodillas al pecho", "45 s"),
     e("Postura del niño", "45 s"),
   ]),
 ]),

 dict(id="quema", nombre="Quema", mins=16, hiit=True,
      desc="Intervalos fuertes. Este es el que de verdad gasta calorías.",
      blocks=[
   w("Calentamiento", 3, "Súbele el pulso antes de arrancar.", [
     e("Marcha en el sitio", "45 s"),
     e("Salto de tijera", "30 s"),
     e("Sentadilla al aire", "15 reps"),
     e("Círculos de brazos", "15 por sentido"),
   ]),
   c("Intervalos", 12, 2, 20, "40 s fuerte · 20 s descanso",
     "Cuarenta segundos a tope, veinte de descanso, y pasas al siguiente. "
     "Al terminar los seis, arrancas la segunda vuelta.", [
     e("Burpee", "40 s", code="1"),
     e("Escaladores", "40 s", code="2"),
     e("Salto de tijera", "40 s", code="3"),
     e("Sentadilla con salto", "40 s", code="4"),
     e("Rodillas altas", "40 s", code="5"),
     e("Plancha", "40 s", code="6"),
   ], timers=[(40, "Trabajo"), (20, "Descanso")]),
   s("Estiramiento", 1, None, [
     e("Cuádriceps de pie", "30 s por pierna"),
     e("Rodillas al pecho", "30 s"),
   ]),
 ]),
]


# ══════════════════════════════════════════════════════════ PECHO

PECHO_VERDAD = [
  ("La grasa del pecho se va con la de todo el cuerpo.",
   "No con ejercicios de pecho. Igual que con la barriga: no se elige de dónde "
   "sale. Lo que sí hacen los ejercicios de acá es construir el músculo que está "
   "debajo, y eso cambia la forma: un pectoral con volumen da borde y levanta "
   "donde antes solo había blando."),
  ("Los dos juntos es lo que cambia la foto.",
   "Bajar grasa con la comida y las caminadas, y construir pecho con estas "
   "rutinas. Por separado cada uno hace la mitad del trabajo."),
  ("Una nota médica que vale la pena saber.",
   "Si al tocarte sientes un bulto firme justo debajo del pezón, en uno o en los "
   "dos lados, y molesta un poco al presionar, eso no es grasa y no se va "
   "entrenando. Se llama ginecomastia, es bastante común y tiene tratamiento. "
   "Vale una consulta médica, sin drama."),
]

PECHO = [

 dict(id="completo", nombre="Pecho completo", mins=20,
      desc="Mancuernas y flexiones. La opción principal.",
      blocks=[
   w("Calentamiento", 4, None, [
     e("Círculos de brazos", "15 por sentido"),
     e("Rotación externa de hombro", "15 por lado"),
     e("Flexiones de rodillas", "10 reps"),
     e("Abre el libro", "8 por lado"),
   ]),
   c("Bloque A", 9, 3, 75, "Tri-serie",
     "A1 → A2 → A3 seguidos, y al terminar los tres descansas.", [
     e("Press de pecho en el piso", "10 reps", "2 mancuernas · 7,5 kg", code="A1"),
     e("Flexión", "10 reps", code="A2"),
     e("Aperturas en el piso", "12 reps", "2 mancuernas · 5 kg", code="A3"),
   ]),
   c("Bloque B", 5, 2, 60, "Superserie", None, [
     e("Press cerrado en el piso", "12 reps", "2 mancuernas · 7,5 kg", code="B1"),
     e("Pullover", "12 reps", "1 mancuerna · 7,5 kg", code="B2"),
   ]),
   s("Estiramiento", 2, None, [
     e("Pecho en el marco de la puerta", "40 s por lado"),
     e("Hombro: brazo cruzado", "30 s por lado"),
   ]),
 ]),

 dict(id="mancuernas", nombre="Sin flexiones", mins=18,
      desc="Todo acostado en el tapete. Para cuando la muñeca o el hombro molestan.",
      blocks=[
   w("Calentamiento", 3, None, [
     e("Círculos de brazos", "15 por sentido"),
     e("Rotación externa de hombro", "15 por lado"),
     e("Abre el libro", "8 por lado"),
   ]),
   c("Bloque A", 8, 3, 75, "Tri-serie", None, [
     e("Press de pecho en el piso", "10 reps", "2 mancuernas · 7,5 kg", code="A1"),
     e("Aperturas en el piso", "12 reps", "2 mancuernas · 5 kg", code="A2"),
     e("Pullover", "12 reps", "1 mancuerna · 7,5 kg", code="A3"),
   ]),
   c("Bloque B", 5, 2, 60, "Superserie", None, [
     e("Press alterno", "10 por brazo", "2 mancuernas · 7,5 kg", code="B1"),
     e("Press cerrado en el piso", "12 reps", "2 mancuernas · 7,5 kg", code="B2"),
   ]),
   s("Estiramiento", 2, None, [
     e("Pecho en el marco de la puerta", "40 s por lado"),
     e("Tríceps: codo arriba", "30 s por brazo"),
   ]),
 ]),

 dict(id="quema", nombre="Pecho y quema", mins=20, hiit=True,
      desc="Pecho intercalado con intervalos. Trabajas el músculo y gastas al tiempo.",
      blocks=[
   w("Calentamiento", 3, None, [
     e("Marcha en el sitio", "45 s"),
     e("Círculos de brazos", "15 por sentido"),
     e("Flexiones de rodillas", "10 reps"),
   ]),
   c("Bloque A", 9, 3, 60, "Tri-serie",
     "El tercero es el de quema: sales del press directo a moverte.", [
     e("Press de pecho en el piso", "10 reps", "2 mancuernas · 7,5 kg", code="A1"),
     e("Flexión ancha", "10 reps", code="A2"),
     e("Burpee", "8 reps", code="A3"),
   ]),
   c("Bloque B", 6, 3, 45, "Tri-serie", None, [
     e("Flexión diamante", "8 reps", code="B1"),
     e("Aperturas en el piso", "12 reps", "2 mancuernas · 5 kg", code="B2"),
     e("Escaladores", "20 (10 por pierna)", code="B3"),
   ]),
   s("Estiramiento", 2, None, [
     e("Pecho en el marco de la puerta", "40 s por lado"),
     e("Rodillas al pecho", "30 s"),
   ]),
 ]),
]
