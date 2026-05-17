import streamlit as st


def configuracion_page(cursor, guardar):

    st.title("⚙️ Configuración")

    st.subheader("Sesión")

    st.write(f"Usuario actual: {st.session_state.usuario}")
    st.write(f"Rol: {st.session_state.rol}")

    if st.button("Cerrar sesión"):

        st.session_state.login = False
        st.session_state.usuario = ""
        st.session_state.rol = ""

        st.rerun()

    st.divider()

    if st.session_state.rol != "Administrador":

        st.info("Solo el administrador puede crear o eliminar usuarios.")
        return

    st.subheader("👥 Usuarios del sistema")

    nuevo_usuario = st.text_input("Nuevo usuario")
    nuevo_password = st.text_input("Contraseña", type="password")

    nuevo_rol = st.selectbox(
        "Rol",
        [
            "Administrador",
            "RH",
            "Contabilidad"
        ]
    )

    if st.button("Crear Usuario"):

        cursor.execute("""
            INSERT INTO usuarios(
                usuario,
                password,
                rol
            )
            VALUES(?,?,?)
        """, (
            nuevo_usuario,
            nuevo_password,
            nuevo_rol
        ))

        guardar()
        st.success("✅ Usuario creado")
        st.rerun()

    usuarios = cursor.execute("""
        SELECT id, usuario, rol
        FROM usuarios
        ORDER BY id DESC
    """).fetchall()

    for usuario in usuarios:

        st.markdown(
            "<div class='card'>",
            unsafe_allow_html=True
        )

        st.write(f"👤 Usuario: {usuario[1]}")
        st.write(f"🔐 Rol: {usuario[2]}")

        if usuario[1] != "admin":

            if st.button(
                "🗑️ Eliminar",
                key=f"user_{usuario[0]}"
            ):

                cursor.execute(
                    "DELETE FROM usuarios WHERE id=?",
                    (usuario[0],)
                )

                guardar()
                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )