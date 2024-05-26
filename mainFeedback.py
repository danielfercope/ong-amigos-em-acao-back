from flask import Flask, render_template, request, redirect, url_for
import random
import os
import mysql.connector

app = Flask(__name__)

# Conexão com o banco de dados MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="banco_dados_pac"
)

@app.route('/')
def form():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    anonimo = 'anonimo' in request.form
    descricao = request.form['descricao']

    # Verificar se a descrição está vazia
    if not descricao:
        return render_template('feedback.html', error_message="Por favor, descreva sua ideia!")

    mycursor = mydb.cursor()

    if anonimo:
        sql = "INSERT INTO feedback (descricaoIdeia) VALUES (%s)"
        val = (descricao,)
    else:
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        sql = "INSERT INTO feedback (nomeUsuario, telefoneUsuario, emailUsuario, descricaoIdeia) VALUES (%s, %s, %s, %s)"
        val = (nome, telefone, email, descricao)

    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
