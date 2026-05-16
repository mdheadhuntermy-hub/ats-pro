import streamlit as st
import pandas as pd


def contabilidad_page(cursor, guardar):

    st.title("💰 Contabilidad")

    clientes = cursor.execute(
        "SELECT empresa FROM clientes ORDER BY empresa"
    ).fetchall()

    lista_clientes = [c[0] for c in clientes]

    if not lista_clientes:
        st.warning("Primero registra clientes")
        return

    st.subheader("Registrar Factura")

    cliente = st.selectbox("Cliente", lista_clientes)
    numero_factura = st.text_input("Número de Factura")
    fecha_factura = st.date_input("Fecha de Factura")
    pagada = st.selectbox("Estado", ["Pendiente", "Pagada"])
    fecha_pago = st.date_input("Fecha de Pago")

    mes = st.selectbox(
        "Mes",
        [
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto",
            "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
    )

    subtotal = st.number_input("Subtotal", min_value=0.0)
    inversion = st.number_input("Inversión", min_value=0.0)

    iva = subtotal * 0.16
    total = subtotal + iva
    utilidad = subtotal - inversion

    c1, c2, c3 = st.columns(3)
    c1.metric("IVA", f"${iva:,.2f}")
    c2.metric("Total", f"${total:,.2f}")
    c3.metric("Utilidad", f"${utilidad:,.2f}")

    if st.button("Guardar Factura"):

        cursor.execute("""
            INSERT INTO facturas(
                cliente,
                numero_factura,
                fecha_factura,
                fecha_pago,
                pagada,
                mes,
                subtotal,
                iva,
                total,
                inversion,
                utilidad
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """, (
            cliente,
            numero_factura,
            str(fecha_factura),
            str(fecha_pago),
            pagada,
            mes,
            subtotal,
            iva,
            total,
            inversion,
            utilidad
        ))

        guardar()
        st.success("✅ Factura guardada")
        st.rerun()

    st.divider()
    st.subheader("📊 Resumen Financiero")

    resumen = cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(total), 0),
            COALESCE(SUM(utilidad), 0)
        FROM facturas
    """).fetchone()

    pendientes = cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM facturas
        WHERE pagada='Pendiente'
    """).fetchone()[0]

    pagadas = cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM facturas
        WHERE pagada='Pagada'
    """).fetchone()[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Facturas", resumen[0])
    c2.metric("Facturado", f"${resumen[1]:,.2f}")
    c3.metric("Utilidad", f"${resumen[2]:,.2f}")
    c4.metric("Pendiente", f"${pendientes:,.2f}")

    st.divider()
    st.subheader("📋 Historial de Facturas")

    facturas = cursor.execute("""
        SELECT *
        FROM facturas
        ORDER BY id DESC
    """).fetchall()

    if facturas:

        df = pd.DataFrame(
            facturas,
            columns=[
                "ID",
                "Cliente",
                "Factura",
                "Fecha Factura",
                "Fecha Pago",
                "Estado",
                "Mes",
                "Subtotal",
                "IVA",
                "Total",
                "Inversión",
                "Utilidad"
            ]
        )

        st.dataframe(df, use_container_width=True)

        for factura in facturas:

            if st.button(
                f"🗑️ Eliminar factura {factura[2]}",
                key=f"fact_{factura[0]}"
            ):
                cursor.execute(
                    "DELETE FROM facturas WHERE id=?",
                    (factura[0],)
                )

                guardar()
                st.rerun()

    else:

        st.info("No hay facturas registradas")