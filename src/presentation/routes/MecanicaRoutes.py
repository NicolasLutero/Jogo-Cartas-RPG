# MecanicaRoutes.py
from flask import Blueprint, session, jsonify, request
from src.presentation.routes.auxiliares import verificar_sessao

# Application Class
from src.application.InventarioUserCase import InventarioUserCase
from src.application.UsuarioUserCase import UsuarioUserCase
inventario_user_case = InventarioUserCase()
usuario_user_case = UsuarioUserCase()

# Exception
from src.presentation.exception.PresentationException import *

# Blueprint
mecanica_bp = Blueprint("mecanica", __name__)


# -----------------------------------------------
# ACESSO AO STATUS DIÁRIO
# -----------------------------------------------
@mecanica_bp.route("/api/usuario/status-diario", methods=["GET"])
def status_diario():
    if not verificar_sessao():
        raise UsuarioNaoAutentificadoException()

    nome = session["usuario"]["nome"]
    status = usuario_user_case.acoes_disponiveis(nome)

    return jsonify({
        "sucesso": True,
        "data": status
    }), 200


# -----------------------------------------------
# BUSCAR CARTAS DE UM USUÁRIO COM FILTRO
# -----------------------------------------------
@mecanica_bp.route("/api/inventario", methods=["POST"])
def buscar_cartas_usuario():
    if not verificar_sessao():
        raise UsuarioNaoAutentificadoException()

    nome = session["usuario"]["nome"]
    dados = request.get_json() or {}
    tipos_filtro = dict(dados)
    cartas = inventario_user_case.buscar_cartas_usuario(nome, tipos_filtro)

    return jsonify({
        "sucesso": True,
        "cartas": cartas
    }), 200


# -----------------------------------------------
# LISTAR TIPOS DE FUNDO, PERSONAGEM E BORDA QUE UM USUÁRIO TEM
# -----------------------------------------------
@mecanica_bp.route("/api/inventario/tipos", methods=["GET"])
def buscar_tipos_cartas():
    if not verificar_sessao():
        raise UsuarioNaoAutentificadoException()

    nome = session["usuario"]["nome"]
    tipos = inventario_user_case.buscar_tipos(nome)

    return jsonify({
        "sucesso": True,
        "tipos": tipos
    }), 200


# -----------------------------------------------
# BUSCAR CARTA DE UM USUÁRIO
# -----------------------------------------------
@mecanica_bp.route("/api/inventario/carta", methods=["POST"])
def buscar_carta_id():
    if not verificar_sessao():
        raise UsuarioNaoAutentificadoException()

    nome = session["usuario"]["nome"]
    dados = request.get_json() or {}
    id_carta = dict(dados)["id"]
    carta = inventario_user_case.buscar_carta_usuario(nome, id_carta)

    return jsonify({
        "sucesso": True,
        "carta": carta
    }), 200


# -----------------------------------------------
# COLETAR CARTAS DIÁRIAS
# -----------------------------------------------
@mecanica_bp.route("/api/usuario/cartas-diarias", methods=["GET"])
def coletar_cartas():
    if not verificar_sessao():
        raise UsuarioNaoAutentificadoException()

    nome = session["usuario"]["nome"]
    cartas = inventario_user_case.coletar_cartas(nome)

    return jsonify({
        "sucesso": True,
        "cartas": cartas
    }), 200


# -----------------------------------------------
# REFORJAR CARTA
# -----------------------------------------------
@mecanica_bp.route("/api/usuario/reforja", methods=["POST"])
def refojar_carta():
    if not verificar_sessao():
        raise UsuarioNaoAutentificadoException()

    nome = session["usuario"]["nome"]
    dados = request.get_json() or {}
    id_carta = dict(dados)["id"]
    carta_reforjada = inventario_user_case.reforjar_carta(nome, id_carta)

    return jsonify({
        "sucesso": True,
        "carta": carta_reforjada
    }), 200


# -----------------------------------------------
# FUNDIR CARTA
# -----------------------------------------------
@mecanica_bp.route("/api/usuario/fundicao", methods=["POST"])
def fundir_carta():
    if not verificar_sessao():
        raise UsuarioNaoAutentificadoException()

    nome = session["usuario"]["nome"]
    dados = request.get_json() or {}
    carta_base = dict(dados)["base_id"]
    carta_sacrificio = dict(dados)["sacrificio_id"]
    carta_fundidao = inventario_user_case.fundir_cartas(nome, carta_base, carta_sacrificio)

    return jsonify({
        "sucesso": True,
        "carta": carta_fundidao
    }), 200
