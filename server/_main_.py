import yaml
from argparse import ArgumentParser
import socket

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
        print(f'Client send message: {b_req.decode()}')
        client.send(b_req)
        client.close()

except KeyboardInterrupt:
    print('Server shutdown')