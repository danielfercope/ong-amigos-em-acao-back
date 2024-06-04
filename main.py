import base64

from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'


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

#CRUD DOS GESTORES
@app.route('/listar-gestores')
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

@app.route('/cadastrar-gestores', methods=['POST'])
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


@app.route('/buscar-gestores', methods=['GET'])
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


@app.route('/atualizar-gestor/<int:id>', methods=['PUT'])
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


@app.route('/deletar-gestor/<int:id>', methods=['DELETE'])
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


#CRUD DOS USUÁRIOS CARENTES
@app.route('/cadastrar-usuario-carente', methods=['POST'])
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

@app.route('/lista-usuario-carente', methods=['GET'])
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

@app.route('/deletar-usuario-carente/<int:userId>', methods=['DELETE'])
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

@app.route('/atualizar-usuario-carente/<int:userId>', methods=['PUT'])
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

#CRUD DOS FEEDBACKS
@app.route('/cadastrar-feedBack', methods=['POST'])
def submit():
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json()
    nome = data.get('nome')
    telefone = data.get('telefone')
    email = data.get('email')

    try:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO feedback (nomeFeedBack, telefoneFeedBack, emailFeedBack) VALUES (%s, %s, %s)",
                       (nome, telefone, email))
        conexao.commit()
        cursor.close()
        conexao.close()

        return jsonify({'message': 'feedBack enviado com sucesso!'}), 201
    except Error as e:
        print(f"Erro ao criar gestor: {e}")
        return jsonify({'error': 'Erro ao cadastrar gestor'}), 500

#CRUD DE EVENTOS
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
        cursor.execute("UPDATE evento SET nome_evento = " + nome_evento + ", data_evento = %s WHERE idEvento = %s", (nome_evento, data_evento, id))
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
