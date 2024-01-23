import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://www.imdb.com/calendar/?region=MX'

#obtener html
#. si el archivo no existe crarlo
#- si existe obtener su contenido
#obtener informacion
# - nombre
# - categorias 
# - repartos
#generar archivo csv

def get_imdb_content():
    headers = {
        'User-Agent' : 'Mozilla/5.0'
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

def create_movie(tag):
    main_div = tag.find('div', {'class' : 'ipc-metadata-list-summary-item__c'})
        
    name =  main_div.div.a.text
    ul_categories = main_div.find('ul', {
        'class' : 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base'
    })
        
    ul_cast = main_div.find('ul', {
        'class' : 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base'
    })
       
    casts = None 
    categories = [category.span.text for category in ul_categories.find_all('li')]
    
    if ul_cast:
        casts = [cast.span.text for cast in ul_cast.find_all('li')]

    return (name, categories, casts)

def main():
    content = get_local_imdb_content()
    
    soup = BeautifulSoup(content, 'html.parser')
   
    li_tags = soup.find_all('li', {
        'data-testid': 'coming-soon-entry',
        'class': 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 eWVqBf'
    })
    
    
    movies = []
    for tag in li_tags:
        movie = create_movie(tag)   
        movies.append(movie)
           
    with open('movies.csv', 'w') as file:
        writer = csv.writer(file, delimiter="-")
        writer.writerow(['name','categories','cast'])
        
        for movie in movies:
            writer.writerow([
                movie[0],
                ",".join(movie[1]),
                ",".join(movie[2]),
            ])
           
if __name__ == '__main__':
    main()
