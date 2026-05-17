# -*- coding: utf-8 -*-

import streamlit as st
import os
import base64

from streamlit_option_menu import option_menu
from auth.login import login
from database.connection import get_connection, get_cursor, init_db

from modules.dashboard import dashboard_page
from modules.clientes import clientes_page
from modules.vacantes import vacantes_page
from modules.candidatos import candidatos_page
from modules.entrevistas import entrevistas_page
from modules.contabilidad import contabilidad_page
from modules.reportes import reportes_page
from modules.configuracion import configuracion_page


st.set_page_config(
    page_title="ATS PRO ELITE",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


bg = get_base64("assets/fondo.jpg")

st.markdown(f"""
<style>
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

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

section[data-testid="stSidebar"] {{
    background: rgba(5,10,20,0.95);
    border-right:1px solid rgba(255,255,255,0.08);
}}

h1,h2,h3,h4,h5,h6,p,span,label,div {{
    color:white !important;
}}

.stTextInput input,
.stTextArea textarea {{
    background-color: rgba(15,23,42,0.95) !important;
    color: white !important;
    border-radius:14px !important;
    border:1px solid rgba(255,255,255,0.20) !important;
}}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {{
    color: #cbd5e1 !important;
}}

.stSelectbox div[data-baseweb="select"] > div {{
    background-color: rgba(15,23,42,0.95) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
}}

.stSelectbox svg {{
    fill: white !important;
}}

.stSelectbox span {{
    color: white !important;
}}

.stSelectbox input {{
    color: white !important;
}}

.stButton button {{
    width:100%;
    border:none;
    border-radius:14px;
    height:48px;
    color:white;
    font-weight:bold;
    background:linear-gradient(90deg,#2563eb,#7c3aed);
}}

.card {{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:24px;
    padding:25px;
    margin-bottom:20px;
    backdrop-filter:blur(14px);
}}


div[data-testid="metric-container"] {{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:22px;
    padding:22px;
}}

.stNumberInput input,
.stDateInput input {{
    background-color: rgba(15,23,42,0.95) !important;
    color: white !important;
    border-radius:14px !important;
    border:1px solid rgba(255,255,255,0.20) !important;
}}

.stNumberInput button,
.stDateInput button {{
    background-color: rgba(15,23,42,0.95) !important;
    color: white !important;
}}

div[data-baseweb="popover"] {{
    background-color: rgba(15,23,42,0.98) !important;
    color: white !important;
}}

div[data-baseweb="popover"] * {{
    background-color: rgba(15,23,42,0.98) !important;
    color: white !important;
}}

ul[role="listbox"] {{
    background-color: rgba(15,23,42,0.98) !important;
}}

li[role="option"] {{
    background-color: rgba(15,23,42,0.98) !important;
    color: white !important;
}}

li[role="option"]:hover {{
    background-color: rgba(37,99,235,0.55) !important;
    color: white !important;
}}

</style>
""", unsafe_allow_html=True)


init_db()

conn = get_connection()
cursor = get_cursor()


def guardar():
    conn.commit()


@st.cache_resource
def cargar_modelo_ia():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def calcular_match(vacante, cv):
    try:
        from sentence_transformers import util

        modelo_ia = cargar_modelo_ia()

        embedding1 = modelo_ia.encode(
            vacante or "",
            convert_to_tensor=True
        )

        embedding2 = modelo_ia.encode(
            cv or "",
            convert_to_tensor=True
        )

        similitud = util.pytorch_cos_sim(
            embedding1,
            embedding2
        )

        score = float(similitud[0][0]) * 100
        score = max(0, min(score, 100))

        return int(score)

    except Exception:
        return 0


login(cursor)


with st.sidebar:

    if os.path.exists("assets/logo.png"):
        st.image(
            "assets/logo.png",
            width=180
        )

    st.markdown("""
    <h1>ATS PRO</h1>
    <p style='color:#94a3b8;'>ELITE 2025</p>
    """, unsafe_allow_html=True)

    rol = st.session_state.get(
        "rol",
        "Administrador"
    )

    if rol == "Administrador":

        opciones_menu = [
            "Dashboard",
            "Clientes",
            "Vacantes",
            "Candidatos",
            "Entrevistas",
            "Contabilidad",
            "Reportes",
            "Configuración"
        ]

    elif rol == "RH":

        opciones_menu = [
            "Dashboard",
            "Vacantes",
            "Candidatos",
            "Entrevistas",
            "Reportes",
            "Configuración"
        ]

    elif rol == "Contabilidad":

        opciones_menu = [
            "Dashboard",
            "Clientes",
            "Contabilidad",
            "Reportes",
            "Configuración"
        ]

    else:

        opciones_menu = [
            "Dashboard",
            "Configuración"
        ]

    menu = option_menu(
    menu_title=None,
    options=opciones_menu,
    icons=[
        "speedometer2",
        "building",
        "briefcase",
        "people",
        "calendar-check",
        "cash-coin",
        "bar-chart-line",
        "gear"
    ],
    default_index=0,
    styles={
        "container": {
            "padding": "6px",
            "background-color": "rgba(15,23,42,0.92)",
            "border-radius": "18px"
        },
        "icon": {
            "color": "#38bdf8",
            "font-size": "18px"
        },
        "nav-link": {
            "font-size": "15px",
            "text-align": "left",
            "margin": "5px 0",
            "border-radius": "12px",
            "color": "#e5e7eb",
            "background-color": "rgba(15,23,42,0.55)",
            "--hover-color": "rgba(37,99,235,0.30)"
        },
        "nav-link-selected": {
            "background": "linear-gradient(90deg,#2563eb,#7c3aed)",
            "color": "#ffffff",
            "font-weight": "700"
        }
    }
)

if menu == "Dashboard":
    dashboard_page(cursor)

elif menu == "Clientes":
    clientes_page(cursor, guardar)

elif menu == "Vacantes":
    vacantes_page(cursor, guardar)

elif menu == "Candidatos":
    candidatos_page(cursor, guardar, calcular_match)

elif menu == "Entrevistas":
    entrevistas_page(cursor, guardar)

elif menu == "Contabilidad":
    contabilidad_page(cursor, guardar)

elif menu == "Reportes":
    reportes_page(cursor)

elif menu == "Configuración":
    configuracion_page(cursor, guardar)