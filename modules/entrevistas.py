import streamlit as st


def entrevistas_page(cursor, guardar):

    st.title("📅 Entrevistas")

    candidatos_db = cursor.execute("""
        SELECT nombre
        FROM candidatos
        ORDER BY nombre
    """).fetchall()

    lista_candidatos = [c[0] for c in candidatos_db]

    if not lista_candidatos:
        st.warning("Primero registra candidatos")
        return

    candidato = st.selectbox("Candidato", lista_candidatos)
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")
    entrevistador = st.text_input("Entrevistador")
    calificacion = st.slider("Calificación", 1, 10, 7)
    observaciones = st.text_area("Observaciones RH")

    resultado = st.selectbox(
        "Resultado",
        [
            "Pendiente",
            "Aprobado",
            "Rechazado",
            "Segunda Entrevista"
        ]
    )

    if st.button("Guardar Entrevista"):

        cursor.execute("""
            INSERT INTO entrevistas(
                candidato,
                fecha,
                hora,
                entrevistador,
                calificacion,
                observaciones,
                resultado
            )
            VALUES(?,?,?,?,?,?,?)
        """, (
            candidato,
            str(fecha),
            str(hora),
            entrevistador,
            calificacion,
            observaciones,
            resultado
        ))

        guardar()
        st.success("✅ Entrevista guardada")
        st.rerun()

    st.divider()
    st.subheader("📋 Historial de Entrevistas")

    entrevistas = cursor.execute("""
        SELECT *
        FROM entrevistas
        ORDER BY id DESC
    """).fetchall()

    if entrevistas:

        for entrevista in entrevistas:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"👤 Candidato: {entrevista[1]}")
            st.write(f"📅 Fecha: {entrevista[2]}")
            st.write(f"🕒 Hora: {entrevista[3]}")
            st.write(f"🧑‍💼 Entrevistador: {entrevista[4]}")
            st.write(f"⭐ Calificación: {entrevista[5]}/10")
            st.write(f"📝 Observaciones RH: {entrevista[6]}")
            st.write(f"📌 Resultado: {entrevista[7]}")

            if st.button(
                "🗑️ Eliminar",
                key=f"entre_{entrevista[0]}"
            ):

                cursor.execute(
                    "DELETE FROM entrevistas WHERE id=?",
                    (entrevista[0],)
                )

                guardar()
                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info("No hay entrevistas")