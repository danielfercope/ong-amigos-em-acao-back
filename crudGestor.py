from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets

from sqlalchemy.orm import relationship

import Database

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste_novo.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/teste2'

secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key
app.app_context().push()
db = SQLAlchemy(app)

class Gestor(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    email = db.Column(db.String(100))
    pin = db.Column(db.String(20))

    def __init__(self, nome_aux, email_aux, pin_aux):
        self.nome = nome_aux
        self.email = email_aux
        self.pin = pin_aux

@app.route('/')
def show_all():
    return render_template('show_all.html', gestores=Gestor.query.all())
    #return render_template('show_all.html', gestores=Database.select_all_gestor())

# Rota para CRIAR gestor
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['nome'] or not request.form['email'] or not request.form['pin']:
            flash("Preencha todos os campos", "Error")
        else:
            gestor = Gestor(request.form['nome'], request.form['email'], request.form['pin'])
            db.session.add(gestor)
            db.session.commit()

            #Database.inserir_gestor(gestor)

            flash("Gestor foi criado com sucesso!")
            return redirect(url_for('show_all'))
    return render_template("new.HTML")

# Rota para EDITAR gestor
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    gestor = Gestor.query.get(id)

    if request.method == 'POST':
        if not request.form['nome'] or not request.form['email'] or not request.form['pin']:
            flash("Preencha todos os campos", "Error")
        else:
            gestor.nome = request.form['nome']
            gestor.email =request.form['email']
            gestor.pin =request.form['pin']

            db.session.commit() # comando commit da execução, para salvar as informações no banco de dados
            #Database.atualizar_gestor(gestor)

            flash("Gestor " + gestor.nome + " editado com sucesso!")  # printar mensagem informativa
            return redirect(url_for('show_all'))

    return render_template('update.html', gestor=gestor)

# Rota para DELETAR um gestor
@app.route('/delete/<int:id>')
def delete(id):
    gestor = Gestor.query.get(id)
    db.session.delete(gestor)
    db.session.commit()
    #Database.deletar_gestor(gestor)

    flash("Gestor " + gestor.nome + " deletado com sucesso!")
    return redirect(url_for('show_all'))

if __name__ == '__main__':
    #db.create_all()
    Database.create_all_tables()
    app.run(port=5000, debug=True)