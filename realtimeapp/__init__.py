from flask import Flask

app = Flask(__name__)

def configure_app():
    app.config['SECRET_KEY'] = "verysecret"
    
    from . import routes

    return app