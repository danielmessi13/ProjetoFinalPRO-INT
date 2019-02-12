import requests

# id = ''
#
# for i in requests.get('http://apiadvisor.climatempo.com.br/api/v1/locale/city?name=Teresina&token=2a691966e8904c5a99c6e582564ee847').json():
#     id = i['id']
#
#
# json_clima = requests.get('http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/'+str(id)+'/days/15?token=2a691966e8904c5a99c6e582564ee847').json()
#
# print(json_clima['data'][0]['temperature']['min'])
# print(json_clima['data'][0]['temperature']['max'])
# print(json_clima['data'][0]['text_icon']['text']['pt'])


cidades = []


api_cidades = requests.get('http://apiadvisor.climatempo.com.br/api/v1/locale/city?state=PI&token=2a691966e8904c5a99c6e582564ee847')
print(api_cidades.status_code)
# for i in api_cidades:
#     cidades.append(i['name'])

print(cidades)
