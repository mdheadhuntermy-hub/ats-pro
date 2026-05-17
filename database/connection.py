import sqlite3
import streamlit as st


DB_NAME = "atspro.db"


@st.cache_resource
def get_connection():

    conn = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

    return conn


def get_cursor():

    conn = get_connection()

    return conn.cursor()


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # =========================================
    # USUARIOS
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        password TEXT,
        rol TEXT
    )
    """)

    # =========================================
    # CLIENTES
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa TEXT,
        contacto TEXT,
        correo TEXT,
        telefono TEXT
    )
    """)

    # =========================================
    # VACANTES
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacantes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        salario TEXT,
        descripcion TEXT
    )
    """)

    # =========================================
    # CANDIDATOS
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidatos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT,
        telefono TEXT,
        skills TEXT,
        score INTEGER,
        estado TEXT,
        vacante TEXT,
        pdf TEXT,
        dictamen TEXT
    )
    """)

    # =========================================
    # ENTREVISTAS
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entrevistas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidato TEXT,
        fecha TEXT,
        hora TEXT,
        entrevistador TEXT,
        calificacion INTEGER,
        observaciones TEXT,
        resultado TEXT
    )
    """)

    # =========================================
    # FACTURAS
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        numero_factura TEXT,
        fecha_factura TEXT,
        fecha_pago TEXT,
        pagada TEXT,
        mes TEXT,
        subtotal REAL,
        iva REAL,
        total REAL,
        inversion REAL,
        utilidad REAL
    )
    """)

    # =========================================
    # CREAR ADMIN
    # =========================================

    usuario_admin = cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario='admin'
    """).fetchone()

    if not usuario_admin:

        cursor.execute("""
            INSERT INTO usuarios(
                usuario,
                password,
                rol
            )
            VALUES(?,?,?)
        """, (
            "admin",
            "Dios2026",
            "Administrador"
        ))

    # =========================================
    # AGREGAR DICTAMEN SI NO EXISTE
    # =========================================

    try:

        cursor.execute("""
            ALTER TABLE candidatos
            ADD COLUMN dictamen TEXT
        """)

    except:
        pass

    conn.commit()