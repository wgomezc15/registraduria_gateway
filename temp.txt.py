
"""Implementacion metodo main para mesas"""


@app.route("/mesas", methods=['GET'])
def getMesas():
    json = miControladorMesa.index()
    return jsonify(json)


@app.route("/mesas", methods=['POST'])
def crearMesa():
    data = request.get_json()
    json = miControladorMesa.create(data)
    return jsonify(json)


@app.route("/mesas/<string:id>", methods=['GET'])
def getMesa(id):
    json = miControladorMesa.show(id)
    return jsonify(json)


@app.route("/mesas/<string:id>", methods=['PUT'])
def modificarMesa(id):
    data = request.get_json()
    json = miControladorMesa.update(id, data)
    return jsonify(json)


@app.route("/mesas/<string:id>", methods=['DELETE'])
def eliminarMesa(id):
    json = miControladorMesa.delete(id)
    return jsonify(json)


"""Implementacion metodo main para partidos"""


@app.route("/partidos", methods=['GET'])
def getPartidos():
    json = miControladorPartido.index()
    return jsonify(json)


@app.route("/partidos", methods=['POST'])
def crearPartido():
    data = request.get_json()
    json = miControladorPartido.create(data)
    return jsonify(json)


@app.route("/partidos/<string:id>", methods=['GET'])
def getPartido(id):
    json = miControladorPartido.show(id)
    return jsonify(json)


@app.route("/partidos/<string:id>", methods=['PUT'])
def modificarPartido(id):
    data = request.get_json()
    json = miControladorPartido.update(id, data)
    return jsonify(json)


@app.route("/partidos/<string:id>", methods=['DELETE'])
def eliminarPartido(id):
    json = miControladorPartido.delete(id)
    return jsonify(json)

"""Implementacion metodo main para resultados"""

@app.route("/resultados", methods=['GET'])
def getResultados():
    json = miControladorResultado.index()
    return jsonify(json)


@app.route("/resultados/<string:id>", methods=['GET'])
def getResultado(id):
    json = miControladorResultado.show(id)
    return jsonify(json)


@app.route("/resultados/partido/<string:id_partido>/candidato/<string:id_candidato>/mesa/<string:id_mesa>", methods=['POST'])
def crearResultado(id_partido,id_candidato, id_mesa):
    data = request.get_json()
    json = miControladorResultado.create(data,id_partido, id_candidato, id_mesa)
    return jsonify(json)


@app.route("/resultados/<string:id_resultado>/partido/<string:id_partido>/candidato/<string:id_candidato>/mesa/<string:id_mesa>", methods=['PUT'])
def modificarResultado(id_resultado,id_partido, id_candidato, id_mesa):
    data = request.get_json()
    json = miControladorResultado.update(id_resultado, data,id_partido, id_candidato, id_mesa)
    return jsonify(json)


@app.route("/resultados/<string:id_resultado>", methods=['DELETE'])
def eliminarResultado(id_resultado):
    json = miControladorResultado.delete(id_resultado)
    return jsonify(json)


@app.route("/resultados/mesa/<string:id_mesa>", methods=['GET'])
def inscritosEnMesa(id_mesa):
    json = miControladorResultado.listarInscritosEnMesa(id_mesa)
    return jsonify(json)


@app.route("/resultados/votaciones_mayores", methods=['GET'])
def getVotacionesMayores(miControladorResultado):
    json = miControladorResultado.votacionesMasAltasPorpartido()
    return jsonify(json)


@app.route("/resultados/promedio_votaciones/mesa/<string:id_mesa>", methods=['GET'])
def getPromedioVotacionEnMesa(id_mesa):
    json = miControladorResultado.promedioVotacionEnMesa(id_mesa)
    return jsonify(json)