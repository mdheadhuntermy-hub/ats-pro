def generar_entrevista_ia(
    vacante,
    skills,
    score
):

    preguntas = []

    preguntas.append(
        f"¿Cuál ha sido tu experiencia más relevante relacionada con {vacante}?"
    )

    preguntas.append(
        "Cuéntame un reto laboral importante y cómo lo resolviste."
    )

    preguntas.append(
        "¿Por qué te interesa esta posición?"
    )

    if score < 50:

        preguntas.append(
            "Detectamos áreas de oportunidad en tu experiencia. ¿Cómo compensas esas áreas?"
        )

    if "lider" in skills.lower():

        preguntas.append(
            "Describe tu experiencia liderando equipos."
        )

    if "ventas" in skills.lower():

        preguntas.append(
            "¿Cómo manejas objeciones con clientes difíciles?"
        )

    if "excel" in skills.lower():

        preguntas.append(
            "¿Qué nivel de Excel manejas y para qué lo utilizas?"
        )

    fortalezas = [
        "Comunicación",
        "Capacidad de adaptación",
        "Experiencia relacionada",
        "Interés en la posición"
    ]

    riesgos = []

    if score < 60:
        riesgos.append(
            "Compatibilidad media con la vacante"
        )

    if score < 40:
        riesgos.append(
            "Experiencia posiblemente insuficiente"
        )

    if not riesgos:
        riesgos.append(
            "Sin riesgos críticos detectados"
        )

    return {
        "preguntas": preguntas,
        "fortalezas": fortalezas,
        "riesgos": riesgos
    }