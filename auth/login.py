import streamlit as st
import os


def login(cursor):

    if "login" not in st.session_state:
        st.session_state.login = False

    if "usuario" not in st.session_state:
        st.session_state.usuario = ""

    if "rol" not in st.session_state:
        st.session_state.rol = ""

    if st.session_state.login:
        return

    col1, col2, col3 = st.columns([1, 1.1, 1])

    with col2:

        st.markdown("""
        <div style="
            background: linear-gradient(
                180deg,
                rgba(15,23,42,0.94),
                rgba(30,41,59,0.90)
            );
            padding:42px;
            border-radius:28px;
            border:1px solid rgba(255,255,255,0.10);
            box-shadow:0 25px 60px rgba(0,0,0,0.45);
            backdrop-filter: blur(18px);
            margin-top:70px;
            text-align:center;
        ">
        """, unsafe_allow_html=True)

        if os.path.exists("assets/logo.png"):

            st.image(
                "assets/logo.png",
                width=170
            )

        st.markdown("""
        <h1 style='
            text-align:center;
            margin-bottom:5px;
            font-size:34px;
            letter-spacing:1px;
        '>
            MDHEADHUNTER
        </h1>

        <p style='
            text-align:center;
            color:#94a3b8;
            margin-bottom:8px;
            font-size:16px;
        '>
            ATS PRO ELITE
        </p>

        <p style='
            text-align:center;
            color:#64748b;
            margin-bottom:30px;
            font-size:13px;
        '>
            Plataforma ejecutiva de reclutamiento inteligente
        </p>
        """, unsafe_allow_html=True)

        usuario = st.text_input(
            "Usuario",
            placeholder="Ingresa tu usuario"
        )

        password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="Ingresa tu contraseña"
        )

        entrar = st.button(
            "Ingresar al sistema",
            use_container_width=True
        )

        st.markdown("""
        <p style='
            text-align:center;
            color:#64748b;
            font-size:12px;
            margin-top:25px;
        '>
            © MDHEADHUNTER • Talent Intelligence Platform
        </p>
        </div>
        """, unsafe_allow_html=True)

    if entrar:

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

            st.error(
                "Usuario o contraseña incorrectos"
            )

    st.stop()