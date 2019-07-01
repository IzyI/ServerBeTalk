from dataclasses import dataclass


@dataclass(order=True)
class ConfTg:
    # Тестовые конфиги
    # curl -v -x socks5://suka:vneq9t4DSW3d@205.204.87.15:1490 http://2ip.ru
    proxy = ['205.204.87.15', '205.204.87.15']
    proxy_port: int = 1490
    proxy_login='suka'
    proxy_password='vneq9t4DSW3d'
    phone: str = '79293621775'
    id: int = 217542
    hash: str = '32d95beedc85b2a078147e9ac2d4c6ac'
