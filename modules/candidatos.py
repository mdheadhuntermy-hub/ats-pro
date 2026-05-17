import streamlit as st
import os
import uuid

from services.pdf_service import extraer_texto_pdf


def generar_dictamen(score, descripcion_vacante, texto_cv, skills):

    if score >= 80:
        resultado = "RECOMENDABLE"
        conclusion = (
            "El candidato presenta una alta compatibilidad con la vacante. "
            "Se recomienda avanzar a entrevista o siguiente etapa del proceso."
        )

    elif score >= 60:
        resultado = "PARCIALMENTE RECOMENDABLE"
        conclusion = (
            "El candidato presenta compatibilidad media con la vacante. "
            "Se recomienda revisión RH para validar experiencia, estabilidad y competencias clave."
        )

    elif score >= 40:
        resultado = "EN OBSERVACIÓN"
        conclusion = (
            "El candidato muestra algunos elementos relacionados con la vacante, "
            "pero requiere validación adicional antes de avanzar."
        )

    else:
        resultado = "NO RECOMENDABLE"
        conclusion = (
            "El candidato presenta baja compatibilidad inicial con la vacante. "
            "No se recomienda avanzar salvo que existan criterios estratégicos adicionales."
        )

    dictamen = f"""
Resultado IA: {resultado}

Match estimado: {score}%

Análisis:
La evaluación considera la descripción de la vacante, el contenido extraído del CV PDF y los comentarios capturados en el campo Skills / Comentarios RH.

Comentarios RH considerados:
{skills if skills else "Sin comentarios adicionales capturados."}

Conclusión:
{conclusion}
"""

    return dictamen.strip()


def ajustar_score_por_comentarios(score, skills):

    texto_negativo = (skills or "").lower()

    palabras_negativas = [
        "no tiene experiencia",
        "sin experiencia",
        "no cuenta con experiencia",
        "sin conocimientos",
        "no sabe",
        "junior",
        "no ha trabajado",
        "no conoce",
        "no domina"
    ]

    for palabra in palabras_negativas:

        if palabra in texto_negativo:
            score -= 25

    score = max(0, min(score, 100))

    return int(score)


def candidatos_page(cursor, guardar, calcular_match):

    st.title("👥 Candidatos")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")

    skills = st.text_area(
        "Skills / Comentarios RH",
        help="Agrega habilidades, observaciones, experiencia relevante o comentarios del reclutador."
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
        st.warning("Primero debes crear una vacante")
        vacante = ""

    cv_pdf = st.file_uploader(
        "Subir CV PDF",
        type=["pdf"]
    )

    if st.button("Guardar Candidato"):

        datos_vacante = cursor.execute("""
            SELECT descripcion
            FROM vacantes
            WHERE titulo=?
        """, (
            vacante,
        )).fetchone()

        if datos_vacante:
            descripcion_vacante = datos_vacante[0]
        else:
            descripcion_vacante = vacante

        texto_cv = ""
        pdf_path = ""

        if cv_pdf is not None:

            if not os.path.exists("cv"):
                os.makedirs("cv")

            filename = f"{uuid.uuid4()}.pdf"
            pdf_path = os.path.join("cv", filename)

            with open(pdf_path, "wb") as f:
                f.write(cv_pdf.read())

            texto_cv = extraer_texto_pdf(pdf_path)

        texto_evaluacion = f"""
        VACANTE:
        {descripcion_vacante}

        CV:
        {texto_cv}

        SKILLS / COMENTARIOS RH:
        {skills}
        """

        if texto_evaluacion.strip():

            with st.spinner("Analizando CV, vacante y comentarios RH con IA..."):

                score_cv = calcular_match(
                    descripcion_vacante,
                    texto_cv
                )

                score_skills = calcular_match(
                    descripcion_vacante,
                    skills
                )

                score = int(
                    (score_cv * 0.7) +
                    (score_skills * 0.3)
                )

                score = ajustar_score_por_comentarios(
                    score,
                    skills
                )

        else:
            score = 0

        dictamen = generar_dictamen(
            score,
            descripcion_vacante,
            texto_cv,
            skills
        )

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
                dictamen
            )
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (
            nombre,
            correo,
            telefono,
            skills,
            score,
            estado,
            vacante,
            pdf_path,
            dictamen
        ))

        guardar()
        st.success("✅ Candidato guardado con dictamen IA")
        st.rerun()

    st.divider()
    st.subheader("📋 Candidatos Registrados")

    busqueda = st.text_input("🔍 Buscar candidato")

    if busqueda:

        candidatos = cursor.execute("""
            SELECT *
            FROM candidatos
            WHERE nombre LIKE ?
            OR skills LIKE ?
            OR vacante LIKE ?
            OR dictamen LIKE ?
            ORDER BY score DESC
        """, (
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%"
        )).fetchall()

    else:

        candidatos = cursor.execute("""
            SELECT *
            FROM candidatos
            ORDER BY score DESC
        """).fetchall()

    if candidatos:

        for candidato in candidatos:

            dictamen = ""

            if len(candidato) > 9 and candidato[9]:
                dictamen = candidato[9]

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"👤 Nombre: {candidato[1]}")
            st.write(f"📧 Correo: {candidato[2]}")
            st.write(f"📱 Teléfono: {candidato[3]}")
            st.write(f"🛠 Skills / Comentarios RH: {candidato[4]}")
            st.write(f"🎯 Match IA: {candidato[5]}%")
            st.write(f"📌 Estado: {candidato[6]}")
            st.write(f"💼 Vacante: {candidato[7]}")

            if dictamen:

                with st.expander("🧠 Ver Dictamen IA"):

                    st.text(dictamen)

            estados = [
                "Filtro RH",
                "Entrevista",
                "Prueba Técnica",
                "Contratado",
                "Rechazado"
            ]

            estado_actual = candidato[6]

            if estado_actual not in estados:
                estado_actual = "Filtro RH"

            nuevo_estado = st.selectbox(
                "Cambiar Estado",
                estados,
                index=estados.index(estado_actual),
                key=f"estado_{candidato[0]}"
            )

            if st.button(
                "Actualizar Estado",
                key=f"update_{candidato[0]}"
            ):

                cursor.execute("""
                    UPDATE candidatos
                    SET estado=?
                    WHERE id=?
                """, (
                    nuevo_estado,
                    candidato[0]
                ))

                guardar()
                st.success("✅ Estado actualizado")
                st.rerun()

            col1, col2 = st.columns(2)

            with col1:

                if candidato[8] and os.path.exists(candidato[8]):

                    with open(candidato[8], "rb") as pdf:

                        st.download_button(
                            "📄 Descargar CV",
                            pdf,
                            file_name=f"{candidato[1]}.pdf",
                            mime="application/pdf",
                            key=f"pdf_{candidato[0]}"
                        )

                elif candidato[8]:

                    st.warning(
                        "El CV ya no está disponible en Render."
                    )

            with col2:

                if st.button(
                    "🗑️ Eliminar",
                    key=f"del_{candidato[0]}"
                ):

                    cursor.execute(
                        "DELETE FROM candidatos WHERE id=?",
                        (candidato[0],)
                    )

                    guardar()
                    st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info("No hay candidatos registrados")