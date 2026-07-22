'''
    Application that implements a habit tracker connected to Pixela API. Requires a venv
    for requests. This lesson follows day 37, where I learned about HTTP requests:
        - GET - fetch data from the server
        - POST - write data to the server w/o worrying about return data
        - PUT - update existing data on the server
        - DELETE - remove data on the server
'''

import os

import requests
import datetime

USERNAME = os.environ.get("USERNAME")
TOKEN = os.environ.get("TOKEN")
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# ------- Create user account
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

# ------- Create a reading graph
# graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

# graph_config = {
#     "id": "graph1",
#     "name": "Reading Graph",
#     "unit": "pages",
#     "type": "int",
#     "color": "ajisai"
# }

# headers = {
#     "X-USER-TOKEN": TOKEN
# }

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

# ----------- Post a pixel to the graph

post_endpoint = "https://pixe.la/v1/users"

graph_config = {
    "id": GRAPH_ID,
    "name": "Reading Graph",
    "unit": "pages",
    "type": "int",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

params = {
    "date": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"),
    "quantity": "10",
}

# response = requests.post(url=f"{post_endpoint}/{USERNAME}/graphs/{graph_config['id']}", json=params, headers=headers)
# print(response.text)

put_params = {
    "quantity": "20"
}

date_to_update = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
update_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date_to_update}"

# Make "put" request to update yesterday's reading pages quantity
# response = requests.put(url=update_pixel_endpoint, json=put_params, headers=headers)
# print(response.text)

# Delete today's pixel data using "delete" request
response = requests.delete(url=update_pixel_endpoint, json=None, headers=headers)
print(response.text)
