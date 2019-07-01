import asyncio
import json

class Protocol:
    async def router_protocol(self, jd, r, w):
        if jd['action'] == "first_connect":
            self.add_writer(jd, r, w)
        else:
            print('else')



    async def write_socks_protocol_first(self, w):
        w.write("first_conect_protocol".encode('utf-8'))
        await w.drain()
