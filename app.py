# =========================================================
# ATS PRO ELITE 2025
# SISTEMA IA RECLUTAMIENTO
# =========================================================

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import pdfplumber
import re
import os
import base64

from io import BytesIO
from streamlit_option_menu import option_menu
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="ATS PRO ELITE",
    page_icon="🚀",
    layout="wide"
)


# =========================================================
# CARGAR FONDO
# =========================================================

def cargar_fondo():

    ruta = "fondo.jpg"

    if os.path.exists(ruta):

        with open(ruta, "rb") as f:

            data = base64.b64encode(
                f.read()
            ).decode()

        return data

    return ""


data = cargar_fondo()


# =========================================================
# CSS PROFESIONAL
# =========================================================

st.markdown(f"""
<style>

/* =========================
FONDO
========================= */

.stApp {{
    background:
    linear-gradient(
        rgba(2,6,23,0.88),
        rgba(2,6,23,0.88)
    ),
    url("data:image/jpg;base64,{data}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}


/* =========================
OCULTAR STREAMLIT
========================= */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}


/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {{

    background:
    rgba(5,10,20,0.95);

    border-right:
    1px solid rgba(255,255,255,0.08);
}}


/* =========================
TEXTOS
========================= */

h1,h2,h3,h4,h5,h6 {{
    color: white !important;
}}

label {{
    color: white !important;
}}

p,span,div {{
    color: white;
}}


/* =========================
INPUTS
========================= */

.stTextInput > div > div > input {{

    background-color:
    rgba(255,255,255,0.08) !important;

    color: white !important;

    border-radius: 12px !important;

    border:
    1px solid rgba(255,255,255,0.12) !important;

    height: 48px !important;

    padding-left: 15px !important;

    font-size: 16px !important;
}}


/* PLACEHOLDER */

.stTextInput input::placeholder {{
    color: #cccccc !important;
}}


/* PASSWORD */

input[type="password"] {{
    color: white !important;
}}


/* TEXTAREA */

textarea {{

    background-color:
    rgba(255,255,255,0.08) !important;

    color: white !important;

    border-radius: 12px !important;

    border:
    1px solid rgba(255,255,255,0.12) !important;
}}


/* SELECTBOX */

.stSelectbox div[data-baseweb="select"] > div {{

    background-color:
    rgba(255,255,255,0.08) !important;

    color: white !important;

    border-radius: 12px !important;
}}


/* BOTONES */

.stButton button {{

    background:
    linear-gradient(
        90deg,
        #0A66C2,
        #007BFF
    );

    color: white !important;

    border: none;

    border-radius: 12px;

    height: 48px;

    font-size: 16px;

    font-weight: bold;

    transition: 0.3s;
}}

.stButton button:hover {{

    transform: scale(1.02);

    box-shadow:
    0 0 15px rgba(0,123,255,0.5);
}}


/* MÉTRICAS */

div[data-testid="stMetric"] {{

    background:
    rgba(255,255,255,0.05);

    padding: 20px;

    border-radius: 20px;

    border:
    1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(10px);
}}


/* DATAFRAME */

[data-testid="stDataFrame"] {{

    background:
    rgba(255,255,255,0.04);

    border-radius: 15px;

    padding: 10px;
}}


/* LOGIN */

.login-box {{

    background:
    rgba(10,15,25,0.88);

    border-radius: 25px;

    padding: 45px;

    max-width: 420px;

    margin: auto;

    margin-top: 80px;

    border:
    1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(20px);
}}


/* LOGIN INPUTS */

div[data-testid="stTextInput"] {{

    max-width: 320px;

    margin: auto;
}}

div[data-testid="stButton"] {{

    max-width: 320px;

    margin: auto;
}}


/* CARD */

.card {{

    background:
    rgba(255,255,255,0.05);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 20px;

    padding: 25px;

    backdrop-filter: blur(10px);

    margin-bottom: 25px;
}}

</style>
""", unsafe_allow_html=True)


# =========================================================
# BASE DE DATOS
# =========================================================

