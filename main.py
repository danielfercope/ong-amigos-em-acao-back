from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error

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

@app.route('/usuarioTradicional', methods=['POST'])
def criar_usuarioTradicional():

    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json()
    userName = data.get('userName')
    userPhone = data.get('userPhone')
    userNeeds = data.get('userNeeds')
    userFamilyDescription = data.get('userFamilyDescription')


    if not (userName and userPhone and userNeeds and userFamilyDescription):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO tradicionalUser (userName, userPhone, userNeeds, userFamilyDescription) VALUES (%s, %s, %s, %s)",
            (userName, userPhone, userNeeds, userFamilyDescription)
        )
        conexao.commit()
        cursor.close()
        conexao.close()
        return jsonify({'message': 'Usuario criado com sucesso!'}), 201
    except Error as e:
        print(f"Erro ao criar usuario: {e}")
        return jsonify({'error': 'Erro ao criar usuario'}), 500

@app.route('/usuarioTradicional', methods=['GET'])
def visualizar_usuarioTradicional():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tradicionalUser")
        tradicionalUser = cursor.fetchall()
        cursor.close()
        conexao.close()
        return jsonify(tradicionalUser), 200
    except Error as e:
        print(f"Erro ao obter usuarios: {e}")
        return jsonify({'error': 'Erro ao obter usuarios'}), 500


@app.route('/usuarioTradicional/<int:userId>', methods=['DELETE'])
def deletar_usuarioTradicional(userId):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tradicionalUser WHERE userId = %s", (userId,))
        conexao.commit()
        cursor.close()
        conexao.close()
        return jsonify("usuario deletado com sucesso"), 200
    except Error as e:
        print(f"Erro ao obter usuarios: {e}")
        return jsonify({'error': 'Erro ao obter usuarios'}), 500

@app.route('/usuarioTradicional/<int:userId>', methods=['PUT'])
def editar_usuarioTradicional(userId):
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json()
    userName = data.get('userName')
    userPhone = data.get('userPhone')
    userNeeds = data.get('userNeeds')
    userFamilyDescription = data.get('userFamilyDescription')

    query = "UPDATE tradicionalUser SET"
    if userName:
        query += ' userName = "' + userName + '",'
    if userPhone:
        query += ' userPhone = "' + userPhone + '",'
    if userNeeds:
        query += ' userNeeds = "' + userNeeds + '",'
    if userFamilyDescription:
        query += ' userFamilyDescription = "' + userFamilyDescription + '",'

    # Remove the last comma
    if query.endswith(','):
        query = query[:-1]

    query += " WHERE userId = "
    query += str(userId)
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
