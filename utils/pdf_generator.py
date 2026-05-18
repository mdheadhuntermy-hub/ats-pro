from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


def generar_pdf_dictamen(
    nombre,
    vacante,
    match,
    estado,
    skills,
    dictamen,
    output_path
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elementos = []

    titulo = Paragraph(
        "<b>MDHEADHUNTER ATS PRO ELITE</b>",
        styles["Title"]
    )

    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    subtitulo = Paragraph(
        "<b>DICTAMEN EJECUTIVO DEL CANDIDATO</b>",
        styles["Heading2"]
    )

    elementos.append(subtitulo)
    elementos.append(Spacer(1, 20))

    data = [
        ["Nombre", nombre],
        ["Vacante", vacante],
        ["Match IA", f"{match}%"],
        ["Estado", estado]
    ]

    tabla = Table(
        data,
        colWidths=[150, 320]
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 25))

    skills_texto = Paragraph(
        f"<b>Comentarios RH:</b><br/><br/>{skills}",
        styles["BodyText"]
    )

    elementos.append(skills_texto)
    elementos.append(Spacer(1, 20))

    dictamen_texto = Paragraph(
        f"<b>Conclusión IA:</b><br/><br/>{dictamen}",
        styles["BodyText"]
    )

    elementos.append(dictamen_texto)
    elementos.append(Spacer(1, 40))

    firma = Paragraph(
        "<b>MDHEADHUNTER</b><br/>Área de Reclutamiento Ejecutivo",
        styles["Normal"]
    )

    elementos.append(firma)

    doc.build(elementos)
def generar_pdf_simple_dictamen(
    titulo,
    nombre,
    vacante,
    dictamen,
    output_path
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(
            "<b>MDHEADHUNTER ATS PRO ELITE</b>",
            styles["Title"]
        )
    )

    elementos.append(Spacer(1, 20))

    elementos.append(
        Paragraph(
            f"<b>{titulo}</b>",
            styles["Heading2"]
        )
    )

    elementos.append(Spacer(1, 20))

    data = [
        ["Candidato", nombre],
        ["Vacante", vacante]
    ]

    tabla = Table(
        data,
        colWidths=[150, 320]
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 25))

    elementos.append(
        Paragraph(
            dictamen.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    elementos.append(Spacer(1, 40))

    elementos.append(
        Paragraph(
            "<b>MDHEADHUNTER</b><br/>Área de Reclutamiento Ejecutivo",
            styles["Normal"]
        )
    )

    doc.build(elementos)