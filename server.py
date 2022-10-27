import pathlib

from http.server import BaseHTTPRequestHandler, HTTPServer
from orm import Task, BaseManager

DB_PATH = pathlib.Path.home() / ".chang/prod.sqlite"
BaseManager.set_connection(settings=DB_PATH)

HOSTNAME = "localhost"
PORT_DEFAULT = 3131
BASE_PATH = pathlib.Path.absolute(pathlib.Path(__file__).parent)

class ChangRequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def component_navbar() -> str:
        with open(file=BASE_PATH / "navbar.html", mode="r", encoding="utf-8") as navbar_html:
            navbar = str(navbar_html.read())
        return navbar

    def root(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(self.component_navbar() + f"<h1>Up and running", "utf-8"))

    def random_int(self):
        import random
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(self.component_navbar() + f"<h1>data: {random.randint(0,10)}</h1>", "utf-8"))

    def all_tasks(self):
        a = Task.objects.read_all()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes(self.component_navbar()+
                f"<h1>Task:{a}</h1>", "utf-8"
            )
        )

    def do_GET(self):
        match self.path:
            case "/":
                self.root()
            case "/tasks":
                self.all_tasks()
            case "/random_int":
                self.random_int()
            case _:
                self.root()


if __name__ == "__main__":

    webServer = HTTPServer((HOSTNAME, PORT_DEFAULT), ChangRequestHandler)
    print("Server started http://%s:%s" % (HOSTNAME, PORT_DEFAULT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