conn = sqlite3.connect(
    "atspro.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa TEXT,
    contacto TEXT,
    correo TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vacantes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    salario TEXT,
    descripcion TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidatos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    correo TEXT,
    telefono TEXT,
    skills TEXT,
    score INTEGER,
    estado TEXT,
    vacante TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entrevistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidato TEXT,
    fecha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS facturas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    monto REAL
)
""")

conn.commit()


# =========================================================
# FUNCIONES IA
# =========================================================

def leer_pdf(pdf_file):

    texto = ""

    with pdfplumber.open(pdf_file) as pdf:

        for pagina in pdf.pages:

            contenido = pagina.extract_text()

            if contenido:
                texto += contenido

    return texto


def extraer_correo(texto):

    correos = re.findall(
        r'[\w\.-]+@[\w\.-]+',
        texto
    )

    return correos[0] if correos else "No encontrado"


def extraer_telefono(texto):

    telefonos = re.findall(
        r'\+?\d[\d\s\-]{8,}',
        texto
    )

    return telefonos[0] if telefonos else "No encontrado"


def extraer_nombre(texto):

    lineas = texto.split("\n")

    return lineas[0] if lineas else "No encontrado"


def detectar_skills(texto):

    skills = [
        "python",
        "excel",
        "sql",
        "power bi",
        "java",
        "javascript",
        "sap",
        "rh",
        "ventas",
        "reclutamiento",
        "english",
        "liderazgo"
    ]

    encontrados = [
        s for s in skills
        if s in texto.lower()
    ]

    return ", ".join(encontrados)


def calcular_match(vacante, cv):

    documentos = [vacante, cv]

    tfidf = TfidfVectorizer().fit_transform(
        documentos
    )

    similitud = cosine_similarity(
        tfidf[0:1],
        tfidf[1:2]
    )[0][0]

    return int(similitud * 100)


# =========================================================
# LOGIN
# =========================================================

if "login" not in st.session_state:
    st.session_state.login = False


if not st.session_state.login:

    st.markdown("""
    <div class="login-box">

    <h1 style='text-align:center;'>
    🚀 ATS PRO ELITE
    </h1>

    <p style='
    text-align:center;
    color:#cfd8dc;
    margin-bottom:30px;
    '>
    Inteligencia Artificial para Reclutamiento
    </p>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5,1,1.5])

    with c2:

        usuario = st.text_input(
            "Usuario"
        )

        password = st.text_input(
            "Contraseña",
            type="password"
        )

        if st.button("Ingresar"):

            if usuario == "admin" and password == "Dios2026":

                st.session_state.login = True
                st.rerun()

            else:

                st.error(
                    "Usuario incorrecto"
                )

    st.stop()


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    st.title("📊 Dashboard Ejecutivo")

    total_clientes = cursor.execute(
        "SELECT COUNT(*) FROM clientes"
    ).fetchone()[0]

    total_vacantes = cursor.execute(
        "SELECT COUNT(*) FROM vacantes"
    ).fetchone()[0]

    total_candidatos = cursor.execute(
        "SELECT COUNT(*) FROM candidatos"
    ).fetchone()[0]

    c1, c2, c3 = st.columns(3)

    c1.metric("Clientes", total_clientes)
    c2.metric("Vacantes", total_vacantes)
    c3.metric("Candidatos", total_candidatos)

    ranking = cursor.execute("""
    SELECT nombre, score
    FROM candidatos
    ORDER BY score DESC
    LIMIT 5
    """).fetchall()

    if ranking:

        fig, ax = plt.subplots()

        ax.barh(
            [x[0] for x in ranking],
            [x[1] for x in ranking]
        )

        st.pyplot(fig)


# =========================================================
# CLIENTES
# =========================================================

def clientes():

    st.title("🏢 Clientes")

    empresa = st.text_input("Empresa")
    contacto = st.text_input("Contacto")
    correo = st.text_input("Correo")

    if st.button("Guardar Cliente"):

        cursor.execute("""
        INSERT INTO clientes(
            empresa,
            contacto,
            correo
        )
        VALUES(?,?,?)
        """, (
            empresa,
            contacto,
            correo
        ))

        conn.commit()

        st.success("Cliente guardado")


# =========================================================
# VACANTES
# =========================================================

def vacantes():

    st.title("💼 Vacantes")

    titulo = st.text_input("Título")
    salario = st.text_input("Salario")
    descripcion = st.text_area("Descripción")

    if st.button("Guardar Vacante"):

        cursor.execute("""
        INSERT INTO vacantes(
            titulo,
            salario,
            descripcion
        )
        VALUES(?,?,?)
        """, (
            titulo,
            salario,
            descripcion
        ))

        conn.commit()

        st.success("Vacante creada")

    st.subheader("Eliminar vacante")

    vacantes_db = cursor.execute("""
    SELECT titulo
    FROM vacantes
    """).fetchall()

    titulos = [
        x[0] for x in vacantes_db
    ]

    if titulos:

        eliminar = st.selectbox(
            "Selecciona vacante",
            titulos
        )

        if st.button(
            "Eliminar vacante"
        ):

            cursor.execute("""
            DELETE FROM vacantes
            WHERE titulo=?
            """, (eliminar,))

            conn.commit()

            st.success(
                "Vacante eliminada"
            )

            st.rerun()


# =========================================================
# CANDIDATOS
# =========================================================

