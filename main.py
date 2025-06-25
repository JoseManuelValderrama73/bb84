from emisor import Emisor
from receptor import Receptor
import asyncio

async def servidor(puerto: int):
    servidor = Receptor(puerto)
    await servidor.start()

async def cliente(msg: str, N: int, host: str, port: int):
    cliente = Emisor(msg, N, host, port)
    await cliente.run()

opcion = int(input("Escuchar mensajes (1)\nEnviar mensaje (2)"))
if opcion == 1:
    asyncio.run(servidor(
        puerto=int(input("Puerto a escuchar: "))
    ))
elif opcion == 2:
    asyncio.run(cliente(
        msg=input("Mensaje a enviar: "),
        N=int(input("Número de valores de seguridad: ")),
        host=input("Host del receptor: "),
        port=int(input("Puerto del receptor: "))
    ))
else:
    print("Opción no válida")
