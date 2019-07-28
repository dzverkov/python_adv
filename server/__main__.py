import yaml
from argparse import ArgumentParser
import socket
import json

from protocol import validate_request, make_responce

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
max_clients = config.get('max_clients')
buffer_size = config.get('buffer_size')
try:

    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(max_clients)

    print(f'Server started with {host}:{port}')

    while True:
        client, cl_adr = sock.accept()
        print(f'Client was detected {cl_adr[0]}:{cl_adr[1]}')

        b_req = client.recv(buffer_size)

        request = json.loads(b_req.decode())

        if validate_request(request):
            print(f'Client send valid request {request}')
            responce = make_responce(request, 200, data=request.get('data'))
        else:
            responce = make_responce(request, 404, 'Wrong request')
            print(f'Client send invalid request {request}')

        str_responce = json.dumps(responce)
        client.send(str_responce.encode())

        client.close()

except KeyboardInterrupt:
    print('Server shutdown')