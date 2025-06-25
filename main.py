from emisor import Emisor
from receptor import Receptor
import asyncio

async def servidor(puerto: int):
    servidor = Receptor(puerto)
    await servidor.start()

async def cliente(msg: str, N: int, host: str, port: int):
    cliente = Emisor(msg, N, host, port)
    await cliente.run()

opcion = int(input("Escuchar mensajes (1)\nEnviar mensaje (2)\n-> "))
if opcion == 1:
    puerto=int(input("Puerto a escuchar: "))
    asyncio.run(servidor(puerto))
elif opcion == 2:
    msg=input("Mensaje a enviar: "),
    n=int(input("Número de bits de seguridad: ")),
    host=input("Host del receptor: "),
    port=int(input("Puerto del receptor: "))
    asyncio.run(cliente(msg, n, host, port))
else:
    print("Opción no válida")
