"""
Antes de ejecutar este programa, se debe instalar flask por medio del comando:
pip install flask
"""
import os
from flask import Flask, jsonify, request
import requests


app = Flask("EvilApi")
app.debug = True

persons = []
subscribers = []



def id_exists(id, persons):
    app.logger.debug("id_exists was called")
    app.logger.debug(id)
    app.logger.debug(persons)
    for person in persons:
        if person["id"] == id:
            return True
    return False

def broadcast_message(msg, subscribers):
    for subscriber in subscribers:
        endpoint = "http://{}:5000/api/v1/message".format(subscriber)
        response = requests.put(url=endpoint, json={"msg": msg})
        app.logger.debug(response.status_code)

"""
PUT /api/v1/message -> toma el mensaje que viene en el request como json y los imprime 
                             por medio del log de debug.
"""
def print_message(msg):
   if not request.is_json:
        return jsonify({
            "msg": "Only json is supported in this api"
        }), 400
    datos = request.get_json()
    app.logger.debug(datos)
    return jsonify({"msg": "mensaje recibido ok"}), 200

"""
POST /api/v1/message -> toma el mensaje y lo redistribuye a la lista de subscribers y 
                              envía los requests por medio de PUT
"""
def spread_message(msg):
    if not request.is_json:
        return jsonify({
            "msg": "Only json is supported in this api"
        }), 400
    datos = request.get_json()
    app.logger.debug(datos)
    for subscriber in subscribers:
        endpoint = "http://{}:5000/api/v1/message".format(subscriber)
        response = requests.post(url=endpoint, json={"msg": msg})
        app.logger.debug(response.status_code)

"""
POST /api/v1/subscriber -> recibe un json con un único valor que se llama "ip" y lo
                                 almacena en una lista en memoria de subscribers
"""
def list_subscriber(ip):
    if not request.is_json:
    return jsonify({
        "msg": "Only json is supported in this api"
    }), 400
    datos = request.get_json()
    for subscriber in subscribers:
        endpoint = "http://{}:5000/api/v1/message".format(subscriber)
        response = requests.put(url=endpoint, json={"msg": msg})
        app.logger.debug(response.status_code)
    return jsonify({"msg": "almacenado en la lista de subscribers"}), 200


def post_subscriber():
    if not request.is_json:
        return jsonify({
            "msg": "Only json is supported in this api"
        }), 400

    datos = request.get_json()

    if "ip" not in datos:
        return jsonify({
            "msg": "An id is required"
        }), 400

    subscribers.append(datos["ip"])
    return jsonify({"msg": "todo salio bien"}), 200

@app.route('/')
def get_root_resource():
    return 'This is a root resource'

@app.route('/api/v1/person', methods=["POST"])
def post_person():
    # esto es una validación para garantizar que los datos vienen en json que es 
    # lo que este servidor sabe interpretar.
    if not request.is_json:
        return jsonify({
            "msg": "Only json is supported in this api"
        }), 400
    
    # Si llegamos acá es porque los datos sí son JSON
    datos = request.get_json()

    # Para poder crear una persona (recurso) es mandatorio 
    # que tenga un id único
    if "id" not in datos:
        return jsonify({
            "msg": "An id is required"
        }), 400

    if id_exists(datos["id"], persons):
        return jsonify({
            "msg": "The provided id is already in use"
        }), 400

    persons.append(datos)

    return jsonify({
        "msg": "Person created"
    }), 201

@app.route('/api/v1/person', methods=["GET"])
def get_person():
    return jsonify(persons), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)