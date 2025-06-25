from emisor import Emisor
from receptor import Receptor
import asyncio
from kernel import printerr

async def servidor(puerto: int):
    servidor = Receptor(puerto)
    await servidor.start()

async def cliente(msg: str, N: int, host: str, port: int):
    cliente = Emisor(msg, N, host, port)
    await cliente.run()

opcion = int(input("Escuchar mensajes (1)\nEnviar mensaje (2)\n-> "))
if opcion == 1:
    asyncio.run(servidor(
        int(input("Puerto a escuchar: "))
    ))
elif opcion == 2:
    host = input("Host del receptor: ")
    port = int(input("Puerto del receptor: "))

    msg = input("Mensaje a enviar: ")
    while msg == "":
        printerr('El mensaje no puede estar vacío.')
        msg = input("Mensaje a enviar: ")

    n = int(input("Número de bits de seguridad: "))
    while n < 1:
        printerr('El número de bits de seguridad debe ser mayor que 0.')
        n = int(input("Número de bits de seguridad: "))
    if n > len(msg):
        print('El numero de bits de seguridad no debe ser demasiado grande.\nArriesga un fallo en el envío del mensaje así como menos seguridad.')
        n = int(input("Número de bits de seguridad: "))
        while n < 1:
            printerr('El número de bits de seguridad debe ser mayor que 0.')
            n = int(input("Número de bits de seguridad: "))

    asyncio.run(cliente(msg, n, host, port))
else:
    printerr("Opción no válida")
