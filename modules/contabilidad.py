import streamlit as st
import pandas as pd


MESES = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]


def contabilidad_page(cursor, guardar):

    st.title("💰 Contabilidad")

    clientes = cursor.execute(
        "SELECT empresa FROM clientes ORDER BY empresa"
    ).fetchall()

    lista_clientes = [c[0] for c in clientes]

    if not lista_clientes:
        st.warning("Primero registra clientes")
        return

    tab1, tab2, tab3 = st.tabs(
        [
            "📄 Facturas",
            "💸 Retiros / Egresos",
            "📊 Resumen"
        ]
    )

    # =====================================================
    # FACTURAS
    # =====================================================

    with tab1:

        st.subheader("Registrar Factura")

        cliente = st.selectbox("Cliente", lista_clientes)

        numero_factura = st.text_input(
            "Número de Factura"
        )

        fecha_factura = st.date_input(
            "Fecha de Factura"
        )

        pagada = st.selectbox(
            "Estado",
            ["Pendiente", "Pagada"]
        )

        fecha_pago = st.date_input(
            "Fecha de Pago"
        )

        mes = st.selectbox(
    	    "Mes",
            [
        	"Enero",
        	"Febrero",
       		"Marzo",
        	"Abril",
        	"Mayo",
        	"Junio",
        	"Julio",
        	"Agosto",
        	"Septiembre",
        	"Octubre",
        	"Noviembre",
        	"Diciembre"
             ]
          
        )

        subtotal = st.number_input(
            "Subtotal",
            min_value=0.0
        )

        inversion = st.number_input(
            "Inversión",
            min_value=0.0
        )

        iva = subtotal * 0.16
        total = subtotal + iva
        utilidad = subtotal - inversion

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "IVA",
            f"${iva:,.2f}"
        )

        c2.metric(
            "Total",
            f"${total:,.2f}"
        )

        c3.metric(
            "Utilidad",
            f"${utilidad:,.2f}"
        )

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

            st.success(
                "✅ Factura guardada"
            )

            st.rerun()

        st.divider()

        st.subheader(
            "📋 Historial de Facturas"
        )

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

            st.dataframe(
                df,
                use_container_width=True
            )

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

            st.info(
                "No hay facturas registradas"
            )

    # =====================================================
    # RETIROS
    # =====================================================

    with tab2:

        st.subheader(
            "Registrar Retiro / Egreso"
        )

        fecha_retiro = st.date_input(
            "Fecha del retiro",
            key="fecha_retiro"
        )

        concepto = st.text_input(
            "Concepto",
            placeholder="Ejemplo: retiro personal, pago proveedor, gasto operativo"
        )

        monto = st.number_input(
            "Monto del retiro",
            min_value=0.0,
            key="monto_retiro"
        )

        mes_retiro = st.selectbox(
            "Mes del retiro",
            MESES,
            key="mes_retiro"
        )

        observaciones = st.text_area(
            "Observaciones",
            key="obs_retiro"
        )

        if st.button(
            "Guardar Retiro / Egreso"
        ):

            cursor.execute("""
                INSERT INTO retiros(
                    fecha,
                    concepto,
                    monto,
                    mes,
                    observaciones
                )
                VALUES(?,?,?,?,?)
            """, (
                str(fecha_retiro),
                concepto,
                monto,
                mes_retiro,
                observaciones
            ))

            guardar()

            st.success(
                "✅ Retiro registrado"
            )

            st.rerun()

        st.divider()

        st.subheader(
            "📋 Historial de Retiros / Egresos"
        )

        retiros = cursor.execute("""
            SELECT *
            FROM retiros
            ORDER BY id DESC
        """).fetchall()

        if retiros:

            df_retiros = pd.DataFrame(
                retiros,
                columns=[
                    "ID",
                    "Fecha",
                    "Concepto",
                    "Monto",
                    "Mes",
                    "Observaciones"
                ]
            )

            st.dataframe(
                df_retiros,
                use_container_width=True
            )

            for retiro in retiros:

                if st.button(
                    f"🗑️ Eliminar retiro {retiro[2]}",
                    key=f"retiro_{retiro[0]}"
                ):

                    cursor.execute(
                        "DELETE FROM retiros WHERE id=?",
                        (retiro[0],)
                    )

                    guardar()

                    st.rerun()

        else:

            st.info(
                "No hay retiros registrados"
            )

    # =====================================================
    # RESUMEN
    # =====================================================

    with tab3:

        st.subheader(
            "📊 Resumen Financiero"
        )

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

        total_retiros = cursor.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM retiros
        """).fetchone()[0]

        inversion_total = cursor.execute("""
            SELECT COALESCE(SUM(inversion), 0)
            FROM facturas
        """).fetchone()[0]

        iva_total = cursor.execute("""
            SELECT COALESCE(SUM(iva), 0)
            FROM facturas
        """).fetchone()[0]

        utilidad_real = (
            pagadas -
            iva_total -
            inversion_total
        )

        saldo_disponible = (
            utilidad_real -
            total_retiros
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Facturas",
            resumen[0]
        )

        c2.metric(
            "Facturado Total",
            f"${resumen[1]:,.2f}"
        )

        c3.metric(
            "Pendiente por Cobrar",
            f"${pendientes:,.2f}"
        )

        c4, c5, c6 = st.columns(3)

        c4.metric(
            "IVA Acumulado",
            f"${iva_total:,.2f}"
        )

        c5.metric(
            "Inversión Total",
            f"${inversion_total:,.2f}"
        )

        c6.metric(
            "Utilidad Disponible",
            f"${saldo_disponible:,.2f}"
        )

        st.divider()

        st.subheader(
            "📅 Resumen por Mes"
        )

        mes_filtro = st.selectbox(
            "Seleccionar mes",
            MESES,
            key="mes_resumen"
        )

        facturado_mes = cursor.execute("""
            SELECT COALESCE(SUM(total), 0)
            FROM facturas
            WHERE mes=?
        """, (
            mes_filtro,
        )).fetchone()[0]

        pagado_mes = cursor.execute("""
            SELECT COALESCE(SUM(total), 0)
            FROM facturas
            WHERE mes=?
            AND pagada='Pagada'
        """, (
            mes_filtro,
        )).fetchone()[0]

        retiros_mes = cursor.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM retiros
            WHERE mes=?
        """, (
            mes_filtro,
        )).fetchone()[0]

        saldo_mes = pagado_mes - retiros_mes

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Facturado Mes",
            f"${facturado_mes:,.2f}"
        )

        m2.metric(
            "Cobrado Mes",
            f"${pagado_mes:,.2f}"
        )

        m3.metric(
            "Retiros Mes",
            f"${retiros_mes:,.2f}"
        )

        m4.metric(
            "Saldo Mes",
            f"${saldo_mes:,.2f}"
        )