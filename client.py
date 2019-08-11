import zlib
import yaml
import json
from argparse import ArgumentParser
import socket
from datetime import datetime
import threading

WRITE_MODE = 'write'
READ_MODE = 'read'


def read(sock, buffersize):
    while True:
        response = sock.recv(buffersize)
        bytes_response = zlib.decompress(response)
        print(f'Server send data: {bytes_response.decode()}')


def make_request(action, data):
    return {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='Sets config file path'
)

# parser.add_argument(
#     '-m', '--mode', type=str, required=False, default=WRITE_MODE,
#     help='Sets client mode'
# )

args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8000,
    'buffer_size': 1024,
    'max_clients': 10
}

if args.config:
    with open(args.config) as f:
        file_config = yaml.load(f, Loader=yaml.Loader)
        config.update(file_config)

host, port = config.get('host'), config.get('port')
buffer_size = config.get('buffer_size')

try:
    sock = socket.socket()
    sock.connect((host, port))
    print('Client was started.')

    read_thread = threading.Thread(
        target=read,
        args=(sock, buffer_size)
    )
    read_thread.start()

    while True:
        action = input('Enter action: ')
        data = input('Enter message: ')

        request = make_request(action, data)
        str_request = json.dumps(request)
        bytes_request = zlib.compress(str_request.encode())

        sock.send(bytes_request)
        print(f'Client send data: {data}')


except KeyboardInterrupt:
    print('Client shutdown')