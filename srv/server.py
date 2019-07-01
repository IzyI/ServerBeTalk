import logging
import struct
import helper as hp
import json
import asyncio
from . import Protocol, User, Postman, ClientConsole, BD_PSQL
import time
import  traceback

class Server(Protocol, User, Postman, ClientConsole, BD_PSQL):
    def __init__(self, config):
        super().__init__()
        self.user_list = list()
        self.protocol_list = list()
        self.postman_list = dict()
        self.pool = False
        self.config = config

    async def handle( self,reader, writer):
        while True:
            try:
                data = await self.readmsg(reader, writer)
                if data == "pong":
                    continue

                await self.router(data, reader, writer)
            except asyncio.TimeoutError:
                print('timeout!')
                break
            except ConnectionResetError:
                print("ConnectionResetError")
                break
            except asyncio.IncompleteReadError:
                print("IncompleteReadError")
                break

            except Exception as e:
                print("Error handle: " + str(e))
                traceback.print_exc()
                # exit()

        self.del_writer(writer)
        writer.close()
        await writer.wait_closed()

    async def main(self):

        s = await asyncio.start_server(
            self.handle, '', 9990, limit=20480)
        addr = s.sockets[0].getsockname()
        print(f'Serving on {addr}')
        async with s:
            await s.serve_forever()


    async def readmsg(self,r, w):
        d = await asyncio.wait_for(r.readexactly(4), timeout=30)
        d = struct.unpack('>I', d)[0]
        d = await asyncio.wait_for(r.readexactly(d), timeout=30)
        d = d.decode("utf-8")
        if d == "ping":
            w.write(struct.pack('>I', 4) + 'pong'.encode("utf-8"))
            await w.drain()
            return "pong"
        return d

    async def check_connect_bd(self):
        if not self.pool:
            await self.create_conn()
            if not self.pool:
                print("закрываю сервер так как не смог подключится к бд")
                exit()
            self.pool = False
        print(self.pool)

    async def router(self, data, r, w):

        await self.check_connect_bd()
        json_data = json.loads(data)

        if json_data['type'] == "protocol":
            await self.router_protocol(json_data, r, w)
        elif json_data['type'] == "user":
            await self.router_user(json_data, r, w)
        elif json_data['type'] == "console_client":
            await self.router_client_console(json_data, r, w)
        elif json_data['type'] == "postman":
            await self.router_postman(json_data, r, w)
        else:
            ...

    def add_writer(self, jd, r, w):

        n = {"addres": w.get_extra_info('peername'), "name": jd['name'], "account": jd['account'], 'writer': w}
        if jd['type']=='protocol':
            self.protocol_list.append(n)
            print("Добавил protocol: "+jd['name']+" account: "+jd['account'])
        else:
            self.user_list.append(n)
            print("Добавил user: " + jd['name'] + " account: " + jd['account'])


    def del_writer(self, w):
        try:
            addres=w.get_extra_info('peername')
            print(f"del_writer: {addres}")
            for i in range(len(self.protocol_list)):
                if addres == self.protocol_list[i]['addres']:
                    del_e=self.protocol_list.pop(i)
                    print("Удалил protocol: "+del_e['name']+" account: "+del_e['account']+" addres:"+str(del_e['addres']))
                    return
            for i in range(len(self.user_list)):
                if addres == self.user_list[i]['addres']:
                    del_e=self.user_list.pop(i)
                    print("Удалил user: "+del_e['name']+" account: "+del_e['account']+" addres:"+str(del_e['addres']))
                    return
            print("ненашел writer "+str(addres)+"в protocol_list user_list")
        except Exception as e:
            traceback.print_exc()
            print("несмог получить адрес во writer: "+str(e))

    async def sending(self,write,msg):
        if not isinstance(msg, bytes):
            if not isinstance(msg, str):
                msg = str(msg)
            msg = msg.encode('utf-8')
        msg = struct.pack('>I', len(msg)) + msg
        write.write(msg)
        await write.drain()
