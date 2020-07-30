from datetime import datetime
import json
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for, session, flash
from flask_migrate import Migrate

#Config class from config.py
from app.config import Config  

#services (JSON service and SQLite service)
from app.json.service import ClientServiceJson
from app.db.service import ClientServiceSQLite, init_db   

from app.db.models import db

# create and configure the app      
app = Flask(__name__)
app.config.from_object(Config())
#add new flask command(use flask init-db for initialize)
app.cli.add_command(init_db)

# loas the messages for templates
with open("app/static/messages.json", encoding='utf-8') as f:
    messages = json.load(f)

print(app.config['STORAGE_MODE'])
if app.config['STORAGE_MODE'] == 'json':
    client_service = ClientServiceJson()
elif app.config['STORAGE_MODE'] == 'sqlite':
    db.init_app(app)
    migrate = Migrate(app, db)
    client_service = ClientServiceSQLite()
else:
    client_service = ClientServiceJson()

#decorator
@app.route("/client")
def index():
    #return "Welcome to my Flash Card Application"
    return render_template(
        "client_liste.html",
        clients=client_service.find_all(),
        msg=messages,
        storage_mode=app.config['STORAGE_MODE']
    )

@app.route('/client/<int:id>')
def show(id):
    try:
        client = client_service.find_by_id(id)
        if client == None:
           abort(404)
        return render_template("client_consult.html",
                               client=client,
                               msg=messages)
    except IndexError:
        abort(404)   

@app.route('/client/new', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nom    = request.form['nom']
        prenom = request.form['prenom']
        error  = None

        if not nom:
            error = 'Nom requis.'
        if not prenom:
            error = 'Prenom requis.'

        if not error:
            #new client
            client = {"id": -1,
                      "nom": nom,
                      "prenom": prenom}

            client_service.save(client, True)

            flash(f"{messages['liste']['actions']['creerSucces']}  {nom} {prenom} ", 'success')
            return redirect(url_for('index'))
        flash(error, 'error')
    else:
        #GET
        return render_template('client_fiche.html', 
                               client={"id":-1,"nom":"","prenom":""},
                               msg=messages)        
 
@app.route('/client/<int:id>/edit', methods=["GET", "POST"])
def edit(id):
    try:
        if request.method == "POST":
            # form has been submitted, process data
            nom    = request.form['nom']
            prenom = request.form['prenom']
            error  = None

            #form_dict = request.form.to_dict()
            #flash(form_dict)

            if not nom:
                error = 'Nom requis.'
            if not prenom:
                error = 'Prenom requis.'
        
            if not error:    
                #modified client    
                client = {"id": id,
                          "nom": nom,
                          "prenom": prenom}

                client_service.save(client, False)
                flash(f"{messages['liste']['actions']['modifierSucces']}  {nom} {prenom} ", 'success')
                return redirect(url_for('index'))

            flash(error, 'error')
        else:
            #GET
            client = client_service.find_by_id(id)
            if client == None:
                abort(404)
            return render_template("client_fiche.html",
                                   client=client,
                                   msg=messages
                                   )
    except IndexError:
        abort(404)

@app.route('/client/<int:id>/delete', methods=["GET", "DELETE"])
def delete(id):
    try:
        if client_service.delete(id):
          flash(f"{messages['liste']['actions']['supprimerSucces']}", 'warning')
        return redirect(url_for('index'))
    except IndexError:
        abort(404)                               

@app.route("/date")
def date():
    sNow = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return "This page was serve at "+sNow

@app.route("/welcome")
def welcome():
    #return "Welcome to my Flash Card Application"
    return render_template("test.html")

# REST APi
@app.route("/clients")
def api_index():
    clients=client_service.find_all()
    return jsonify(clients)


@app.route("/clients/<int:id>")
def api_show(id):
    try:
        client = client_service.find_by_id(id)
        if client == None:
           return {"error": "Pas trouvé"}
        return client
    except IndexError:
        abort(404)

@app.route('/clients/new', methods=["GET", "POST"])
def api_create():
    if request.method == "POST":
         # process json data from request
        data = request.get_json()
        nom    = None
        prenom = None
        error  = None

        if 'nom' in data:
            nom    = request.json['nom']     # ou data['nom]
        else:
            error = 'Nom requis.'

        if 'prenom' in data:
            prenom = request.json['prenom']
        else:
            error = 'Prenom requis.'

        if not error:
            #new client
            client = {"id": -1,
                      "nom": nom,
                      "prenom": prenom}

            client_service.save(client, True)
            print(f"{messages['liste']['actions']['creerSucces']}  {nom} {prenom} ", 'success')
            return api_index()
        
        print(error)
        return {"error": error}
    else:
        #GET
        return {"id":-1,"nom":"","prenom":""}


@app.route('/clients/<int:id>/edit', methods=["GET", "POST"])
def api_edit(id):
    try:
        if request.method == "POST":
            # process json data from request
            data = request.get_json()
            id = None
            nom = None
            prenom = None
            error  = None

            if 'id' in data:
                id    = request.json['id']     
            else:
                error = 'Id requis in JSON request.'

            if 'nom' in data:
                nom    = request.json['nom']     # ou data['nom]
            else:
                error = 'Nom requis in JSON request.'

            if 'prenom' in data:
                prenom = request.json['prenom']
            else:
                error = 'Prenom requis in JSON request.'
        
            if not error:    
                #modified client    
                client = {"id": id,
                          "nom": nom,
                          "prenom": prenom}

                client_service.save(client, False)
                print(f"{messages['liste']['actions']['modifierSucces']}  {nom} {prenom} ", 'success')
                return api_index()

            print(error)
            return {"error": error}
        else:
            #GET
            client = client_service.find_by_id(id)
            if client == None:
                return {"error": "Not found"}
            return client
    except IndexError:
        abort(404)

@app.route('/clients/<int:id>/delete', methods=["GET", "DELETE"])
def api_delete(id):
    try:
        if client_service.delete(id):
          print(f"{messages['liste']['actions']['supprimerSucces']}", 'warning')
        return api_index()
    except IndexError:
        abort(404)   
