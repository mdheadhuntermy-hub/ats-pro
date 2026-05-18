import streamlit as st
import os
import uuid

from utils.pdf_generator import generar_pdf_dictamen, generar_pdf_simple_dictamen
from services.pdf_service import extraer_texto_pdf


def generar_dictamen(score, descripcion_vacante, texto_cv, skills):

    if score >= 80:
        resultado = "RECOMENDABLE"
        conclusion = (
            "El candidato presenta una alta compatibilidad con la vacante. "
            "Se recomienda avanzar a entrevista o siguiente etapa del proceso."
        )
    elif score >= 60:
        resultado = "PARCIALMENTE RECOMENDABLE"
        conclusion = (
            "El candidato presenta compatibilidad media con la vacante. "
            "Se recomienda revisión RH para validar experiencia, estabilidad y competencias clave."
        )
    elif score >= 40:
        resultado = "EN OBSERVACIÓN"
        conclusion = (
            "El candidato muestra algunos elementos relacionados con la vacante, "
            "pero requiere validación adicional antes de avanzar."
        )
    else:
        resultado = "NO RECOMENDABLE"
        conclusion = (
            "El candidato presenta baja compatibilidad inicial con la vacante. "
            "No se recomienda avanzar salvo que existan criterios estratégicos adicionales."
        )

    dictamen = f"""
Resultado IA: {resultado}

Match estimado: {score}%

Análisis:
La evaluación considera la descripción de la vacante, el contenido extraído del CV PDF y los comentarios capturados en el campo Skills / Comentarios RH.

Comentarios RH considerados:
{skills if skills else "Sin comentarios adicionales capturados."}

Conclusión:
{conclusion}
"""

    return dictamen.strip()


def generar_dictamen_seguridad(texto_seguridad):

    texto = (texto_seguridad or "").lower()

    riesgo = "BAJO"
    resultado = "APTO"
    observaciones = "No se identifican observaciones relevantes de riesgo."

    palabras_riesgo = [
        "antecedentes",
        "negativo",
        "registro judicial",
        "listas",
        "sat 69",
        "sat-69",
        "sat 69b",
        "sat-69b",
        "pld",
        "riesgo",
        "observación"
    ]

    for palabra in palabras_riesgo:
        if palabra in texto:
            riesgo = "REVISAR"
            resultado = "APTO CON OBSERVACIONES"
            observaciones = (
                "El estudio contiene términos que requieren revisión manual por RH "
                "antes de emitir una decisión final."
            )

    if "no se han encontrado registros" in texto or "sin observaciones" in texto:
        riesgo = "BAJO"
        resultado = "APTO"
        observaciones = (
            "El estudio no muestra hallazgos relevantes en antecedentes, listas o cumplimiento."
        )

    dictamen = f"""
DICTAMEN DE SEGURIDAD Y CONFIABILIDAD

Resultado: {resultado}
Nivel de riesgo: {riesgo}

Resumen:
Se analizó el estudio de seguridad cargado para el candidato, considerando identidad, historial laboral, listas, antecedentes y cumplimiento cuando la información está disponible en el documento.

Observaciones:
{observaciones}

Conclusión:
El candidato puede continuar en el proceso siempre que la información documental sea consistente con los criterios internos de contratación.
"""

    return dictamen.strip()


def generar_dictamen_psicometrico(texto_psicometrico):

    texto = (texto_psicometrico or "").lower()

    resultado = "RECOMENDABLE"
    observaciones = (
        "El perfil psicométrico no muestra alertas críticas evidentes en el documento analizado."
    )

    palabras_alerta = [
        "bajo",
        "riesgo",
        "no recomendable",
        "alerta",
        "impulsividad",
        "deshonestidad",
        "inestabilidad",
        "conflicto",
        "agresividad"
    ]

    for palabra in palabras_alerta:
        if palabra in texto:
            resultado = "RECOMENDABLE CON RESERVAS"
            observaciones = (
                "El reporte contiene elementos que requieren revisión RH antes de avanzar. "
                "Se recomienda validar competencias, estabilidad, apego a normas y ajuste al puesto."
            )

    if "no recomendable" in texto:
        resultado = "NO RECOMENDABLE"
        observaciones = (
            "El reporte presenta indicadores desfavorables. Se recomienda no avanzar "
            "sin una revisión profunda del caso."
        )

    dictamen = f"""
DICTAMEN PSICOMÉTRICO

Resultado: {resultado}

Resumen:
Se analizó el reporte psicométrico cargado para el candidato, considerando competencias, rasgos conductuales, ajuste al puesto y posibles indicadores de riesgo.

Observaciones:
{observaciones}

Conclusión:
La decisión final debe complementarse con entrevista RH, referencias laborales y criterios específicos de la vacante.
"""

    return dictamen.strip()


