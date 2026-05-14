import streamlit as st

from database import cursor, conn


def mostrar_vacantes():

    st.title("💼 Vacantes")

    titulo = st.text_input("Título")
    empresa = st.text_input("Empresa")
    ubicacion = st.text_input("Ubicación")
    salario = st.text_input("Salario")
    descripcion = st.text_area("Descripción")

    if st.button("Guardar Vacante"):

        cursor.execute(
            "INSERT INTO vacantes(titulo,empresa,ubicacion,salario,descripcion) VALUES(?,?,?,?,?)",
            (titulo, empresa, ubicacion, salario, descripcion)
        )

        conn.commit()

        st.success("Vacante guardada")