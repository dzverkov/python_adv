import yaml
from argparse import ArgumentParser
import socket
import json
import logging

from actions import resolve
from protocol import validate_request, make_response

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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)

host, port = config.get('host'), config.get('port')
max_clients = config.get('max_clients')
buffer_size = config.get('buffer_size')
try:

    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(max_clients)

    logging.info( f'Server started with {host}:{port}')

    while True:
        client, cl_adr = sock.accept()
        logging.info(f'Client was detected {cl_adr[0]}:{cl_adr[1]}')

        b_req = client.recv(buffer_size)

        request = json.loads(b_req.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    logging.info(f'Client send valid request {request}')
                    response = controller(request)
                except Exception as err:
                    logging.critical(f'Internal server error {err}')
                    response = make_response(request, 500, 'Internal server error')
            else:
                logging.error(f'Controller with action name {action_name} does not exists')
                response = make_response(request, 404, 'Wrong request')
        else:
            logging.error(f'Client send invalid request {request}')
            response = make_response(request, 404, 'Wrong request')

        str_response = json.dumps(response)
        client.send(str_response.encode())

        client.close()

except KeyboardInterrupt:
    print('Server shutdown')
