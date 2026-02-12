# MecanicaRoutes.py
from flask import Blueprint, session, jsonify, request
from src.application.InventarioService import InventarioService
from src.application.UsuarioService import UsuarioService

mecanica_bp = Blueprint("mecanica", __name__)


# =========================
# Listar Tipos de Fundo, Personagem e Borda Que O Usuário Tem
# =========================

@mecanica_bp.route("/api/inventario/tipos", methods=["GET"])
def tipos():
    if "usuario" not in session:
        return jsonify({
            "sucesso": False,
            "mensagem": "Não autenticado"
        }), 401

    tipos = InventarioService().listar_tipos(session["usuario"]["nome"])

    return jsonify({
        "sucesso": True,
        "tipos": tipos
    }), 200


# =========================
# Buscar Cartas do Usuário (com filtro)
# =========================

@mecanica_bp.route("/api/inventario/", methods=["POST"])
def buscar_cartas_usuario():
    if "usuario" not in session:
        return jsonify({
            "sucesso": False,
            "mensagem": "Não autenticado"
        }), 401

    nome = session["usuario"]["nome"]
    dados = request.get_json() or {}

    # lista de personagens selecionados
    tipos = dict(dados)

    cartas = InventarioService().buscar_cartas_usuario(nome, tipos)

    return jsonify({
        "sucesso": True,
        "cartas": cartas
    }), 200


# =========================
# Acesso Ao Status Diario
# =========================

@mecanica_bp.route("/api/usuario/status-diario", methods=["GET"])
def status_diario():
    if "usuario" not in session:
        return jsonify({
            "sucesso": False,
            "mensagem": "Não autenticado"
        }), 401

    nome = session["usuario"]["nome"]
    status = UsuarioService().acoes_disponiveis(nome)

    if not status:
        return jsonify({
            "sucesso": False,
            "mensagem": "Usuário não encontrado"
        }), 404

    else:
        return jsonify({
            "sucesso": True,
            "data": status
        }), 200


# =========================
# Coleta de Cartas Diárias
# =========================

@mecanica_bp.route("/api/usuario/cartas-diarias", methods=["GET"])
def coletar_cartas():
    if "usuario" not in session:
        return jsonify({
            "sucesso": False,
            "mensagem": "Não autenticado"
        }), 401

    nome = session["usuario"]["nome"]

    # Verifica disponibilidade no banco
    status = UsuarioService().acoes_disponiveis(nome)

    if not status:
        return jsonify({
            "sucesso": False,
            "mensagem": "Usuário não encontrado"
        }), 404

    # Se já usou hoje
    if not status["cartas_diarias"]:
        return jsonify({
            "sucesso": False,
            "mensagem": "Cartas diárias já foram coletadas hoje"
        }), 403

    # Gera as cartas
    cartas = UsuarioService().coletar_cartas(nome)

    return jsonify({
        "sucesso": True,
        "cartas": cartas
    }), 200
