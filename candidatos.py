import streamlit as st

from database import cursor


def mostrar_candidatos():

    st.title("👥 Candidatos")

    candidatos = cursor.execute(
        "SELECT * FROM candidatos"
    ).fetchall()

    for c in candidatos:

        st.markdown(f'''
        ### 👤 {c[1]}

        🎯 Score: {c[5]}%

        📌 Estado: {c[6]}
        ''')