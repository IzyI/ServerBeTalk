from telethon.sync import TelegramClient
import socks
import json
from config import ConfTg
import asyncio
import concurrent.futures
import struct
import traceback
from telethon import functions, types, events
from telethon.tl.types import UpdateShortMessage, InputPhoneContact, UpdateNewMessage, UserStatusOffline, \
    UserStatusOnline, UpdateUserStatus

proxy = (socks.SOCKS5, ConfTg.proxy[0], ConfTg.proxy_port, True, ConfTg.proxy_login, ConfTg.proxy_password)


class TelegramProtocol(TelegramClient):
    def __init__(self, phone, api_id, api_hash, proxy=None):
        super().__init__(phone, api_id, api_hash, proxy=proxy)
        self.add_event_handler(self.my_event_handler_Test, events.NewMessage)
        self.reader, self.writer = None, None
        self.current_account=phone
        self.loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=1))

    async def readmsg(self):
        d = await asyncio.wait_for(self.reader.readexactly(4), timeout=30)
        d = struct.unpack('>I', d)[0]
        d = await asyncio.wait_for(self.reader.readexactly(d), timeout=30)
        d = d.decode("utf-8")
        if d == "pong":
            return "pong"
        return d

    async def sending(self,msg):
        if not isinstance(msg, bytes):
            if not isinstance(msg, str):
                msg = str(msg)
            msg = msg.encode('utf-8')
        msg = struct.pack('>I', len(msg)) + msg
        self.writer.write(msg)
        await self.writer.drain()

    def create_first_msg(self,result):
        data = {'action': 'first_connect', 'type': 'protocol', 'name': 'telegram', 'account': self.current_account}
        contacts = []
        user = dict()
        for i in result:
            ien = i.entity
            if i.is_user and not ien.bot:
                user['id_user'] = i.id
                user['nickname'] = i.name
                info = dict()
                if ien.username:
                    info['username'] = ien.username
                if ien.phone:
                    info['phone'] = ien.phone
                if ien.lang_code:
                    info['phone'] = ien.lang_code
                if info:
                    user['info'] = info
                user['status'] = True if isinstance(ien.status, UserStatusOnline) else False
                contacts.append(user)
        data["data"] = contacts

        return data

    async def close_tcp_client(self):
        print(self.writer)
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.reader, self.writer = None, None
            print("Закрыл TCP клиент")

    async def tcp_client_start(self):
        while True:
            try:
                self.reader, self.writer = await asyncio.open_connection('localhost', 9990)
            except OSError as e:
                print("OSError : tcp_client_start")
                await asyncio.sleep(5)
                continue


            try:
                data=dict()
                result=await self.get_dialogs()
                data=self.create_first_msg(result)
                await self.sending(json.dumps(data))
                # await self.sending(data)
            except :
                traceback.print_exc()
                print("Не отправил первое сообщение: "+str(data))
                await self.close_tcp_client()
                continue



            while True:
                try:
                    data = await self.readmsg()
                    print("DATA <<<:  "+str(data)+"\n")
                    if data == "pong":
                        continue
                except asyncio.TimeoutError:
                    print("asyncio.TimeoutError")
                    break
                except ConnectionResetError:
                    print("ConnectionResetError")
                    break
                except asyncio.IncompleteReadError:
                    print("asyncio.IncompleteReadError")
                    break
                # except Exception as e:
                #     SERVER.logger.error("Error handle: " + str(e))
                #     break


            await self.close_tcp_client()

    async def my_event_handler_Test(self, event):
        if 'hello' in event.raw_text:
            self.writer.write(struct.pack('>I', 5) + 'hello'.encode("utf-8"))
            await event.reply('hi!')

    async def ping(self):
        while True:
            await asyncio.sleep(28)
            try:
                if self.writer:
                    self.writer.write(struct.pack('>I', 4) + 'ping'.encode("utf-8"))
                    print("good ping")
            except Exception as e:
                print("bad ping")
                print(e)

    def create_my_task(self):
        self.loop.create_task(self.tcp_client_start())
        self.loop.create_task(self.ping())
        ...


client = TelegramProtocol(ConfTg.phone, ConfTg.id, ConfTg.hash, proxy=proxy)

client.start(phone=ConfTg.phone)
client.create_my_task()
client.run_until_disconnected()
