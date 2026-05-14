import streamlit as st

from database import cursor, conn


def mostrar_clientes():

    st.title("🏢 Clientes")

    empresa = st.text_input("Empresa")
    contacto = st.text_input("Contacto")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")

    if st.button("Guardar Cliente"):

        cursor.execute(
            "INSERT INTO clientes(empresa,contacto,telefono,correo) VALUES(?,?,?,?)",
            (empresa, contacto, telefono, correo)
        )

        conn.commit()

        st.success("Cliente guardado")