#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import json
import time
import logging

from logger import LoggingConsumer, LoggingProducer
import config

host = ('192.168.200.114', 8888)

LoggingConsumer()
logger = LoggingProducer().get_default_logger()

class Resquest(BaseHTTPRequestHandler):

	def _set_response(self, code:int, header:str):
		self.send_response(code)
		self.send_header('Content-type', header)
		self.end_headers()

	def get_method_test(self, query):
		data = {
			"get test" : "get method"
		}
		self._set_response(200, 'application/json')
		self.wfile.write(json.dumps(data).encode())

	def get_method_raspberry(self, query):
		data = {
			"method" : "raspberry",
			"status" : "ok",
		}
		save = {
		}
		if len(query) > 0:
			paramlist = query.split('&')
			for param in paramlist:
				pl = param.split('=')
				save[pl[0]] = pl[1]
		self._set_response(200, 'application/json')
		self.wfile.write(json.dumps(data).encode())
		if len(save) != 0:
			logger.info(json.dumps(save))

	def do_GET(self):
		parsed_path = parse.urlparse(self.path)
		print(parsed_path.path)
		print(parsed_path.query)
		if parsed_path.path == "/test":
			self.get_method_test(parsed_path.query)
		elif parsed_path.path == "/raspberry":
			self.get_method_raspberry(parsed_path.query)
		elif parsed_path.path == "/esp32":
			self.get_method_raspberry(parsed_path.query)
		else:
			self._set_response(404, 'text/html')

	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
			str(self.path), str(self.headers), post_data.decode('utf-8'))
		self._set_response(200, 'text/html')
		self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

if __name__ == '__main__':
	server = HTTPServer(host, Resquest)
	print("Starting server, listen at: %s:%s" % host)
	server.serve_forever()
