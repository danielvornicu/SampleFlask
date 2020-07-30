from app.db.models import db, Client, Adresse, Commande
from datetime import date

#to initialize the database with 5 clients
import click
from flask.cli import with_appcontext

@click.command('init-db')
@with_appcontext
def init_db():
    adresses = [
               Adresse('16 rue des lilas d''Espagne', 'Appartement 12', 92400, 'Courbevoie'),
               Adresse('127 Avenue Jean Jaures', 'Appt 101', 92140, 'CLAMART'),
               Adresse('36B Rue Monttessuy', 'Etage 6', 91260, 'JUVISY')

    ]
    clients = [
              Client('DANIEL', 'VORNICU', 2), 
              Client('ALINA', 'VORNICU', 2),
              Client('LUCA', 'VORNICU', 2),
              Client('SOFIA', 'VORNICU', 2),
              Client('ERIC', 'SIBER', 1)
    ]
    commandes = [
                 Commande(2, 150, date.today(), 1),
                 Commande(1, 100, date.today(), 2)
    ]

    #remove all rows
    db.session.query(Commande).delete()
    db.session.query(Client).delete()
    db.session.query(Adresse).delete()

    #add data   
    db.session.add_all(adresses)
    db.session.add_all(clients)
    db.session.add_all(commandes)
    db.session.commit()
    click.echo('Initialized the database.')

class ClientServiceSQLite:
    def __init__(self):
        """
        Constructor 
        """
        print('Constructor SQLite client service')

    #find all
    def find_all(self):
        clients = Client.query.all();
        clients_json = [c.to_json() for c in clients]
        return clients_json;

    # find client by id
    def find_by_id(self,id):
        client = Client.query.filter_by(id=id).first_or_404()
        return client.as_dict();

    # create/update client
    def save(self, client, isCreation):
        if isCreation:
            client = Client(prenom=client['prenom'], nom=client['nom'])
            db.session.add(client)
            db.session.commit()
        else:
            clientBase = Client.query.filter_by(id=client['id']).first_or_404()
            if clientBase:
                clientBase.prenom = client['prenom']
                clientBase.nom = client['nom']
                db.session.add(clientBase)
                db.session.commit()

    # delete client
    def delete(self, id):
        client = Client.query.filter_by(id=id).first_or_404()
        if client:
            db.session.delete(client)
            db.session.commit()
            return True
        else:
            return False