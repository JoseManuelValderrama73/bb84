from emisor import Emisor
from receptor import Receptor
import asyncio
from kernel import CommunicationManager

async def servidor():
    servidor = Receptor(10, 8888)
    await servidor.start()

async def cliente():
    cliente = Emisor("Hello, World!", 10, "192.168.1.50", 8888)
    await cliente.run()

if input("Run server? (y/n): ").strip().lower() == 'y':
    asyncio.run(servidor())
else:
    asyncio.run(cliente())
