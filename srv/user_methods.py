import asyncio
import json

class User:
    async def router_user(self,jd, r, w):
        if jd['action']=='first_connect':
            if self.__add_user(jd, w, r):
                print("first_conect_user", self.user_list)
                await self.sending(w,json.dumps({"first_conect_user":True}))
        else:
            ...

    def __auth_user(self, password, login):
        #  TODO: переделать в хешину и сделать  аунтефикацию
        return True

    def __check_once_user(self, name):
        if name in self.user_list:
            return False
        else:
            return True


    def __add_user(self, jd, w, r):
        if self.__auth_user(jd['password'], jd['login']) and self.__check_once_user(jd['name']):
            self.user_list[jd['name']] = [w.get_extra_info('peername'), r, w]
            return True
        print("Not auth: "+str(jd))
        return False