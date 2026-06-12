import sqlite3
import streamlit as st
import os


if os.path.exists("/data"):
    DB_NAME = "/data/atspro.db"
else:
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


def agregar_columna(cursor, tabla, columna, tipo):

    try:
        cursor.execute(
            f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}"
        )
    except:
        pass


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        password TEXT,
        rol TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa TEXT,
        contacto TEXT,
        correo TEXT,
        telefono TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacantes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        salario TEXT,
        descripcion TEXT,
        creado_por TEXT
    )
    """)

    agregar_columna(cursor, "vacantes", "creado_por", "TEXT")

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
        dictamen TEXT,
        seguridad_pdf TEXT,
        dictamen_seguridad TEXT,
        psicometrico_pdf TEXT,
        dictamen_psicometrico TEXT,
        creado_por TEXT
    )
    """)

    agregar_columna(cursor, "candidatos", "dictamen", "TEXT")
    agregar_columna(cursor, "candidatos", "seguridad_pdf", "TEXT")
    agregar_columna(cursor, "candidatos", "dictamen_seguridad", "TEXT")
    agregar_columna(cursor, "candidatos", "psicometrico_pdf", "TEXT")
    agregar_columna(cursor, "candidatos", "dictamen_psicometrico", "TEXT")
    agregar_columna(cursor, "candidatos", "creado_por", "TEXT")

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS retiros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        concepto TEXT,
        monto REAL,
        mes TEXT,
        observaciones TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_candidatos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidato_id INTEGER,
        candidato TEXT,
        accion TEXT,
        detalle TEXT,
        usuario TEXT,
        fecha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banco_cv(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT,
        telefono TEXT,
        ciudad TEXT,
        perfil TEXT,
        area TEXT,
        skills TEXT,
        salario TEXT,
        disponibilidad TEXT,
        comentarios TEXT,
        pdf TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS propuestas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        cliente TEXT,
        contacto TEXT,
        empresa TEXT,
        servicio TEXT,
        perfil TEXT,
        honorarios TEXT,
        anticipo TEXT,
        garantia TEXT,
        vigencia TEXT,
        condiciones TEXT,
        estado TEXT,
        pdf TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS acuerdos_anticipo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        empresa TEXT,
        contacto TEXT,
        puesto TEXT,
        vacantes INTEGER,
        salario REAL,
        porcentaje REAL,
        honorarios REAL,
        anticipo REAL,
        iva REAL,
        total REAL,
        pdf TEXT
    )
    """)

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

    conn.commit()