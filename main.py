from emisor import Emisor
from receptor import Receptor
import asyncio
from kernel import CommunicationManager

async def run_client():
    comm = CommunicationManager(mode="client", host="192.168.1.50", port=8888)
    await comm.start()

    await comm.send("Hello from A!")
    response = await comm.receive()
    print("[A] Got:", response)

    await comm.close()

class Server(CommunicationManager):
    async def on_ready(self):
        msg = await self.receive()
        print("[B] Received:", msg)
        await self.send("Hello from B!")

async def run_server():
    server = Server(mode="server", host="0.0.0.0", port=8888)
    await server.start()
"""
async def run_server():
    server = Emisor("hola mundo", 10, '0.0.0.0', 8888)
    await server.start()
"""

if input("Run server? (y/n): ").strip().lower() == 'y':
    asyncio.run(run_server())
else:
    asyncio.run(run_client())
