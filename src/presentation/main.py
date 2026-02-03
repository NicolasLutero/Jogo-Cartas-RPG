from flask import Flask

from routes.SiteRoutes import site_bp
from routes.LoginCadastroRoutes import login_cadastro_bp
from routes.UsuarioRoutes import usuario_bp
blueprints = [site_bp, login_cadastro_bp, usuario_bp]

class Server(Flask):
    def __init__(self, import_name: str):
        super().__init__(
            import_name,
            template_folder="ui/templates",
            static_folder="ui/static"
        )
        self._registrar_rotas()
        self.pedidos = []

    def _registrar_rotas(self) -> None:
        # BluePrints
        for bp in blueprints:
            self.register_blueprint(bp)


if __name__ == "__main__":
    app = Server(__name__)
    app.secret_key = "ABCDE12345FGHIJ67890"
    app.run(host="0.0.0.0", port=5050, debug=True)
