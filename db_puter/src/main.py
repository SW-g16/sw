import requests
import time
from flask import Flask, request

import constants as c

app = Flask(__name__)


global num_requests
num_requests=0

global start_time
start_time = time.time()

import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

INTERVAL = 30

def terminal_update():

    global num_requests
    print 'received', num_requests,'requests in the last %d seconds' % INTERVAL
    num_requests = 0

set_interval(terminal_update,INTERVAL)

@app.route('/store', methods=['POST'])
def store():

    # copied and trimmed from course tutorial

    global num_requests
    num_requests +=1

    endpoint = c.ENDPOINT
    data = request.form['data'].encode('utf-8')

    #print data

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


if __name__ == '__main__':
    app.debug = True
    app.run()
