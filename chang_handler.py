import re
import pathlib

from http.server import BaseHTTPRequestHandler, HTTPServer
from ui_components import *
from model import Task

HOSTNAME = "localhost"
PORT_DEFAULT = 3131
BASE_PATH = pathlib.Path.absolute(pathlib.Path(__file__).parent)


def render_layout(replacement: str):
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
        all_tasks = Task.objects.mode_select()
        self.wfile.write(bytes(render_layout(replacement=app(all_tasks)), "utf-8"))

    def send_css(self):
        """static-file-method"""
        # Begin decorator
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
            case "/main.css":
                self.send_css()
            case _:
                self.root()


if __name__ == "__main__":
    from orm import SQLiteManager

    DB_PATH = pathlib.Path.home() / ".chang/prod.db"
    SQLiteManager.set_connection(settings=DB_PATH)

    webServer = HTTPServer((HOSTNAME, PORT_DEFAULT), ChangRequestHandler)
    print("Server started http://%s:%s" % (HOSTNAME, PORT_DEFAULT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
