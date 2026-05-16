import streamlit as st


def login(cursor):

    if "login" not in st.session_state:
        st.session_state.login = False

    if "usuario" not in st.session_state:
        st.session_state.usuario = ""

    if "rol" not in st.session_state:
        st.session_state.rol = ""

    if not st.session_state.login:

        st.title("ATS PRO ELITE")
        st.caption("Sistema Inteligente de Reclutamiento")

        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):

            user = cursor.execute("""
                SELECT usuario, rol
                FROM usuarios
                WHERE usuario=?
                AND password=?
            """, (
                usuario,
                password
            )).fetchone()

            if user:

                st.session_state.login = True
                st.session_state.usuario = user[0]
                st.session_state.rol = user[1]
                st.rerun()

            else:

                st.error("Usuario o contraseña incorrectos")

        st.stop()