from NB import NB
from vocab import Vocab

import socket
import os
import torch
import json

# Constants

BUFF_SIZE = 16384       # 16kb, assume probably nothing exceeds this.
FAKE_NEWS_PORT = 5000   # just some random 4 numbers port that nobody uses anyways

# Generate predictor (NB)

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(SCRIPT_PATH, 'training_dataset')
TRUE_FILE = os.path.join(SCRIPT_PATH, 'True.csv')
FAKE_FILE = os.path.join(SCRIPT_PATH, 'Fake.csv')

vocab = Vocab(true_file= TRUE_FILE, fake_file= FAKE_FILE, active_words_count= 2000)
x, y = vocab.get_training_data()
predictor = NB(x= torch.tensor(x), y= torch.tensor(y), k= 2)

# Create a TCP socket binding to port 5000, only listen to localhost.

server_sock = socket.socket(socket.AddressFamily.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('localhost', FAKE_NEWS_PORT))

server_sock.listen(1)
print('--------listening--------')
while True:
    comm, _ = server_sock.accept()
    
    def send_json(jsonable):
        comm.send((json.dumps(jsonable) + '\n').encode())
     
    print('--------accepted connection--------')

    # NOTE: assume BUFF_SIZE is probably enough, but
    # if message grows in size, we probably need to have
    # a function that takes in chunks.
    data = comm.recv(BUFF_SIZE)
    if not data:
        comm.close()
        break
    try:
        news = json.loads(data)
    except json.JSONDecodeError:
        send_json({'status': 'error', 'error': 'malformed json object received'})
        continue
        
    # send {'status': 'ok', 'result': 'real' or 'fake'}
    if news['func'] == 'predict_real_fake':
        if 'title' not in news or 'text' not in news:
            send_json({
                'status': 'error',
                'error': 'title or/and text key not in json for prediction'
            })

        else:
            res = predictor.predict(torch.tensor(vocab.get_parameter(news)))
            send_json({
                'status': 'ok',
                'result': 'real' if res == 0 else 'fake',
            })

    comm.close()
    print('--------closed connection--------')

