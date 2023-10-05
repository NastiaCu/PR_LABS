import socket
import signal
import sys
import threading
import json
import re  

HOST = '127.0.0.1' 
PORT = 8080 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")

def load_product_details_from_json(json_file):
      with open(json_file, 'r') as file:
         product_details = json.load(file)
      return product_details
  

PRODUCTS_JSON_FILE = 'products.json'

product_details = load_product_details_from_json(PRODUCTS_JSON_FILE)

product_url_pattern = re.compile(r'^/products/(\d+)$')

def handle_request(client_socket):
   request_data = client_socket.recv(1024).decode('utf-8')
   print(f"Received Request:\n{request_data}")

   request_lines = request_data.split('\n')
   request_line = request_lines[0].strip().split()
   method = request_line[0]
   path = request_line[1]

   response_content = ''
   status_code = 200

   if path == '/':
      with open('home.html', 'r') as home:
         response_content = home.read()
   elif path == '/about':
      with open('about.html', 'r') as about:
         response_content = about.read()
   elif path == '/products':
      with open('products.html', 'r') as products:
         response_content = products.read()
   else:
      match = product_url_pattern.match(path)
      if match:
         product_id = int(match.group(1))
         if 0 <= product_id < len(product_details):
            product = product_details[product_id]
            response_content = f"""
            <p>{product['name']}</p>
            <p>Author: {product['author']}</p>
            <p>Price: {product['price']}</p>
            <p>Description: {product['description']}</p>
            """
         else:
            response_content = '404 Not Found'
            status_code = 404
      else:
         response_content = '404 Not Found'
         status_code = 404

   response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
   client_socket.send(response.encode('utf-8'))

   client_socket.close()


def signal_handler(sig, frame):
   print("\nShutting down the server...")
   server_socket.close()
   sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
   client_socket, client_address = server_socket.accept()
   print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

   client_handler = threading.Thread(target=handle_request, args=(client_socket,))
   client_handler.start()
