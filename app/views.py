"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash,  jsonify

from app.forms import ClienteForm
from app.models import Cliente
import json
# import sqlite3

###
# Routing for your application.
###


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    json_body = busca_cpf(req)
    
    
    return jsonify(json_body)

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/clientes')
def show_clientes():
    clientes = db.session.query(Cliente).all() # or you could have used Cliente.query.all()

    return render_template('show_clientes.html', clientes=clientes)

@app.route('/add-cliente', methods=['POST', 'GET'])
def add_cliente():
    cliente_form = ClienteForm()

    if request.method == 'POST':
        if cliente_form.validate_on_submit():
            # Get validated data from form
            nome = cliente_form.nome.data # You could also have used request.form['name']
            email = cliente_form.email.data # You could also have used request.form['email']
            cpf = cliente_form.cpf.data
            tipo = cliente_form.tipo.data
            time_coracao = cliente_form.time_coracao.data

            # save cliente to database
            cliente = Cliente(nome, email, cpf, tipo, time_coracao)
            db.session.add(cliente)
            db.session.commit()

            flash('Cliente successfully added')
            return redirect(url_for('show_clientes'))

    flash_errors(cliente_form)
    return render_template('add_cliente.html', form=cliente_form)

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


def busca_cpf(req):
    fulfillmentMessages = []
    cpf = req["queryResult"]['parameters']['cpf']
    clientes = db.session.query(Cliente).filter_by(cpf=cpf)
    
    exists = db.session.query(clientes.exists()).scalar()
    
    if exists:
        for c in clientes:
            fulfillmentMessages.append({"text": {"text": ["Olá " + c.nome + " tudo bem? Encontramos seu cadastro "]}})
            fulfillmentMessages.append({"text": {"text": ["email: " + c.email]}})
            fulfillmentMessages.append({"text": {"text": ["Nivel Socio: " + c.tipo]}})
            fulfillmentMessages.append({"text": {"text": ["Time do Coração: " + c.time_coracao]}})   
    else:
       fulfillmentMessages.append({"text": {"text": ["Desculpe-nos, não encontramos o cadastro para o CPF informado."]}})
    
    return { "fulfillmentMessages": fulfillmentMessages }
    
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
