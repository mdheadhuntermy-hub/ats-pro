import streamlit as st
import os
import uuid

from services.pdf_service import extraer_texto_pdf


def candidatos_page(cursor, guardar, calcular_match):

    st.title("👥 Candidatos")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")
    skills = st.text_input("Skills")

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

    # =========================================
    # VACANTES
    # =========================================

    vacantes_db = cursor.execute("""
        SELECT titulo
        FROM vacantes
        ORDER BY titulo
    """).fetchall()

    lista_vacantes = [v[0] for v in vacantes_db]

    if lista_vacantes:

        vacante = st.selectbox(
            "Vacante",
            lista_vacantes
        )

    else:

        st.warning(
            "Primero debes crear una vacante"
        )

        vacante = ""

    # =========================================
    # PDF
    # =========================================

    cv_pdf = st.file_uploader(
        "Subir CV PDF",
        type=["pdf"]
    )

    # =========================================
    # GUARDAR
    # =========================================

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

        texto_cv = skills

        pdf_path = ""

        if cv_pdf is not None:

            if not os.path.exists("cv"):
                os.makedirs("cv")

            filename = f"{uuid.uuid4()}.pdf"

            pdf_path = os.path.join(
                "cv",
                filename
            )

            with open(pdf_path, "wb") as f:
                f.write(cv_pdf.read())

            texto_cv = extraer_texto_pdf(
                pdf_path
            )

        score = calcular_match(
            descripcion_vacante,
            texto_cv
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
                pdf
            )
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            nombre,
            correo,
            telefono,
            skills,
            score,
            estado,
            vacante,
            pdf_path
        ))

        guardar()

        st.success(
            "✅ Candidato guardado"
        )

        st.rerun()

    # =========================================
    # LISTA
    # =========================================

    st.divider()

    st.subheader(
        "📋 Candidatos Registrados"
    )

    busqueda = st.text_input(
        "🔍 Buscar candidato"
    )

    if busqueda:

        candidatos = cursor.execute("""
            SELECT *
            FROM candidatos
            WHERE nombre LIKE ?
            OR skills LIKE ?
            OR vacante LIKE ?
            ORDER BY score DESC
        """, (
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

    # =========================================
    # TARJETAS
    # =========================================

    if candidatos:

        for candidato in candidatos:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(
                f"👤 Nombre: {candidato[1]}"
            )

            st.write(
                f"📧 Correo: {candidato[2]}"
            )

            st.write(
                f"📱 Teléfono: {candidato[3]}"
            )

            st.write(
                f"🛠 Skills: {candidato[4]}"
            )

            st.write(
                f"🎯 Match IA: {candidato[5]}%"
            )

            st.write(
                f"📌 Estado: {candidato[6]}"
            )

            nuevo_estado = st.selectbox(
                "Cambiar Estado",
                [
                    "Filtro RH",
                    "Entrevista",
                    "Prueba Técnica",
                    "Contratado",
                    "Rechazado"
                ],
                index=[
                    "Filtro RH",
                    "Entrevista",
                    "Prueba Técnica",
                    "Contratado",
                    "Rechazado"
                ].index(candidato[6]),
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

                st.success(
                    "✅ Estado actualizado"
                )

                st.rerun()

            st.write(
                f"💼 Vacante: {candidato[7]}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if candidato[8]:

                    with open(
                        candidato[8],
                        "rb"
                    ) as pdf:

                        st.download_button(
                            "📄 Descargar CV",
                            pdf,
                            file_name=f"{candidato[1]}.pdf",
                            mime="application/pdf",
                            key=f"pdf_{candidato[0]}"
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

        st.info(
            "No hay candidatos registrados"
        )