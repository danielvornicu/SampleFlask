"""
model.py
--------
Implements the model for our website by simulating a database.

Note: although this is nice as a simple example, don't do this in a real-world
production setting. Having a global object for application data is asking for
trouble. Instead, use a real database layer, like
https://flask-sqlalchemy.palletsprojects.com/.
"""

import json


def load_json():
    with open("app/json/clients.json", encoding='utf-8') as f:
        return json.load(f)

def save_json():
    with open("app/json/clients.json", 'w') as f:
        return json.dump(db, f)

# find the pos with id in json array
def get_json_index(id):
    index = -1
    for i, item in enumerate(db):
        if item['id'] == id:
            index = i
            break
    return index

# find the max id in json array
def get_json_max_id():
    if len(db)>0:
        client = max(db, key=lambda db: db['id'])
        return client['id']

db = load_json()
