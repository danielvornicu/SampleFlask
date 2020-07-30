from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Adresse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Ligne1 = db.Column(db.String(255))
    ligne2 = db.Column(db.String(255))
    code_postal = db.Column(db.Integer)
    ville = db.Column(db.String(255))

    def __init__(self, Ligne1, Ligne2, code_postal, ville):
        self.Ligne1 = Ligne1
        self.ligne2 = Ligne2
        self.code_postal = code_postal
        self.ville = ville

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(255))
    nom = db.Column(db.String(255))
    adresse_id = db.Column(db.Integer, db.ForeignKey('adresse.id'), nullable=True)
    commandes = db.relationship('Commande', backref='author', lazy=True)

    def __init__(self, prenom, nom, adresse_id =None):
        self.prenom = prenom
        self.nom = nom
        self.adresse_id = adresse_id    
        
    #output the object as a dictionary
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    #same thing: output the object as a dictionary(json)
    def to_json(self):
        return {
            "id": int(self.id),
            "prenom": self.prenom,
            "nom": self.nom
           # "adresse_id" : int(self.adresse_id)
        }

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_produits = db.Column(db.Integer)
    montant = db.Column(db.Integer)
    date_commande = db.Column(db.Date, server_default=db.func.now())
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    def __init__(self, nombre_produits, montant, date_commande, client_id):
        self.nombre_produits = nombre_produits
        self.montant = montant
        self.date_commande = date_commande
        self.client_id = client_id