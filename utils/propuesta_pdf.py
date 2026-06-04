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

    nombre_empresa = empresa if empresa else cliente

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
            f"""
            Estimados representantes de <b>{limpiar_texto(nombre_empresa).upper()}</b>:<br/><br/>
            Agradecemos la oportunidad de presentar nuestra propuesta comercial para apoyarlos
            en la atracción, evaluación y selección de talento especializado.
            """,
            texto
        )
    )

    elementos.append(
        Paragraph(
            "1. NUESTRO COMPROMISO ESTRATÉGICO",
            seccion
        )
    )

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
                Paragraph("60% del salario mensual bruto", texto_normal)
            ],
            [
                Paragraph("<b>Perfiles Administrativos:</b> Coordinaciones, analistas y mandos medios.", texto_normal),
                Paragraph("80% del salario mensual bruto", texto_normal)
            ],
            [
                Paragraph("<b>Dirección y Gerencia:</b> Liderazgo estratégico y alta dirección.", texto_normal),
                Paragraph("100% del salario mensual bruto", texto_normal)
            ],
        ],
        colWidths=[330, 140]
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

    elementos.append(Spacer(1, 6))
    elementos.append(
        Paragraph(
            "<i>* Los honorarios se calculan sobre el salario mensual bruto del candidato contratado. Precios más IVA.</i>",
            texto_normal
        )
    )

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

    elementos.append(Spacer(1, 12))

    elementos.append(
        Paragraph(
            """
            <b>Condiciones de pago:</b><br/>
	    • Para iniciar el proceso de búsqueda, se requiere un anticipo equivalente al 30% de los honorarios del servicio contratado.<br/>
	    • El 70% restante será facturado y pagadero al ingreso o contratación del candidato seleccionado.<br/>
	    • Los honorarios se calculan sobre el salario mensual bruto del candidato contratado, de acuerdo con el nivel del perfil solicitado.<br/>
	    • El pago deberá realizarse dentro de los 3 días naturales posteriores a la emisión de la factura, salvo acuerdo distinto por escrito.<br/>
	    • Los precios y honorarios indicados no incluyen IVA, salvo que se especifique expresamente lo contrario.
            """,
            texto
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            """
            <b>Exclusividad de la vacante:</b><br/>
            La presente propuesta no implica exclusividad salvo acuerdo expreso por escrito.
            En caso de búsqueda exclusiva, MDHEADHUNTER será el proveedor autorizado para la gestión del proceso
            durante la vigencia acordada.
            """,
            texto
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            """
            <b>Contratación posterior de candidatos:</b><br/>
            Si la empresa contratante incorpora a cualquier candidato presentado por MDHEADHUNTER dentro de los
            12 meses posteriores a su presentación, se generarán los honorarios correspondientes conforme al perfil contratado.
            """,
            texto
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            """
            <b>Excepciones de garantía:</b><br/>
            La garantía quedará sin efecto si la baja del colaborador se debe a cambios en las condiciones laborales,
            incumplimiento de prestaciones, falta de herramientas de trabajo, modificación de salario, clima laboral desfavorable,
            reestructura interna, cambio de jefe directo, malos tratos o causas ajenas al desempeño del candidato.
            """,
            texto
        )
    )


    elementos.append(Spacer(1, 25))

    firma_data = [
        [
            Paragraph("_____________________________<br/>Nombre y firma", texto_normal),
            Paragraph("_____________________________<br/>Cargo", texto_normal)
        ],
        [
            Paragraph("_____________________________<br/>Fecha de aceptación", texto_normal),
            Paragraph("_____________________________<br/>Empresa", texto_normal)
        ],
    ]

    tabla_firmas = Table(
        firma_data,
        colWidths=[235, 235]
    )

    tabla_firmas.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
    ]))

    elementos.append(
        Paragraph(
            "<b>ACEPTACIÓN DE LA PROPUESTA</b>",
            seccion
        )
    )

    elementos.append(tabla_firmas)

    elementos.append(Spacer(1, 12))

    elementos.append(
        Paragraph(
            "MDHEADHUNTER RECLUTADOR ESTRATÉGICO | admi@mdheadhunter.com.mx<br/>"
            '"Mejores decisiones para su organización"',
            footer
        )
    )

    doc.build(elementos)