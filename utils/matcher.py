from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calcular_match(vacante, cv):

    textos = [vacante.lower(), cv.lower()]

    vectorizer = TfidfVectorizer()

    matriz = vectorizer.fit_transform(textos)

    similitud = cosine_similarity(
        matriz[0:1],
        matriz[1:2]
    )[0][0]

    return round(similitud * 100, 2)