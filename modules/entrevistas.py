import streamlit as st

from services.interview_summary_ai import (
    generar_resumen_entrevista
)


def color_resultado(resultado):

    colores = {
        "Pendiente": "#2563eb",
        "Aprobado": "#16a34a",
        "Rechazado": "#dc2626",
        "Segunda Entrevista": "#f59e0b"
    }

    return colores.get(
        resultado,
        "#334155"
    )


def entrevistas_page(cursor, guardar):

    st.title("📅 Entrevistas")

    candidatos_db = cursor.execute("""
        SELECT nombre
        FROM candidatos
        ORDER BY nombre
    """).fetchall()

    lista_candidatos = [
        c[0]
        for c in candidatos_db
    ]

    if not lista_candidatos:

        st.warning(
            "Primero registra candidatos"
        )

        return

    st.markdown("""
    <div style="
        background:rgba(15,23,42,0.70);
        padding:18px;
        border-radius:18px;
        margin-bottom:20px;
        border:1px solid rgba(255,255,255,0.08);
    ">
        Registro ejecutivo de entrevistas RH.
    </div>
    """, unsafe_allow_html=True)

    candidato = st.selectbox(
        "Candidato",
        lista_candidatos
    )

    col1, col2 = st.columns(2)

    with col1:

        fecha = st.date_input(
            "Fecha"
        )

    with col2:

        hora = st.time_input(
            "Hora"
        )

    entrevistador = st.text_input(
        "Entrevistador"
    )

    calificacion = st.slider(
        "Calificación",
        1,
        10,
        7
    )

    observaciones = st.text_area(
        "Observaciones RH",
        height=150
    )

    if observaciones:

        resumen_ia = generar_resumen_entrevista(
            observaciones,
            calificacion
        )

        with st.expander(
            "🤖 Resumen IA Entrevista"
        ):

            st.text(resumen_ia)

    resultado = st.selectbox(
        "Resultado",
        [
            "Pendiente",
            "Aprobado",
            "Rechazado",
            "Segunda Entrevista"
        ]
    )

    if st.button(
        "Guardar Entrevista"
    ):

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

        st.success(
            "✅ Entrevista guardada"
        )

        st.rerun()

    st.divider()

    st.subheader(
        "📋 Historial de Entrevistas"
    )

    entrevistas = cursor.execute("""
        SELECT *
        FROM entrevistas
        ORDER BY id DESC
    """).fetchall()

    if entrevistas:

        for entrevista in entrevistas:

            color = color_resultado(
                entrevista[7]
            )

            st.markdown(f"""
            <div style="
                background:#0f172a;
                padding:18px;
                border-radius:18px;
                margin-bottom:18px;
                border-left:6px solid {color};
                box-shadow:0 0 10px rgba(0,0,0,0.20);
            ">
            """, unsafe_allow_html=True)

            st.markdown(
                f"### 👤 {entrevista[1]}"
            )

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    f"📅 Fecha: {entrevista[2]}"
                )

                st.write(
                    f"🕒 Hora: {entrevista[3]}"
                )

                st.write(
                    f"🧑‍💼 Entrevistador: {entrevista[4]}"
                )

            with c2:

                st.write(
                    f"⭐ Calificación: {entrevista[5]}/10"
                )

                st.write(
                    f"📌 Resultado: {entrevista[7]}"
                )

            with st.expander(
                "📝 Ver Observaciones RH"
            ):

                st.info(
                    entrevista[6]
                )

                resumen_ia = generar_resumen_entrevista(
                    entrevista[6],
                    entrevista[5]
                )

                st.divider()

                st.subheader(
                    "🤖 Resumen IA"
                )

                st.text(
                    resumen_ia
                )

            if st.button(
                "🗑️ Eliminar",
                key=f"entre_{entrevista[0]}"
            ):

                cursor.execute("""
                    DELETE FROM entrevistas
                    WHERE id=?
                """, (
                    entrevista[0],
                ))

                guardar()

                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No hay entrevistas registradas"
        )