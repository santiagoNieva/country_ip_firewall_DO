import requests
import pickle
import envs

token = envs.token
id_firewall = envs.id_firewall

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


