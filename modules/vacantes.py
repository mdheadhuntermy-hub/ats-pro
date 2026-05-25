import streamlit as st


def vacantes_page(cursor, guardar):

    st.title("💼 Vacantes")

    rol = st.session_state.get("rol", "")
    usuario = st.session_state.get("usuario", "")

    try:
        cursor.execute("""
            ALTER TABLE vacantes
            ADD COLUMN creado_por TEXT
        """)
    except:
        pass

    titulo = st.text_input("Título")
    salario = st.text_input("Salario")
    descripcion = st.text_area("Descripción")

    if st.button("Guardar Vacante"):

        cursor.execute("""
            INSERT INTO vacantes(
                titulo,
                salario,
                descripcion,
                creado_por
            )
            VALUES(?,?,?,?)
        """, (
            titulo,
            salario,
            descripcion,
            usuario
        ))

        guardar()

        st.success("✅ Vacante guardada")

        st.rerun()

    st.divider()

    st.subheader("📋 Vacantes Registradas")

    if rol == "RH":

        vacantes = cursor.execute("""
            SELECT *
            FROM vacantes
            WHERE creado_por=?
            ORDER BY id DESC
        """, (
            usuario,
        )).fetchall()

    else:

        vacantes = cursor.execute("""
            SELECT *
            FROM vacantes
            ORDER BY id DESC
        """).fetchall()

    if vacantes:

        for vacante in vacantes:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"💼 Vacante: {vacante[1]}")
            st.write(f"💰 Salario: {vacante[2]}")
            st.write(f"📝 Descripción: {vacante[3]}")

            if len(vacante) > 4:
                st.caption(
                    f"👤 Reclutador: {vacante[4]}"
                )

            with st.expander("✏️ Editar Vacante"):

                nuevo_titulo = st.text_input(
                    "Nuevo título",
                    value=vacante[1],
                    key=f"titulo_{vacante[0]}"
                )

                nuevo_salario = st.text_input(
                    "Nuevo salario",
                    value=vacante[2],
                    key=f"salario_{vacante[0]}"
                )

                nueva_descripcion = st.text_area(
                    "Nueva descripción",
                    value=vacante[3],
                    key=f"descripcion_{vacante[0]}"
                )

                if st.button(
                    "Guardar Cambios",
                    key=f"guardar_vac_{vacante[0]}"
                ):

                    cursor.execute("""
                        UPDATE vacantes
                        SET titulo=?,
                            salario=?,
                            descripcion=?
                        WHERE id=?
                    """, (
                        nuevo_titulo,
                        nuevo_salario,
                        nueva_descripcion,
                        vacante[0]
                    ))

                    guardar()

                    st.success(
                        "✅ Vacante actualizada"
                    )

                    st.rerun()

            if st.button(
                "🗑️ Eliminar",
                key=f"vac_{vacante[0]}"
            ):

                cursor.execute(
                    "DELETE FROM vacantes WHERE id=?",
                    (vacante[0],)
                )

                guardar()

                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info("No hay vacantes registradas")