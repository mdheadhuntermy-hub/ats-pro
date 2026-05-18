def generar_resumen_entrevista(
    observaciones,
    calificacion
):

    texto = (observaciones or "").lower()

    fortalezas = []
    riesgos = []

    if "lider" in texto:
        fortalezas.append(
            "Capacidad de liderazgo"
        )

    if "ventas" in texto:
        fortalezas.append(
            "Perfil comercial"
        )

    if "excel" in texto:
        fortalezas.append(
            "Conocimientos administrativos"
        )

    if "conflicto" in texto:
        riesgos.append(
            "Posibles dificultades interpersonales"
        )

    if "inestable" in texto:
        riesgos.append(
            "Posible riesgo de rotación"
        )

    if "nervioso" in texto:
        riesgos.append(
            "Inseguridad durante entrevista"
        )

    if calificacion >= 8:

        recomendacion = (
            "RECOMENDABLE"
        )

    elif calificacion >= 6:

        recomendacion = (
            "RECOMENDABLE CON RESERVAS"
        )

    else:

        recomendacion = (
            "NO RECOMENDABLE"
        )

    resumen = f"""
Resumen Ejecutivo RH

Calificación final: {calificacion}/10

Recomendación:
{recomendacion}

Fortalezas detectadas:
{', '.join(fortalezas) if fortalezas else 'No identificadas'}

Riesgos detectados:
{', '.join(riesgos) if riesgos else 'Sin riesgos relevantes'}

Conclusión:
La recomendación final debe complementarse con referencias laborales,
pruebas psicométricas y validación del cliente.
"""

    return resumen.strip()