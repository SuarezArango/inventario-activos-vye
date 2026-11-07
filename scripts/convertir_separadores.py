"""Convierte fórmulas Power Fx del formato en inglés (separador ',') al de configuración
regional en español (separador ';' y encadenamiento ';;'). Respeta textos entre comillas
y comentarios //. Uso: python scripts/convertir_separadores.py"""
import pathlib, re

def convertir(linea: str) -> str:
    out, i, en_texto = [], 0, False
    while i < len(linea):
        c = linea[i]
        if not en_texto and linea.startswith("//", i):
            out.append(linea[i:]); break
        if c == '"':
            en_texto = not en_texto; out.append(c)
        elif en_texto:
            out.append(c)
        elif c == ";":
            out.append(";;")
        elif c == ",":
            out.append(";")
        elif c == "." and i > 0 and linea[i-1].isdigit() and i + 1 < len(linea) and linea[i+1].isdigit():
            out.append(",")          # decimales: 1.5 -> 1,5
        else:
            out.append(c)
        i += 1
    return "".join(out)

base = pathlib.Path(__file__).resolve().parent.parent / "powerapps"
for f in sorted(base.glob("*.fx")):
    texto = "\n".join(convertir(l) for l in f.read_text(encoding="utf-8").splitlines()) + "\n"
    (base / "es-CO" / f.name).write_text(texto, encoding="utf-8")
    print("convertido:", f.name)
