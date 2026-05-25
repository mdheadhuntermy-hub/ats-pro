import streamlit as st
from datetime import datetime


def color_estado(estado):

    colores = {
        "Filtro RH": "#2563eb",
        "Entrevista": "#f59e0b",
        "Prueba Técnica": "#8b5cf6",
        "Contratado": "#16a34a",
        "Rechazado": "#dc2626"
    }

    return colores.get(estado, "#334155")


def registrar_historial(
    cursor,
    candidato_id,
    candidato,
    accion,
    detalle
):

    usuario = st.session_state.get(
        "usuario",
        "Sistema"
    )

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    cursor.execute("""
        INSERT INTO historial_candidatos(
            candidato_id,
            candidato,
            accion,
            detalle,
            usuario,
            fecha
        )
        VALUES(?,?,?,?,?,?)
    """, (
        candidato_id,
        candidato,
        accion,
        detalle,
        usuario,
        fecha
    ))


def mostrar_timeline(cursor, candidato_id):

    historial = cursor.execute("""
        SELECT accion, detalle, usuario, fecha
        FROM historial_candidatos
        WHERE candidato_id=?
        ORDER BY id DESC
        LIMIT 10
    """, (
        candidato_id,
    )).fetchall()

    if historial:

        for item in historial:

            st.markdown(f"""
            <div style="
                background:#0f172a;
                padding:10px;
                border-radius:10px;
                margin-bottom:10px;
                border-left:4px solid #38bdf8;
            ">
                <b>{item[0]}</b><br>
                {item[1]}<br>
                👤 {item[2]}<br>
                🕒 {item[3]}
            </div>
            """, unsafe_allow_html=True)

    else:

        st.info("Sin historial")


def kanban_page(cursor, guardar):

    st.title("📌 Pipeline Kanban")

    rol = st.session_state.get("rol", "")
    usuario = st.session_state.get("usuario", "")

    estados = [
        "Filtro RH",
        "Entrevista",
        "Prueba Técnica",
        "Contratado",
        "Rechazado"
    ]

    columnas = st.columns(len(estados))

    for i, estado in enumerate(estados):

        with columnas[i]:

            color = color_estado(estado)

            if rol == "RH":

                candidatos = cursor.execute("""
                    SELECT
                        id,
                        nombre,
                        vacante,
                        score
                    FROM candidatos
                    WHERE estado=?
                    AND creado_por=?
                    ORDER BY score DESC
                """, (
                    estado,
                    usuario
                )).fetchall()

            else:

                candidatos = cursor.execute("""
                    SELECT
                        id,
                        nombre,
                        vacante,
                        score
                    FROM candidatos
                    WHERE estado=?
                    ORDER BY score DESC
                """, (
                    estado,
                )).fetchall()

            st.markdown(f"""
            <div style="
                background:{color};
                padding:12px;
                border-radius:14px;
                text-align:center;
                font-weight:bold;
                color:white;
                margin-bottom:15px;
                font-size:18px;
            ">
                {estado}<br>
                <span style="font-size:13px;">
                    {len(candidatos)} candidato(s)
                </span>
            </div>
            """, unsafe_allow_html=True)

            if candidatos:

                for candidato in candidatos:

                    candidato_id = candidato[0]
                    nombre = candidato[1]
                    vacante = candidato[2]
                    score = candidato[3]

                    st.markdown(f"""
                    <div style="
                        background:#0f172a;
                        padding:14px;
                        border-radius:16px;
                        margin-bottom:15px;
                        border-top:5px solid {color};
                        box-shadow:0 0 12px rgba(0,0,0,0.25);
                    ">
                    """, unsafe_allow_html=True)

                    st.markdown(
                        f"### 👤 {nombre}"
                    )

                    st.write(f"💼 {vacante}")
                    st.write(f"🎯 Match IA: {score}%")

                    nuevo_estado = st.selectbox(
                        "Mover",
                        estados,
                        index=estados.index(estado),
                        key=f"estado_{candidato_id}"
                    )

                    if st.button(
                        "Actualizar",
                        key=f"move_{candidato_id}"
                    ):

                        if nuevo_estado != estado:

                            cursor.execute("""
                                UPDATE candidatos
                                SET estado=?
                                WHERE id=?
                            """, (
                                nuevo_estado,
                                candidato_id
                            ))

                            registrar_historial(
                                cursor,
                                candidato_id,
                                nombre,
                                "Cambio de Estado",
                                f"{estado} → {nuevo_estado}"
                            )

                            guardar()

                            st.success(
                                "✅ Estado actualizado"
                            )

                            st.rerun()

                    with st.expander("📋 RH"):

                        detalle = cursor.execute("""
                            SELECT
                                correo,
                                telefono,
                                skills,
                                dictamen,
                                dictamen_seguridad,
                                dictamen_psicometrico,
                                creado_por
                            FROM candidatos
                            WHERE id=?
                        """, (
                            candidato_id,
                        )).fetchone()

                        if detalle:

                            st.write(f"📧 {detalle[0]}")
                            st.write(f"📱 {detalle[1]}")

                            st.write("🛠 Skills")
                            st.info(detalle[2])

                            st.write("🧠 Dictamen IA")
                            st.text(detalle[3])

                            st.write("🛡️ Seguridad")
                            st.text(detalle[4])

                            st.write("🧠 Psicométrico")
                            st.text(detalle[5])

                            if rol != "RH":
                                st.caption(
                                    f"👤 Reclutador: {detalle[6]}"
                                )

                    with st.expander("🕒 Timeline"):

                        mostrar_timeline(
                            cursor,
                            candidato_id
                        )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

            else:

                st.markdown("""
                <div style="
                    background:#0f172a;
                    padding:15px;
                    border-radius:15px;
                    text-align:center;
                    opacity:0.75;
                    border:1px dashed rgba(255,255,255,0.15);
                ">
                    Sin candidatos
                </div>
                """, unsafe_allow_html=True)