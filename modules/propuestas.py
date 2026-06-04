import streamlit as st
import pandas as pd
import os
from datetime import date

from utils.propuesta_pdf import generar_pdf_propuesta


def propuestas_page(cursor, guardar):

    st.title("📄 Propuestas / Cotizaciones")

    st.subheader("Crear nueva propuesta")

    fecha = st.date_input(
        "Fecha",
        value=date.today()
    )

    tipo_documento = st.selectbox(
        "Tipo de documento",
        [
            "Propuesta Comercial",
            "Cotización Formal"
        ]
    )

    cliente = st.text_input(
        "Cliente / Dirigido a"
    )

    contacto = st.text_input(
        "Contacto"
    )

    empresa = st.text_input(
        "Empresa"
    )

    servicio = st.selectbox(
        "Servicio",
        [
            "Reclutamiento y Selección",
            "Headhunting",
            "Evaluación Integral",
            "Reclutamiento Operativo",
            "Reclutamiento Administrativo",
            "Reclutamiento Gerencial / Directivo"
        ]
    )

    perfil = st.text_input(
        "Perfil / Vacante",
        placeholder="Opcional si solo es propuesta comercial"
    )

    honorarios = st.text_input(
        "Honorarios",
        placeholder="Opcional. Ejemplo: 60%, 80%, 100% o $8,000 MXN"
    )

    anticipo = st.text_input(
        "Anticipo",
        placeholder="Opcional. Ejemplo: 30%"
    )

    garantia = st.text_input(
        "Garantía",
        value="Operativos y Administrativos: 30 días naturales de cobertura. Nivel Gerencial: 45 días naturales de cobertura."
    )

    vigencia = st.text_input(
        "Vigencia",
        value="15 días naturales"
    )

    condiciones = st.text_area(
        "Condiciones comerciales",
        value="""El servicio inicia una vez confirmada la propuesta comercial.

El proceso incluye búsqueda, filtro curricular, contacto inicial, validación de experiencia y presentación de candidatos alineados al perfil solicitado.

Los honorarios aplican por candidato contratado.

La reposición aplica únicamente si el candidato no continúa dentro del periodo de garantía establecido."""
    )

    estado = st.selectbox(
        "Estado",
        [
            "Pendiente",
            "Enviada",
            "Aprobada",
            "Rechazada"
        ]
    )

    if st.button("Guardar y Generar PDF"):

        if not os.path.exists("propuestas_pdf"):
            os.makedirs("propuestas_pdf")

        nombre_empresa = empresa if empresa else cliente
        nombre_perfil = perfil if perfil else tipo_documento

        nombre_archivo = f"propuesta_{nombre_empresa}_{nombre_perfil}.pdf"
        nombre_archivo = nombre_archivo.replace(" ", "_").replace("/", "_")

        pdf_path = os.path.join(
            "propuestas_pdf",
            nombre_archivo
        )

        generar_pdf_propuesta(
            output_path=pdf_path,
            fecha=str(fecha),
            cliente=cliente,
            contacto=contacto,
            empresa=empresa,
            servicio=servicio,
            perfil=perfil,
            honorarios=honorarios,
            anticipo=anticipo,
            garantia=garantia,
            vigencia=vigencia,
            condiciones=condiciones,
            tipo_documento=tipo_documento
        )

        cursor.execute("""
            INSERT INTO propuestas(
                fecha,
                cliente,
                contacto,
                empresa,
                servicio,
                perfil,
                honorarios,
                anticipo,
                garantia,
                vigencia,
                condiciones,
                estado,
                pdf
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            str(fecha),
            cliente,
            contacto,
            empresa,
            servicio,
            perfil,
            honorarios,
            anticipo,
            garantia,
            vigencia,
            condiciones,
            estado,
            pdf_path
        ))

        guardar()

        st.success(
            "✅ Propuesta guardada y PDF generado"
        )

        st.rerun()

    st.divider()

    st.subheader("📋 Historial de Propuestas")

    propuestas = cursor.execute("""
        SELECT *
        FROM propuestas
        ORDER BY id DESC
    """).fetchall()

    if propuestas:

        df = pd.DataFrame(
            propuestas,
            columns=[
                "ID",
                "Fecha",
                "Cliente",
                "Contacto",
                "Empresa",
                "Servicio",
                "Perfil",
                "Honorarios",
                "Anticipo",
                "Garantía",
                "Vigencia",
                "Condiciones",
                "Estado",
                "PDF"
            ]
        )

        st.dataframe(
            df[
                [
                    "ID",
                    "Fecha",
                    "Cliente",
                    "Empresa",
                    "Servicio",
                    "Perfil",
                    "Honorarios",
                    "Estado"
                ]
            ],
            use_container_width=True
        )

        for propuesta in propuestas:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"📅 Fecha: {propuesta[1]}")
            st.write(f"👤 Cliente: {propuesta[2]}")
            st.write(f"🏢 Empresa: {propuesta[4]}")
            st.write(f"🧾 Servicio: {propuesta[5]}")

            if propuesta[6]:
                st.write(f"💼 Perfil: {propuesta[6]}")

            if propuesta[7]:
                st.write(f"💰 Honorarios: {propuesta[7]}")

            if propuesta[8]:
                st.write(f"💵 Anticipo: {propuesta[8]}")

            st.write(f"📌 Estado: {propuesta[12]}")

            nuevo_estado = st.selectbox(
                "Actualizar estado",
                [
                    "Pendiente",
                    "Enviada",
                    "Aprobada",
                    "Rechazada"
                ],
                index=[
                    "Pendiente",
                    "Enviada",
                    "Aprobada",
                    "Rechazada"
                ].index(propuesta[12]) if propuesta[12] in [
                    "Pendiente",
                    "Enviada",
                    "Aprobada",
                    "Rechazada"
                ] else 0,
                key=f"estado_prop_{propuesta[0]}"
            )

            if st.button(
                "Actualizar Estado",
                key=f"upd_prop_{propuesta[0]}"
            ):

                cursor.execute("""
                    UPDATE propuestas
                    SET estado=?
                    WHERE id=?
                """, (
                    nuevo_estado,
                    propuesta[0]
                ))

                guardar()

                st.success(
                    "✅ Estado actualizado"
                )

                st.rerun()

            col1, col2 = st.columns(2)

            with col1:

                if propuesta[13] and os.path.exists(propuesta[13]):

                    with open(propuesta[13], "rb") as pdf:

                        st.download_button(
                            "⬇️ Descargar PDF",
                            pdf,
                            file_name=os.path.basename(propuesta[13]),
                            mime="application/pdf",
                            key=f"pdf_prop_{propuesta[0]}"
                        )

                else:

                    st.warning(
                        "PDF no disponible"
                    )

            with col2:

                if st.button(
                    "🗑️ Eliminar",
                    key=f"del_prop_{propuesta[0]}"
                ):

                    cursor.execute(
                        "DELETE FROM propuestas WHERE id=?",
                        (propuesta[0],)
                    )

                    guardar()

                    st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No hay propuestas registradas"
        )