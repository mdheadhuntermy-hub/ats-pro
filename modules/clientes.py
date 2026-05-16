import streamlit as st


def clientes_page(cursor, guardar):

    st.title("🏢 Clientes")

    empresa = st.text_input("Empresa")
    contacto = st.text_input("Contacto")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")

    if st.button("Guardar Cliente"):

        cursor.execute("""
            INSERT INTO clientes(
                empresa,
                contacto,
                correo,
                telefono
            )
            VALUES(?,?,?,?)
        """, (
            empresa,
            contacto,
            correo,
            telefono
        ))

        guardar()
        st.success("✅ Cliente guardado")
        st.rerun()

    st.divider()
    st.subheader("📋 Clientes Registrados")

    clientes = cursor.execute("""
        SELECT *
        FROM clientes
        ORDER BY id DESC
    """).fetchall()

    if clientes:

        for cliente in clientes:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"🏢 Empresa: {cliente[1]}")
            st.write(f"👤 Contacto: {cliente[2]}")
            st.write(f"📧 Correo: {cliente[3]}")
            st.write(f"📱 Teléfono: {cliente[4]}")

            with st.expander("✏️ Editar Cliente"):

                nueva_empresa = st.text_input(
                    "Nueva empresa",
                    value=cliente[1],
                    key=f"empresa_{cliente[0]}"
                )

                nuevo_contacto = st.text_input(
                    "Nuevo contacto",
                    value=cliente[2],
                    key=f"contacto_{cliente[0]}"
                )

                nuevo_correo = st.text_input(
                    "Nuevo correo",
                    value=cliente[3],
                    key=f"correo_{cliente[0]}"
                )

                nuevo_telefono = st.text_input(
                    "Nuevo teléfono",
                    value=cliente[4],
                    key=f"telefono_{cliente[0]}"
                )

                if st.button(
                    "Guardar Cambios",
                    key=f"guardar_cliente_{cliente[0]}"
                ):

                    cursor.execute("""
                        UPDATE clientes
                        SET empresa=?,
                            contacto=?,
                            correo=?,
                            telefono=?
                        WHERE id=?
                    """, (
                        nueva_empresa,
                        nuevo_contacto,
                        nuevo_correo,
                        nuevo_telefono,
                        cliente[0]
                    ))

                    guardar()
                    st.success("✅ Cliente actualizado")
                    st.rerun()

            if st.button(
                "🗑️ Eliminar",
                key=f"cliente_{cliente[0]}"
            ):

                cursor.execute(
                    "DELETE FROM clientes WHERE id=?",
                    (cliente[0],)
                )

                guardar()
                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info("No hay clientes registrados")