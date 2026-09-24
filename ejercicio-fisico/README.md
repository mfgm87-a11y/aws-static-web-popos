# Ejercicio físico en casa

Siete rutinas de 30 minutos, una para cada día. Todos los días se trabaja
pierna, pecho, espalda, brazo y core, pero cada día le toca una parte distinta
de cada área.

**Para usarlas:** <https://claude.ai/artifact/5dmToemYQhgZSRNAAxqaW6>

Esa página se abre en el celular al lado del tapete. Tiene casillas para ir
marcando ejercicios, contador de rondas y cronómetro de descanso.

---

## Qué hay en esta carpeta

El menú tiene cuatro entradas: **rutinas por día**, **rutina aleatoria**,
**abdominales** y **pecho**. Debajo, el banco de ejercicios, la guía y la
progresión.

| Ruta | Qué es |
|---|---|
| `web/index.html` | El menú: las cuatro entradas |
| `web/dias.html` | Escoger día, más la tabla de rotación |
| `web/dia-1.html` … `web/dia-7.html` | Una rutina por día |
| `web/aleatoria.html` | Generador: arma una rutina de 30 min al azar |
| `web/abdominales.html` | Cuatro rutinas: core, costados, abdomen bajo y quema |
| `web/pecho.html` | Tres rutinas de pectoral |
| `web/banco.html` | Los 97 ejercicios con su dibujo, con buscador |
| `web/guia.html` | Equipo, cargas, cómo leer una ficha, reglas |
| `web/progresion.html` | Cuándo subir peso y tabla de registro |
| `build.py` | Rutinas de la semana y plantilla de todas las páginas |
| `secciones.py` | Rutinas de abdominales y pecho |
| `figuras.py` | Motor de dibujo: figuras de palo en SVG |
| `dibujos.py` | Una pose por ejercicio (89 dibujos) |
| `fichas.py` | Cadencia, hasta dónde, versión fácil y error común |

Las páginas de `web/` son generadas. Para regenerarlas:

```bash
python3 build.py
```

Dónde tocar según lo que quieras cambiar:

- **Un ejercicio de la semana** → diccionario `DATA` en `build.py`
- **Una rutina de abdominales o pecho** → `secciones.py`
- **La cadencia, la versión fácil o el error común** → lista `FICHAS` en `fichas.py`
- **Un dibujo** → `DIB[...]` en `dibujos.py`. Las poses se definen por coordenadas
  (dónde va el tobillo, dónde la muñeca) y `figuras.py` resuelve los ángulos.
- **Qué ejercicios entran al generador aleatorio** → el campo `cat` de cada ficha

### Hoja de contacto de los dibujos

Para revisar los 89 dibujos de una sola vez, genera una página con todos:

```python
import dibujos
print(dibujos.DIB["sentadilla_goblet"])
```

---

## El equipo que suponen estas rutinas

| Elemento | Detalle |
|---|---|
| 2 mancuernas ajustables | 7,5 kg cada una: 2 discos de 2,5 kg + 2 de 1,25 kg por mancuerna |
| 4 discos sueltos | 1 kg cada uno |
| Vara larga | Une las dos mancuernas en una barra de ~19 kg |
| Silla | **Solo para sentarse.** No se sube uno en ella ni se empuja contra la pared |
| Sofá | Borde firme para las flexiones con manos elevadas |
| Tapete | Zona de trabajo de suelo |
| Espejo | Revisar técnica en sentadilla y peso muerto |

Cargas disponibles por mancuerna: **2,5 → 5 → 7,5 → 9,5 kg**.
Con todos los discos en la vara: **~19 kg**.

---

## Lo que trae cada ejercicio

Un dibujo con la posición de inicio y la de llegada, con la línea punteada roja
marcando hasta dónde llega el movimiento. Al lado, dos datos:

- **Cadencia** — tres números: segundos para bajar, pausa abajo, segundos para
  subir. `3-1-1` es bajar en tres, parar uno, subir en uno.
- **Hasta dónde** — el punto exacto donde termina el recorrido.

Y dentro de *Cómo se hace*: la técnica, la versión más fácil para arrancar y el
error que casi todo el mundo comete.

---

## La rotación

| Día | Pierna | Pecho | Espalda | Brazo |
|---|---|---|---|---|
| 1 · Lun | Cuádriceps | Medio | Dorsal ancho | Bíceps |
| 2 · Mar | Isquios, glúteo | Superior | Media, romboides | Tríceps largo |
| 3 · Mié | Unilateral | Externo | Dorsal unilateral | Braquial |
| 4 · Jue | Glúteo medio | Inferior | Trapecio, hombro post. | Tríceps lateral |
| 5 · Vie | Complejo | Complejo | Complejo | Complejo |
| 6 · Sáb | Pantorrilla | — | Erectores | Hombro medial |
| 7 · Dom | Movilidad | Movilidad | Movilidad | Movilidad |

El domingo es suave a propósito: movilidad y core ligero, sin mancuernas.

---

## Sobre bajar de peso

Las secciones de abdominales y pecho dicen esto en la propia página, y conviene
que quede escrito también acá: **no se puede quemar grasa de un sitio en
particular**. Los abdominales no quitan la barriga y los ejercicios de pecho no
quitan la grasa del pecho. Lo que trabajan es el músculo que queda debajo.

Lo que mueve la grasa, en orden: comer menos de lo que se gasta, mantener el
músculo mientras se baja, y gastar más. Los bloques de *quema* de esta carpeta
hacen lo tercero. Los dos primeros no los hace ninguna rutina.

---

## Lo que esto no es

Una rutina general para alguien sano que entrena en casa. No sustituye a un
profesional. Con una lesión, una condición cardíaca, o mucho tiempo sin
moverse, primero un médico o un fisioterapeuta.
