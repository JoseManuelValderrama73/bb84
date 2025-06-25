from kernel import *

class Emisor(CommunicationManager):
    def __init__(self, msg: str, N: int, host: str, port: int):
        super().__init__('client', host, port)
        self.msg = msg
        self.N = N
        self.mapaQbits = []

    async def run(self):
        await self.start()
        await self.send(self.N)

        numQbits = len(self.msg) * N_BITS_FACTOR
        qbits = self.generarQbits(numQbits)
        await self.send(qbits)
        ejes = [tupla[0] for tupla in self.mapaQbits]

        await self.send(ejes)
        ejesReceptor = await self.receive()
        self.purgarMapa(ejesReceptor)

        indices = await self.receive()
        valoresSeguridad = await self.receive()
        # Use the same indices to extract values for comparison
        valores_emisor = [self.mapaQbits[i][1] for i in indices]
        if valores_emisor == valoresSeguridad:
            await self.send(VALIDO)
            valores = [tupla[1] for tupla in self.mapaQbits]
            c = Cifrado(valores)
            cifrado = c.cifrar(self.msg)
            await self.send(cifrado)
        else:
            print("Valores de seguridad no coinciden, mensaje no enviado")
            await self.send(INVALIDO)

        await self.close()
        
    def generarQbits(self, numQbits: int) -> list:
        from kernel import Qbit
        qbits = []
        for _ in range(numQbits):
            eje, valor = random.choice([0, 1]), random.choice([0, 1])
            qbit = Qbit(eje, valor)
            qbits.append(qbit)
            self.mapaQbits.append((eje, valor))
        return qbits

    def purgarMapa(self, ejesReceptor: list):
        nuevoMapa = []
        for i in range(len(self.mapaQbits)):
            if self.mapaQbits[i][0] == ejesReceptor[i]:
                nuevoMapa.append(self.mapaQbits[i])
        self.mapaQbits = nuevoMapa
    
    def comprobarValoresSeguridad(self, valoresSeguridad: list) -> bool:
        for i in range(self.N):
            if self.mapaQbits[i][1] != valoresSeguridad[i]:
                return False
        return True