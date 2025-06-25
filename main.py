from emisor import Emisor
from receptor import Receptor
import asyncio
from kernel import CommunicationManager

async def run_client():
    comm = CommunicationManager("client", "192.168.1.50", 8888)
    await comm.start()

    await comm.send("Hello from A!")
    response = await comm.receive()
    print("[A] Got:", response)

    await comm.close()

async def run_server():
    server = Receptor(10, 8888)
    await server.start()

if input("Run server? (y/n): ").strip().lower() == 'y':
    asyncio.run(run_server())
else:
    asyncio.run(run_client())
