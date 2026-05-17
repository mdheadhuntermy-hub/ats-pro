import streamlit as st


def login(cursor):

    if "login" not in st.session_state:
        st.session_state.login = False

    if "usuario" not in st.session_state:
        st.session_state.usuario = ""

    if "rol" not in st.session_state:
        st.session_state.rol = ""

    if st.session_state.login:
        return

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        st.markdown("""
        <div style="
            background: rgba(15,23,42,0.88);
            padding:40px;
            border-radius:24px;
            border:1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(14px);
            margin-top:80px;
        ">
        """, unsafe_allow_html=True)

        st.markdown("""
        <h1 style='text-align:center;'>MDHEADHUNTER</h1>
        <p style='text-align:center;color:#94a3b8;margin-bottom:30px;'>
        ATS PRO ELITE
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
            "Ingresar",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

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

            st.error("Usuario o contraseña incorrectos")

    st.stop()