import PyPDF2
import re

def leer_pdf(file):

    texto = ""

    lector = PyPDF2.PdfReader(file)

    for pagina in lector.pages:
        texto += pagina.extract_text() or ""

    return texto.lower()

def extraer_datos(texto):

    # EMAIL
    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        texto
    )

    # TELÉFONO
    telefono = re.findall(
        r"\b\d{10}\b",
        texto
    )

    # NOMBRE SIMPLE
    lineas = texto.split("\n")

    nombre = lineas[0] if lineas else "No detectado"

    return {
        "nombre": nombre.title(),
        "correo": email[0] if email else "",
        "telefono": telefono[0] if telefono else ""
    }
def extraer_skills(texto):

    skills_lista = [

        "excel",
        "sap",
        "python",
        "power bi",
        "lean manufacturing",
        "autocad",
        "solidworks",
        "reclutamiento",
        "nomina",
        "inventarios",
        "sql",
        "java",
        "c++",
        "logistica",
        "calidad",
        "iso 9001",
        "scrum",
        "kanban",
        "manufactura",
        "produccion",
        "ventas",
        "rh",
        "recursos humanos"

    ]

    encontradas = []

    texto = texto.lower()

    for skill in skills_lista:

        if skill in texto:
            encontradas.append(skill)

    return encontradas
import re

def extraer_experiencia(texto):

    texto = texto.lower()

    # AÑOS EXPERIENCIA
    años = re.findall(
        r"(\d+)\s*años",
        texto
    )

    experiencia = años[0] if años else "No detectado"

    # EMPRESAS
    empresas_conocidas = [

        "femsa",
        "ternium",
        "whirlpool",
        "cemex",
        "heineken",
        "deloitte",
        "amazon",
        "toyota",
        "kia",
        "john deere",
        "gm",
        "pepsi",
        "sigma",
        "nemak"

    ]

    empresas_detectadas = []

    for empresa in empresas_conocidas:

        if empresa in texto:
            empresas_detectadas.append(
                empresa.title()
            )

    # CARGOS
    cargos = [

        "ingeniero",
        "analista",
        "supervisor",
        "gerente",
        "coordinador",
        "reclutador",
        "operador",
        "tecnico",
        "lider"

    ]

    cargos_detectados = []

    for cargo in cargos:

        if cargo in texto:
            cargos_detectados.append(
                cargo.title()
            )

    return {
        "experiencia": experiencia,
        "empresas": empresas_detectadas,
        "cargos": cargos_detectados
    }