import base64
def set_bg():
    with open("fondo.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{data}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()
import streamlit as st
st.markdown("""
<style>
.stButton>button {
    background-color: #0A66C2;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import pdfplumber
import re
from io import BytesIO
from streamlit_option_menu import option_menu
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CONFIGURACIÓN GENERAL
st.set_page_config(
    page_title='ATS PRO 7.0',
    page_icon='🚀',
    layout='wide'
)

# BASE DE DATOS
conn = sqlite3.connect('atspro.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa TEXT,
    contacto TEXT,
    correo TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS vacantes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    salario TEXT,
    descripcion TEXT
)
''')

cursor.execute('''
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
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS facturas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    monto REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS entrevistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidato TEXT,
    fecha TEXT
)
''')

conn.commit()


# FUNCIONES PDF
def leer_pdf(pdf_file):
    texto = ''
    with pdfplumber.open(pdf_file) as pdf:
        for pagina in pdf.pages:
            contenido = pagina.extract_text()
            if contenido:
                texto += contenido
    return texto


def extraer_correo(texto):
    correos = re.findall(r'[\w\.-]+@[\w\.-]+', texto)
    return correos[0] if correos else 'No encontrado'


def extraer_telefono(texto):
    telefonos = re.findall(r'\+?\d[\d\s\-]{8,}', texto)
    return telefonos[0] if telefonos else 'No encontrado'


def extraer_nombre(texto):
    return texto.split('\n')[0] if texto else 'No encontrado'


def detectar_skills(texto):
    skills = [
        'python',
        'excel',
        'sql',
        'power bi',
        'reclutamiento',
        'ventas',
        'java',
        'javascript',
        'sap',
        'rh',
        'autocad',
        'english',
        'liderazgo'
    ]

    encontrados = [s for s in skills if s in texto.lower()]
    return ', '.join(encontrados)


def analizar_cv(texto, score):
    texto = texto.lower()

    experiencia = len(re.findall(r'\d+\s*(años|anos)', texto))

    idiomas = []
    if 'english' in texto or 'ingles' in texto:
        idiomas.append('Inglés')

    if score >= 80:
        recomendacion = '🟢 Recomendado'
    elif score >= 60:
        recomendacion = '🟡 Revisar'
    else:
        recomendacion = '🔴 No recomendado'

    return experiencia, idiomas, recomendacion


def calcular_match(vacante, cv):
    documentos = [vacante, cv]
    tfidf = TfidfVectorizer().fit_transform(documentos)
    similitud = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return int(similitud * 100)


# DASHBOARD
def mostrar_dashboard():
    st.title('📊 Dashboard')

    total_clientes = cursor.execute(
        'SELECT COUNT(*) FROM clientes'
    ).fetchone()[0]

    total_vacantes = cursor.execute(
        'SELECT COUNT(*) FROM vacantes'
    ).fetchone()[0]

    total_candidatos = cursor.execute(
        'SELECT COUNT(*) FROM candidatos'
    ).fetchone()[0]

    c1, c2, c3 = st.columns(3)

    c1.metric('Clientes', total_clientes)
    c2.metric('Vacantes', total_vacantes)
    c3.metric('Candidatos', total_candidatos)

    st.subheader('🏆 Top candidatos')

    ranking = cursor.execute(
        '''
        SELECT nombre, score
        FROM candidatos
        ORDER BY score DESC
        LIMIT 5
        '''
    ).fetchall()

    if ranking:
        fig, ax = plt.subplots()

        ax.barh(
            [x[0] for x in ranking],
            [x[1] for x in ranking]
        )

        st.pyplot(fig)

        for candidato in ranking:
            st.write(
                f'⭐ {candidato[0]} - {candidato[1]}%'
            )


# CLIENTES
def mostrar_clientes():
    st.title('🏢 Clientes')

    empresa = st.text_input('Empresa')
    contacto = st.text_input('Contacto')
    correo = st.text_input('Correo')

    if st.button('Guardar Cliente'):
        cursor.execute(
            '''
            INSERT INTO clientes(
                empresa,
                contacto,
                correo
            )
            VALUES(?,?,?)
            ''',
            (
                empresa,
                contacto,
                correo
            )
        )

        conn.commit()
        st.success('Cliente guardado correctamente')


# VACANTES
def mostrar_vacantes():
    st.title('💼 Vacantes')

    titulo = st.text_input('Título')
    salario = st.text_input('Salario')
    descripcion = st.text_area('Descripción')

    if st.button('Guardar Vacante'):
        cursor.execute(
            '''
            INSERT INTO vacantes(
                titulo,
                salario,
                descripcion
            )
            VALUES(?,?,?)
            ''',
            (
                titulo,
                salario,
                descripcion
            )
        )

        conn.commit()
        st.success('Vacante creada correctamente')


# CANDIDATOS
def mostrar_candidatos():
    st.title('👥 ATS IA')

    vacantes = cursor.execute(
        '''
        SELECT id, titulo, descripcion
        FROM vacantes
        '''
    ).fetchall()

    if not vacantes:
        st.warning('Primero crea una vacante')
        return

    vacante = st.selectbox(
        'Vacante',
        vacantes,
        format_func=lambda x: x[1]
    )

    archivo = st.file_uploader(
        'Sube CV PDF',
        type=['pdf']
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

        experiencia, idiomas, recomendacion = analizar_cv(
            texto,
            score
        )

        estado = 'Filtro RH'

        if score >= 80:
            estado = 'Entrevista'
        elif score < 60:
            estado = 'Rechazado'

        existe = cursor.execute(
            '''
            SELECT id
            FROM candidatos
            WHERE correo=?
            ''',
            (correo,)
        ).fetchone()

        if not existe:
            cursor.execute(
                '''
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
                ''',
                (
                    nombre,
                    correo,
                    telefono,
                    skills,
                    score,
                    estado,
                    vacante[1]
                )
            )

            conn.commit()

        st.subheader('📄 Análisis CV')
        st.write(f'**Nombre:** {nombre}')
        st.write(f'**Correo:** {correo}')
        st.write(f'**Teléfono:** {telefono}')
        st.write(f'**Skills:** {skills}')
        st.write(f'**Experiencia detectada:** {experiencia} referencias')
        st.write(f'**Idiomas:** {", ".join(idiomas) if idiomas else "No detectados"}')
        st.write(f'**Score Match:** {score}%')
        st.write(f'**Recomendación IA:** {recomendacion}')

    candidatos = cursor.execute(
        '''
        SELECT *
        FROM candidatos
        WHERE vacante=?
        ORDER BY score DESC
        ''',
        (vacante[1],)
    ).fetchall()

    df = pd.DataFrame(
        candidatos,
        columns=[
            'ID',
            'Nombre',
            'Correo',
            'Telefono',
            'Skills',
            'Score',
            'Estado',
            'Vacante'
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader('📊 Resumen candidatos')

    contratados = len(
        df[df['Estado'] == 'Contratado']
    ) if not df.empty else 0

    entrevistas = len(
        df[df['Estado'] == 'Entrevista']
    ) if not df.empty else 0

    r1, r2 = st.columns(2)

    r1.metric(
        'Contratados',
        contratados
    )

    r2.metric(
        'Entrevistas',
        entrevistas
    )

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine='openpyxl'
    ) as writer:
        df.to_excel(
            writer,
            index=False
        )

    st.download_button(
        '📥 Descargar Excel',
        excel_buffer.getvalue(),
        'candidatos.xlsx'
    )

    estados = [
        'Filtro RH',
        'Entrevista',
        'Proceso',
        'Contratado',
        'Rechazado'
    ]

    for candidato in candidatos:
        col1, col2, col3 = st.columns([4, 2, 1])

        col1.write(
            f'👤 {candidato[1]} | 🎯 {candidato[5]}%'
        )

        nuevo_estado = col2.selectbox(
            'Estado',
            estados,
            index=estados.index(candidato[6])
            if candidato[6] in estados else 0,
            key=f'estado_{candidato[0]}'
        )

        if nuevo_estado != candidato[6]:
            cursor.execute(
                '''
                UPDATE candidatos
                SET estado=?
                WHERE id=?
                ''',
                (
                    nuevo_estado,
                    candidato[0]
                )
            )

            conn.commit()
            st.rerun()

        if col3.button(
            '🗑️',
            key=f'del_{candidato[0]}'
        ):
            cursor.execute(
                '''
                DELETE FROM candidatos
                WHERE id=?
                ''',
                (candidato[0],)
            )

            conn.commit()
            st.rerun()


# ENTREVISTAS
def mostrar_entrevistas():
    st.title('📅 Entrevistas')

    candidato = st.text_input(
        'Nombre candidato'
    )

    fecha = st.date_input(
        'Fecha entrevista'
    )

    preguntas = {
        'Desarrollador': [
            '¿Qué experiencia tienes con Python?',
            '¿Cómo manejas errores en código?',
            '¿Has trabajado con bases de datos?'
        ],
        'Ventas': [
            '¿Cómo manejas objeciones?',
            '¿Cómo cierras una venta?',
            '¿Cómo atraes clientes?'
        ],
        'RH': [
            '¿Cómo filtras candidatos?',
            '¿Qué ATS has utilizado?',
            '¿Cómo realizas entrevistas?'
        ]
    }

    tipo = st.selectbox(
        'Tipo entrevista',
        [
            'Desarrollador',
            'Ventas',
            'RH'
        ]
    )

    st.subheader(
        '🤖 Preguntas sugeridas'
    )

    for pregunta in preguntas[tipo]:
        st.write(
            '• ' + pregunta
        )

    if st.button(
        'Guardar entrevista'
    ):
        cursor.execute(
            '''
            INSERT INTO entrevistas(
                candidato,
                fecha
            )
            VALUES(?,?)
            ''',
            (
                candidato,
                str(fecha)
            )
        )

        conn.commit()
        st.success(
            'Entrevista agendada'
        )

    st.subheader(
        'Entrevistas programadas'
    )

    entrevistas = cursor.execute(
        '''
        SELECT *
        FROM entrevistas
        '''
    ).fetchall()

    for entrevista in entrevistas:
        st.write(
            f'👤 {entrevista[1]} | 📅 {entrevista[2]}'
        )


# CONTABILIDAD
def mostrar_contabilidad():
    st.title('💰 Contabilidad')

    cliente = st.text_input('Cliente')
    monto = st.number_input(
        'Monto',
        min_value=0.0
    )

    if st.button(
        'Guardar Factura'
    ):
        cursor.execute(
            '''
            INSERT INTO facturas(
                cliente,
                monto
            )
            VALUES(?,?)
            ''',
            (
                cliente,
                monto
            )
        )

        conn.commit()

    facturas = cursor.execute(
        '''
        SELECT *
        FROM facturas
        '''
    ).fetchall()

    for factura in facturas:
        st.write(
            f'🧾 {factura[1]} - ${factura[2]}'
        )


# REPORTES
def mostrar_reportes():
    st.title('📈 Reportes')

    total = cursor.execute(
        '''
        SELECT SUM(monto)
        FROM facturas
        '''
    ).fetchone()[0] or 0

    total_candidatos = cursor.execute(
        'SELECT COUNT(*) FROM candidatos'
    ).fetchone()[0]

    total_vacantes = cursor.execute(
        'SELECT COUNT(*) FROM vacantes'
    ).fetchone()[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        'Ingresos',
        f'${total}'
    )

    c2.metric(
        'Candidatos',
        total_candidatos
    )

    c3.metric(
        'Vacantes',
        total_vacantes
    )

    datos = cursor.execute(
        '''
        SELECT estado, COUNT(*)
        FROM candidatos
        GROUP BY estado
        '''
    ).fetchall()

    if datos:
        fig, ax = plt.subplots()

        ax.pie(
            [x[1] for x in datos],
            labels=[x[0] for x in datos]
        )

        st.pyplot(fig)


# CONFIGURACIÓN
def mostrar_configuracion():
    st.title('⚙️ Configuración')

    if st.button(
        'Cerrar sesión'
    ):
        st.session_state.login = False
        st.rerun()


# LOGIN
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.image("logo.png", width=200)
    st.title('🚀 ATS PRO')

    usuario = st.text_input('Usuario')

    contraseña = st.text_input(
        'Contraseña',
        type='password'
    )

    if st.button(
        'Ingresar'
    ):
        if usuario == 'admin' and contraseña == 'Dios2026':
            st.session_state.login = True
            st.rerun()
        else:
            st.error(
                'Usuario o contraseña incorrectos'
            )

    st.stop()


# MENÚ LATERAL
with st.sidebar:
    menu = option_menu(
        None,
        [
            'Dashboard',
            'Clientes',
            'Vacantes',
            'Candidatos',
            'Entrevistas',
            'Contabilidad',
            'Reportes',
            'Configuración'
        ],
        icons=[
            'speedometer2',
            'building',
            'briefcase',
            'people',
            'calendar',
            'cash-stack',
            'bar-chart',
            'gear'
        ]
    )


# NAVEGACIÓN
if menu == 'Dashboard':
    mostrar_dashboard()

elif menu == 'Clientes':
    mostrar_clientes()

elif menu == 'Vacantes':
    mostrar_vacantes()

elif menu == 'Candidatos':
    mostrar_candidatos()

elif menu == 'Entrevistas':
    mostrar_entrevistas()

elif menu == 'Contabilidad':
    mostrar_contabilidad()

elif menu == 'Reportes':
    mostrar_reportes()

elif menu == 'Configuración':
    mostrar_configuracion()