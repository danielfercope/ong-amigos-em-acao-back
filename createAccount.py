from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error
import bcrypt

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
            database='usuarioTradicional'
        )
        print("Conexão ao banco de dados MySQL bem-sucedida")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route('/createAccount', methods=['POST'])
def criar_conta():

    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json()
    createName = data.get('createName')
    createEmail = data.get('createEmail')
    createPassword = data.get('createPassword')
    hash = bcrypt.hashpw(createPassword.encode('utf-8'), bcrypt.gensalt(13))

    #Lembrar de salvar o numero do salt armazenado em um local seguro (variavel de ambiente)

    if not (createName and createEmail and createPassword):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO createAccount (createName, createEmail, createPassword) VALUES (%s, %s, %s)",
            (createName, createEmail, hash)
        )

        conexao.commit()
        cursor.close()
        conexao.close()
        return jsonify({'message': 'Usuario criado com sucesso!'}), 201
    except Error as e:
        print(f"Erro ao criar usuario: {e}")
        return jsonify({'error': 'Erro ao criar usuario'}), 500

@app.route('/viewAccount', methods=['GET'])
def visualizar_usuarios():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM createAccount") #Tirar o view Hash
        createAccount = cursor.fetchall()
        cursor.close()
        conexao.close()
        return jsonify(createAccount), 200
    except Error as e:
        print(f"Erro ao obter usuarios: {e}")
        return jsonify({'error': 'Erro ao obter usuarios'}), 500


@app.route('/deleteAccount/<int:createId>', methods=['DELETE'])
def deletar_usuario(createId):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM createAccount WHERE createId = %s", (createId,))
        conexao.commit()
        cursor.close()
        conexao.close()
        return jsonify("usuario deletado com sucesso"), 200
    except Error as e:
        print(f"Erro ao obter usuarios: {e}")
        return jsonify({'error': 'Erro ao obter usuarios'}), 500

@app.route('/editAccount/<int:createId>', methods=['PUT'])
def editar_usuario(createId):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json()
    createName = data.get('createName')
    createEmail = data.get('createEmail')
    createPassword = data.get('createPassword')

    query = "UPDATE createAccount SET"
    if createName:
        query += ' createName = "' + createName + '",'
    if createEmail:
        query += ' createEmail = "' + createEmail + '",'
    if createPassword:
        query += ' createPassword = "' + createPassword + '",'

    # Remove the last comma
    if query.endswith(','):
        query = query[:-1]

    query += " WHERE createId = "
    query += str(createId)
    print(query)

    try:
        cursor = conexao.cursor()
        cursor.execute(query)
        conexao.commit()
        cursor.close()
        conexao.close()
        return jsonify("usuario editado com sucesso"), 200
    except Error as e:
        print(f"Erro ao obter usuarios: {e}")
        return jsonify({'error': 'Erro ao obter usuarios'}), 500


if __name__ == "__main__":
    app.run(debug=True)

