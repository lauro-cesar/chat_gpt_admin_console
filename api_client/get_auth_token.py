import requests
import os 

url ="https://aidata.ewinfo.com.br/api-token-auth/"

requestBody ={
    "username":"api",
    "password":""
}

authtoken =  requests.post(url,json=requestBody)

print(authtoken.json())