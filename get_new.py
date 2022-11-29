import requests
from bs4 import BeautifulSoup as bs
import pickle

url = "https://www.countryipblocks.net/acl.php"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'}
payload = {'countries[]': 'AR', 'format1': '1', 'get_acl': 'Create+ACL'}

pagina = requests.post(url,data=payload,headers=headers)

sopa = bs(pagina.content)

texto = sopa.find(id="textareaAll").text

listado = texto.replace(" ","").split("\n")

with open('old','rb') as handle:
    actual = pickle.load(handle)

if not listado == actual:
    print(f"NO SON IGUALES -> {len(listado)} vs {len(actual)}")
    for x in actual:
        if not x in listado:
            print(x, "nose encuentra")

    with open('old','wb') as handle:
        pickle.dump(listado,handle)
        
else:
    print(f"SI SON IGUALES -> {len(listado)} vs {len(actual)}")
