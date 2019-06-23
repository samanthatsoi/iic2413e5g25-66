# -*- coding: utf-8 -*-
# main.py
from flask import Flask, jsonify, request
from pymongo import MongoClient
import simplejson as json

USER_KEYS = ['message', 'lat', 'long', 'date']
### Pymongo

client = MongoClient()
db = client["proyecto"]
messages = db.messages
users = db.users
resultados = db.messages.find({}, {"id": 1})[0]
"""
print(resultados)
"""
## Flask

app = Flask(__name__)

@app.route("/") # Tipo GET
def hello():
    return "Hello World!"

@app.route("/messages")
def get_messages():
    resultados = [u for u in messages.find({}, {"_id": 0})]
    return jsonify(resultados)

@app.route("/messages/byid/<int:id>")
def get_message(id):
    message = list(messages.find({"id": id}, {"_id": 0}))
    return jsonify(message)

@app.route("/users/byid/<int:id>")
def get_user(id):
    user = list(users.find({"uid": id}, {"_id": 0}))
    messages1 = list(messages.find({"sender": id}, {"_id": 0}))
    return jsonify(user + messages1)

#Se debe ingresar el texto de forma frase1_frase2...
@app.route("/messages/bytext/inorin/<text>")
def get_message_exacttext(text):
    text = text.split("_")
    palabras = ""
    for palabra in text:
        palabras += "\"{}\"".format(palabra)
    message = list(messages.find({"$text": {"$search": palabras}},{"_id": 0}))
    return jsonify(message)


#Se debe ingresar el texto de forma palabra1_palabra2...
@app.route("/messages/bytext/notin/<text>")
def get_message_notin(text):
    text = text.split("_")
    ugly = []
    for palabra in text:
        palabra = "\"{}\"".format(palabra)
        message = list(messages.find({"$text": {"$search": palabra}},{"id": 1}))
        for mes in message:
            ugly.append(mes["id"])
    messages2 = list(messages.find({}, {"_id": 0}))
    final = []
    for mes in messages2:
        if mes["id"] not in ugly:
            final.append(mes)
    return jsonify(final)

#Se debe ingresar el texto de forma palabra1_palabra2...
@app.route("/messages/bytext/deseable/<text>")
def get_message_deseable(text):
    text = text.split("_")
    palabras = ""
    for palabra in text:
        palabras += "{}".format(palabra)
        palabras+= " "
    message = list(messages.find({"$text": {"$search": palabras}},{"_id": 0}))
    return jsonify(message)

#Se debe ingresar el texto de forma palabrasiosi_palabrasiosi_...+palabradeseable1_palabradeseable2...-palabranodeseada_...
@app.route("/messages/bytext/consulta/<text>")
def get_message_consulta(text):
    des = text.find("+")
    no = text.find("-")
    if no > 0 and des>0:
        debe = text[:des]
        debe = debe.split("_")
        deseable = text[des+1:no]
        deseable = deseable.split("_")
        no_debe = text[no+1:]
        no_debe = no_debe.split("_")
    elif des > 0 and no < 0: 
        debe = text[:des]
        debe = debe.split("_")
        deseable = text[des+1:]
        deseable = deseable.split("_")
        no_debe = []
    elif des<0 and no>0:
        debe = text[:no]
        debe = debe.split("_")
        deseable = []
        no_debe = text[no+1:]
        no_debe = no_debe.split("_")
    elif des ==0 or no ==0:
        debe = []
        if des ==0:
            if no > 0:
                deseable = text[1:no]
                deseable = deseable.split("_")
                no_debe = text[no+1:]
                no_debe = no_debe.split("_")
            else:
                deseable = text[1:].split("_")
                no_debe =[]
        else:
            no_debe = text[1:].split("_")
            deseable = []
    else:
        debe = text.split("_")
        deseable = []
        no_debe = []
    palabras1 = ""
    for palabra in debe:
        palabras1 += "\"{}\"".format(palabra)
    for palabra in deseable:
        palabras1 += "{}".format(palabra)
    message1 = list(messages.find({"$text": {"$search": palabras1}},{"_id": 0}))
    ugly = []
    for palabra in no_debe:
        palabra = "\"{}\"".format(palabra)
        message2 = list(messages.find({"$text": {"$search": palabra}},{"id": 1}))
        for mes in message2:
            ugly.append(mes["id"])
    final = []
    if len(palabras1) >0:
        for mes in message1:
            if mes["id"] not in ugly:
                final.append(mes)
        return jsonify(final)
    else:
        messages3 = list(messages.find({}, {"_id": 0}))
        for mes in messages3:
            if mes["id"] not in ugly:
                final.append(mes)
        return jsonify(final)


