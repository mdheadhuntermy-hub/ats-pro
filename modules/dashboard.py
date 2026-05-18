import streamlit as st
import pandas as pd


def dashboard_page(cursor):

    st.title("📊 Dashboard Ejecutivo")

    total_clientes = cursor.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    total_vacantes = cursor.execute("SELECT COUNT(*) FROM vacantes").fetchone()[0]
    total_candidatos = cursor.execute("SELECT COUNT(*) FROM candidatos").fetchone()[0]
    total_entrevistas = cursor.execute("SELECT COUNT(*) FROM entrevistas").fetchone()[0]

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

    st.subheader("ATS PRO ELITE • Executive Analytics")
    st.caption("Indicadores ejecutivos de reclutamiento y operación RH.")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🏢 Clientes", total_clientes)
    c2.metric("💼 Vacantes", total_vacantes)
    c3.metric("👥 Candidatos", total_candidatos)
    c4.metric("📅 Entrevistas", total_entrevistas)

    c5, c6, c7, c8 = st.columns(4)

    c5.metric("🏆 Contratados", contratados)
    c6.metric("❌ Rechazados", rechazados)
    c7.metric("💰 Facturación", f"${ingresos:,.0f}")
    c8.metric("📈 Utilidad", f"${utilidad:,.0f}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Pipeline Reclutamiento")

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
            st.info("Sin información")

    with col2:
        st.subheader("🏅 Top Candidatos")

        candidatos = cursor.execute("""
            SELECT nombre, vacante, score
            FROM candidatos
            ORDER BY score DESC
            LIMIT 10
        """).fetchall()

        if candidatos:
            df = pd.DataFrame(
                candidatos,
                columns=["Nombre", "Vacante", "Match IA"]
            )

            st.dataframe(
                df,
                use_container_width=True
            )
        else:
            st.info("Sin candidatos")

    st.divider()

    st.subheader("📅 Entrevistas Recientes")

    entrevistas = cursor.execute("""
        SELECT candidato, fecha, entrevistador, resultado
        FROM entrevistas
        ORDER BY id DESC
        LIMIT 5
    """).fetchall()

    if entrevistas:
        for entrevista in entrevistas:
            st.info(
                f"👤 {entrevista[0]} | 📅 {entrevista[1]} | "
                f"🧑‍💼 {entrevista[2]} | 📌 {entrevista[3]}"
            )
    else:
        st.info("No hay entrevistas recientes")