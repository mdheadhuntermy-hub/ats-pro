import re
import pdfplumber

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def leer_pdf(pdf_file):

    texto = ""

    with pdfplumber.open(pdf_file) as pdf:

        for pagina in pdf.pages:

            contenido = pagina.extract_text()

            if contenido:
                texto += contenido

    return texto


def calcular_match(vacante, cv):

    documentos = [vacante, cv]

    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(documentos)

    similitud = cosine_similarity(
        tfidf[0:1],
        tfidf[1:2]
    )

    return int(similitud[0][0] * 100)


def extraer_correo(texto):

    match = re.findall(
        r'[\w\.-]+@[\w\.-]+',
        texto
    )

    return match[0] if match else "No encontrado"