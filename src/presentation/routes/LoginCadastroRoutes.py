# LoginCadastroRoutes.py
from flask import Blueprint, request, jsonify, session
import hashlib

# Application Class
from src.application.UsuarioUserCase import UsuarioUserCase
usuario_user_case = UsuarioUserCase()

# Exceptions
from src.presentation.exception.PresentationException import *

# Blueprint
login_cadastro_bp = Blueprint("login_cadastro", __name__)


# -----------------------------------------------
# AUXILIAR
# -----------------------------------------------
def hash_sha256(txt: str) -> str:
    hash_txt = hashlib.sha256(txt.encode("utf-8"))
    return hash_txt.hexdigest()

def extrair_dados(dados, campos):
    if not dados:
        raise DadosInvalidosException()
    dados_extraidor = [dados.get(campo) for campo in campos]
    if any(dado is None for dado in dados_extraidor):
        raise DadosFaltantesException()
    return dados_extraidor


# -----------------------------------------------
# CADASTRO
# -----------------------------------------------
@login_cadastro_bp.route("/api/cadastro", methods=["POST"])
def cadastrar_usuario():
    dados = request.get_json()

    nome, senha = extrair_dados(dados, ["nome", "senha"])
    senha = hash_sha256(senha)
    usuario_user_case.criar_usuario(nome, senha)
    session["usuario"] = {"nome": nome}

    return jsonify({
        "sucesso": True,
        "mensagem": "Usuário cadastrado com sucesso"
    }), 201


# -----------------------------------------------
# LOGIN
# -----------------------------------------------
@login_cadastro_bp.route("/api/login", methods=["POST"])
def login_usuario():
    dados = request.get_json()

    nome, senha = extrair_dados(dados, ["nome", "senha"])
    usuario_user_case.validar_login(nome, senha)
    session["usuario"] = {"nome": nome}

    return jsonify({"sucesso": True, "mensagem": "Login válido"}), 200
