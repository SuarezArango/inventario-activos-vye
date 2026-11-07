"""
Genera datos sintéticos de prueba para el prototipo (≈500 activos) en CSV,
listos para cargar a Microsoft Lists con scripts/aprovisionar_listas.ps1
o con la opción "Crear lista desde CSV / Excel" de Microsoft Lists.

Uso:
    python scripts/generar_datos_prueba.py --activos 500 --salida data
Los datos son ficticios: no corresponden a personas ni equipos reales.
"""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEDES = [
    ("Sede Principal", "Medellín", "Sede principal"),
    ("Operación Minera Norte", "Segovia", "Operación / Obra"),
    ("Operación Vial Oriente", "Rionegro", "Operación / Obra"),
    ("Bodega Central", "Itagüí", "Bodega"),
]
AREAS = ["Dirección", "TI", "Administrativa / Financiera", "Operaciones / Campo", "Talento Humano"]
TIPOS = {  # tipo: (peso, marcas)
    "Portátil": (0.38, ["Lenovo", "HP", "Dell"]),
    "Escritorio": (0.22, ["Lenovo", "HP", "Dell"]),
    "Monitor": (0.18, ["Samsung", "LG", "Dell"]),
    "Impresora": (0.05, ["Epson", "HP", "Kyocera"]),
    "Periférico": (0.08, ["Logitech", "Genius", "HP"]),
    "Móvil": (0.06, ["Samsung", "Motorola", "Xiaomi"]),
    "Equipo de red": (0.03, ["Cisco", "Ubiquiti", "TP-Link"]),
}
PROCESADORES = ["Intel Core i3", "Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7"]
NOMBRES = ["Ana", "Luis", "María", "Carlos", "Paula", "Jorge", "Diana", "Andrés", "Laura", "Felipe",
           "Sandra", "Juan", "Camila", "Diego", "Natalia", "Óscar", "Valentina", "Héctor", "Lina", "Mateo"]
APELLIDOS = ["Gómez", "Restrepo", "Ospina", "Zapata", "Cardona", "Mejía", "Rendón", "Arango",
             "Vélez", "Muñoz", "Giraldo", "Henao", "Londoño", "Toro", "Quintero"]
HOY = date(2026, 11, 7)


def correo(nombre: str, apellido: str) -> str:
    limpio = lambda s: (s.lower().replace("á", "a").replace("é", "e").replace("í", "i")
                        .replace("ó", "o").replace("ú", "u").replace("ñ", "n"))
    return f"{limpio(nombre)}.{limpio(apellido)}@viasyexplanaciones.demo"


