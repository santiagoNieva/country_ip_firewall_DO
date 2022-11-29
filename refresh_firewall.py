import requests
import pickle

token = 'dop_v1_718154e5889255f84cbacea37f58e4842f183d75719b0860ee772d10d3deba78'
id_firewall = 'a5ccdf94-a387-441a-bee8-e5f4afb34cbd'

headers = {
    'Content-Type':'application/json',
    'Authorization': f'Bearer {token}'
}

url_get = f"https://api.digitalocean.com/v2/firewalls/{id_firewall}"
url_post = f"https://api.digitalocean.com/v2/firewalls/{id_firewall}/rules"

probando = requests.get(url_get,headers=headers)

print(probando.content)

with open('old','rb') as handle:
    listado = pickle.load(handle)

cant_reglas = len(listado) // 1000
i = 0
while i <= cant_reglas:
    listado_1000 = listado[(i*1000):(i+1)*1000]
    puerto = 80
    data = {
        "inbound_rules":[
            {
                "protocol":"tcp",
                "ports":puerto,
                "sources":{
                    "addresses":listado_1000
                }
            }
        ]
    }
    enviando = requests.post(url_post, json=data, headers=headers)
    print(f"i={i} 80 - {enviando.content}")

    puerto = 443
    data = {
        "inbound_rules":[
            {
                "protocol":"tcp",
                "ports":puerto,
                "sources":{
                    "addresses":listado_1000
                }
            }
        ]
    }
    enviando = requests.post(url_post, json=data, headers=headers)
    print(f"i={i} 443 - {enviando.content}")

    i += 1


