Using Flask, SQLAlchemy (mapping) and Sqlite (embedded database) Python packages

List environemments:
conda env list

#Create a conda Environment for the project(ex: SampleFlask, version python >= 3). First with command promt ge to d:\python\examples\
conda create -n SampleFlask python=3
conda activate SampleFlask
conda deactivate

Install the latest Flask release(from the new environment and from the new folder):
(SampleFlask) d:\python\examples\SampleFlask>python -m pip install flask
conda list

From SampleFlask directory run these commands:
#location of module containing our application
set FLASK_APP=app.clients_app.py
#enable development features like debuging
set FLASK_ENV=development
flask run
flask run --host=127.0.0.0 --port=3000


Flask Routes:
http://localhost:5000/client
http://localhost:5000/client/new
http://localhost:5000/client/1  - consult
http://localhost:5000/client/1/edit
http://localhost:5000/client/1/delete

http://localhost:5000/welcome - test page

REST Api:
http://localhost:5000/clients                    HTTP GET         - get all clients
http://localhost:5000/clients/new                HTTP GET/POST    - create client
http://localhost:5000/clients/1                  HTTP GET         - consult client
http://localhost:5000/clients/1/edit             HTTP GET/POST    - edit client
http://localhost:5000/clients/1/delete           HTTP GET/DELETE  - delete client


With JSON file: 
Set STORAGE_MODE = 'json' in config.py

With Flask-SQLAlchemy(sqlite database):
Set STORAGE_MODE = 'sqlite' in config.py 

Then from SampleFlask directory run these commands:
flask db init    -create our migrations
flask db migrate - generate the tables from Models (Client, Adresse, Commande)
flask db upgrade - if this application uses SQLite, the upgrade command will detect that a database does not exist and will create it

To initialise the SQLite database, I add a new command 'init-db' that can be called with the flask command. Ex: flask init-db

Command Line Shell For SQLite
SampleFlask>sqlite3
sqlite>.open db/clients.db
sqlite>.tables
sqlite>select * from client;
sqlite>.exit

Git: A new repo from an existing project
git init
git add app/db/* app/json/*  app/templates/*
git add app/static/* -f
git add app/config.py app/clients_app.py readme.txt
git commit -m "first commit"
Connect it to github ad create a new repository: SampleFlask
git remote add origin https://github.com/danielvornicu/SampleFlask.git
git push -u origin master