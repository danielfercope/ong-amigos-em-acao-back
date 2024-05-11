from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error
import os
import base64

app = Flask(__name__)
CORS(app)


app.config['UPLOAD_FOLDER'] = 'uploads'


# Função para conectar ao banco de dados
def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='banco'
        )
        print("Conexão ao banco de dados MySQL bem-sucedida")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

    @app.route('/usuarioTradicional-post', methods=['POST'])
def criar_usuarioTradicional():
        conexao = conectar_bd()
        if not conexao:
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

        nomeUsuario = request.form.get('nomeUsuario')
        telefoneUsuario = request.form.get('telefoneUsuario')
        necessidadeUsuario = request.files['necessidadeUsuario']
        descricaoFamiliarUsuario = request.files['descricaoFamiliarUsuario']

        if not (nomeUsuario and telefoneUsuario and necessidadeUsuario and descricaoFamiliarUsuario):
            return jsonify ({'erro': 'Erro ao conectar ao banco de dados'}), 400

        try:
            cursor = conectar_bd()
            cursor.execute("INSERT INTO evento (nomeUsuario, telefoneUsuario, necessidadeUsuario, descricaoFamiliarUsuario) VALUES (%s, %s, %s, %s)", (nomeUsuario, telefoneUsuario, necessidadeUsuario, descricaoFamiliarUsuario)
            conexao.commit()
            cursor.close()
            conexao.close()
            return jsonify({'message': 'Evento criado com sucesso!'}), 201
        except Error as e:
            print(f"Erro ao criar evento: {e}")
            return jsonify({'error': 'Erro ao criar evento'}), 500



