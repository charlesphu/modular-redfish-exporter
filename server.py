import socketserver
import importlib
import os
import handler

PORT = 9100


class HttpServerHandler(handler.HttpServerHandler):
    pass


class ReloadableServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with ReloadableServer(("", PORT), HttpServerHandler) as httpd:
        print(f"Serving at port {PORT}")

        last_mtime = os.path.getmtime(handler.__file__)

        while True:
            current_mtime = os.path.getmtime(handler.__file__)

            if current_mtime != last_mtime:
                importlib.reload(handler)
                HttpServerHandler.__bases__ = (handler.HttpServerHandler,)
                last_mtime = current_mtime
                print("Reloaded handler.py")

            httpd.handle_request()