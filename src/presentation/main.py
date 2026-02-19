# main.py
from flask import Flask, jsonify, send_from_directory
from pathlib import Path
import os

# Blueprints Routes
from routes.SiteRoutes import site_bp
from routes.LoginCadastroRoutes import login_cadastro_bp
from routes.MecanicaRoutes import mecanica_bp
blueprints = [site_bp, login_cadastro_bp, mecanica_bp]

# Exception
from src.presentation.exception.HttpExceptionMapper import HttpExceptionMapper


class Server(Flask):
    def __init__(self, import_name: str):
        super().__init__(
            import_name,
            template_folder="ui/templates",
            static_folder="ui/static"
        )
        self._registrar_rotas()
        self._registrar_handlers()

    def _registrar_rotas(self) -> None:
        @self.route('/favicon.ico', methods=["GET"])
        def favicon():
            return send_from_directory(
                os.path.join(Path(__file__).resolve().parents[2],'img'),
                'favicon.ico',
                mimetype='image/vnd.microsoft.icon'
            ), 200

        for bp in blueprints:
            self.register_blueprint(bp)

    def _registrar_handlers(self) -> None:
        @self.errorhandler(Exception)
        def handle_http_mapper(e):
            http_error = HttpExceptionMapper.map_http(e)

            if http_error:
                return jsonify({
                    "sucesso": False,
                    "mensagem": str(http_error)
                }), http_error.status_code

            print(e)
            return jsonify({
                "sucesso": False,
                "mensagem": "Erro interno do servidor"
            }), 500

if __name__ == "__main__":
    app = Server(__name__)
    app.secret_key = "ABCDE12345FGHIJ67890"
    app.run(host="0.0.0.0", port=5050, debug=True)
