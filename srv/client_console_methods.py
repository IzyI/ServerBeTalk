import asyncio
import json
import copy
class ClientConsole:
    async def router_client_console(self, jd, r, w):
        if jd['action'] == "get_connect_list":
            if self.__auth(w):
                protocol_listcopy = []
                for i in self.protocol_list:
                    s=dict(i)
                    s.pop('writer')
                    protocol_listcopy.append(s)
                #  TODO: сделать для self.user_list свой копир
                user_listcopy=self.user_list
                json_data={"user_list":str(user_listcopy),"protocol_list":protocol_listcopy}
                print('get_info_list')
                await self.sending(w, json.dumps(json_data))
        else:
            ...

    def __auth(self,w):
        #  TODO: переделать в зависимости от  текущего сервера
        return True

