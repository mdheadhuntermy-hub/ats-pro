import streamlit as st
import os
import uuid

from services.interview_ai import generar_entrevista_ia
from utils.pdf_generator import generar_pdf_dictamen, generar_pdf_simple_dictamen
from services.pdf_service import extraer_texto_pdf


def ajustar_score_por_comentarios(score, skills):

    texto = (skills or "").lower()

    negativos = [
        "sin experiencia",
        "no tiene experiencia",
        "no cuenta con experiencia",
        "no domina",
        "no sabe",
        "no conoce",
        "junior",
        "poca experiencia",
        "mala comunicación",
        "inestable",
        "rotación",
        "conflictivo"
    ]

    positivos = [
        "experiencia comprobable",
        "excelente comunicación",
        "liderazgo",
        "estable",
        "experiencia real",
        "alto dominio",
        "domina",
        "especialista",
        "senior",
        "buen perfil",
        "recomendable"
    ]

    for palabra in negativos:
        if palabra in texto:
            score -= 18

    for palabra in positivos:
        if palabra in texto:
            score += 10

    return max(0, min(int(score), 100))


def generar_dictamen(score, descripcion_vacante, texto_cv, skills):

    if score >= 85:
        resultado = "ALTAMENTE RECOMENDABLE"
        conclusion = "El candidato presenta alta compatibilidad con la vacante."
    elif score >= 70:
        resultado = "RECOMENDABLE"
        conclusion = "El candidato cumple con varios criterios relevantes del puesto."
    elif score >= 55:
        resultado = "RECOMENDABLE CON RESERVAS"
        conclusion = "El candidato requiere validación adicional en entrevista RH."
    elif score >= 40:
        resultado = "EN OBSERVACIÓN"
        conclusion = "El candidato muestra compatibilidad parcial."
    else:
        resultado = "NO RECOMENDABLE"
        conclusion = "El candidato presenta baja compatibilidad inicial."

    return f"""
Resultado IA: {resultado}

Match estimado: {score}%

Criterios considerados:
- Descripción de la vacante
- Contenido del CV
- Skills / Observaciones RH
- Señales positivas o negativas agregadas por RH

Observaciones RH:
{skills if skills else "Sin observaciones RH capturadas."}

Conclusión:
{conclusion}
""".strip()


def generar_dictamen_seguridad(texto_seguridad):

    texto = (texto_seguridad or "").lower()

    riesgo = "BAJO"
    resultado = "APTO"

    if "antecedentes" in texto or "riesgo" in texto or "negativo" in texto:
        riesgo = "REVISAR"
        resultado = "APTO CON OBSERVACIONES"

    if "no se han encontrado registros" in texto or "sin observaciones" in texto:
        riesgo = "BAJO"
        resultado = "APTO"

    return f"""
DICTAMEN DE SEGURIDAD

Resultado: {resultado}
Riesgo: {riesgo}

Conclusión:
Se recomienda validación RH final conforme a política interna.
""".strip()


def generar_dictamen_psicometrico(texto_psicometrico):

    texto = (texto_psicometrico or "").lower()

    resultado = "RECOMENDABLE"

    if "no recomendable" in texto:
        resultado = "NO RECOMENDABLE"
    elif "agresividad" in texto or "inestabilidad" in texto or "riesgo" in texto:
        resultado = "RECOMENDABLE CON RESERVAS"

    return f"""
DICTAMEN PSICOMÉTRICO

Resultado: {resultado}

Conclusión:
Evaluación basada en resultados psicométricos cargados. Se recomienda complementar con entrevista RH.
""".strip()


def guardar_archivo_pdf(archivo, carpeta):

    if archivo is None:
        return "", ""

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    filename = f"{uuid.uuid4()}.pdf"
    ruta = os.path.join(carpeta, filename)

    with open(ruta, "wb") as f:
        f.write(archivo.read())

    texto = extraer_texto_pdf(ruta)

    return ruta, texto


def calcular_score_profesional(calcular_match, descripcion_vacante, texto_cv, skills):

    score_cv = calcular_match(
        descripcion_vacante,
        texto_cv
    )

    score_rh = calcular_match(
        descripcion_vacante,
        skills
    )

    texto_completo = f"""
    CV:
    {texto_cv}

    OBSERVACIONES RH:
    {skills}
    """

    score_contexto = calcular_match(
        descripcion_vacante,
        texto_completo
    )

    score = int(
        (score_cv * 0.40) +
        (score_rh * 0.40) +
        (score_contexto * 0.20)
    )

    score = ajustar_score_por_comentarios(
        score,
        skills
    )

    return score


