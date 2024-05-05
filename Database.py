import sqlite3
from sqlite3 import Error

from crudGestor import Gestor


# Criar conexão com o banco de dados
def create_connection():
    try:
        conn = sqlite3.connect('instance/teste_novo.db')
    except Error as e:
        print(e)

    return conn

# Criar todas as tabelas

def create_all_tables():
    conn = create_connection()

    sql_gestor = ("CREATE TABLE IF NOT EXISTS gestor ("
                     "student_id INTEGER NOT NULL, "
                     "nome VARCHAR(200), "
                     "email VARCHAR(100), "
                     "pin VARCHAR(20), "
                     "PRIMARY KEY (student_id)"
                     ")")

    create_table(conn, sql_gestor)

def create_table(conn, sql_query):
    try:
        c = conn.cursor()
        c.execute(sql_query)
        conn.commit()
    except Error as e:
        print(e)

# Inserir registro no banco de dados
def inserir_gestor(gestor):
    conn = create_connection()
    with conn:
        sql_query = "INSERT INTO gestor(nome, email, pin) VALUES (?, ?, ?, ?)"
        c = conn.cursor()
        task = (gestor.nome, gestor.email, gestor.pin)
        c.execute(sql_query, task)
        conn.commit()

        return c.lastrowid

# Deletar registro no banco de dados
def deletar_gestor(gestor):
    conn = create_connection()
    with conn:
        sql_query = "DELETE FROM gestor WHERE student_id=?"
        c = conn.cursor()
        task = (gestor.id,)
        c.execute(sql_query, task)
        conn.commit()

        return c.lastrowid

# Atualizar registro no banco de dados
def atualizar_gestor(gestor):
    conn = create_connection()
    with conn:
        sql_query = "UPDATE gestor SET nome=?, email=?, pin=? WHERE student_id=?"
        c = conn.cursor()
        task = (gestor.nome, gestor.email, gestor.pin, gestor.id)
        c.execute(sql_query, task)
        conn.commit()

        return c.lastrowid

# Select all gestor
def select_all_gestor():
    lista_gestor = []

    conn = create_connection()
    with conn:
        sql_query = "SELECT * FROM gestor"
        c = conn.cursor()
        c.execute(sql_query)

        rows = c.fetchall()

        for row in rows:
            gestor = Gestor(row[1], row[2], row[3])
            gestor.id = row[0]
            lista_gestor.append(gestor)

    return lista_gestor