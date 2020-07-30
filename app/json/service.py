from app.json.model import db, save_json, get_json_index, get_json_max_id

class ClientServiceJson:
    #find all
    def find_all(self):
        return db

    # find client by id
    def find_by_id(self,id):
        #find the pos with id in json array
        index = get_json_index(id)
        if index == -1:
            return None
        client = db[index]
        return client;

    # create/update client
    def save(self, client, isCreation):
        if isCreation:
            client['id'] = get_json_max_id() + 1
            db.append(client)
        else:
            #find the pos with id in json array
            index = get_json_index(client['id']) 

            # update the json
            db[index]['nom'] = client['nom']
            db[index]['prenom'] = client['prenom']
        save_json()

    # delete client
    def delete(self, id):
        #find the pos with id in json array
        index = get_json_index(id)
        if index >= 0:
            del db[index]
            save_json()
            return True
        else:
            return False
