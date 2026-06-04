from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os


AZUL = colors.HexColor("#06244a")
DORADO = colors.HexColor("#d6a642")
GRIS = colors.HexColor("#4b5563")
NEGRO = colors.HexColor("#111827")


def limpiar_texto(texto):

    if texto is None:
        return ""

    return str(texto).replace("&", "&amp;").replace("\n", "<br/>").strip()


def agregar_linea(label, valor):

    if valor and str(valor).strip():
        return f"• <b>{label}:</b> {limpiar_texto(valor)}<br/>"

    return ""


def generar_pdf_propuesta(
    output_path,
    fecha,
    cliente,
    contacto,
    empresa,
    servicio,
    perfil,
    honorarios,
    anticipo,
    garantia,
    vigencia,
    condiciones,
    tipo_documento="Propuesta Comercial"
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    seccion = ParagraphStyle(
        "Seccion",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=AZUL,
        spaceBefore=12,
        spaceAfter=8
    )

    texto = ParagraphStyle(
        "Texto",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=NEGRO,
        alignment=TA_JUSTIFY
    )

    texto_normal = ParagraphStyle(
        "TextoNormal",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=NEGRO
    )

    texto_blanco = ParagraphStyle(
        "TextoBlanco",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=colors.white,
        alignment=TA_JUSTIFY
    )

    encabezado_tabla = ParagraphStyle(
        "EncabezadoTabla",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=colors.white
    )

    footer = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=GRIS,
        alignment=TA_CENTER
    )

    elementos = []

    logo_path = "assets/logo_mdheadhunter.jpg"

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=200,
            height=75
        )

        encabezado = Table(
            [[logo, ""]],
            colWidths=[240, 240]
        )

        encabezado.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEBELOW", (0, 0), (-1, -1), 1, DORADO),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))

        elementos.append(encabezado)

    else:

        elementos.append(
            Paragraph(
                "<b>MDHEADHUNTER</b><br/>RECLUTADOR ESTRATÉGICO",
                seccion
            )
        )

    elementos.append(Spacer(1, 18))

    dirigido = ""

    if empresa and empresa.strip():
        dirigido += f"<b>{limpiar_texto(empresa).upper()}</b>"

    elif cliente and cliente.strip():
        dirigido += f"<b>{limpiar_texto(cliente).upper()}</b>"

    if contacto and contacto.strip():
        dirigido += f"<br/>Contacto: {limpiar_texto(contacto)}"

    datos = [
        [
            Paragraph(
                "<b>DIRIGIDO A:</b><br/>" + dirigido,
                texto_normal
            ),
            Paragraph(
                "<b>FECHA:</b><br/>" + limpiar_texto(fecha),
                texto_normal
            )
        ]
    ]

    tabla_datos = Table(
        datos,
        colWidths=[250, 230]
    )

    tabla_datos.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, colors.HexColor("#d1d5db")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    elementos.append(tabla_datos)
    elementos.append(Spacer(1, 20))

    elementos.append(
        Paragraph(
            "Estimados, es un placer saludarle. Agradecemos la oportunidad de presentarle nuestra "
            "propuesta de colaboración técnica para la gestión de su capital humano.",
            texto
        )
    )

    elementos.append(
        Paragraph(
            "1. NUESTRO COMPROMISO ESTRATÉGICO",
            seccion
        )
    )

    nombre_empresa = empresa if empresa else cliente

    elementos.append(
        Paragraph(
            f"""
            En MDHEADHUNTER, no solo cubrimos vacantes; identificamos el motor del éxito de su empresa.
            Nuestro proceso se basa en una metodología de selección 360° que garantiza que cada candidato
            no solo cumpla con las habilidades técnicas, sino que posea los valores y la ética necesarios
            para integrarse a <b>{limpiar_texto(nombre_empresa).upper()}</b> de manera inmediata y productiva.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "2. METODOLOGÍA Y ALCANCE INTEGRAL",
            seccion
        )
    )

    elementos.append(
        Paragraph(
            """
            Cada proceso contratado incluye filtros de seguridad, evaluación y validación profesional:<br/><br/>
            • <b>Inteligencia de Datos y Seguridad:</b> Validación documental y análisis preventivo de riesgos.<br/>
            • <b>Verificación de Trayectoria:</b> Validación de experiencia, referencias laborales y competencias clave.<br/>
            • <b>Evaluación Psicométrica:</b> Aplicación de herramientas para medir personalidad, honestidad, liderazgo y ajuste al puesto.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "3. ESQUEMA DE INVERSIÓN",
            seccion
        )
    )

    elementos.append(
        Paragraph(
            "Nuestros honorarios se calculan con base en el nivel de responsabilidad de la posición "
            "y el sueldo base mensual bruto del candidato seleccionado.",
            texto
        )
    )

    tabla_honorarios = Table(
        [
            [
                Paragraph("<b>CATEGORÍA DE PERFIL</b>", encabezado_tabla),
                Paragraph("<b>HONORARIOS</b>", encabezado_tabla)
            ],
            [
                Paragraph("<b>Perfiles Operativos:</b> Personal de línea, auxiliares y técnicos.", texto_normal),
                Paragraph("60%", texto_normal)
            ],
            [
                Paragraph("<b>Perfiles Administrativos:</b> Coordinaciones, analistas y mandos medios.", texto_normal),
                Paragraph("80%", texto_normal)
            ],
            [
                Paragraph("<b>Dirección y Gerencia:</b> Liderazgo estratégico y alta dirección.", texto_normal),
                Paragraph("100%", texto_normal)
            ],
        ],
        colWidths=[370, 100]
    )

    tabla_honorarios.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elementos.append(Spacer(1, 10))
    elementos.append(tabla_honorarios)

    elementos.append(PageBreak())

    garantia_box = Table(
        [[
            Paragraph(
                f"""
                <b><font color='#d6a642'>RESPALDO Y GARANTÍA DE SATISFACCIÓN</font></b><br/><br/>
                Confiamos plenamente en nuestro proceso. Por ello, si el colaborador causa baja
                por motivo imputable a su desempeño o renuncia voluntaria, MDHEADHUNTER repondrá
                la posición sin costo adicional conforme a la garantía establecida:<br/><br/>
                {limpiar_texto(garantia)}
                """,
                texto_blanco
            )
        ]],
        colWidths=[470]
    )

    garantia_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL),
        ("BOX", (0, 0), (-1, -1), 0.5, AZUL),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
    ]))

    elementos.append(garantia_box)
    elementos.append(Spacer(1, 24))

    elementos.append(
        Paragraph(
            "4. TÉRMINOS Y CONDICIONES COMERCIALES",
            seccion
        )
    )

    texto_condiciones = ""
    texto_condiciones += agregar_linea("Servicio", servicio)
    texto_condiciones += agregar_linea("Perfil / Vacante", perfil)
    texto_condiciones += agregar_linea("Honorarios", honorarios)
    texto_condiciones += agregar_linea("Anticipo", anticipo)
    texto_condiciones += agregar_linea("Vigencia", vigencia)

    if condiciones and condiciones.strip():
        texto_condiciones += "<br/>" + limpiar_texto(condiciones)

    elementos.append(
        Paragraph(
            texto_condiciones,
            texto
        )
    )

    info_servicio = []

    if servicio:
        info_servicio.append(["Servicio:", limpiar_texto(servicio)])

    if perfil:
        info_servicio.append(["Perfil / Vacante:", limpiar_texto(perfil)])

    if honorarios:
        info_servicio.append(["Honorarios:", limpiar_texto(honorarios)])

    if anticipo:
        info_servicio.append(["Anticipo:", limpiar_texto(anticipo)])

    if vigencia:
        info_servicio.append(["Vigencia:", limpiar_texto(vigencia)])

    if info_servicio:

        tabla_info = Table(
            [[
                Paragraph("<b>Nivel del servicio contratado</b>", texto_normal),
                ""
            ]] + [
                [
                    Paragraph(f"<b>{fila[0]}</b>", texto_normal),
                    Paragraph(fila[1], texto_normal)
                ]
                for fila in info_servicio
            ],
            colWidths=[180, 290]
        )

        tabla_info.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f3f4f6")),
            ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#e5e7eb")),
            ("SPAN", (0, 0), (-1, 0)),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))

        elementos.append(Spacer(1, 18))
        elementos.append(tabla_info)

    elementos.append(Spacer(1, 35))

    elementos.append(
        Paragraph(
            "_____________________________<br/>Aceptación " + limpiar_texto(nombre_empresa),
            texto_normal
        )
    )

    elementos.append(Spacer(1, 35))

    elementos.append(
        Paragraph(
            "MDHEADHUNTER RECLUTADOR ESTRATÉGICO | admi@mdheadhunter.com.mx<br/>"
            '"Mejores decisiones para su organización"',
            footer
        )
    )

    doc.build(elementos)