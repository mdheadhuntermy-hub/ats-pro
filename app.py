# =========================================================
# ATS PRO ELITE 2025 - PREMIUM UI
# =========================================================

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
import base64
from streamlit_option_menu import option_menu

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="ATS PRO ELITE",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# FONDO
# =========================================================

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg = get_base64("fondo.jpg")

# =========================================================
# CSS PREMIUM
# =========================================================

st.markdown(f"""
<style>

/* ===== FONDO ===== */

.stApp {{
    background:
    linear-gradient(
        rgba(3,8,20,0.88),
        rgba(3,8,20,0.88)
    ),
    url("data:image/jpg;base64,{bg}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* ===== OCULTAR ===== */

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {{

    background:
    rgba(5,10,20,0.95);

    border-right:
    1px solid rgba(255,255,255,0.08);
}}

/* ===== TEXTOS ===== */

h1,h2,h3,h4,h5,h6 {{
    color:white !important;
}}

p,span,label,div {{
    color:white !important;
}}

/* ===== INPUTS ===== */

.stTextInput input {{
    background:
    rgba(255,255,255,0.08) !important;

    color:white !important;

    border-radius:14px !important;

    border:
    1px solid rgba(255,255,255,0.10) !important;

    height:45px !important;
}}

textarea {{
    background:
    rgba(255,255,255,0.08) !important;

    color:white !important;

    border-radius:14px !important;
}}

/* ===== BOTONES ===== */

.stButton button {{

    width:100%;

    border:none;

    border-radius:14px;

    height:48px;

    color:white;

    font-weight:bold;

    background:
    linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    transition:0.3s;
}}

.stButton button:hover {{

    transform:translateY(-2px);

    box-shadow:
    0 0 20px rgba(37,99,235,0.4);
}}

/* ===== CARDS ===== */

.card {{

    background:
    rgba(255,255,255,0.05);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:24px;

    padding:25px;

    backdrop-filter:blur(14px);

    margin-bottom:20px;

    box-shadow:
    0 0 25px rgba(0,0,0,0.25);
}}

/* ===== METRICS ===== */

div[data-testid="metric-container"] {{

    background:
    rgba(255,255,255,0.05);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:22px;

    padding:22px;

    backdrop-filter:blur(10px);
}}

/* ===== DATAFRAME ===== */

[data-testid="stDataFrame"] {{

    background:
    rgba(255,255,255,0.04);

    border-radius:20px;

    padding:10px;
}}

/* ===== LOGIN ===== */

.login-box {{

    background:
    rgba(10,15,25,0.92);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:28px;

    padding:50px;

    max-width:420px;

    margin:auto;

    margin-top:100px;

    backdrop-filter:blur(20px);

    text-align:center;
}}

/* ===== LOGIN CAMPOS ===== */

div[data-testid="stTextInput"] {{
    max-width:320px;
    margin:auto;
}}

div[data-testid="stButton"] {{
    max-width:320px;
    margin:auto;
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(
    "atspro.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================================
# LOGIN
# =========================================================

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("""
    <div class='login-box'>

    <h1>🚀 ATS PRO ELITE</h1>

    <p style='color:#cbd5e1;'>
    Sistema Inteligente de Reclutamiento
    </p>

    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1.5,1,1.5])

    with c2:

        usuario = st.text_input("Usuario")
        password = st.text_input(
            "Contraseña",
            type="password"
        )

        st.write("")

        if st.button("Ingresar"):

            if usuario == "admin" and password == "Dios2026":

                st.session_state.login = True
                st.rerun()

            else:
                st.error("Credenciales incorrectas")

    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <h1 style='font-size:35px;'>
    🚀 ATS PRO
    </h1>

    <p style='color:#94a3b8;'>
    ELITE 2025
    </p>
    """, unsafe_allow_html=True)

    menu = option_menu(
        "",
        [
            "Dashboard",
            "Clientes",
            "Vacantes",
            "Candidatos",
            "Entrevistas",
            "Contabilidad",
            "Reportes",
            "Configuración"
        ],
        icons=[
            "grid",
            "building",
            "briefcase",
            "people",
            "calendar",
            "cash-stack",
            "bar-chart",
            "gear"
        ],
        default_index=0
    )

# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.markdown("""
    <h1>
    👋 Bienvenido Administrador
    </h1>

    <p style='color:#cbd5e1;'>
    Sistema ATS Inteligente con IA
    </p>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("Clientes", "12")

    with c2:
        st.metric("Vacantes", "8")

    with c3:
        st.metric("Candidatos", "54")

    with c4:
        st.metric("Entrevistas", "6")

    st.write("")

    col1,col2 = st.columns([1.3,1])

    with col1:

        st.markdown("""
        <div class='card'>
        <h3>🏆 Top Candidatos</h3>
        </div>
        """, unsafe_allow_html=True)

        candidatos = [
            "Juan Pérez",
            "Ana López",
            "Carlos Ruiz",
            "María Torres"
        ]

        scores = [95,88,80,74]

        fig, ax = plt.subplots()

        ax.barh(candidatos, scores)

        ax.set_facecolor("none")

        fig.patch.set_alpha(0)

        st.pyplot(fig)

    with col2:

        st.markdown("""
        <div class='card'>
        <h3>📊 Estados ATS</h3>
        </div>
        """, unsafe_allow_html=True)

        estados = [
            "Entrevista",
            "Filtro RH",
            "Rechazado"
        ]

        valores = [12,8,4]

        fig2, ax2 = plt.subplots()

        ax2.pie(
            valores,
            labels=estados,
            autopct='%1.1f%%'
        )

        fig2.patch.set_alpha(0)

        st.pyplot(fig2)

