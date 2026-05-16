import streamlit as st
import pandas as pd


def dashboard_page(cursor):

    st.title("🚀 ATS PRO ELITE")
    st.subheader("Dashboard Ejecutivo")

    total_clientes = cursor.execute("""
        SELECT COUNT(*) FROM clientes
    """).fetchone()[0]

    total_vacantes = cursor.execute("""
        SELECT COUNT(*) FROM vacantes
    """).fetchone()[0]

    total_candidatos = cursor.execute("""
        SELECT COUNT(*) FROM candidatos
    """).fetchone()[0]

    total_entrevistas = cursor.execute("""
        SELECT COUNT(*) FROM entrevistas
    """).fetchone()[0]

    contratados = cursor.execute("""
        SELECT COUNT(*) FROM candidatos
        WHERE estado='Contratado'
    """).fetchone()[0]

    rechazados = cursor.execute("""
        SELECT COUNT(*) FROM candidatos
        WHERE estado='Rechazado'
    """).fetchone()[0]

    ingresos = cursor.execute("""
        SELECT COALESCE(SUM(total),0)
        FROM facturas
    """).fetchone()[0]

    utilidad = cursor.execute("""
        SELECT COALESCE(SUM(utilidad),0)
        FROM facturas
    """).fetchone()[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes", total_clientes)
    c2.metric("Vacantes", total_vacantes)
    c3.metric("Candidatos", total_candidatos)

    c4, c5, c6 = st.columns(3)
    c4.metric("Contratados", contratados)
    c5.metric("Rechazados", rechazados)
    c6.metric("Entrevistas", total_entrevistas)

    c7, c8 = st.columns(2)
    c7.metric("Facturación", f"${ingresos:,.2f}")
    c8.metric("Utilidad", f"${utilidad:,.2f}")

    st.divider()

    st.subheader("🎯 Top Candidatos")

    candidatos = cursor.execute("""
        SELECT nombre, vacante, score, estado
        FROM candidatos
        ORDER BY score DESC
        LIMIT 10
    """).fetchall()

    if candidatos:
        df = pd.DataFrame(
            candidatos,
            columns=["Nombre", "Vacante", "Match", "Estado"]
        )

        st.dataframe(
            df,
            width="stretch"
        )
    else:
        st.info("No hay candidatos")

    st.divider()

    st.subheader("📈 Pipeline Reclutamiento")

    pipeline = cursor.execute("""
        SELECT estado, COUNT(*)
        FROM candidatos
        GROUP BY estado
    """).fetchall()

    if pipeline:
        df_pipeline = pd.DataFrame(
            pipeline,
            columns=["Estado", "Cantidad"]
        )

        st.bar_chart(
            df_pipeline,
            x="Estado",
            y="Cantidad"
        )
    else:
        st.info("No hay datos para mostrar")