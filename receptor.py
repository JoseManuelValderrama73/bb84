from kernel import *
import random

class Receptor(CommunicationManager):
    def __init__(self, port: int):
        super().__init__('server', '0.0.0.0', port)
        self.mapaQbits = []

    async def run(self):
        N = await self.receive()
        qbits = await self.receive()
        self.generarMapaQbits(qbits)
        ejes = [tupla[0] for tupla in self.mapaQbits]

        await self.send(ejes)
        ejesEmisor = await self.receive()
        self.purgarMapa(ejesEmisor)

        indices = random.sample(range(len(self.mapaQbits)), N)
        valores_seguridad = [self.mapaQbits[i][1] for i in indices]
        await self.send(indices)
        await self.send(valores_seguridad)

        msg = None
        if (await self.receive() == VALIDO):
            msg_cif = await self.receive()
            valores = [tupla[1] for tupla in self.mapaQbits]
            c = Cifrado(valores)
            try:
                msg = c.descifrar(msg_cif)
                self.tratarMensaje(msg)
            except ValueError as e:
                printerr(f"Error al descifrar el mensaje: {e}")


    async def salir(self):
        await self.close()

    def generarMapaQbits(self, qbits) -> list:
        for qbit in qbits:
            eje, valor = qbit.leer(random.choice([0, 1]))
            self.mapaQbits.append((eje, valor))
        
    def purgarMapa(self, ejesReceptor: list):
        nuevoMapa = []
        for i in range(len(self.mapaQbits)):
            if self.mapaQbits[i][0] == ejesReceptor[i]:
                nuevoMapa.append(self.mapaQbits[i])
        self.mapaQbits = nuevoMapa
    
    def tratarMensaje(self, msg: str):
        print("Mensaje recibido:", msg)