# =========================================================
# CLIENTES
# =========================================================

elif menu == "Clientes":

    st.title("🏢 Clientes")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    empresa = st.text_input("Empresa")
    contacto = st.text_input("Contacto")
    correo = st.text_input("Correo")

    if st.button("Guardar Cliente"):
        st.success("Cliente guardado")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# VACANTES
# =========================================================

elif menu == "Vacantes":

    st.title("💼 Vacantes")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    titulo = st.text_input("Título")
    salario = st.text_input("Salario")
    descripcion = st.text_area("Descripción")

    if st.button("Guardar Vacante"):
        st.success("Vacante creada")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CANDIDATOS
# =========================================================

elif menu == "Candidatos":

    st.title("👥 ATS IA")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.file_uploader(
        "Subir CV PDF",
        type=["pdf"]
    )

    st.dataframe(pd.DataFrame({
        "Nombre":[
            "Juan",
            "Ana"
        ],
        "Score":[95,88],
        "Estado":[
            "Entrevista",
            "Filtro RH"
        ]
    }))

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ENTREVISTAS
# =========================================================

elif menu == "Entrevistas":

    st.title("📅 Entrevistas")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.text_input("Candidato")
    st.date_input("Fecha")

    if st.button("Guardar entrevista"):
        st.success("Entrevista guardada")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CONTABILIDAD
# =========================================================

elif menu == "Contabilidad":

    st.title("💰 Contabilidad")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.text_input("Cliente")
    st.number_input("Monto")

    if st.button("Guardar factura"):
        st.success("Factura guardada")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# REPORTES
# =========================================================

elif menu == "Reportes":

    st.title("📈 Reportes")

    fig, ax = plt.subplots()

    ax.plot(
        [1,2,3,4],
        [10,20,15,30]
    )

    fig.patch.set_alpha(0)

    st.pyplot(fig)

# =========================================================
# CONFIG
# =========================================================

elif menu == "Configuración":

    st.title("⚙️ Configuración")

    if st.button("Cerrar sesión"):

        st.session_state.login = False
        st.rerun()