import sys
import yaml
import socketserver
import re

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HOST = ""
PORT = 9100

redfishYaml = None

def expandPaths(url, responseJson, patterns):
    expandedPaths = []
    for pattern in patterns:
        if pattern in responseJson.keys():
            expandedPaths.append(url + pattern)
    return expandedPaths

def discover(url):
    # add timestamp, serial number, platform / system type to catalog

def quickcheck(url):
    # use expanded-paths.yml

def probe(ip, password):
    # if file.contains(url) and currtime - url.timestamp > 24hr:
    #   discover(url)
    # else
    # quickcheck(url)

class HttpServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/metrics":
            body = self.metricsBody()
        elif path == "/probe":
            query = parsed.query
            print("this is the path:", path, "\nthis is the query:", query)
            params = parse_qs(query)
            body = self.metricsBody() # what is this?
            targetIp = params['target'][0]
            targetModule = params['module'][0]

            if targetIp and targetModule and redfishYaml[targetModule]:
                module = redfishYaml[targetModule]
                print(module)
                basepath = f"https://{targetIp}"
                if 'basePath' in module:
                    basepath += module['basePath']
                    module.pop('basePath')

                # do we really need categories, or can we just use category name in yaml
                curlpaths = [basepath]
                for category in module:
                    for categoryName in module[category]:
                        if 'path' not in module[category][categoryName]:
                            warn("No path provided, skiping ...")
                            break

                        # constructing curl commands
                        parts = re.findall(r'[^{}]+|\{[^}]+\}', path)
                        for part in parts:
                            if part.startswith("{") and part.endswith("}"):
                                # search for potential matches
                                if part not in module[category][categoryName]:
                                    warn(f"placeholder {match} not found, skipping ...")
                                    break
                                newpaths = []
                                for url in curlpaths:
                                    url += prefix
                                    print("querying:", url, "for matches")
                                    curlpaths.append(url)

                                    response = requests.get(
                                        url,
                                        auth=("root", "password"),
                                        verify=False
                                    )
                                    data = response.json()
                                    # regex match each match
                                    for placeholder in module[category][categoryName][part]:
                                        matches = re.match(placeholder. data.keys())
                                        if matches:
                                            newpaths.append(url + matches)
                                curlpaths = newpaths

                                url = basepath + part
                            else:
                                prefix = part;
                for url in curlpaths:
                    response = requests.get(
                        url,
                        auth=("root", "password"),
                        verify=False
                    )
                    data = response.json


                    #     bracketMatch = re.findall(r'\{([^}]+)\}', path)
                    #     placeholdersFound = True
                    #     paths = []
                    #     if bracketMatch:
                    #         for match in bracketMatch:
                    #         prefixMatch = re.findall(r'^(.*?)\{', path)
                    #             if match not in module[category][categoryName]:
                    #                 warn(f"placeholder {match} not found, skipping ...")
                    #                 placeholdersFound = false

                        
                    #     if not placeholdersFound:
                    #         break;
                    # print(category)
                    # module[category]
            self.send_error(404)

        else:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode())

    def metricsBody(self) -> str:
        return (
            "# TYPE redfish_exporter_up gauge\n"
            "redfish_exporter_up 1\n"
        )

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with open("redfish-paths.yml", encoding="utf-8") as f:
        redfishYaml = yaml.safe_load(f)
    with socketserver.TCPServer(("", PORT), HttpServerHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

    # handler = HttpServerHandler.new()
    # handler.serve_forever()
