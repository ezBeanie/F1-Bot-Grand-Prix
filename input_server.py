import http.server
import record_training_data

class HttpServerHandler(http.server.BaseHTTPRequestHandler):
	"""
	A simple HTTP server capable of handling GET and POST requests
	"""

	def _set_headers(self, response=None, connection=None):
		self.send_response(200)
		self.send_header('Content-Type', 'text/html; charset=utf-8')

		if response is not None:
			self.send_header('Content-Length', len(response))
		if connection is not None:
			self.send_header('Connection', connection)
		self.end_headers()

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		# print('POST received\n')
		self.send_response(200)
		self.protocol_version = 'HTTP/1.1'
		self.end_headers()
		content_length = int(self.headers['Content-Length'])
		input = self.rfile.read(content_length).decode('utf-8').replace('payload=', '').split("x")
		response = b'ok'
		self.wfile.write(response)

	def log_message(self, format, *args):
		return