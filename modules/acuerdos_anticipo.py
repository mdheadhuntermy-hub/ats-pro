import streamlit as st
import pandas as pd
import os
from datetime import date

from utils.acuerdo_anticipo_pdf import generar_pdf_acuerdo_anticipo


def acuerdos_anticipo_page(cursor, guardar):

    st.title("📑 Acuerdos de Anticipo")

    st.subheader("Crear nuevo acuerdo")

    clientes_db = cursor.execute("""
        SELECT empresa, contacto
        FROM clientes
        ORDER BY empresa
    """).fetchall()

    usar_cliente = st.checkbox(
        "Usar cliente registrado",
        value=True
    )

    empresa = ""
    contacto = ""

    if usar_cliente and clientes_db:

        lista_clientes = [c[0] for c in clientes_db]

        empresa_seleccionada = st.selectbox(
            "Seleccionar cliente",
            lista_clientes
        )

        datos_cliente = cursor.execute("""
            SELECT empresa, contacto
            FROM clientes
            WHERE empresa=?
        """, (
            empresa_seleccionada,
        )).fetchone()

        empresa = datos_cliente[0] if datos_cliente else ""
        contacto = datos_cliente[1] if datos_cliente else ""

        st.info(f"🏢 Empresa: {empresa} | 👤 Contacto: {contacto}")

    else:

        empresa = st.text_input("Empresa")
        contacto = st.text_input("Contacto / Representante")

    fecha = st.date_input(
        "Fecha",
        value=date.today()
    )

    puesto = st.text_input(
        "Puesto / Vacante"
    )

    vacantes = st.number_input(
        "Número de vacantes",
        min_value=1,
        value=1,
        step=1
    )

    salario = st.number_input(
        "Salario mensual bruto",
        min_value=0.0,
        step=500.0
    )

    tipo_perfil = st.selectbox(
        "Tipo de perfil",
        [
            "Operativo",
            "Administrativo",
            "Gerencial / Directivo"
        ]
    )

    if tipo_perfil == "Operativo":
        porcentaje = 60.0
    elif tipo_perfil == "Administrativo":
        porcentaje = 80.0
    else:
        porcentaje = 100.0

    honorarios = salario * (porcentaje / 100) * vacantes
    anticipo = honorarios * 0.30
    iva = anticipo * 0.16
    total = anticipo + iva

    st.divider()

    st.subheader("Cálculo automático")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Honorarios", f"${honorarios:,.2f}")
    c2.metric("Anticipo 30%", f"${anticipo:,.2f}")
    c3.metric("IVA 16%", f"${iva:,.2f}")
    c4.metric("Total anticipo", f"${total:,.2f}")

    if st.button("Guardar y Generar Acuerdo PDF"):

        if not empresa:
            st.error("Debes capturar la empresa.")
            return

        if not puesto:
            st.error("Debes capturar el puesto.")
            return

        if salario <= 0:
            st.error("Debes capturar el salario mensual.")
            return

        if not os.path.exists("acuerdos_anticipo_pdf"):
            os.makedirs("acuerdos_anticipo_pdf")

        nombre_archivo = f"acuerdo_anticipo_{empresa}_{puesto}.pdf"
        nombre_archivo = nombre_archivo.replace(" ", "_").replace("/", "_")

        pdf_path = os.path.join(
            "acuerdos_anticipo_pdf",
            nombre_archivo
        )

        generar_pdf_acuerdo_anticipo(
            output_path=pdf_path,
            fecha=str(fecha),
            empresa=empresa,
            contacto=contacto,
            puesto=puesto,
            vacantes=vacantes,
            salario=salario,
            porcentaje=porcentaje,
            honorarios=honorarios,
            anticipo=anticipo,
            iva=iva,
            total=total
        )

        cursor.execute("""
            INSERT INTO acuerdos_anticipo(
                fecha,
                empresa,
                contacto,
                puesto,
                vacantes,
                salario,
                porcentaje,
                honorarios,
                anticipo,
                iva,
                total,
                pdf
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            str(fecha),
            empresa,
            contacto,
            puesto,
            int(vacantes),
            salario,
            porcentaje,
            honorarios,
            anticipo,
            iva,
            total,
            pdf_path
        ))

        guardar()

        st.success("✅ Acuerdo de anticipo generado correctamente")
        st.rerun()

    st.divider()

    st.subheader("📋 Historial de Acuerdos")

    acuerdos = cursor.execute("""
        SELECT *
        FROM acuerdos_anticipo
        ORDER BY id DESC
    """).fetchall()

    if acuerdos:

        df = pd.DataFrame(
            acuerdos,
            columns=[
                "ID",
                "Fecha",
                "Empresa",
                "Contacto",
                "Puesto",
                "Vacantes",
                "Salario",
                "Porcentaje",
                "Honorarios",
                "Anticipo",
                "IVA",
                "Total",
                "PDF"
            ]
        )

        st.dataframe(
            df[
                [
                    "ID",
                    "Fecha",
                    "Empresa",
                    "Puesto",
                    "Vacantes",
                    "Salario",
                    "Porcentaje",
                    "Honorarios",
                    "Anticipo",
                    "Total"
                ]
            ],
            use_container_width=True
        )

        for acuerdo in acuerdos:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"📅 Fecha: {acuerdo[1]}")
            st.write(f"🏢 Empresa: {acuerdo[2]}")
            st.write(f"👤 Contacto: {acuerdo[3]}")
            st.write(f"💼 Puesto: {acuerdo[4]}")
            st.write(f"🔢 Vacantes: {acuerdo[5]}")
            st.write(f"💰 Salario: ${acuerdo[6]:,.2f}")
            st.write(f"📌 Comisión: {acuerdo[7]:,.0f}%")
            st.write(f"🧾 Honorarios: ${acuerdo[8]:,.2f}")
            st.write(f"💵 Anticipo: ${acuerdo[9]:,.2f}")
            st.write(f"🧮 IVA: ${acuerdo[10]:,.2f}")
            st.write(f"✅ Total anticipo: ${acuerdo[11]:,.2f}")

            col1, col2 = st.columns(2)

            with col1:

                if acuerdo[12] and os.path.exists(acuerdo[12]):

                    with open(acuerdo[12], "rb") as pdf:

                        st.download_button(
                            "⬇️ Descargar PDF",
                            pdf,
                            file_name=os.path.basename(acuerdo[12]),
                            mime="application/pdf",
                            key=f"pdf_acuerdo_{acuerdo[0]}"
                        )

                else:

                    st.warning("PDF no disponible")

            with col2:

                if st.button(
                    "🗑️ Eliminar",
                    key=f"del_acuerdo_{acuerdo[0]}"
                ):

                    cursor.execute(
                        "DELETE FROM acuerdos_anticipo WHERE id=?",
                        (acuerdo[0],)
                    )

                    guardar()
                    st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info("No hay acuerdos registrados")