# SiteRoutes.py
import base64
from io import BytesIO
from flask import Blueprint, render_template, request, jsonify

from src.domain.service.ImagemCartaGenerator import ImagemCartaGenerator

site_bp = Blueprint("site", __name__)

# --- Autenticação ---
@site_bp.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@site_bp.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")

# --- Home ---
@site_bp.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

# --- Funcionalidades ---
@site_bp.route("/cartas_diarias", methods=["GET"])
def cartas_diarias():
    return render_template("cartas_diarias.html")

@site_bp.route("/inventario", methods=["GET"])
def inventario():
    return render_template("inventario.html")

@site_bp.route("/fundicao", methods=["GET"])
def fundicao():
    return render_template("fundicao.html")

@site_bp.route("/reforjar", methods=["GET"])
def reforjar():
    return render_template("reforjar.html")

# --- Imagens das Cartas ---
@site_bp.route("/img", methods=["POST"])
def gerar_imagem_carta():
    data = request.get_json()

    fundo = data.get("fundo")
    personagem = data.get("personagem")
    borda = data.get("borda")

    # validação básica
    if not fundo or not personagem or not borda:
        return jsonify({
            "sucesso": False,
            "mensagem": "Parâmetros inválidos"
        }), 400

    try:
        # gera imagem Pillow
        img = ImagemCartaGenerator().gerar_carta(fundo, personagem, borda)

        # buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # base64
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return jsonify({
            "sucesso": True,
            "imagem": img_base64
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "sucesso": False,
            "mensagem": "Erro ao gerar imagem",
            "erro": str(e)
        }), 500
