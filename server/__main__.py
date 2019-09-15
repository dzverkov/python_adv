import yaml
from argparse import ArgumentParser
import socket
import json
import logging
import select
import threading

from handlers import handle_default_request

def read(sock, connections, requests, buffersize):
    try:
        bytes_request = sock.recv(buffersize)
    except Exception:
        connections.remove(sock)
    else:
        requests.append(bytes_request)


def write(sock, connections, response):
    try:
        sock.send(response)
    except Exception:
        connections.remove(sock)


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

requests = []
connections = []

host, port = config.get('host'), config.get('port')
max_clients = config.get('max_clients')
buffer_size = config.get('buffer_size')

try:

    sock = socket.socket()
    sock.bind((host, port))
    sock.setblocking(False)
    sock.settimeout(0)
    sock.listen(max_clients)

    logging.info(f'Server started with {host}:{port}')

    while True:
        try:
            client, cl_adr = sock.accept()
            connections.append(client)
            logging.info(f'Client was detected {cl_adr[0]}:{cl_adr[1]}')
        except:
            pass

        if connections:
            rlist, wlist, xlist = select.select(
                connections, connections, connections, 0
            )

            for read_client in rlist:
                read_thread = threading.Thread(
                    target=read,
                    args=(read_client, connections, requests, buffer_size)
                )
                read_thread.start()

            if requests:
                bytes_request = requests.pop()
                bytes_response = handle_default_request(bytes_request)

                for write_client in wlist:
                    write_thread = threading.Thread(
                        target=write,
                        args=(write_client, connections, bytes_response)
                    )
                    write_thread.start()

except KeyboardInterrupt:
    print('Server shutdown.')
