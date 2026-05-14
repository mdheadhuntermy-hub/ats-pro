import streamlit as st

from database import cursor, conn


def mostrar_entrevistas():

    st.title("📅 Entrevistas")

    candidato = st.text_input("Candidato")
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")
    entrevistador = st.text_input("Entrevistador")

    if st.button("Agendar"):

        cursor.execute(
            "INSERT INTO entrevistas(candidato,fecha,hora,entrevistador) VALUES(?,?,?,?)",
            (
                candidato,
                str(fecha),
                str(hora),
                entrevistador
            )
        )

        conn.commit()

        st.success("Entrevista agendada")