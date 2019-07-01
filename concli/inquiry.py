import socket
import threading
import yaml
import sys
import requests
import helper
import logging
import struct
import json
import time
import click
from  config import ConfConCli
from pprint import pprint
class Client(socket.socket):
    def __init__(self,  ip, port):
        socket.socket.__init__(self)
        # self.api_session = requests.Session()
        # self.api_session.auth = (config.x_id, config.x_key)
        # self.config = config
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.logger = logging.getLogger(__name__)
        self.sock.connect((self.ip, self.port))

    def sending(self, msg):
        if not isinstance(msg, bytes):
            if not isinstance(msg, str):
                msg = str(msg)
            msg = msg.encode('utf-8')
        msg = struct.pack('>I', len(msg)) + msg
        self.sock.send(msg)

    def read(self):
        leng_data= struct.unpack('>I', self.sock.recv(4))[0]
        data=self.sock.recv(leng_data)
        data = data.decode('utf-8')

        try:
            return json.loads(data)
        except:
            return data

    def close(self):
        self.sock.close()

@click.group()
@click.option('-host', default="localhost", help='Хост')
@click.option('-port', default=9990, help='Порт')
@click.pass_context
def cli(ctx,host,port):
    ctx.ensure_object(dict)
    ctx.obj['Client'] = Client
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    pass


@click.command()
@click.option('-name', default=ConfConCli.name, help='имя')
@click.pass_context
def first_connect(ctx,name):
    client=ctx.obj['Client'](ctx.obj['host'],int(ctx.obj['port']))
    msg = json.dumps({"action": "first_connect",
                      "type": "user",
                      "name": name,
                      "login": name,
                      "password": "фиауа3й4рпайцзу7амфывСВ%;ччв5634у"})
    client.sending(msg)
    result = client.read()
    print(result)
    client.close()


@click.command()
@click.pass_context
def get_connect_list(ctx):
    client=ctx.obj['Client'](ctx.obj['host'],int(ctx.obj['port']))
    msg = json.dumps({"action": "get_connect_list",
                      "type": "console_client"})
    client.sending(msg)
    result = client.read()
    print(result)
    client.close()



cli.add_command(first_connect)
cli.add_command(get_connect_list)

if __name__ == '__main__':
    cli()
