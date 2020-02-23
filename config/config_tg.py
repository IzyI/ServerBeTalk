from dataclasses import dataclass


@dataclass(order=True)
class ConfTg:
    # Тестовые конфиги
    proxy = ['205.204.87.43', '205.204.87.23']
    proxy_port: int = 1490
    proxy_login='suka'
    proxy_password='vneq9t4DSW3d'
    phone: str = '234234535'
    id: int = 217542
    hash: str = '32d95beedc85b2a078147e9ac2d4c6ac'
