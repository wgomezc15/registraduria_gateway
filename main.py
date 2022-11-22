from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
import datetime
import requests
import re

app=Flask(__name__)
cors = CORS(app)

from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
app.config["JWT_SECRET_KEY"]="super-secret" #Cambiar por el que se conveniente
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def create_token():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url=dataConfig["url-backend-security"]+'/usuarios/validar'
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        user = response.json()
        expires = datetime.timedelta(seconds=60 * 60*24)
        access_token = create_access_token(identity=user, expires_delta=expires)
        return jsonify({"token": access_token, "user_id": user["_id"]})
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

@app.before_request
def before_request_callback():
    endPoint=limpiarURL(request.path)
    excludedRoutes=["/login"]
    if excludedRoutes.__contains__(request.path):
        print("ruta excluida ",request.path)
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        if usuario["rol"] is not None:
            tienePersmiso=validarPermiso(endPoint,request.method,usuario["rol"]["_id"])
            if not tienePersmiso:
                return jsonify({"message": "Permission denied"}), 401
        else:
            return jsonify({"message": "Permission denied"}), 401

def limpiarURL(url):
    partes = request.path.split("/")
    for laParte in partes:
        if re.search('\\d', laParte):
            url = url.replace(laParte, "?")
    return url

def validarPermiso(endPoint,metodo,idRol):

    url=dataConfig["url-backend-security"]+"/permisos-roles/validar-permiso/rol/"+str(idRol)
    tienePermiso=False
    headers = {"Content-Type": "application/json; charset=utf-8"}
    body={"url":endPoint,
    "metodo":metodo
    }
    response = requests.get(url, json=body, headers=headers)
    try:
        data = response.json()
        if("_id" in data):
            tienePermiso=True
    except:
        pass
    return tienePermiso


###############

@app.route("/candidato", methods=['GET'])
def getCandidatos():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/candidato'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidato", methods=['POST'])
def crearCandidato():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/candidato'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)


@app.route("/candidato/<string:id>", methods=['GET'])
def getCandidato(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/candidato/' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/candidato/<string:id>", methods=['PUT'])
def modificarCandidato(id):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/candidato/' + id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)


@app.route("/candidato/<string:id>", methods=['DELETE'])
def eliminarCandidato(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/candidato/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

###############
"""Implementacion metodo main para mesas"""


@app.route("/mesa", methods=['GET'])
def getMesas():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/mesas'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/mesa", methods=['POST'])
def crearMesa():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/mesas'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)


@app.route("/mesa/<string:id>", methods=['GET'])
def getMesa(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/mesas/' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/mesa/<string:id>", methods=['PUT'])
def modificarMesa(id):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/mesas/' + id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)


@app.route("/mesa/<string:id>", methods=['DELETE'])
def eliminarMesa(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/mesas/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)


###############
"""Implementacion metodo main para partidos"""


@app.route("/partido", methods=['GET'])
def getPartidos():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/partidos'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/partido", methods=['POST'])
def crearPartido():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/partidos'
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)


@app.route("/partido/<string:id>", methods=['GET'])
def getPartido(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/partidos/' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/partido/<string:id>", methods=['PUT'])
def modificarPartido(id):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/partidos/' + id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)


@app.route("/partido/<string:id>", methods=['DELETE'])
def eliminarPartido(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/partidos/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

###############

"""Implementacion metodo main para resultados"""

@app.route("/resultado", methods=['GET'])
def getResultados():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/resultado/<string:id>", methods=['GET'])
def getResultado(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados/' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/resultado/partido/<string:id_partido>/candidato/<string:id_candidato>/mesa/<string:id_mesa>", methods=['POST'])
def crearResultado(id_partido,id_candidato, id_mesa):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados/partido/' + id_partido + '/candidato/' + id_candidato + '/mesa/' + id_mesa
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/resultado/<string:id_resultado>/partido/<string:id_partido>/candidato/<string:id_candidato>/mesa/<string:id_mesa>", methods=['PUT'])
def modificarResultado(id_resultado,id_partido, id_candidato, id_mesa):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados' + id_resultado, id_partido, id_candidato, id_mesa
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/resultado/<string:id_resultado>", methods=['DELETE'])
def eliminarResultado(id_resultado):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados' + id_resultado
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/resultado/mesa/<string:id_mesa>", methods=['GET'])
def inscritosEnMesa(id_mesa):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados' + id_mesa
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/resultado/votaciones_mayores", methods=['GET'])
def getVotacionesMayores(miControladorResultado):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)


@app.route("/resultado/promedio_votaciones/mesa/<string:id_mesa>", methods=['GET'])
def getPromedioVotacionEnMesa(id_mesa):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/resultados' + id_mesa
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)





def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])