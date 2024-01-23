import requests
from bs4 import BeautifulSoup

URL = 'https://www.imdb.com/calendar/?region=MX'

#obtener html
#. si el archivo no existe crarlo
#- si existe obtener su contenido
#obtener informacion
#generar archivo csv

def get_imdb_content():
    headers = {
        'User-Agent' : 'Mozila/5.0'
    }
    
    response = requests.get(URL, headers = headers)
    #ahora obtenemos el maquetado y demas
    print(response.status_code)
    
    if response.status_code == 200:
        return response.text
    
    return None
    
def create_imdb_file_local(content):
    try:
        with open('imdb.html', 'w') as file:
            file.write(content)
    except:
        pass

def get_imdb_file_local():
    content = None
    try:
        with open('imdb.html', 'r') as file:
            content = file.read()
    except:
        pass

    return content

def get_local_imdb_content():
    content = get_imdb_file_local()
    
    if content:
        return content
    
    content = get_imdb_content()
    create_imdb_file_local(content)
    
    return content

def main():
    content = get_local_imdb_content()
    print(content)
    
    
if __name__ == '__main__':
    main()