def candidatos_page(cursor, guardar, calcular_match):

    st.title("👥 Candidatos")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")

    skills = st.text_area(
        "Skills / Comentarios RH",
        help="Aquí agrega todo lo que el CV no diga: experiencia real, actitud, liderazgo, estabilidad, red flags, dominio técnico, etc."
    )

    estado = st.selectbox(
        "Estado",
        [
            "Filtro RH",
            "Entrevista",
            "Prueba Técnica",
            "Contratado",
            "Rechazado"
        ]
    )

    vacantes_db = cursor.execute("""
        SELECT titulo
        FROM vacantes
        ORDER BY titulo
    """).fetchall()

    lista_vacantes = [v[0] for v in vacantes_db]

    if lista_vacantes:
        vacante = st.selectbox("Vacante", lista_vacantes)
    else:
        vacante = ""

    cv_pdf = st.file_uploader("Subir CV PDF", type=["pdf"])
    seguridad_pdf = st.file_uploader("📄 Estudio de Seguridad PDF", type=["pdf"])
    psicometrico_pdf = st.file_uploader("🧠 Pruebas Psicométricas PDF", type=["pdf"])

    if st.button("Guardar Candidato"):

        datos_vacante = cursor.execute("""
            SELECT descripcion
            FROM vacantes
            WHERE titulo=?
        """, (
            vacante,
        )).fetchone()

        descripcion_vacante = datos_vacante[0] if datos_vacante else vacante

        pdf_path, texto_cv = guardar_archivo_pdf(cv_pdf, "cv")
        seguridad_path, texto_seguridad = guardar_archivo_pdf(seguridad_pdf, "seguridad")
        psicometrico_path, texto_psicometrico = guardar_archivo_pdf(psicometrico_pdf, "psicometricos")

        score = calcular_score_profesional(
            calcular_match,
            descripcion_vacante,
            texto_cv,
            skills
        )

        dictamen = generar_dictamen(
            score,
            descripcion_vacante,
            texto_cv,
            skills
        )

        dictamen_seguridad = generar_dictamen_seguridad(texto_seguridad)
        dictamen_psicometrico = generar_dictamen_psicometrico(texto_psicometrico)

        cursor.execute("""
            INSERT INTO candidatos(
                nombre,
                correo,
                telefono,
                skills,
                score,
                estado,
                vacante,
                pdf,
                dictamen,
                seguridad_pdf,
                dictamen_seguridad,
                psicometrico_pdf,
                dictamen_psicometrico
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            nombre,
            correo,
            telefono,
            skills,
            score,
            estado,
            vacante,
            pdf_path,
            dictamen,
            seguridad_path,
            dictamen_seguridad,
            psicometrico_path,
            dictamen_psicometrico
        ))

        guardar()
        st.success("✅ Candidato guardado con evaluación IA mejorada")
        st.rerun()

    st.divider()

    candidatos = cursor.execute("""
        SELECT *
        FROM candidatos
        ORDER BY score DESC
    """).fetchall()

    if candidatos:

        for candidato in candidatos:

            dictamen = candidato[9] if len(candidato) > 9 else ""
            dictamen_seguridad = candidato[11] if len(candidato) > 11 else ""
            dictamen_psicometrico = candidato[13] if len(candidato) > 13 else ""

            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.write(f"👤 Nombre: {candidato[1]}")
            st.write(f"📧 Correo: {candidato[2]}")
            st.write(f"📱 Teléfono: {candidato[3]}")
            st.write(f"🛠 Observaciones RH: {candidato[4]}")
            st.write(f"🎯 Match IA: {candidato[5]}%")
            st.write(f"📌 Estado: {candidato[6]}")
            st.write(f"💼 Vacante: {candidato[7]}")

            with st.expander("🤖 Entrevista IA"):

                entrevista_ia = generar_entrevista_ia(
                    candidato[7],
                    candidato[4],
                    candidato[5]
                )

                st.subheader("Preguntas sugeridas")

                for pregunta in entrevista_ia["preguntas"]:
                    st.write(f"• {pregunta}")

                st.subheader("Fortalezas detectadas")

                for fortaleza in entrevista_ia["fortalezas"]:
                    st.success(fortaleza)

                st.subheader("Riesgos detectados")

                for riesgo in entrevista_ia["riesgos"]:
                    st.warning(riesgo)

            if dictamen:

                with st.expander("🧠 Ver Dictamen IA"):
                    st.text(dictamen)

            if dictamen_seguridad:

                with st.expander("🛡️ Dictamen Seguridad"):
                    st.text(dictamen_seguridad)

            if dictamen_psicometrico:

                with st.expander("🧠 Dictamen Psicométrico"):
                    st.text(dictamen_psicometrico)

            with st.expander("✏️ Editar Candidato"):

                nuevo_nombre = st.text_input(
                    "Nombre",
                    value=candidato[1],
                    key=f"n_{candidato[0]}"
                )

                nuevo_correo = st.text_input(
                    "Correo",
                    value=candidato[2],
                    key=f"c_{candidato[0]}"
                )

                nuevo_telefono = st.text_input(
                    "Teléfono",
                    value=candidato[3],
                    key=f"t_{candidato[0]}"
                )

                nuevo_skills = st.text_area(
                    "Skills / Comentarios RH",
                    value=candidato[4],
                    key=f"s_{candidato[0]}"
                )

                if st.button(
                    "💾 Guardar Cambios",
                    key=f"save_{candidato[0]}"
                ):

                    cursor.execute("""
                        UPDATE candidatos
                        SET
                            nombre=?,
                            correo=?,
                            telefono=?,
                            skills=?
                        WHERE id=?
                    """, (
                        nuevo_nombre,
                        nuevo_correo,
                        nuevo_telefono,
                        nuevo_skills,
                        candidato[0]
                    ))

                    guardar()
                    st.success("✅ Candidato actualizado")
                    st.rerun()

            if st.button(
                "🗑️ Eliminar",
                key=f"del_{candidato[0]}"
            ):

                cursor.execute("""
                    DELETE FROM candidatos
                    WHERE id=?
                """, (
                    candidato[0],
                ))

                guardar()
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("No hay candidatos registrados")