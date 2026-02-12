# LoginCadastroRoutes.py
from flask import Blueprint, request, jsonify, session
from src.application.UsuarioService import UsuarioService
import hashlib

login_cadastro_bp = Blueprint("login_cadastro", __name__)

# -----------------------------
# Utilitário interno
# -----------------------------

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

# -----------------------------
# Cadastro
# -----------------------------
@login_cadastro_bp.route("/api/cadastro", methods=["POST"])
def cadastrar_usuario():
    dados = request.get_json()

    if not dados:
        return jsonify({"sucesso": False, "mensagem": "Dados inválidos"}), 400

    nome = dados.get("nome")
    senha = dados.get("senha")

    if not nome or not senha:
        return jsonify({"sucesso": False, "mensagem": "Campos obrigatórios ausentes"}), 400

    senha_hash = hash_senha(senha)

    usuario = {
        "nome": nome,
        "senha": senha_hash
    }

    controle = UsuarioService()

    if controle.usuario_existe(nome):
        return jsonify({
            "sucesso": False,
            "mensagem": "Usuário já existe"
        }), 409

    controle.criar_usuario(usuario)

    session["usuario"] = {"nome": nome}
    return jsonify({
        "sucesso": True,
        "mensagem": "Usuário cadastrado com sucesso"
    }), 201


# -----------------------------
# Login
# -----------------------------
@login_cadastro_bp.route("/api/login", methods=["POST"])
def login_usuario():
    dados = request.get_json()

    if not dados:
        return jsonify({"sucesso": False, "mensagem": "Dados inválidos"}), 400

    nome = dados.get("nome")
    senha = dados.get("senha")

    if not nome or not senha:
        return jsonify({"sucesso": False, "mensagem": "Campos obrigatórios ausentes"}), 400

    senha_hash = hash_senha(senha)

    controle = UsuarioService()

    if not controle.usuario_existe(nome):
        return jsonify({
            "sucesso": False,
            "mensagem": "Usuário não encontrado"
        }), 404

    if not controle.validar_login(nome, senha_hash):
        return jsonify({
            "sucesso": False,
            "mensagem": "Senha incorreta"
        }), 401

    session["usuario"] = {"nome": nome}
    return jsonify({
        "sucesso": True,
        "mensagem": "Login válido"
    }), 200
