# Ejercicio físico en casa

Siete rutinas de 30 minutos, una para cada día. Todos los días se trabaja
pierna, pecho, espalda, brazo y core, pero cada día le toca una parte distinta
de cada área.

**Para usarlas:** <https://claude.ai/artifact/5dmToemYQhgZSRNAAxqaW6>

Esa página se abre en el celular al lado del tapete. Tiene casillas para ir
marcando ejercicios, contador de rondas y cronómetro de descanso.

---

## Qué hay en esta carpeta

| Ruta | Qué es |
|---|---|
| `web/index.html` | Índice: equipo, configuraciones de carga, rotación de la semana |
| `web/dia-1.html` … `web/dia-7.html` | Una rutina por día |
| `web/progresion.html` | Cuándo subir peso y tabla de registro |
| `build.py` | Genera las 9 páginas. **Aquí vive el contenido.** |

Las páginas de `web/` son generadas. Para cambiar un ejercicio, edita el
diccionario `DATA` en `build.py` y vuelve a correr:

```bash
python3 build.py
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

## Lo que esto no es

Una rutina general para alguien sano que entrena en casa. No sustituye a un
profesional. Con una lesión, una condición cardíaca, o mucho tiempo sin
moverse, primero un médico o un fisioterapeuta.