def generar(n_activos: int, salida: Path, semilla: int = 2026) -> None:
    rnd = random.Random(semilla)
    salida.mkdir(parents=True, exist_ok=True)

    personas = [(f"{rnd.choice(NOMBRES)} {ap}", ap) for ap in APELLIDOS for _ in range(3)]
    personas = [(nom, correo(nom.split()[0], ap), rnd.choice(AREAS)) for nom, ap in personas]

    with open(salida / "sedes.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Title", "Ciudad", "TipoSede", "Activa"])
        for s in SEDES:
            w.writerow([*s, "Sí"])

    activos, asignaciones, mantenimientos = [], [], []
    tipos, pesos = list(TIPOS), [v[0] for v in TIPOS.values()]
    for i in range(1, n_activos + 1):
        tipo = rnd.choices(tipos, pesos)[0]
        marca = rnd.choice(TIPOS[tipo][1])
        compra = HOY - timedelta(days=rnd.randint(60, 365 * 9))
        garantia = compra + timedelta(days=365 * rnd.choice([1, 2, 3]))
        es_pc = tipo in ("Portátil", "Escritorio")
        antiguedad = (HOY - compra).days / 365
        estado = rnd.choices(["Asignado", "Disponible", "En mantenimiento", "Dado de baja"],
                             [0.72, 0.12, 0.08, 0.08 if antiguedad > 6 else 0.01])[0]
        condicion = "Malo" if estado == "Dado de baja" else rnd.choices(
            ["Bueno", "Regular", "Malo"], [0.7, 0.22, 0.08] if antiguedad < 5 else [0.4, 0.4, 0.2])[0]
        sede = rnd.choices([s[0] for s in SEDES], [0.55, 0.2, 0.17, 0.08])[0]
        custodio = rnd.choice(personas) if estado == "Asignado" else ("", "", rnd.choice(AREAS))
        ult_mant = compra + timedelta(days=rnd.randint(0, max(1, (HOY - compra).days)))
        placa = f"VYE-{i:04d}"
        activos.append({
            "Title": placa,
            "Serial": f"{marca[:2].upper()}{rnd.randint(10**7, 10**8 - 1)}",
            "TipoActivo": tipo,
            "Marca": marca,
            "Modelo": f"{marca[:3].upper()}-{rnd.randint(100, 999)}",
            "Procesador": rnd.choice(PROCESADORES) if es_pc else "",
            "RAM_GB": rnd.choice([4, 8, 8, 16, 16, 32]) if es_pc else "",
            "Almacenamiento_GB": rnd.choice([256, 512, 512, 1000]) if es_pc else "",
            "SistemaOperativo": rnd.choice(["Windows 10 Pro", "Windows 11 Pro", "Windows 11 Pro"]) if es_pc else "",
            "FechaCompra": compra.isoformat(),
            "FechaFinGarantia": garantia.isoformat(),
            "ValorCompra": {"Portátil": 3_800_000, "Escritorio": 3_200_000, "Monitor": 750_000,
                            "Impresora": 1_500_000, "Periférico": 120_000, "Móvil": 1_100_000,
                            "Equipo de red": 2_400_000}[tipo] + rnd.randint(-15, 25) * 10_000,
            "Estado": estado,
            "Condicion": condicion,
            "Sede": sede,
            "Area": custodio[2],
            "CustodioNombre": custodio[0],
            "CustodioCorreo": custodio[1],
            "UltimoMantenimiento": ult_mant.isoformat(),
            "ProximoMantenimiento": (ult_mant + timedelta(days=180)).isoformat() if es_pc else "",
            "Observaciones": "",
        })
        if estado == "Asignado":
            asignaciones.append({
                "Title": f"MOV-{len(asignaciones) + 1:05d}", "Activo": placa, "TipoMovimiento": "Asignación",
                "CustodioNombre": custodio[0], "CustodioCorreo": custodio[1], "Area": custodio[2],
                "SedeDestino": sede, "FechaMovimiento": (compra + timedelta(days=rnd.randint(1, 30))).isoformat(),
                "RegistradoPor": "Mesa de ayuda TI", "ActaAceptada": "Sí", "Observaciones": "Carga inicial",
            })
        if es_pc and rnd.random() < 0.6:
            correctivo = rnd.random() < 0.3
            mantenimientos.append({
                "Title": f"MNT-{len(mantenimientos) + 1:05d}", "Activo": placa,
                "TipoMantenimiento": "Correctivo" if correctivo else "Preventivo",
                "EstadoMantenimiento": "En curso" if estado == "En mantenimiento" else "Finalizado",
                "FechaProgramada": ult_mant.isoformat(),
                "FechaRealizada": "" if estado == "En mantenimiento" else ult_mant.isoformat(),
                "Tecnico": rnd.choice(["Técnico TI 1", "Técnico TI 2", "Proveedor externo"]),
                "Costo": rnd.choice([0, 0, 80_000, 150_000, 350_000]) if correctivo else 0,
                "Descripcion": rnd.choice(["Limpieza y actualización", "Cambio de disco a SSD",
                                           "Ampliación de RAM", "Reinstalación de SO", "Revisión general"]),
            })

    for nombre, filas in (("activos.csv", activos), ("asignaciones.csv", asignaciones),
                          ("mantenimientos.csv", mantenimientos)):
        with open(salida / nombre, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0]))
            w.writeheader()
            w.writerows(filas)

    with open(salida / "usuarios_app.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Title", "Correo", "Rol", "Habilitado"])
        w.writerow(["Administrador TI (reemplazar)", "admin@tu-dominio.com", "Administrador", "Sí"])
        w.writerow(["Auxiliar inventario (reemplazar)", "inventario@tu-dominio.com", "Inventario", "Sí"])
        w.writerow(["Consulta gerencia (reemplazar)", "gerencia@tu-dominio.com", "Consulta", "Sí"])

    print(f"Activos: {len(activos)} | Asignaciones: {len(asignaciones)} | Mantenimientos: {len(mantenimientos)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--activos", type=int, default=500)
    p.add_argument("--salida", type=Path, default=Path("data"))
    a = p.parse_args()
    generar(a.activos, a.salida)
