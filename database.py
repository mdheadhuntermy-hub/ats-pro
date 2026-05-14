import sqlite3

conn = sqlite3.connect(
    "ats.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa TEXT,
    contacto TEXT,
    telefono TEXT,
    correo TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS vacantes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    empresa TEXT,
    ubicacion TEXT,
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
    notas TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS entrevistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidato TEXT,
    fecha TEXT,
    hora TEXT,
    entrevistador TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS facturas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    vacante TEXT,
    monto TEXT,
    estado TEXT
)
''')

conn.commit()