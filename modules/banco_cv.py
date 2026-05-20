import streamlit as st
import os
import uuid

from services.pdf_service import extraer_texto_pdf


def guardar_cv(archivo):

    if archivo is None:
        return ""

    if not os.path.exists("banco_cv"):
        os.makedirs("banco_cv")

    filename = f"{uuid.uuid4()}.pdf"
    ruta = os.path.join("banco_cv", filename)

    with open(ruta, "wb") as f:
        f.write(archivo.read())

    return ruta


def banco_cv_page(cursor, guardar):

    st.title("📁 Banco de CV")

    st.subheader("Agregar perfil al banco")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")
    ciudad = st.text_input("Ciudad")
    perfil = st.text_input("Perfil profesional")
    area = st.text_input("Área")
    skills = st.text_area("Skills / Palabras clave")
    salario = st.text_input("Salario deseado")
    disponibilidad = st.text_input("Disponibilidad")
    comentarios = st.text_area("Comentarios RH")

    cv_pdf = st.file_uploader(
        "Subir CV PDF",
        type=["pdf"],
        key="banco_cv_pdf"
    )

    if st.button("Guardar en Banco de CV"):

        pdf_path = guardar_cv(cv_pdf)

        if cv_pdf is not None and pdf_path:
            texto_cv = extraer_texto_pdf(pdf_path)

            skills = f"""
            {skills}

            TEXTO CV:
            {texto_cv}
            """

        cursor.execute("""
            INSERT INTO banco_cv(
                nombre,
                correo,
                telefono,
                ciudad,
                perfil,
                area,
                skills,
                salario,
                disponibilidad,
                comentarios,
                pdf
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """, (
            nombre,
            correo,
            telefono,
            ciudad,
            perfil,
            area,
            skills,
            salario,
            disponibilidad,
            comentarios,
            pdf_path
        ))

        guardar()

        st.success("✅ CV guardado en banco")
        st.rerun()

    st.divider()

    st.subheader("🔎 Buscar perfiles")

    busqueda = st.text_input(
        "Buscar por nombre, ciudad, perfil, área, skills o comentarios"
    )

    if busqueda:

        perfiles = cursor.execute("""
            SELECT *
            FROM banco_cv
            WHERE nombre LIKE ?
            OR ciudad LIKE ?
            OR perfil LIKE ?
            OR area LIKE ?
            OR skills LIKE ?
            OR comentarios LIKE ?
            ORDER BY id DESC
        """, (
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%"
        )).fetchall()

    else:

        perfiles = cursor.execute("""
            SELECT *
            FROM banco_cv
            ORDER BY id DESC
        """).fetchall()

    if perfiles:

        for perfil_cv in perfiles:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"👤 Nombre: {perfil_cv[1]}")
            st.write(f"📧 Correo: {perfil_cv[2]}")
            st.write(f"📱 Teléfono: {perfil_cv[3]}")
            st.write(f"📍 Ciudad: {perfil_cv[4]}")
            st.write(f"💼 Perfil: {perfil_cv[5]}")
            st.write(f"🏷 Área: {perfil_cv[6]}")
            st.write(f"🛠 Skills: {perfil_cv[7]}")
            st.write(f"💰 Salario deseado: {perfil_cv[8]}")
            st.write(f"⏱ Disponibilidad: {perfil_cv[9]}")
            st.write(f"📝 Comentarios RH: {perfil_cv[10]}")

            col1, col2 = st.columns(2)

            with col1:

                if perfil_cv[11] and os.path.exists(perfil_cv[11]):

                    with open(perfil_cv[11], "rb") as pdf:

                        st.download_button(
                            "📄 Descargar CV",
                            pdf,
                            file_name=f"{perfil_cv[1]}.pdf",
                            mime="application/pdf",
                            key=f"banco_pdf_{perfil_cv[0]}"
                        )

            with col2:

                if st.button(
                    "🗑️ Eliminar",
                    key=f"banco_del_{perfil_cv[0]}"
                ):

                    cursor.execute(
                        "DELETE FROM banco_cv WHERE id=?",
                        (perfil_cv[0],)
                    )

                    guardar()
                    st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info("No hay perfiles guardados")