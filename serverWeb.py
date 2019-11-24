# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from pathlib import Path

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
		elif Path("Interface/"+path).is_file() and not path.find("/../"):
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(open("Interface/"+path, "rb").read())
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
		s1 = self.path.split("?", 2)
		path = s1[0]
		args = dict()
		if len(s1) < 2:
			return path, args
		s2 = s1[1].split("&")
		for arg in s2:
			s3 = arg.split("=", 2)
			if len(s3) == 1:
				args[s3[0]] = ""
			else:
				args[s3[0]] = s3[1]
		return path, args




if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")