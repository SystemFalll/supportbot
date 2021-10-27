from flask import Flask
from threading import Thread
import sys

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()