def candidatos():

    st.title("👥 ATS IA")

    vacantes_db = cursor.execute("""
    SELECT id, titulo, descripcion
    FROM vacantes
    """).fetchall()

    if not vacantes_db:

        st.warning(
            "Primero crea una vacante"
        )

        return

    vacante = st.selectbox(
        "Vacante",
        vacantes_db,
        format_func=lambda x: x[1]
    )

    archivo = st.file_uploader(
        "Sube CV PDF",
        type=["pdf"]
    )

    if archivo:

        texto = leer_pdf(archivo)

        nombre = extraer_nombre(texto)
        correo = extraer_correo(texto)
        telefono = extraer_telefono(texto)
        skills = detectar_skills(texto)

        score = calcular_match(
            vacante[2],
            texto
        )

        estado = "Filtro RH"

        if score >= 80:
            estado = "Entrevista"

        elif score < 60:
            estado = "Rechazado"

        cursor.execute("""
        INSERT INTO candidatos(
            nombre,
            correo,
            telefono,
            skills,
            score,
            estado,
            vacante
        )
        VALUES(?,?,?,?,?,?,?)
        """, (
            nombre,
            correo,
            telefono,
            skills,
            score,
            estado,
            vacante[1]
        ))

        conn.commit()

        st.success("CV analizado")

        st.write(f"👤 {nombre}")
        st.write(f"📧 {correo}")
        st.write(f"📱 {telefono}")
        st.write(f"🛠 {skills}")
        st.write(f"🎯 Match: {score}%")

    candidatos_db = cursor.execute("""
    SELECT nombre, score, estado
    FROM candidatos
    ORDER BY score DESC
    """).fetchall()

    if candidatos_db:

        df = pd.DataFrame(
            candidatos_db,
            columns=[
                "Nombre",
                "Score",
                "Estado"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        excel = BytesIO()

        with pd.ExcelWriter(
            excel,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        st.download_button(
            "📥 Descargar Excel",
            excel.getvalue(),
            "candidatos.xlsx"
        )

    st.subheader("Eliminar candidato")

    nombres = [
        x[0] for x in candidatos_db
    ]

    if nombres:

        eliminar = st.selectbox(
            "Selecciona candidato",
            nombres
        )

        if st.button(
            "Eliminar candidato"
        ):

            cursor.execute("""
            DELETE FROM candidatos
            WHERE nombre=?
            """, (eliminar,))

            conn.commit()

            st.success(
                "Candidato eliminado"
            )

            st.rerun()


# =========================================================
# ENTREVISTAS
# =========================================================

def entrevistas():

    st.title("📅 Entrevistas")

    candidato = st.text_input(
        "Nombre candidato"
    )

    fecha = st.date_input(
        "Fecha entrevista"
    )

    if st.button(
        "Guardar entrevista"
    ):

        cursor.execute("""
        INSERT INTO entrevistas(
            candidato,
            fecha
        )
        VALUES(?,?)
        """, (
            candidato,
            str(fecha)
        ))

        conn.commit()

        st.success(
            "Entrevista agendada"
        )

    entrevistas_db = cursor.execute("""
    SELECT *
    FROM entrevistas
    """).fetchall()

    for entrevista in entrevistas_db:

        st.write(
            f"👤 {entrevista[1]} | 📅 {entrevista[2]}"
        )


# =========================================================
# CONTABILIDAD
# =========================================================

def contabilidad():

    st.title("💰 Contabilidad")

    cliente = st.text_input(
        "Cliente"
    )

    monto = st.number_input(
        "Monto",
        min_value=0.0
    )

    if st.button(
        "Guardar Factura"
    ):

        cursor.execute("""
        INSERT INTO facturas(
            cliente,
            monto
        )
        VALUES(?,?)
        """, (
            cliente,
            monto
        ))

        conn.commit()

        st.success(
            "Factura guardada"
        )

    facturas = cursor.execute("""
    SELECT *
    FROM facturas
    """).fetchall()

    for factura in facturas:

        st.write(
            f"🧾 {factura[1]} - ${factura[2]}"
        )


# =========================================================
# REPORTES
# =========================================================

def reportes():

    st.title("📈 Reportes")

    datos = cursor.execute("""
    SELECT estado, COUNT(*)
    FROM candidatos
    GROUP BY estado
    """).fetchall()

    if datos:

        fig, ax = plt.subplots()

        ax.pie(
            [x[1] for x in datos],
            labels=[x[0] for x in datos]
        )

        st.pyplot(fig)


# =========================================================
# CONFIGURACIÓN
# =========================================================

def configuracion():

    st.title("⚙️ Configuración")

    if st.button(
        "Cerrar sesión"
    ):

        st.session_state.login = False
        st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    menu = option_menu(
        "ATS PRO",
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
            "speedometer2",
            "building",
            "briefcase",
            "people",
            "calendar",
            "cash-stack",
            "bar-chart",
            "gear"
        ],
        menu_icon="rocket",
        default_index=0
    )


# =========================================================
# NAVEGACIÓN
# =========================================================

if menu == "Dashboard":
    dashboard()

elif menu == "Clientes":
    clientes()

elif menu == "Vacantes":
    vacantes()

elif menu == "Candidatos":
    candidatos()

elif menu == "Entrevistas":
    entrevistas()

elif menu == "Contabilidad":
    contabilidad()

elif menu == "Reportes":
    reportes()

elif menu == "Configuración":
    configuracion()