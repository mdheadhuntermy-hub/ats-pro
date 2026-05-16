import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from io import BytesIO


def reportes_page(cursor):

    st.title("📈 Reportes")

    candidatos = cursor.execute("""
        SELECT nombre,
               correo,
               telefono,
               skills,
               score,
               estado,
               vacante
        FROM candidatos
        ORDER BY score DESC
    """).fetchall()

    if candidatos:

        df = pd.DataFrame(
            candidatos,
            columns=[
                "Nombre",
                "Correo",
                "Teléfono",
                "Skills",
                "Match IA",
                "Estado",
                "Vacante"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # =====================================
        # EXPORTAR EXCEL
        # =====================================

        excel = BytesIO()

        with pd.ExcelWriter(
            excel,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Candidatos"
            )

        st.download_button(
            "📥 Descargar Reporte Excel",
            excel.getvalue(),
            "reporte_candidatos.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:

        st.info(
            "No hay candidatos para reportar"
        )

    st.divider()

    # =====================================
    # GRÁFICA
    # =====================================

    datos = cursor.execute("""
        SELECT estado,
               COUNT(*)
        FROM candidatos
        GROUP BY estado
    """).fetchall()

    if datos:

        estados = [x[0] for x in datos]

        valores = [x[1] for x in datos]

        fig, ax = plt.subplots()

        ax.pie(
            valores,
            labels=estados,
            autopct="%1.1f%%"
        )

        fig.patch.set_alpha(0)

        st.pyplot(fig)

    else:

        st.info(
            "No hay datos para mostrar"
        )