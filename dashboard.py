import streamlit as st
import matplotlib.pyplot as plt

from database import cursor


def mostrar_dashboard():

    st.title("📊 Dashboard")

    total_vacantes = cursor.execute(
        "SELECT COUNT(*) FROM vacantes"
    ).fetchone()[0]

    total_candidatos = cursor.execute(
        "SELECT COUNT(*) FROM candidatos"
    ).fetchone()[0]

    total_clientes = cursor.execute(
        "SELECT COUNT(*) FROM clientes"
    ).fetchone()[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Vacantes", total_vacantes)
    col2.metric("Candidatos", total_candidatos)
    col3.metric("Clientes", total_clientes)

    ranking = cursor.execute('''
    SELECT nombre, score
    FROM candidatos
    ORDER BY score DESC
    LIMIT 5
    ''').fetchall()

    if ranking:

        nombres = [r[0] for r in ranking]
        scores = [r[1] for r in ranking]

        fig, ax = plt.subplots()

        ax.barh(nombres, scores)

        st.pyplot(fig)