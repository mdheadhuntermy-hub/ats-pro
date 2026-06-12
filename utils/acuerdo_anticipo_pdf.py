from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
import os


AZUL = colors.HexColor("#06244a")
DORADO = colors.HexColor("#d6a642")
NEGRO = colors.HexColor("#111827")
GRIS = colors.HexColor("#4b5563")


def money(valor):
    return f"${valor:,.2f} MXN"


def generar_pdf_acuerdo_anticipo(
    output_path,
    fecha,
    empresa,
    contacto,
    puesto,
    vacantes,
    salario,
    porcentaje,
    honorarios,
    anticipo,
    iva,
    total
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=35,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "Titulo",
        parent=styles["Title"],
        fontSize=15,
        leading=19,
        textColor=AZUL,
        alignment=1
    )

    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Heading2"],
        fontSize=11,
        leading=14,
        textColor=AZUL,
        spaceBefore=10,
        spaceAfter=6
    )

    texto = ParagraphStyle(
        "Texto",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        textColor=NEGRO,
        alignment=TA_JUSTIFY
    )

    texto_normal = ParagraphStyle(
        "TextoNormal",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        textColor=NEGRO
    )

    encabezado_tabla = ParagraphStyle(
        "EncabezadoTabla",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    elementos = []

    logo_path = "assets/logo_mdheadhunter.jpg"

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=190,
            height=70
        )

        encabezado = Table(
            [[logo, ""]],
            colWidths=[230, 280]
        )

        encabezado.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEBELOW", (0, 0), (-1, -1), 1, DORADO),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))

        elementos.append(encabezado)
        elementos.append(Spacer(1, 14))

    elementos.append(
        Paragraph(
            "<b>ACUERDO DE ANTICIPO PARA SERVICIOS DE RECLUTAMIENTO</b>",
            titulo
        )
    )

    elementos.append(Spacer(1, 14))

    elementos.append(
        Paragraph(
            """
            <b>Entre:</b><br/>
            <b>MDHEADHUNTER</b>, con domicilio en Monterrey, Nuevo León, México,
            representada en este acto por Diana Patricia Acosta Vélez, en adelante
            <b>"La Agencia"</b>.
            """,
            texto
        )
    )

    elementos.append(Spacer(1, 8))

    elementos.append(
        Paragraph(
            f"""
            <b>Y</b><br/>
            <b>{empresa.upper()}</b>, representada en este acto por {contacto if contacto else "su representante autorizado"},
            en adelante <b>"El Cliente"</b>.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "OBJETO",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            El Cliente contrata a La Agencia para llevar a cabo el proceso de reclutamiento
            y selección de personal para la siguiente vacante:
            """,
            texto
        )
    )

    tabla = Table(
        [
            [
                Paragraph("<b>Puesto</b>", encabezado_tabla),
                Paragraph("<b>Vacantes</b>", encabezado_tabla),
                Paragraph("<b>Salario mensual</b>", encabezado_tabla),
                Paragraph("<b>Comisión</b>", encabezado_tabla),
                Paragraph("<b>Total comisión</b>", encabezado_tabla),
                Paragraph("<b>Anticipo 30%</b>", encabezado_tabla),
            ],
            [
                Paragraph(puesto, texto_normal),
                Paragraph(str(vacantes), texto_normal),
                Paragraph(money(salario), texto_normal),
                Paragraph(f"{porcentaje:.0f}%", texto_normal),
                Paragraph(money(honorarios), texto_normal),
                Paragraph(money(anticipo), texto_normal),
            ]
        ],
        colWidths=[130, 55, 90, 60, 90, 90]
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elementos.append(Spacer(1, 8))
    elementos.append(tabla)

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            f"""
            <b>Total vacantes:</b> {vacantes}<br/>
            <b>Total comisión agencia:</b> {money(honorarios)} más IVA.<br/>
            <b>Anticipo 30%:</b> {money(anticipo)} más IVA.<br/>
            <b>IVA 16% sobre anticipo:</b> {money(iva)}<br/>
            <b>Total anticipo a pagar:</b> {money(total)}
            """,
            texto_normal
        )
    )

    elementos.append(
        Paragraph(
            "ANTICIPO",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            f"""
            Para iniciar el proceso de reclutamiento, El Cliente se compromete a realizar
            un pago anticipado equivalente al 30% de la comisión acordada, es decir,
            <b>{money(anticipo)} más IVA</b>. El saldo restante equivalente al 70%
            de la comisión será facturado al momento en que el candidato seleccionado
            acepte formalmente la oferta laboral o inicie labores con El Cliente, lo que ocurra primero.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "CONDICIONES DEL SERVICIO",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            1. La Agencia iniciará el proceso una vez recibido el anticipo correspondiente.<br/>
            2. La Agencia emitirá el CFDI correspondiente al anticipo recibido.<br/>
            3. El saldo restante equivalente al 70% de la comisión será facturado al momento
            en que el candidato seleccionado acepte formalmente la oferta laboral o inicie labores
            con El Cliente, lo que ocurra primero.<br/>
            4. En caso de cancelación por parte de El Cliente una vez iniciado el proceso,
            el anticipo no será reembolsable.<br/>
            5. La Agencia presentará candidatos que cumplan razonablemente con el perfil
            proporcionado por El Cliente.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "GARANTÍA DE REPOSICIÓN",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            En caso de que el candidato contratado renuncie voluntariamente o sea dado de baja
            dentro del periodo de garantía aplicable por causas no atribuibles a El Cliente,
            La Agencia realizará una reposición sin costo adicional por una única ocasión.
            Para perfiles operativos y administrativos la garantía será de 30 días naturales;
            para perfiles gerenciales o directivos será de 45 días naturales.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "CONTRATACIÓN DE CANDIDATOS PRESENTADOS",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            Si El Cliente contrata directa o indirectamente a cualquier candidato presentado
            por La Agencia dentro de los doce (12) meses posteriores a su presentación,
            se generará el derecho al cobro total de la comisión pactada.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "DEVOLUCIÓN DEL ANTICIPO",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            En caso de que La Agencia no presente al menos tres candidatos que cumplan
            razonablemente con el perfil solicitado dentro de los treinta (30) días naturales
            posteriores al inicio formal de la búsqueda, El Cliente podrá solicitar por escrito
            la devolución del anticipo, misma que será realizada dentro de los quince (15)
            días hábiles siguientes a la solicitud.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "CONFIDENCIALIDAD",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            Ambas partes se comprometen a mantener estricta confidencialidad respecto de
            la información comercial, financiera, operativa y de candidatos intercambiada
            durante la prestación del servicio.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "FORMA DE PAGO",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            Banco: BBVA<br/>
            Cuenta: 1595219099<br/>
            CLABE: 012580015952190998<br/>
            Titular: Diana Patricia Acosta Vélez
            """,
            texto_normal
        )
    )

    elementos.append(
        Paragraph(
            "ACEPTACIÓN",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            """
            Las partes manifiestan su conformidad con los términos del presente acuerdo
            y lo firman en Monterrey, Nuevo León, a la fecha de su suscripción.
            """,
            texto
        )
    )

    elementos.append(Spacer(1, 25))

    firmas = Table(
        [
            [
                Paragraph("_____________________________<br/>Diana Patricia Acosta Vélez<br/>MDHEADHUNTER", texto_normal),
                Paragraph(f"_____________________________<br/>Representante Autorizado<br/>{empresa.upper()}", texto_normal)
            ],
            [
                Paragraph("Fecha: ________________", texto_normal),
                Paragraph("Fecha: ________________", texto_normal)
            ]
        ],
        colWidths=[250, 250]
    )

    firmas.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))

    elementos.append(firmas)

    doc.build(elementos)