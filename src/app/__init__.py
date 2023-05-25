import importlib
import os

import yaml
from flask import Flask

from app.extensions import register_extensions

config = yaml.load(open('config.yml', 'r'), Loader=yaml.FullLoader)


def create_app():
    app = Flask(__name__)
    app.config.update(config)

    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    dir_path = f'{app.name}/blueprints'  # app/blueprints/xxx
    mod_path = f'{app.name}.blueprints'  # app.blueprints.xxx
    for file in os.listdir(dir_path):
        if file.startswith('__'):
            continue
        mod_name = file[:-3] if file.endswith('.py') else file
        module = importlib.import_module(f'{mod_path}.{mod_name}')
        app.register_blueprint(getattr(module, 'bp'))
        print(f'Register blueprint: {module.__name__}')
