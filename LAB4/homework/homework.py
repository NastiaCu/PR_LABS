import socket
from bs4 import BeautifulSoup
import json

HOST = '127.0.0.1'
PORT = 8080

def send_request(path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    request = f'GET {path} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n'
    client_socket.send(request.encode('utf-8'))

    response = b''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    client_socket.close()
    return response.decode('utf-8')

def parse_static_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    h1_content = soup.find('h1').text
    paragraphs = soup.find_all('p')
    p_contents = [p.text for p in paragraphs]
    return {'title': h1_content, 'paragraphs': p_contents, 'html_content': page_content}

def scrape_static_pages():
    home_page_content = send_request('/')
    about_page_content = send_request('/about')
    products_page_content = send_request('/products')  

    home_content = parse_static_page(home_page_content)
    about_content = parse_static_page(about_page_content)
    products_content = parse_static_page(products_page_content)

    data = {
        'home': home_content,
        'about': about_content,
        'products': products_content
    }

    return data

def scrape_product_details(product_id):
    product_path = f'/products/{product_id}'
    product_page_content = send_request(product_path)
    product_data = parse_product_page(product_page_content, product_path)
    if product_data:
        product_filename = f'product_{product_id}.json'
        with open(product_filename, 'w', encoding='utf-8') as product_file:
            json.dump(product_data, product_file, indent=4, ensure_ascii=False)

def parse_product_page(page_content, page_path):
    soup = BeautifulSoup(page_content, 'html.parser')
    
    if page_path.startswith('/products/'):
        name = soup.find_all('p')[0].text.strip()
        author = soup.find_all('p')[1].text.strip().replace('Author: ', '')
        price = soup.find_all('p')[2].text.strip().replace('Price: ', '')
        description = soup.find_all('p')[3].text.strip().replace('Description: ', '')
        
        product_data = {
            'name': name,
            'author': author,
            'price': float(price),  
            'description': description
        }

        return product_data

    return None

if __name__ == '__main__':
    static_page_data = scrape_static_pages()

    for page_name, page_data in static_page_data.items():
        with open(f'saved_{page_name}.html', 'w', encoding='utf-8') as html_file:
            html_file.write(page_data['html_content'])

    for product_id in range(2):  
        scrape_product_details(product_id)
