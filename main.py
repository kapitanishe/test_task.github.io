from flask import Flask
from flask_jwt_extended import JWTManager

from app.http_layer.routes import register_routes
from config import Config


def main():
    app = Flask(__name__)

    app.config.from_object(Config)
    JWTManager(app)

    register_routes(app)
    app.run(host="127.0.0.1", port=7000, debug=False)


if __name__ == "__main__":
    main()
