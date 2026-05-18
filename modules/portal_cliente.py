import streamlit as st
import pandas as pd
import os


def portal_cliente_page(cursor, guardar):

    st.title("🏢 Portal Cliente")

    st.markdown("""
    <div style="
        background:rgba(15,23,42,0.75);
        padding:20px;
        border-radius:18px;
        margin-bottom:20px;
        border:1px solid rgba(255,255,255,0.08);
    ">
        Portal ejecutivo para revisión de candidatos.
    </div>
    """, unsafe_allow_html=True)

    vacantes = cursor.execute("""
        SELECT DISTINCT vacante
        FROM candidatos
        ORDER BY vacante
    """).fetchall()

    lista_vacantes = [
        v[0]
        for v in vacantes
    ]

    if not lista_vacantes:

        st.warning(
            "No hay vacantes registradas"
        )

        return

    vacante = st.selectbox(
        "Vacante",
        lista_vacantes
    )

    candidatos = cursor.execute("""
        SELECT *
        FROM candidatos
        WHERE vacante=?
        ORDER BY score DESC
    """, (
        vacante,
    )).fetchall()

    if candidatos:

        for candidato in candidatos:

            color = "#2563eb"

            if candidato[6] == "Contratado":
                color = "#16a34a"

            elif candidato[6] == "Rechazado":
                color = "#dc2626"

            st.markdown(f"""
            <div style="
                background:#0f172a;
                padding:18px;
                border-radius:18px;
                margin-bottom:18px;
                border-left:6px solid {color};
            ">
            """, unsafe_allow_html=True)

            st.markdown(
                f"### 👤 {candidato[1]}"
            )

            st.write(
                f"🎯 Match IA: {candidato[5]}%"
            )

            st.write(
                f"📌 Estado: {candidato[6]}"
            )

            with st.expander(
                "🧠 Ver Dictamen IA"
            ):

                st.text(
                    candidato[9]
                )

            if len(candidato) > 11:

                with st.expander(
                    "🛡️ Dictamen Seguridad"
                ):

                    st.text(
                        candidato[11]
                    )

            if len(candidato) > 13:

                with st.expander(
                    "🧠 Dictamen Psicométrico"
                ):

                    st.text(
                        candidato[13]
                    )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Aprobar",
                    key=f"approve_{candidato[0]}"
                ):

                    cursor.execute("""
                        UPDATE candidatos
                        SET estado=?
                        WHERE id=?
                    """, (
                        "Aprobado Cliente",
                        candidato[0]
                    ))

                    guardar()

                    st.success(
                        "Candidato aprobado"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Rechazar",
                    key=f"reject_{candidato[0]}"
                ):

                    cursor.execute("""
                        UPDATE candidatos
                        SET estado=?
                        WHERE id=?
                    """, (
                        "Rechazado Cliente",
                        candidato[0]
                    ))

                    guardar()

                    st.warning(
                        "Candidato rechazado"
                    )

                    st.rerun()

            if candidato[8] and os.path.exists(candidato[8]):

                with open(
                    candidato[8],
                    "rb"
                ) as pdf:

                    st.download_button(
                        "📄 Descargar CV",
                        pdf,
                        file_name=f"{candidato[1]}.pdf",
                        mime="application/pdf",
                        key=f"cv_cliente_{candidato[0]}"
                    )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No hay candidatos para esta vacante"
        )