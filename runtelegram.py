from protocols import  TelegramProtocol
from config import ConfTg

client = TelegramProtocol(ConfTg.phone, ConfTg.id, ConfTg.hash, proxy=proxy)
client.start(phone=ConfTg.phone)
client.create_my_task()
client.run_until_disconnected()