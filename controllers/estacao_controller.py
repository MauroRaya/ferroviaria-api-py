from flask import Flask, Blueprint, jsonify, request
from models.estacao import Estacao, validate_fields, validate_id

station_bp = Blueprint('station', __name__, url_prefix='/estacao')

@station_bp.route("/", methods=['POST'])
def station_post():
    data = request.json

    nome       = data.get('nome')
    cidade     = data.get('cidade')
    capacidade = data.get('capacidade')

    station, error = Estacao.add(nome, cidade, capacidade)

    if error:
        return jsonify({ 'error': error }), 400
    
    return {'id': station.id, 'nome': station.nome, 'cidade': station.cidade, 'capacidade': station.capacidade}, 201


@station_bp.route('/', methods=['GET'])
def station_get():
    stations = Estacao.get()

    if not stations:
        return jsonify({ 'message': 'Nenhuma estação encontrada' }), 404
    
    stations_dict = [{'id': station.id, 'nome': station.nome, 'cidade': station.cidade, 'capacidade': station.capacidade} for station in stations]
    return jsonify(stations_dict), 200


@station_bp.route('/<int:station_id>', methods=['GET'])
def station_get_by_id(station_id):
    station, error = Estacao.get_by_id(station_id)

    if error:
        return jsonify({ 'error': error }), 400
    
    if not station:
        return jsonify({ 'message': 'Nenhuma estação encontrada' }), 404
    
    station_dict = {'id': station.id, 'nome': station.nome, 'cidade': station.cidade, 'capacidade': station.capacidade}
    return jsonify(station_dict), 200


@station_bp.route("/<int:station_id>", methods=['PUT'])
def station_put(station_id):
    data = request.json

    nome       = data.get('nome')
    cidade     = data.get('cidade')
    capacidade = data.get('capacidade')

    station, error = Estacao.update(nome, cidade, capacidade, station_id)

    if error:
        return jsonify({ 'error': error }), 400
    
    return {'id': station.id, 'nome': station.nome, 'cidade': station.cidade, 'capacidade': station.capacidade}, 200


@station_bp.route("/<int:station_id>", methods=['DELETE'])
def station_delete(station_id):
    station, error = Estacao.remove_by_id(station_id)

    if error:
        return jsonify({ 'error': error }), 400
    
    return jsonify({ 'message': f'Estação {station.nome} foi deletada com sucesso' }), 200