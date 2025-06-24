from emisor import Emisor
from receptor import Receptor
import asyncio

async def main():
    atob = asyncio.Queue()
    btoa = asyncio.Queue()
    e = Emisor("jose manuel", 5, atob, btoa)
    r = Receptor(5, atob, btoa)
    tareaEmisor = asyncio.create_task(e.run())
    tareaReceptor = asyncio.create_task(r.run())
    await asyncio.gather(tareaEmisor, tareaReceptor)

asyncio.run(main())