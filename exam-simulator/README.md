# Simulador KCNA y KCSA

Simulador de práctica para los exámenes **KCNA** (Kubernetes and Cloud Native Associate) y **KCSA** (Kubernetes and Cloud Native Security Associate) de la CNCF / Linux Foundation.

- **618 preguntas originales**: 310 de KCNA y 308 de KCSA, repartidas según el peso oficial de cada dominio.
- Interfaz, preguntas y opciones **en inglés**, como en la plataforma del examen real (Previous, Flag, Next, Review & submit…); explicaciones **en español** que dicen por qué la respuesta es correcta y por qué fallan las otras.
- Modo **Practice**: compruebas cada respuesta (Check) y ves la explicación al instante.
- Modo **Exam**: 60 preguntas con el reparto oficial por dominio, sin pistas, con opción de marcar (Flag) y revisar, y nota al final (aprobado ≥ 75 %).
- **Timed / untimed**: con tiempo son 90 minutos para 60 preguntas (unos 90 s por pregunta, también en las prácticas cortas).
- Progreso por dominio, historial de intentos, repaso de falladas y reanudación de sesiones. Todo se guarda en el navegador; en el enlace publicado en claude.ai también se sincroniza con tu cuenta.

## Abrirlo

`web/simulador-k8s.html` es un único archivo que funciona sin conexión: puedes abrirlo directamente en el navegador del celular o del computador.

Para publicarlo junto con el resto del sitio en el bucket S3 que crea la infraestructura de `infra/`:

```bash
aws s3 cp web/simulador-k8s.html s3://aws-static-web-popos/simulador-k8s.html --content-type "text/html; charset=utf-8"
# o todo el sitio:
aws s3 sync web/ s3://aws-static-web-popos/
```

Queda disponible en `http://<website_endpoint>/simulador-k8s.html` (el endpoint sale de `terraform output website_endpoint`).

## Editar o añadir preguntas

Las preguntas viven en `exam-simulator/banks/kcna/*.md` y `exam-simulator/banks/kcsa/*.md`, con este formato:

```markdown
### [dominio/Tema/nivel]
Question text in English (admite `código` y bloques de código).
- [ ] incorrect option
- [x] correct option
- [ ] incorrect option
- [ ] incorrect option
> Explicación en español.
```

- `dominio` empieza en 1 y `Tema` debe ser uno de los temas definidos para ese dominio en `build.py`.
- `nivel`: 1 = recordar, 2 = entender, 3 = escenario.
- Varias `[x]` crean una pregunta de selección múltiple; el enunciado debe decir `(Choose two.)`.
- No uses opciones como "All of the above": el orden de las opciones se baraja en cada sesión.

Después de editar, valida y regenera el HTML:

```bash
python3 exam-simulator/build.py --check   # solo valida y muestra estadísticas
python3 exam-simulator/build.py           # valida y regenera web/simulador-k8s.html
```

La validación revisa el formato, los temas, las respuestas duplicadas y el reparto por dominio, y avisa si la respuesta correcta suele ser la opción más larga (una pista que no debería existir).

## Fuentes

- Currículos oficiales: [github.com/cncf/curriculum](https://github.com/cncf/curriculum). KCNA usa el temario vigente desde noviembre de 2025 (44 / 28 / 16 / 12) y KCSA el de seis dominios (14 / 22 / 22 / 16 / 16 / 10).
- Documentación de Kubernetes v1.37 para los datos técnicos (versiones, valores por defecto, Pod Security Standards, RBAC, auditoría…).

Las preguntas son originales y están pensadas para entrenar; no son preguntas filtradas del examen real.
