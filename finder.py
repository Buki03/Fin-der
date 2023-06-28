import requests
import pprint

# API KEY + requests
api = 'sDf70ANa1m7mGGYOBzj16IfL2suTebt4tv37UVYE'
in_ad = input() #input adress
ipaddress = in_ad.replace(':', '%3A')
url = 'https://api.ipbase.com/v2/info?apikey=' + api + '&ip=' + ipaddress
response = requests.get(url).json()

# Printing user's location
# user_loc = response["data"]["location"]["city"]["name"]
pprint.pprint(response["data"]["location"]["city"]["name"])

# Converting To Dataframe