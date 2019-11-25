# Python 3 server example
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from correlation import getAssociativity
from hierarchy_tree import getHierarchyTree
from vocabulary import Vocabulary

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		path, args = self.parsePath()
		print(path, args)
		if path == "/hierarchy":
			self.send_response(200)
			self.send_header("Content-type", "application/json")
			self.end_headers()
			parts = None if "parts" not in args else args["parts"][0]
			fileName = None if "fileName" not in args else args["fileName"][0]
			self.wfile.write(bytes(json.dumps(getHierarchyTree(voc, fileName, parts)), "utf-8"))
		elif path == "/associativity":
			self.send_response(200)
			self.send_header("Content-type", "application/json")
			self.end_headers()
			fileName = None if "fileName" not in args else args["fileName"][0]
			filter = None if "filter" not in args else args["filter"][0].split(" : ")
			self.wfile.write(bytes(json.dumps(getAssociativity(voc, fileName, filter)), "utf-8"))
		elif Path("Interface" + path).is_file() and -1 == path.find("/../"):
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(open("Interface" + path, "rb").read())
			print("sended file : " + "Interface" + path)
		else:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(open("Interface/index.html", "rb").read())
		# self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
		# self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
		# self.wfile.write(bytes("<body>", "utf-8"))
		# self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
		# self.wfile.write(bytes("</body></html>", "utf-8"))

	def parsePath(self):
		url = urlparse(self.path)
		return url.path, parse_qs(url.query)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python %s <vocfile> " % sys.argv[0])
		sys.exit(1)

	if not os.path.isfile(sys.argv[1]):
		print("Data file %s not found" % (sys.argv[2]))
		sys.exit(1)

	voc = Vocabulary(sys.argv[1])
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")
