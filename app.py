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
from modules.kanban import kanban_page
from modules.entrevistas import entrevistas_page
from modules.contabilidad import contabilidad_page
from modules.reportes import reportes_page
from modules.configuracion import configuracion_page
from modules.portal_cliente import portal_cliente_page


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
    linear-gradient(rgba(3,8,20,0.88), rgba(3,8,20,0.88)),
    url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

section[data-testid="stSidebar"] {{
    min-width: 280px !important;
    width: 280px !important;
    background: rgba(5,10,20,0.95) !important;
    border-right:1px solid rgba(255,255,255,0.08) !important;
}}

section[data-testid="stSidebar"] > div {{
    display: block !important;
    visibility: visible !important;
}}

h1,h2,h3,h4,h5,h6,p,span,label,div {{
    color:white !important;
}}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input {{
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

div[data-baseweb="popover"],
div[data-baseweb="popover"] *,
ul[role="listbox"],
li[role="option"] {{
    background-color: rgba(15,23,42,0.98) !important;
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


rol = st.session_state.get("rol", "")

if rol == "Administrador":
    opciones_menu = [
        "Dashboard",
        "Clientes",
        "Vacantes",
        "Candidatos",
        "Kanban",
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
        "Kanban",
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

elif rol == "Cliente":
    opciones_menu = [
        "Portal Cliente",
        "Configuración"
    ]

else:
    opciones_menu = [
        "Dashboard",
        "Configuración"
    ]


iconos = {
    "Dashboard": "speedometer2",
    "Clientes": "building",
    "Vacantes": "briefcase",
    "Candidatos": "people",
    "Kanban": "kanban",
    "Entrevistas": "calendar-check",
    "Contabilidad": "cash-coin",
    "Reportes": "bar-chart-line",
    "Portal Cliente": "person-badge",
    "Configuración": "gear"
}

iconos_menu = [
    iconos.get(opcion, "circle")
    for opcion in opciones_menu
]


with st.sidebar:

    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=170)

    st.subheader("MDHEADHUNTER")
    st.caption("ATS PRO ELITE")
    st.divider()

    st.write(f"👤 Usuario: {st.session_state.usuario}")
    st.write(f"🔐 Rol: {st.session_state.rol}")

    st.divider()

    menu = option_menu(
        menu_title=None,
        options=opciones_menu,
        icons=iconos_menu,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "8px",
                "background-color": "#0f172a",
                "border-radius": "18px"
            },
            "icon": {
                "color": "#38bdf8",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "5px",
                "padding": "12px",
                "border-radius": "12px",
                "--hover-color": "#1e293b"
            },
            "nav-link-selected": {
                "background-color": "#2563eb"
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

elif menu == "Kanban":
    kanban_page(cursor, guardar)

elif menu == "Entrevistas":
    entrevistas_page(cursor, guardar)

elif menu == "Contabilidad":
    contabilidad_page(cursor, guardar)

elif menu == "Reportes":
    reportes_page(cursor)

elif menu == "Configuración":
    configuracion_page(cursor, guardar)

elif menu == "Portal Cliente":
    portal_cliente_page(cursor, guardar)