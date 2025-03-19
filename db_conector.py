from mysql.connector import Error
import mysql.connector
import os

def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST'),      
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("Conexão ao banco de dados MySQL bem-sucedida")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
