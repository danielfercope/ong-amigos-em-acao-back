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
            password='admin123',
            database='banco'
        )
        print("Conexão ao banco de dados MySQL bem-sucedida")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Rota para criar um novo evento
@app.route('/evento-post', methods=['POST'])
def criar_evento():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    nome_evento = request.form.get('nome_evento')
    data_evento = request.form.get('data_evento')
    imagem_evento = request.files['imagem_evento']

    # Verifica se todos os campos necessários foram enviados
    if not (nome_evento and data_evento and imagem_evento):
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

    try:
        cursor = conexao.cursor()
        imagem_bytes = imagem_evento.read()
        imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')

        cursor.execute("INSERT INTO evento (nome_evento, data_evento, imagem_evento) VALUES (%s, %s, %s)", (nome_evento, data_evento, imagem_base64))
        conexao.commit()
        cursor.close()
        conexao.close()

        return jsonify({'message': 'Evento criado com sucesso!'}), 201
    except Error as e:
        print(f"Erro ao criar evento: {e}")
        return jsonify({'error': 'Erro ao criar evento'}), 500

@app.route('/evento-get', methods=['GET'])
def obter_eventos():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM evento")
        eventos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return jsonify(eventos), 200
    except Error as e:
        print(f"Erro ao obter eventos: {e}")
        return jsonify({'error': 'Erro ao obter eventos'}), 500

# Rota para atualizar um evento existente
@app.route('/evento-update/<int:id>', methods=['PUT'])
def atualizar_evento(id):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    nome_evento = request.form.get('nome_evento')
    data_evento = request.form.get('data_evento')

    if not (nome_evento and data_evento):
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

    try:
        cursor = conexao.cursor()
        cursor.execute("UPDATE evento SET nome_evento = %s, data_evento = %s WHERE idEvento = %s", (nome_evento, data_evento, id))
        conexao.commit()
        cursor.close()
        conexao.close()

        return jsonify({'message': 'Evento atualizado com sucesso!'}), 200
    except Error as e:
        print(f"Erro ao atualizar evento: {e}")
        return jsonify({'error': 'Erro ao atualizar evento'}), 500

@app.route('/evento-delete/<int:id>', methods=['DELETE'])
def deletar_evento(id):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor()

        # Exclui o evento do banco de dados
        cursor.execute("DELETE FROM evento WHERE idEvento = %s", (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

        return jsonify({'message': 'Evento excluído com sucesso!'}), 200
    except Error as e:
        print(f"Erro ao excluir evento: {e}")
        return jsonify({'error': 'Erro ao excluir evento'}), 500

if __name__ == '__main__':
    app.run(debug=True)
