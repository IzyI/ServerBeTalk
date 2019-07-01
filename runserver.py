import asyncio
import time
from srv import Server
from config import ConfServer
import helper as hp
import logging
import struct
import traceback



config = ConfServer()
SERVER = Server(config)




if __name__ == "__main__":
    asyncio.run(SERVER.main())
