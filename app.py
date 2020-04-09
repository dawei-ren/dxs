from flask import Flask
from myApp import my_app
from chat import chat_app
from myApp.scripts.test_script import test_command, root_path
from tests.test_all import test_all
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # 跨域
    CORS(app, resources='/*')
    app.register_blueprint(my_app, url_prefix='/myapp')
    app.register_blueprint(chat_app, url_prefix='/chat')
    app.cli.add_command(test_command)
    app.cli.add_command(root_path)
    app.cli.add_command(test_all)

    app.config['SECRET_KEY'] = 'secret!'

    return app


app = create_app()