#Se debe ingresar el texto de forma palabrasiosi_palabrasiosi_...+palabradeseable1_palabradeseable2...-palabranodeseada_...=idusuario
@app.route("/messages/bytext/consultaid/<text>")
def get_message_consulta2(text):
    text = text.split("=")
    id = int(text[1])
    text = text[0]
    des = text.find("+")
    no = text.find("-")
    if no > 0 and des>0:
        debe = text[:des]
        debe = debe.split("_")
        deseable = text[des+1:no]
        deseable = deseable.split("_")
        no_debe = text[no+1:]
        no_debe = no_debe.split("_")
    elif des > 0 and no < 0: 
        debe = text[:des]
        debe = debe.split("_")
        deseable = text[des+1:]
        deseable = deseable.split("_")
        no_debe = []
    elif des<0 and no>0:
        debe = text[:no]
        debe = debe.split("_")
        deseable = []
        no_debe = text[no+1:]
        no_debe = no_debe.split("_")
    elif des ==0 or no ==0:
        debe = []
        if des ==0:
            if no > 0:
                deseable = text[1:no]
                deseable = deseable.split("_")
                no_debe = text[no+1:]
                no_debe = no_debe.split("_")
            else:
                deseable = text[1:].split("_")
                no_debe =[]
        else:
            no_debe = text[1:].split("_")
            deseable = []
    else:
        debe = text.split("_")
        deseable = []
        no_debe = []
    palabras1 = ""
    for palabra in debe:
        palabras1 += "\"{}\"".format(palabra)
    for palabra in deseable:
        palabras1 += "{}".format(palabra)
    message1 = list(messages.find({"$text": {"$search": palabras1}, "sender": id},{"_id": 0}))
    ugly = []
    for palabra in no_debe:
        palabra = "\"{}\"".format(palabra)
        message2 = list(messages.find({"$text": {"$search": palabra}, "sender": id},{"id": 1}))
        for mes in message2:
            ugly.append(mes["id"])
    final = []
    if len(palabras1) >0:
        for mes in message1:
            if mes["id"] not in ugly:
                final.append(mes)
        return jsonify(final)
    else:
        messages3 = list(messages.find({"sender": id}, {"_id": 0}))
        for mes in messages3:
            if mes["id"] not in ugly:
                final.append(mes)
        return jsonify(final)
        
# Aca se deben ingresar las id de la forma id1_id2
@app.route("/messages/byusers/<ids>")
def get_messages_between(ids):
    id1, id2 = int(ids.split("_")[0]), int(ids.split("_")[1])
    messages1 = list(messages.find({"receptant": id1, "sender": id2}, {"_id": 0}))
    messages2 = list(messages.find({"receptant": id2, "sender": id1}, {"_id": 0}))
    return jsonify(messages1 + messages2)


###################### POST ######################
#para id1 como key, value debe el id de usuario 1. para id2 como key, value debe el id de usuario 2.
@app.route("/messages/enviar/<ids>", methods = ['POST'])
def enviar_mensaje(ids):
    if request.method == 'POST':
        id1, id2 = int(ids.split("_")[0]), int(ids.split("_")[1])
        data = {key: request.json[key] for key in USER_KEYS}
       
        # dado dos ids
        data["sender"] = id1
        data["receptant"] = id2
        # Se genera el uid
        count = messages.count_documents({})
        data["id"] = count + 1

        result = messages.insert_one(data)

        if (result): 
            output = "1 mensaje creado" 
            success = True
        else:
            output = "No se pudo crear el mensaje"
            success = False
        return jsonify({'success': success, 'message': output})
    else:
        return 'No está utilizando POST'

###################### DELETE ######################
#aca se debe ingresar el id de mensaje
@app.route("/messages/eliminar/<int:id>", methods = ['DELETE'])
def eliminar_mensaje(id):
 #   return 'ok'
    if request.method == 'DELETE':
        message = list(messages.find({"id": id}, {"_id": 0}))
        messages.delete_one({"id": id})
        messageDeleted = list(messages.find({"id": id}, {"_id": 0}))
        return jsonify(messageDeleted)
    else:
        return 'No está utilizando DELETE'

#main run !
if __name__ == "__main__":
    app.run()
