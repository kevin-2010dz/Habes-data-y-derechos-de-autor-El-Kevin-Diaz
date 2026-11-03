#!/usr/bin/env python3
"""Build the integrated Spanish Activity 4 hand-in PDF from repository docs."""

from __future__ import annotations

import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "Actividad 4.pdf"


def inline_markup(text: str) -> str:
    """Translate the limited inline Markdown used by these source files."""
    pieces: list[str] = []
    cursor = 0
    link_re = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    for match in link_re.finditer(text):
        pieces.append(escape(text[cursor:match.start()]))
        label, url = match.groups()
        pieces.append(f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#155E91">{escape(label)}</link>')
        cursor = match.end()
    pieces.append(escape(text[cursor:]))
    value = "".join(pieces)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    return value


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("DocTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#12304A"), alignment=TA_CENTER, spaceAfter=12),
        "subtitle": ParagraphStyle("Subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=13, leading=18, textColor=colors.HexColor("#34516B"), alignment=TA_CENTER, spaceAfter=8),
        "h1": ParagraphStyle("H1Custom", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=colors.HexColor("#12304A"), spaceBefore=8, spaceAfter=9, keepWithNext=True),
        "h2": ParagraphStyle("H2Custom", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#155E91"), spaceBefore=10, spaceAfter=6, keepWithNext=True),
        "h3": ParagraphStyle("H3Custom", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#1D405A"), spaceBefore=8, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("BodyCustom", parent=base["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13.2, textColor=colors.HexColor("#18232C"), alignment=TA_LEFT, spaceAfter=6),
        "bullet": ParagraphStyle("BulletCustom", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, leftIndent=14, firstLineIndent=-9, textColor=colors.HexColor("#18232C"), spaceAfter=3),
        "small": ParagraphStyle("SmallCustom", parent=base["BodyText"], fontName="Helvetica", fontSize=8.2, leading=11, textColor=colors.HexColor("#4A5864"), spaceAfter=4),
        "table": ParagraphStyle("TableCustom", parent=base["BodyText"], fontName="Helvetica", fontSize=7.4, leading=9.3, textColor=colors.HexColor("#18232C"), spaceAfter=1),
        "tablehead": ParagraphStyle("TableHeadCustom", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=7.5, leading=9.4, textColor=colors.white, spaceAfter=1),
    }


def markdown_flows(markdown: str, styles: dict, start_part_pages: bool = False):
    lines = markdown.splitlines()
    flows = []
    paragraph_lines: list[str] = []
    index = 0
    list_kind = None

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(s.strip() for s in paragraph_lines).strip()
            if text:
                flows.append(Paragraph(inline_markup(text), styles["body"]))
            paragraph_lines = []

    while index < len(lines):
        line = lines[index].rstrip()
        if not line.strip():
            flush_paragraph()
            list_kind = None
            index += 1
            continue

        if line.startswith("|"):
            flush_paragraph()
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            rows = []
            for table_line in table_lines:
                cells = [cell.strip() for cell in table_line.strip("|").split("|")]
                if cells and all(re.fullmatch(r":?-{2,}:?", cell.replace(" ", "")) for cell in cells):
                    continue
                rows.append(cells)
            if rows:
                width_count = max(len(row) for row in rows)
                rows = [row + [""] * (width_count - len(row)) for row in rows]
                wrapped = []
                for row_index, row in enumerate(rows):
                    style = styles["tablehead"] if row_index == 0 else styles["table"]
                    wrapped.append([Paragraph(inline_markup(cell), style) for cell in row])
                widths = [172 * mm / width_count] * width_count
                table = Table(wrapped, colWidths=widths, repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#155E91")),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B9C7D1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F7FA")]),
                ]))
                flows.extend([Spacer(1, 3), table, Spacer(1, 6)])
            continue

        if line.startswith("#"):
            flush_paragraph()
            level = len(line) - len(line.lstrip("#"))
            heading = line[level:].strip()
            if start_part_pages and level == 2 and re.match(r"Parte\s+3\b", heading, re.I):
                flows.append(PageBreak())
            style = styles["h1"] if level == 1 else styles["h2"] if level == 2 else styles["h3"]
            flows.append(Paragraph(inline_markup(heading), style))
            index += 1
            continue

        if line.startswith(">"):
            flush_paragraph()
            quote = line.lstrip("> ").strip()
            quote_style = ParagraphStyle("Quote", parent=styles["small"], leftIndent=8, borderColor=colors.HexColor("#C4D4E0"), borderWidth=0, textColor=colors.HexColor("#405565"))
            flows.append(Paragraph(inline_markup(quote), quote_style))
            index += 1
            continue

        bullet_match = re.match(r"^\s*(?:[-+]\s+|\d+\.\s+)(.+)$", line)
        if bullet_match:
            flush_paragraph()
            bullet = "-"
            flows.append(Paragraph(f"{bullet} {inline_markup(bullet_match.group(1))}", styles["bullet"]))
            list_kind = "list"
            index += 1
            continue

        if re.fullmatch(r"-{3,}", line.strip()):
            flush_paragraph()
            flows.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCD8E0"), spaceBefore=4, spaceAfter=8))
            index += 1
            continue

        paragraph_lines.append(line)
        index += 1

    flush_paragraph()
    return flows


def footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#CBD6DE"))
    canvas.setLineWidth(0.5)
    canvas.line(19 * mm, 16 * mm, width - 19 * mm, 16 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#536472"))
    canvas.drawString(19 * mm, 10.5 * mm, "Actividad 4 | Guía de aprendizaje SENA")
    canvas.drawRightString(width - 19 * mm, 10.5 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4, rightMargin=19 * mm, leftMargin=19 * mm,
        topMargin=19 * mm, bottomMargin=22 * mm,
        title="Actividad 4 - Habeas Data, derechos de autor y copias de seguridad",
        author="Kevin Díaz",
        subject="Guía de aprendizaje SENA 03_04",
    )
    story = [Spacer(1, 20 * mm), Paragraph("ACTIVIDAD 4", styles["title"]),
             Paragraph("Habeas Data, derechos de autor y tipos de copia de seguridad", styles["subtitle"]),
             Spacer(1, 8 * mm), HRFlowable(width="70%", thickness=2, color=colors.HexColor("#155E91"), hAlign="CENTER", spaceAfter=10 * mm)]
    cover = [
        ("Aprendiz", "Kevin Díaz"),
        ("Programa", "Técnico en Sistemas Teleinformáticas, código 233108 V1"),
        ("Proyecto", "Integración de servicios tecnológicos, hardware, software y redes de datos en una mesa de ayuda (2093369)"),
        ("Fase", "Planeación"),
        ("Competencia", "220501121 - Operación de herramientas informáticas"),
        ("Resultado de aprendizaje", "RAP 03 - Planificar la información según criterios de ciberseguridad"),
        ("Fecha", "2 de noviembre de 2026"),
    ]
    for label, value in cover:
        story.append(Paragraph(f"<b>{escape(label)}:</b> {escape(value)}", styles["body"]))
    story.extend([Spacer(1, 10 * mm), Paragraph("Introducción", styles["h2"]),
                  Paragraph("Esta entrega desarrolla los seis apartados de la guía de aprendizaje y relaciona sus ejercicios con la protección de datos, el respeto a los derechos de autor y la disponibilidad de la información en una mesa de ayuda. Los formatos y controles se presentan como propuestas académicas para adaptar y aprobar antes de aplicarlos en una organización real.", styles["body"]),
                  Paragraph("Objetivos", styles["h2"]),
                  Paragraph("- Analizar casos de tratamiento de datos personales y uso de obras protegidas.<br/>- Identificar normas y autoridades colombianas relevantes.<br/>- Proponer controles de acceso, monitoreo, mejora y respaldo.<br/>- Entregar un consentimiento modelo, un póster y procedimientos verificables.", styles["body"]),
                  Paragraph("Justificación", styles["h2"]),
                  Paragraph("La mesa de ayuda puede tratar datos personales, configuraciones, inventarios y registros. Definir finalidades, permisos, trazabilidad y restauración ayuda a reducir accesos indebidos y pérdidas de información; verificar licencias protege el trabajo de autores y titulares.", styles["body"]),
                  PageBreak()])

    main_case = (ROOT / "docs/05_habeas_data_derechos_autor/marco_normativo_y_casos.md").read_text(encoding="utf-8")
    main_case = re.sub(r"^# Actividad 4:.*\n+", "", main_case, count=1)
    story.extend(markdown_flows(main_case, styles, start_part_pages=True))

    consent = (ROOT / "docs/05_habeas_data_derechos_autor/formato_autorizacion_tratamiento.md").read_text(encoding="utf-8")
    story.extend(markdown_flows(consent, styles))

    presentation = (ROOT / "docs/05_habeas_data_derechos_autor/guion_presentacion.md").read_text(encoding="utf-8")
    story.extend(markdown_flows(presentation, styles))

    backup = (ROOT / "docs/04_backups/plan_y_prueba_recuperacion.md").read_text(encoding="utf-8")
    story.append(PageBreak())
    story.extend(markdown_flows(backup, styles))

    story.extend([PageBreak(), Paragraph("Materiales complementarios en el repositorio", styles["h1"]),
                  Paragraph("El póster de herramientas se adjunta como archivo SVG en docs/04_backups/poster_herramientas_backup.svg. Los scripts de ejemplo están en scripts/backup.py y scripts/audit_access_log.py; se verificaron en un entorno local de prueba con datos ficticios. El script de respaldo genera un ZIP y verifica hashes SHA-256, pero no cifra ni sustituye un producto empresarial.", styles["body"]),
                  Paragraph("Fuentes y alcance", styles["h2"]),
                  Paragraph("Las referencias oficiales de normas, autoridades y sanción están incluidas en la Parte 3. La revisión normativa corresponde al 2 de noviembre de 2026; verificar el texto vigente antes de utilizar estas propuestas como políticas reales. El guion de presentación es una base de narración y no constituye una publicación en Powtoon ni un archivo de audio.", styles["body"]),
                  Paragraph("Evidencia de práctica de backup", styles["h2"]),
                  Paragraph("Para la entrega práctica, registrar una copia creada con la herramienta seleccionada, adjuntar evidencia permitida y completar la prueba de restauración en templates/registro_prueba_restauracion.csv. No incluir información de clientes, credenciales ni respaldos reales en un repositorio público.", styles["body"])])

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__":
    build()