def ajustar_score_por_comentarios(score, skills):

    texto_negativo = (skills or "").lower()

    palabras_negativas = [
        "no tiene experiencia",
        "sin experiencia",
        "no cuenta con experiencia",
        "sin conocimientos",
        "no sabe",
        "junior",
        "no ha trabajado",
        "no conoce",
        "no domina"
    ]

    for palabra in palabras_negativas:
        if palabra in texto_negativo:
            score -= 25

    score = max(0, min(score, 100))

    return int(score)


def guardar_archivo_pdf(archivo, carpeta):

    if archivo is None:
        return "", ""

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    filename = f"{uuid.uuid4()}.pdf"
    ruta = os.path.join(carpeta, filename)

    with open(ruta, "wb") as f:
        f.write(archivo.read())

    texto = extraer_texto_pdf(ruta)

    return ruta, texto


def candidatos_page(cursor, guardar, calcular_match):

    st.title("👥 Candidatos")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")

    skills = st.text_area(
        "Skills / Comentarios RH",
        help="Agrega habilidades, observaciones, experiencia relevante o comentarios del reclutador."
    )

    estado = st.selectbox(
        "Estado",
        [
            "Filtro RH",
            "Entrevista",
            "Prueba Técnica",
            "Contratado",
            "Rechazado"
        ]
    )

    vacantes_db = cursor.execute("""
        SELECT titulo
        FROM vacantes
        ORDER BY titulo
    """).fetchall()

    lista_vacantes = [v[0] for v in vacantes_db]

    if lista_vacantes:
        vacante = st.selectbox("Vacante", lista_vacantes)
    else:
        st.warning("Primero debes crear una vacante")
        vacante = ""

    cv_pdf = st.file_uploader(
        "Subir CV PDF",
        type=["pdf"],
        key="cv_pdf"
    )

    seguridad_pdf = st.file_uploader(
        "📄 Estudio de Seguridad PDF",
        type=["pdf"],
        key="seguridad_pdf"
    )

    psicometrico_pdf = st.file_uploader(
        "🧠 Pruebas Psicométricas PDF",
        type=["pdf"],
        key="psicometrico_pdf"
    )

    if st.button("Guardar Candidato"):

        datos_vacante = cursor.execute("""
            SELECT descripcion
            FROM vacantes
            WHERE titulo=?
        """, (
            vacante,
        )).fetchone()

        if datos_vacante:
            descripcion_vacante = datos_vacante[0]
        else:
            descripcion_vacante = vacante

        pdf_path, texto_cv = guardar_archivo_pdf(cv_pdf, "cv")
        seguridad_path, texto_seguridad = guardar_archivo_pdf(seguridad_pdf, "seguridad")
        psicometrico_path, texto_psicometrico = guardar_archivo_pdf(psicometrico_pdf, "psicometricos")

        texto_evaluacion = f"""
        VACANTE:
        {descripcion_vacante}

        CV:
        {texto_cv}

        SKILLS / COMENTARIOS RH:
        {skills}
        """

        if texto_evaluacion.strip():

            with st.spinner("Analizando CV, vacante y comentarios RH con IA..."):

                score_cv = calcular_match(descripcion_vacante, texto_cv)
                score_skills = calcular_match(descripcion_vacante, skills)

                score = int(
                    (score_cv * 0.7) +
                    (score_skills * 0.3)
                )

                score = ajustar_score_por_comentarios(score, skills)

        else:
            score = 0

        dictamen = generar_dictamen(
            score,
            descripcion_vacante,
            texto_cv,
            skills
        )

        dictamen_seguridad = ""
        if texto_seguridad.strip():
            dictamen_seguridad = generar_dictamen_seguridad(texto_seguridad)

        dictamen_psicometrico = ""
        if texto_psicometrico.strip():
            dictamen_psicometrico = generar_dictamen_psicometrico(texto_psicometrico)

        cursor.execute("""
            INSERT INTO candidatos(
                nombre,
                correo,
                telefono,
                skills,
                score,
                estado,
                vacante,
                pdf,
                dictamen,
                seguridad_pdf,
                dictamen_seguridad,
                psicometrico_pdf,
                dictamen_psicometrico
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            nombre,
            correo,
            telefono,
            skills,
            score,
            estado,
            vacante,
            pdf_path,
            dictamen,
            seguridad_path,
            dictamen_seguridad,
            psicometrico_path,
            dictamen_psicometrico
        ))

        guardar()
        st.success("✅ Candidato guardado con dictámenes")
        st.rerun()

    st.divider()
    st.subheader("📋 Candidatos Registrados")

    busqueda = st.text_input("🔍 Buscar candidato")

    if busqueda:

        candidatos = cursor.execute("""
            SELECT *
            FROM candidatos
            WHERE nombre LIKE ?
            OR skills LIKE ?
            OR vacante LIKE ?
            OR dictamen LIKE ?
            OR dictamen_seguridad LIKE ?
            OR dictamen_psicometrico LIKE ?
            ORDER BY score DESC
        """, (
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%"
        )).fetchall()

    else:

        candidatos = cursor.execute("""
            SELECT *
            FROM candidatos
            ORDER BY score DESC
        """).fetchall()

    if candidatos:

        for candidato in candidatos:

            dictamen = candidato[9] if len(candidato) > 9 and candidato[9] else ""
            seguridad_path = candidato[10] if len(candidato) > 10 and candidato[10] else ""
            dictamen_seguridad = candidato[11] if len(candidato) > 11 and candidato[11] else ""
            psicometrico_path = candidato[12] if len(candidato) > 12 and candidato[12] else ""
            dictamen_psicometrico = candidato[13] if len(candidato) > 13 and candidato[13] else ""

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.write(f"👤 Nombre: {candidato[1]}")
            st.write(f"📧 Correo: {candidato[2]}")
            st.write(f"📱 Teléfono: {candidato[3]}")
            st.write(f"🛠 Skills / Comentarios RH: {candidato[4]}")
            st.write(f"🎯 Match IA: {candidato[5]}%")
            st.write(f"📌 Estado: {candidato[6]}")
            st.write(f"💼 Vacante: {candidato[7]}")

            if dictamen:

                with st.expander("🧠 Ver Dictamen IA"):

                    st.text(dictamen)

                    pdf_path = f"dictamen_{candidato[1]}.pdf"

                    if st.button(
                        "📄 Generar PDF Ejecutivo",
                        key=f"pdf_dictamen_{candidato[0]}"
                    ):

                        generar_pdf_dictamen(
                            nombre=candidato[1],
                            vacante=candidato[7],
                            match=candidato[5],
                            estado=candidato[6],
                            skills=candidato[4],
                            dictamen=dictamen,
                            output_path=pdf_path
                        )

                        st.success("PDF generado correctamente")

                    if os.path.exists(pdf_path):

                        with open(pdf_path, "rb") as pdf:

                            st.download_button(
                                label="⬇️ Descargar PDF Ejecutivo",
                                data=pdf,
                                file_name=pdf_path,
                                mime="application/pdf",
                                key=f"download_dictamen_{candidato[0]}"
                            )

            if dictamen_seguridad:

                with st.expander("🛡️ Ver Dictamen de Seguridad"):

                    st.text(dictamen_seguridad)

                    pdf_seguridad = f"dictamen_seguridad_{candidato[1]}.pdf"

                    if st.button(
                        "📄 Generar PDF Seguridad",
                        key=f"pdf_seguridad_dictamen_{candidato[0]}"
                    ):

                        generar_pdf_simple_dictamen(
                            titulo="DICTAMEN DE SEGURIDAD Y CONFIABILIDAD",
                            nombre=candidato[1],
                            vacante=candidato[7],
                            dictamen=dictamen_seguridad,
                            output_path=pdf_seguridad
                        )

                        st.success("PDF de seguridad generado correctamente")

                    if os.path.exists(pdf_seguridad):

                        with open(pdf_seguridad, "rb") as pdf:

                            st.download_button(
                                label="⬇️ Descargar PDF Seguridad",
                                data=pdf,
                                file_name=pdf_seguridad,
                                mime="application/pdf",
                                key=f"download_pdf_seguridad_{candidato[0]}"
                            )

            if dictamen_psicometrico:

                with st.expander("🧠 Ver Dictamen Psicométrico"):

                    st.text(dictamen_psicometrico)

                    pdf_psicometrico = f"dictamen_psicometrico_{candidato[1]}.pdf"

                    if st.button(
                        "📄 Generar PDF Psicométrico",
                        key=f"pdf_psicometrico_dictamen_{candidato[0]}"
                    ):

                        generar_pdf_simple_dictamen(
                            titulo="DICTAMEN PSICOMÉTRICO",
                            nombre=candidato[1],
                            vacante=candidato[7],
                            dictamen=dictamen_psicometrico,
                            output_path=pdf_psicometrico
                        )

                        st.success("PDF psicométrico generado correctamente")

                    if os.path.exists(pdf_psicometrico):

                        with open(pdf_psicometrico, "rb") as pdf:

                            st.download_button(
                                label="⬇️ Descargar PDF Psicométrico",
                                data=pdf,
                                file_name=pdf_psicometrico,
                                mime="application/pdf",
                                key=f"download_pdf_psicometrico_{candidato[0]}"
                            )

            estados = [
                "Filtro RH",
                "Entrevista",
                "Prueba Técnica",
                "Contratado",
                "Rechazado"
            ]

            estado_actual = candidato[6]

            if estado_actual not in estados:
                estado_actual = "Filtro RH"

            nuevo_estado = st.selectbox(
                "Cambiar Estado",
                estados,
                index=estados.index(estado_actual),
                key=f"estado_{candidato[0]}"
            )

            if st.button(
                "Actualizar Estado",
                key=f"update_{candidato[0]}"
            ):

                cursor.execute("""
                    UPDATE candidatos
                    SET estado=?
                    WHERE id=?
                """, (
                    nuevo_estado,
                    candidato[0]
                ))

                guardar()
                st.success("✅ Estado actualizado")
                st.rerun()

            col1, col2, col3 = st.columns(3)

            with col1:

                if candidato[8] and os.path.exists(candidato[8]):

                    with open(candidato[8], "rb") as pdf:

                        st.download_button(
                            "📄 Descargar CV",
                            pdf,
                            file_name=f"{candidato[1]}.pdf",
                            mime="application/pdf",
                            key=f"pdf_cv_{candidato[0]}"
                        )

                elif candidato[8]:

                    st.warning("CV no disponible en Render.")

            with col2:

                if seguridad_path and os.path.exists(seguridad_path):

                    with open(seguridad_path, "rb") as pdf:

                        st.download_button(
                            "🛡️ Descargar Seguridad",
                            pdf,
                            file_name=f"seguridad_{candidato[1]}.pdf",
                            mime="application/pdf",
                            key=f"pdf_seguridad_{candidato[0]}"
                        )

                elif seguridad_path:

                    st.warning("Estudio de seguridad no disponible en Render.")

            with col3:

                if psicometrico_path and os.path.exists(psicometrico_path):

                    with open(psicometrico_path, "rb") as pdf:

                        st.download_button(
                            "🧠 Descargar Psicométrico",
                            pdf,
                            file_name=f"psicometrico_{candidato[1]}.pdf",
                            mime="application/pdf",
                            key=f"pdf_psicometrico_{candidato[0]}"
                        )

                elif psicometrico_path:

                    st.warning("Psicométrico no disponible en Render.")

            if st.button(
                "🗑️ Eliminar",
                key=f"del_{candidato[0]}"
            ):

                cursor.execute(
                    "DELETE FROM candidatos WHERE id=?",
                    (candidato[0],)
                )

                guardar()
                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.info("No hay candidatos registrados")