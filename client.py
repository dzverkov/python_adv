import yaml
import json
from argparse import ArgumentParser
import socket
from datetime import datetime

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='Sets config file path'
)

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

    action = input('Enter action: ')
    data = input('Enter message: ')

    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }

    str_request = json.dumps(request)

    sock.send(str_request.encode())

    print(f'Client send data: {data}')

    b_response = sock.recv(buffer_size)
    print(f'Server send data: {b_response.decode()}')

except KeyboardInterrupt:
    print('Client shutdown')