#!/usr/bin/env python3
"""Simulacro de estudio para el examen AMIB Figura 3 (sin dependencias externas).

Ejemplos:
    python simulacro.py                      # 20 preguntas, modo estudio
    python simulacro.py -n 40 --modo examen  # 40 preguntas, resultados al final
    python simulacro.py -m deuda             # solo preguntas del módulo "Deuda"
    python simulacro.py --tiempo 60          # límite de 60 minutos
    python simulacro.py --listar             # muestra los módulos disponibles
"""
import argparse
import json
import random
import time
from collections import defaultdict
from pathlib import Path

BANCO = Path(__file__).with_name("preguntas.json")
LETRAS = "abcd"
APROBATORIO = 60  # % de referencia para estudiar; NO es el puntaje oficial de la AMIB


def cargar_banco(modulo=None):
    with open(BANCO, encoding="utf-8") as f:
        preguntas = json.load(f)
    if modulo:
        preguntas = [p for p in preguntas if modulo.lower() in p["modulo"].lower()]
    return preguntas


def mezclar_opciones(p):
    """Devuelve (textos mezclados, índice de la correcta en el nuevo orden)."""
    pares = list(enumerate(p["opciones"]))
    random.shuffle(pares)
    textos = [texto for _, texto in pares]
    correcta = next(i for i, (orig, _) in enumerate(pares) if orig == p["correcta"])
    return textos, correcta


def pedir_respuesta(num, total, p, textos):
    print(f"\n[{num}/{total}] ({p['modulo']})")
    print(p["pregunta"])
    for letra, texto in zip(LETRAS, textos):
        print(f"  {letra}) {texto}")
    while True:
        r = input("Tu respuesta (a-d, s = terminar): ").strip().lower()
        if r == "s":
            return None
        if r and r in LETRAS[: len(textos)]:
            return LETRAS.index(r)
        print("Opción no válida.")


def resumen(resultados, inicio):
    if not resultados:
        print("\nNo respondiste ninguna pregunta.")
        return
    total = len(resultados)
    aciertos = sum(r["ok"] for r in resultados)
    minutos = (time.time() - inicio) / 60
    print("\n" + "=" * 50)
    print(f"Resultado: {aciertos}/{total} ({aciertos / total:.0%}) en {minutos:.1f} min")

    por_modulo = defaultdict(lambda: [0, 0])
    for r in resultados:
        por_modulo[r["modulo"]][1] += 1
        por_modulo[r["modulo"]][0] += r["ok"]
    print("\nPor módulo:")
    for modulo, (ok, n) in sorted(por_modulo.items()):
        aviso = "  <- repasar" if ok / n * 100 < APROBATORIO else ""
        print(f"  {modulo:<24} {ok}/{n} ({ok / n:.0%}){aviso}")

    errores = [r for r in resultados if not r["ok"]]
    if errores:
        print("\nPreguntas para repasar:")
        for r in errores:
            print(f"\n- {r['pregunta']}")
            print(f"  Tu respuesta: {r['tuya']}")
            print(f"  Correcta:     {r['correcta']}")
            print(f"  Explicación:  {r['explicacion']}")
    print(
        f"\nNota: el {APROBATORIO}% es solo una referencia de estudio, "
        "no el puntaje oficial de la AMIB."
    )


def main():
    ap = argparse.ArgumentParser(description="Simulacro de estudio AMIB Figura 3")
    ap.add_argument("-n", "--num", type=int, default=20, help="número de preguntas")
    ap.add_argument("-m", "--modulo", help="filtra por módulo (texto parcial)")
    ap.add_argument(
        "--modo",
        choices=["estudio", "examen"],
        default="estudio",
        help="estudio: retroalimentación inmediata; examen: resultados al final",
    )
    ap.add_argument("--tiempo", type=int, help="límite de tiempo en minutos")
    ap.add_argument("--semilla", type=int, help="semilla para repetir el mismo orden")
    ap.add_argument("--listar", action="store_true", help="lista los módulos y sale")
    args = ap.parse_args()

    if args.semilla is not None:
        random.seed(args.semilla)

    banco = cargar_banco()
    if args.listar:
        conteo = defaultdict(int)
        for p in banco:
            conteo[p["modulo"]] += 1
        for modulo, n in sorted(conteo.items()):
            print(f"{modulo}: {n} preguntas")
        return

    banco = cargar_banco(args.modulo)
    if not banco:
        print("No hay preguntas para ese módulo. Usa --listar para ver los disponibles.")
        return

    seleccion = random.sample(banco, min(args.num, len(banco)))
    inicio = time.time()
    limite = args.tiempo * 60 if args.tiempo else None
    resultados = []

    try:
        for i, p in enumerate(seleccion, 1):
            if limite and time.time() - inicio > limite:
                print("\nSe terminó el tiempo.")
                break
            textos, correcta = mezclar_opciones(p)
            eleccion = pedir_respuesta(i, len(seleccion), p, textos)
            if eleccion is None:
                break
            ok = eleccion == correcta
            resultados.append(
                {
                    "modulo": p["modulo"],
                    "pregunta": p["pregunta"],
                    "ok": ok,
                    "tuya": textos[eleccion],
                    "correcta": textos[correcta],
                    "explicacion": p["explicacion"],
                }
            )
            if args.modo == "estudio":
                print("Correcto." if ok else f"Incorrecto. Era: {LETRAS[correcta]}) {textos[correcta]}")
                print(f"  {p['explicacion']}")
    except (KeyboardInterrupt, EOFError):
        print("\nSimulacro interrumpido.")

    resumen(resultados, inicio)


if __name__ == "__main__":
    main()
