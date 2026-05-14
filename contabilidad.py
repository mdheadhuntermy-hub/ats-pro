import streamlit as st

from database import cursor, conn


def mostrar_contabilidad():

    st.title("💰 Contabilidad")

    cliente = st.text_input("Cliente")
    vacante = st.text_input("Vacante")
    monto = st.text_input("Monto")

    estado = st.selectbox(
        "Estado",
        ["Pendiente", "Pagada"]
    )

    if st.button("Guardar Factura"):

        cursor.execute(
            "INSERT INTO facturas(cliente,vacante,monto,estado) VALUES(?,?,?,?)",
            (
                cliente,
                vacante,
                monto,
                estado
            )
        )

        conn.commit()

        st.success("Factura guardada")