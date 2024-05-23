from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para conectar ao banco de dados
def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='amigosemacao'
        )
        print("Conexão ao banco de dados MySQL bem-sucedida")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Rota para renderizar a página principal com a lista de gestores
@app.route('/')
def index():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM gestores")
        gestores = cursor.fetchall()
        cursor.close()
        conexao.close()
        return render_template('index.html', gestores=gestores)
    except Error as e:
        print(f"Erro ao obter gestores: {e}")
        return jsonify({'error': 'Erro ao obter gestores'}), 500

# Rota para criar um novo gestor
@app.route('/gestor-post', methods=['POST'])
def criar_gestor():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    nome = request.form.get('nomeGestor')
    email = request.form.get('emailGestor')
    pin = request.form.get('pinGestor')

    if not (nome and email and pin):
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

    try:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO gestores (nomeGestor, emailGestor, pinGestor) VALUES (%s, %s, %s)", (nome, email, pin))
        conexao.commit()
        cursor.close()
        conexao.close()

        return jsonify({'message': 'Gestor criado com sucesso!'}), 201
    except Error as e:
        print(f"Erro ao criar gestor: {e}")
        return jsonify({'error': 'Erro ao criar gestor'}), 500

# Rota para obter todos os gestores
@app.route('/gestor-get', methods=['GET'])
def obter_gestores():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM gestores")
        gestores = cursor.fetchall()
        cursor.close()
        conexao.close()
        return jsonify(gestores), 200
    except Error as e:
        print(f"Erro ao obter gestores: {e}")
        return jsonify({'error': 'Erro ao obter gestores'}), 500

# Rota para atualizar um gestor existente
@app.route('/gestor-update/<int:id>', methods=['PUT'])
def atualizar_gestor(id):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    nome = request.form.get('nomeGestor')
    email = request.form.get('emailGestor')
    pin = request.form.get('pinGestor')

    if not (nome and email and pin):
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

    try:
        cursor = conexao.cursor()
        cursor.execute("UPDATE gestores SET nomeGestor = %s, emailGestor = %s, pinGestor = %s WHERE idGestor = %s", (nome, email, pin, id))
        conexao.commit()
        cursor.close()
        conexao.close()

        return jsonify({'message': 'Gestor atualizado com sucesso!'}), 200
    except Error as e:
        print(f"Erro ao atualizar gestor: {e}")
        return jsonify({'error': 'Erro ao atualizar gestor'}), 500

# Rota para deletar um gestor existente
@app.route('/gestor-delete/<int:id>', methods=['DELETE'])
def deletar_gestor(id):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM gestores WHERE idGestor = %s", (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

        return jsonify({'message': 'Gestor excluído com sucesso!'}), 200
    except Error as e:
        print(f"Erro ao excluir gestor: {e}")
        return jsonify({'error': 'Erro ao excluir gestor'}), 500

if __name__ == '__main__':
    app.run(debug=True)
