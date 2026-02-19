# SiteRoutes.py
from flask import Blueprint, render_template, request, jsonify, session
from io import BytesIO
import base64

# Application Class
from src.domain.service.ImagemCartaGenerator import ImagemCartaGenerator
imagem_carta_generator = ImagemCartaGenerator()

# Exception
from src.presentation.exception.PresentationException import *

# Blueprint
site_bp = Blueprint("site", __name__)


# -----------------------------------------------
# AUTENTIFICAÇÃO
# -----------------------------------------------
@site_bp.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@site_bp.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")

# -----------------------------------------------
# HOME
# -----------------------------------------------
@site_bp.route("/home", methods=["GET"])
def home():
    if "usuario" not in session:
        return render_template("login.html")
    return render_template("home.html")

# -----------------------------------------------
# FUNCIONALIDADES
# -----------------------------------------------
@site_bp.route("/cartas_diarias", methods=["GET"])
def cartas_diarias():
    if "usuario" not in session:
        return render_template("login.html")
    return render_template("cartas_diarias.html")

@site_bp.route("/inventario", methods=["GET"])
def inventario():
    if "usuario" not in session:
        return render_template("login.html")
    return render_template("inventario.html")

@site_bp.route("/fundicao", methods=["GET"])
def fundicao():
    if "usuario" not in session:
        return render_template("login.html")
    return render_template("fundicao.html")

@site_bp.route("/reforja", methods=["GET"])
def reforjar():
    if "usuario" not in session:
        return render_template("login.html")
    return render_template("reforja.html")

# -----------------------------------------------
# ACESSO AO GERADOR DE IMAGEM
# -----------------------------------------------
@site_bp.route("/img", methods=["POST"])
def gerar_imagem_carta():
    dados = request.get_json()
    if not dados:
        raise DadosInvalidosException()

    fundo = dados.get("fundo")
    personagem = dados.get("personagem")
    borda = dados.get("borda")

    if not fundo or not personagem or not borda:
        raise DadosFaltantesException

    try:
        img = imagem_carta_generator.gerar_carta(fundo, personagem, borda)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return jsonify({
            "sucesso": True,
            "imagem": img_base64
        }), 200

    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": "Erro ao gerar imagem",
            "erro": str(e)
        }), 500
