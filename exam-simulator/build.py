#!/usr/bin/env python3
"""Construye el simulador KCNA / KCSA a partir de los bancos de preguntas en Markdown.

Uso:
  python3 exam-simulator/build.py                 # valida y genera web/simulador-k8s.html
  python3 exam-simulator/build.py --check         # solo valida y muestra estadísticas
  python3 exam-simulator/build.py --fragment OUT  # además genera la versión sin <head>/<body>

Formato de cada pregunta (banks/<examen>/*.md):

  ### [dominio/Tema/nivel]          dominio empieza en 1; nivel 1=recordar, 2=entender, 3=escenario
  Enunciado en inglés (puede tener `código` y bloques ```).
  - [ ] opción incorrecta
  - [x] opción correcta            (varias [x] = selección múltiple; el enunciado debe decir "(Choose two.)")
  - [ ] opción incorrecta
  - [ ] opción incorrecta
  > Explicación en español. Una línea ">" vacía separa párrafos.
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUT_FULL = REPO / "web" / "simulador-k8s.html"

EXAMS = {
    "kcna": {
        "code": "KCNA",
        "name": "Kubernetes and Cloud Native Associate",
        "questions": 60,
        "minutes": 90,
        "pass": 75,
        "domains": [
            {"name": "Kubernetes Fundamentals", "weight": 44,
             "topics": ["Core Concepts", "Administration", "Scheduling", "Containerization"],
             "syllabus": ["Kubernetes Core Concepts", "Administration", "Scheduling", "Containerization"]},
            {"name": "Container Orchestration", "weight": 28,
             "topics": ["Networking", "Security", "Troubleshooting", "Storage"],
             "syllabus": ["Networking", "Security", "Troubleshooting", "Storage"]},
            {"name": "Cloud Native Application Delivery", "weight": 16,
             "topics": ["Application Delivery", "Debugging"],
             "syllabus": ["Application Delivery", "Debugging"]},
            {"name": "Cloud Native Architecture", "weight": 12,
             "topics": ["Observability", "Ecosystem & Principles", "Community & Collaboration"],
             "syllabus": ["Observability", "Cloud Native Ecosystem and Principles",
                          "Cloud Native Community and Collaboration"]},
        ],
    },
    "kcsa": {
        "code": "KCSA",
        "name": "Kubernetes and Cloud Native Security Associate",
        "questions": 60,
        "minutes": 90,
        "pass": 75,
        "domains": [
            {"name": "Overview of Cloud Native Security", "weight": 14,
             "topics": ["4Cs", "Cloud & Infrastructure", "Controls & Frameworks", "Isolation",
                        "Artifact & Image Security", "Workload & Code Security"],
             "syllabus": ["The 4Cs of Cloud Native Security", "Cloud Provider and Infrastructure Security",
                          "Controls and Frameworks", "Isolation Techniques",
                          "Artifact Repository and Image Security", "Workload and Application Code Security"]},
            {"name": "Kubernetes Cluster Component Security", "weight": 22,
             "topics": ["API Server", "Controller Manager", "Scheduler", "Kubelet", "Container Runtime",
                        "KubeProxy", "Pod", "etcd", "Container Networking", "Client Security", "Storage"],
             "syllabus": ["API Server", "Controller Manager", "Scheduler", "Kubelet", "Container Runtime",
                          "KubeProxy", "Pod", "Etcd", "Container Networking", "Client Security", "Storage"]},
            {"name": "Kubernetes Security Fundamentals", "weight": 22,
             "topics": ["Pod Security Standards", "Pod Security Admission", "Authentication", "Authorization",
                        "Secrets", "Isolation & Segmentation", "Audit Logging", "Network Policy"],
             "syllabus": ["Pod Security Standards", "Pod Security Admissions", "Authentication", "Secrets",
                          "Isolation and Segmentation", "Audit Logging", "Network Policy"]},
            {"name": "Kubernetes Threat Model", "weight": 16,
             "topics": ["Trust Boundaries", "Persistence", "Denial of Service", "Malicious Code",
                        "Network Attacker", "Sensitive Data", "Privilege Escalation"],
             "syllabus": ["Kubernetes Trust Boundaries and Data Flow", "Persistence", "Denial of Service",
                          "Malicious Code Execution and Compromised Applications in Containers",
                          "Attacker on the Network", "Access to Sensitive Data", "Privilege Escalation"]},
            {"name": "Platform Security", "weight": 16,
             "topics": ["Supply Chain", "Image Repository", "Observability", "Service Mesh", "PKI",
                        "Connectivity", "Admission Control"],
             "syllabus": ["Supply Chain Security", "Image Repository", "Observability", "Service Mesh", "PKI",
                          "Connectivity", "Admission Control"]},
            {"name": "Compliance and Security Frameworks", "weight": 10,
             "topics": ["Compliance Frameworks", "Threat Modeling", "Supply Chain Compliance",
                        "Automation & Tooling"],
             "syllabus": ["Compliance Frameworks", "Threat Modeling Frameworks", "Supply Chain Compliance",
                          "Automation and Tooling"]},
        ],
    },
}

HEAD = re.compile(r"^### \[(\d+)\s*/\s*([^/\]]+?)\s*/\s*([123])\]\s*$")
OPT = re.compile(r"^- \[([ xX])\] (.+)$")
CHOOSE = {2: "(Choose two.)", 3: "(Choose three.)"}
BANNED_OPTS = re.compile(r"\b(all|none) of the above\b|\bboth [a-d] and [a-d]\b|^[a-d] and [a-d]$", re.I)


class BankError(Exception):
    pass


def parse_file(exam, path):
    meta = EXAMS[exam]
    questions, errors = [], []
    cur = None
    in_fence = False

    def close(q):
        where = q["src"]
        stem = "\n".join(q["stem"]).strip()
        exp = "\n".join(q["exp"]).strip()
        dom = q["d"]
        if not 0 <= dom < len(meta["domains"]):
            errors.append(f"{where}: dominio {dom + 1} no existe")
            return
        if q["t"] not in meta["domains"][dom]["topics"]:
            errors.append(f"{where}: tema '{q['t']}' no pertenece al dominio {dom + 1}")
        if not stem:
            errors.append(f"{where}: enunciado vacío")
        if not exp:
            errors.append(f"{where}: falta la explicación")
        if not 3 <= len(q["opts"]) <= 5:
            errors.append(f"{where}: {len(q['opts'])} opciones (se esperan 3-5)")
        if not q["ans"]:
            errors.append(f"{where}: no hay respuesta marcada con [x]")
        if len(q["ans"]) > 1:
            tag = CHOOSE.get(len(q["ans"]))
            if not tag or tag not in stem:
                errors.append(f"{where}: {len(q['ans'])} respuestas correctas pero el enunciado no dice {tag}")
        elif "(Choose" in stem:
            errors.append(f"{where}: dice '(Choose ...)' pero solo tiene una respuesta correcta")
        if len(set(o.lower() for o in q["opts"])) != len(q["opts"]):
            errors.append(f"{where}: opciones repetidas")
        for o in q["opts"]:
            if BANNED_OPTS.search(o):
                errors.append(f"{where}: opción '{o}' depende del orden (las opciones se barajan)")
        norm = re.sub(r"\s+", " ", stem.lower())
        qid = exam + "-" + hashlib.sha1((exam + "|" + norm).encode("utf-8")).hexdigest()[:8]
        questions.append({
            "i": qid, "d": dom, "t": q["t"], "l": q["l"],
            "q": stem, "o": q["opts"], "a": q["ans"], "e": exp, "src": where,
        })

    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        m = HEAD.match(line) if not in_fence else None
        if m:
            if cur:
                close(cur)
            cur = {"src": f"{path.parent.name}/{path.name}:{n}", "d": int(m.group(1)) - 1,
                   "t": m.group(2).strip(), "l": int(m.group(3)),
                   "stem": [], "opts": [], "ans": [], "exp": [], "state": "stem"}
            continue
        if cur is None:
            continue
        if cur["state"] == "stem":
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                cur["stem"].append(line)
                continue
            if in_fence:
                cur["stem"].append(line)
                continue
        om = OPT.match(line)
        if om and cur["state"] in ("stem", "opts"):
            cur["state"] = "opts"
            if om.group(1).lower() == "x":
                cur["ans"].append(len(cur["opts"]))
            cur["opts"].append(om.group(2).strip())
            continue
        if line.startswith(">") and cur["state"] in ("opts", "exp"):
            cur["state"] = "exp"
            cur["exp"].append(line[1:].strip())
            continue
        if cur["state"] == "stem":
            cur["stem"].append(line)
        elif line.strip():
            errors.append(f"{path.parent.name}/{path.name}:{n}: texto inesperado fuera del bloque: {line[:60]!r}")
    if cur:
        close(cur)
    if in_fence:
        errors.append(f"{path.name}: bloque ``` sin cerrar")
    return questions, errors


def load_bank(exam):
    files = sorted((ROOT / "banks" / exam).glob("*.md"))
    questions, errors = [], []
    for f in files:
        qs, errs = parse_file(exam, f)
        questions.extend(qs)
        errors.extend(errs)
    seen = {}
    for q in questions:
        if q["i"] in seen:
            errors.append(f"{q['src']}: enunciado duplicado de {seen[q['i']]}")
        seen[q["i"]] = q["src"]
    return questions, errors


def stats(exam, questions):
    meta = EXAMS[exam]
    total = len(questions)
    print(f"\n== {meta['code']}: {total} preguntas ==")
    by_dom = Counter(q["d"] for q in questions)
    by_topic = defaultdict(Counter)
    for q in questions:
        by_topic[q["d"]][q["t"]] += 1
    for i, d in enumerate(meta["domains"]):
        n = by_dom.get(i, 0)
        pct = 100 * n / total if total else 0
        print(f"  D{i + 1} {d['name']:<40} {n:>4}  {pct:5.1f}%  (oficial {d['weight']}%)")
        print("       " + ", ".join(f"{t}: {by_topic[i].get(t, 0)}" for t in d["topics"]))
    lv = Counter(q["l"] for q in questions)
    print("  Nivel: " + ", ".join(f"{k}={lv.get(k, 0)}" for k in (1, 2, 3)))
    multi = sum(1 for q in questions if len(q["a"]) > 1)
    print(f"  Selección múltiple: {multi}")
    single = [q for q in questions if len(q["a"]) == 1]
    longest = sum(1 for q in single
                  if len(q["o"][q["a"][0]]) == max(len(o) for o in q["o"])
                  and sum(1 for o in q["o"] if len(o) == len(q["o"][q["a"][0]])) == 1)
    if single:
        print(f"  La correcta es la opción más larga: {longest}/{len(single)} ({100 * longest / len(single):.0f}%)")
    pos = Counter(q["a"][0] for q in single)
    print("  Posición de la correcta antes de barajar: " + ", ".join(f"{k}:{pos[k]}" for k in sorted(pos)))
    exp_len = [len(q["e"]) for q in questions]
    if exp_len:
        print(f"  Explicación: media {sum(exp_len) // len(exp_len)} caracteres, mínima {min(exp_len)}")


def build_payload():
    payload = {"exams": {}}
    all_errors = []
    for exam, meta in EXAMS.items():
        questions, errors = load_bank(exam)
        all_errors.extend(errors)
        stats(exam, questions)
        payload["exams"][exam] = {
            **{k: v for k, v in meta.items()},
            "bank": [{k: v for k, v in q.items() if k != "src"} for q in questions],
        }
    return payload, all_errors


def render(payload, fragment):
    template = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = template.replace("__BANK_JSON__", data)
    head, sep, body = template.partition("<!--/HEAD-->")
    if not sep:
        raise BankError("src/app.html debe contener el marcador <!--/HEAD-->")
    head = head.replace("<!--HEAD-->", "").strip()
    body = body.strip()
    if fragment:
        return head + "\n" + body + "\n"
    return (
        "<!doctype html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="solo validar los bancos")
    ap.add_argument("--fragment", metavar="OUT", help="ruta para la versión sin <head>/<body>")
    args = ap.parse_args()

    payload, errors = build_payload()
    if errors:
        print(f"\n{len(errors)} error(es):", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)
    if args.check:
        print("\nBancos válidos.")
        return
    OUT_FULL.write_text(render(payload, fragment=False), encoding="utf-8")
    print(f"\nGenerado {OUT_FULL.relative_to(REPO)} ({OUT_FULL.stat().st_size // 1024} KB)")
    if args.fragment:
        out = Path(args.fragment)
        out.write_text(render(payload, fragment=True), encoding="utf-8")
        print(f"Generado {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
