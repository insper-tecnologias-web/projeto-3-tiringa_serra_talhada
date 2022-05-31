import requests  
from bs4 import BeautifulSoup  
    
def getdata(url):  
    r = requests.get(url)  
    return r.text  

htmldata = getdata("https://www.lelloimoveis.com.br/venda/residencial/1-pagina/")  
soup = BeautifulSoup(htmldata, 'html.parser')  
for item in soup.find_all('img'): 
    item['src']
print(item['src'])