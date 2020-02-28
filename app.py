from flask import Flask
from myApp import my_app
from myApp.scripts.test_script import test_command, root_path
from tests.test_all import test_all


def create_app():
    app = Flask(__name__)
    app.register_blueprint(my_app, url_prefix='/myapp')
    app.cli.add_command(test_command)
    app.cli.add_command(root_path)
    app.cli.add_command(test_all)
    return app


app = create_app()
