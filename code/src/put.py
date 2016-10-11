
# only requested asynchronously by import.js

import requests

def store(endpoint,data):

    # copied and trimmed from course tutorial

    transaction_begin_url = endpoint + '/transaction/begin'

    # Start the transaction, and get a transaction_id

    response = requests.post(transaction_begin_url,headers={'Accept': 'text/plain'})
    transaction_id = response.content

    # POST the data to the transaction

    post_url = endpoint + '/' + transaction_id + '/add'
    response = requests.post(post_url, data=data,headers={'Accept': 'text/plain','Content-type': 'text/turtle'})

    if response.status_code != 200: return str(response.content)

    transaction_close_url = endpoint + '/transaction/commit/' + transaction_id
    response = requests.post(transaction_close_url)

    if response.status_code != 200: return str(response.content)
    else: return 'Ok!'