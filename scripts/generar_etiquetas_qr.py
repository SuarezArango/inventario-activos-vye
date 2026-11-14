"""Genera etiquetas con código QR para las placas de los activos (HU-06).

El QR contiene solo la placa (p. ej. "VYE-0001"), que es lo que lee el control
"Lector de código de barras" de la pantalla VerificacionScreen en Power Apps.

Uso:
    python scripts/generar_etiquetas_qr.py              # primeras 20 placas
    python scripts/generar_etiquetas_qr.py 1 500        # rango de placas
Salida: docs/etiquetas_qr.pdf (hoja carta, 4 columnas x 5 filas)
"""
import csv
import sys
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

RAIZ = Path(__file__).resolve().parent.parent
desde = int(sys.argv[1]) if len(sys.argv) > 1 else 1
hasta = int(sys.argv[2]) if len(sys.argv) > 2 else 20

with open(RAIZ / "data" / "activos.csv", encoding="utf-8-sig") as f:
    activos = list(csv.DictReader(f))[desde - 1:hasta]

salida = RAIZ / "docs" / "etiquetas_qr.pdf"
c = canvas.Canvas(str(salida), pagesize=letter)
c.setTitle("Etiquetas QR - Inventario de activos TI - Vías y Explanaciones")
ancho_pag, alto_pag = letter
cols, filas = 4, 5
margen = 12 * mm
celda_w = (ancho_pag - 2 * margen) / cols
celda_h = (alto_pag - 2 * margen) / filas
lado_qr = 32 * mm

for i, a in enumerate(activos):
    if i and i % (cols * filas) == 0:
        c.showPage()
    pos = i % (cols * filas)
    x = margen + (pos % cols) * celda_w
    y = alto_pag - margen - (pos // cols + 1) * celda_h
    c.setDash(2, 2)
    c.setStrokeGray(0.6)
    c.rect(x + 2, y + 2, celda_w - 4, celda_h - 4)
    c.setDash()

    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + celda_w / 2, y + celda_h - 12, "VÍAS Y EXPLANACIONES · ACTIVO TI")
    qr = QrCodeWidget(a["Title"], barLevel="M")
    b = qr.getBounds()
    d = Drawing(lado_qr, lado_qr, transform=[lado_qr / (b[2] - b[0]), 0, 0, lado_qr / (b[3] - b[1]), 0, 0])
    d.add(qr)
    renderPDF.draw(d, c, x + (celda_w - lado_qr) / 2, y + celda_h - 16 - lado_qr)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(x + celda_w / 2, y + 26, a["Title"])
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + celda_w / 2, y + 15, f'{a["TipoActivo"]} {a["Marca"]} · S/N {a["Serial"]}')

c.save()
print(f"{len(activos)} etiquetas -> {salida}")
