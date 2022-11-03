import re
import pathlib

from http.server import BaseHTTPRequestHandler, HTTPServer
from model import Task

HOSTNAME = "localhost"
PORT_DEFAULT = 3131
BASE_PATH = pathlib.Path.absolute(pathlib.Path(__file__).parent)


def navlink(route, link):
    return f"<a href='{route}'>{link}</a>"


def navbar():
    anchors = {"/": "Home", "tasks": "All Tasks", "random_int": "Random Integer"}
    return f"<nav>{' '.join([navlink(r, l) for r, l in anchors.items()])}</nav>"


def _tasks(a):
    return f"<h1>{a}</h1>"


def render_layout(replacement: str):
    replacement = navbar() + replacement
    with open(file="index.html", mode="r", encoding="utf-8") as index_html:
        index = index_html.read()
        final_index = re.sub(pattern="{{%app_entry%}}", repl=replacement, string=index)
        return final_index


class ChangRequestHandler(BaseHTTPRequestHandler):

    # View-method
    def root(self):
        # Begin decorator
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # End decorator
        self.wfile.write(bytes(render_layout(replacement=""), "utf-8"))

    # View-method
    def random_int(self):
        # Begin decorator
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # End decorator
        import random

        randint_to_render = random.randint(0, 10)

        self.wfile.write(
            bytes(
                render_layout(replacement=f"<h1>data: {randint_to_render}</h1>"),
                "utf-8",
            )
        )

    # View-method
    def all_tasks(self):
        # Begin decorator
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # end decorator
        a = Task.objects.select()
        self.wfile.write(bytes(render_layout(replacement=_tasks(a)), "utf-8"))

    # static-file-method
    def send_css(self):
        self.send_response(200)
        self.send_header("Content-type", "text/css")
        self.end_headers()
        # end decorator
        with open(file="main.css", mode="r", encoding="utf-8") as main_css:
            main = main_css.read()
            self.wfile.write(bytes(main, "utf-8"))

    def do_GET(self):
        match self.path:
            case "":
                self.root()
            case "/":
                self.root()
            case "/tasks":
                self.all_tasks()
            case "/random_int":
                self.random_int()
            case "/main.css":
                self.send_css()
            case _:
                self.root()


if __name__ == "__main__":
    from orm import SQLiteManager

    DB_PATH = pathlib.Path.home() / ".chang/prod.sqlite"
    SQLiteManager.set_connection(settings=DB_PATH)

    webServer = HTTPServer((HOSTNAME, PORT_DEFAULT), ChangRequestHandler)
    print("Server started http://%s:%s" % (HOSTNAME, PORT_DEFAULT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
