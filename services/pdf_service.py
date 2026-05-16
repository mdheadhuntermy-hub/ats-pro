import pdfplumber


def extraer_texto_pdf(pdf_path):

    texto = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for pagina in pdf.pages:

                contenido = pagina.extract_text()

                if contenido:
                    texto += contenido + "\n"

    except Exception as e:

        texto = f"ERROR PDF: {str(e)}"

    return texto