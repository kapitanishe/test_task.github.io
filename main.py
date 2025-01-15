from flask import Flask
from app.http_layer.routes import register_routes


def main():
    app = Flask(__name__)

    register_routes(app)  # Регистрация маршрутов
    app.run(host="0.0.0.0", port=7000, debug=False)


if __name__ == "__main__":
    main()

