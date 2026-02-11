from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'

    @app.route('/')
    def home():
        return "Produce Vendor Portal is Running 🚀"

    return app
