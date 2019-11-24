# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

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
			self.wfile.write(bytes("{}", "utf-8"))
		elif Path("Interface"+path).is_file() and -1 == path.find("/../"):
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(open("Interface"+path, "rb").read())
			print("sended file : "+"Interface"+path)
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
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")