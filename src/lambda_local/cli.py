from crypt import methods
import os
import subprocess
import sys

from flask import Flask, request

# from config import get_config

app = Flask('lambda-local')

# config = get_config()

def pprint(msg: str):
    print(f"\033[4m{msg}\033[0m")
    print("")

def install_requirements():
    for dir in os.listdir("functions"):
        requirements_file = os.path.join("functions", dir, "requirements.txt")
        if os.path.exists(requirements_file):
            pprint(f"Installing requirements from {requirements_file}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        pprint(f"Requirements file {requirements_file} doesn't exist")

def camelcase(value: str) -> str:
    return ''.join(word.capitalize() or '_' for word in value.split('_'))

def flask_handler():
    path = request.path
    function_name = path.lstrip('/')
    function_path = os.path.abspath(os.path.join("functions", function_name))
    if function_path not in sys.path:
        sys.path.append(function_path)

    import importlib.util
    # spec = importlib.util.spec_from_file_location(mod_name, path)
    spec = importlib.util.spec_from_file_location(function_name, f"{function_path}/index.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["index"] = mod
    spec.loader.exec_module(mod)

    func = getattr(mod, 'lambda_handler')

    event = request.json
    return func(event, {})

def start_server():
    for dir in os.listdir("functions"):
        # sys.path.append(os.path.join("functions", dir))
        # handler = getattr(pkg, "lambda_handler")
        app.add_url_rule(f"/{dir}", methods=["POST"], view_func=flask_handler)
    app.run()

def main():
    install_requirements()
    start_server()