from kernel import *

class Emisor():
    def __init__(self, msg: str, N: int):
        self.msg = msg
        self.N = N
        self.mapaQbits = []
    
    async def on_ready(self):
        msg = await self.receive()
        print("[B] Received:", msg)
        await self.send("Hello from B!")

"""
    async def run(self):
        numQbits = len(self.msg) * N_BITS_FACTOR
        qbits = self.generarQbits(numQbits)
        await self.atob.put(qbits)
        ejes = [tupla[0] for tupla in self.mapaQbits]

        await self.atob.put(ejes)
        ejesReceptor = await self.btoa.get()
        self.purgarMapa(ejesReceptor)

        indices = await self.btoa.get()
        valoresSeguridad = await self.btoa.get()
        # Use the same indices to extract values for comparison
        valores_emisor = [self.mapaQbits[i][1] for i in indices]
        if valores_emisor == valoresSeguridad:
            await self.atob.put(VALIDO)
            valores = [tupla[1] for tupla in self.mapaQbits]
            c = Cifrado(valores)
            cifrado = c.cifrar(self.msg)
            await self.atob.put(cifrado)
        else:
            print("Valores de seguridad no coinciden, mensaje no enviado")
            await self.atob.put(INVALIDO)
        
    def generarQbits(self, numQbits: int) -> list:
        from kernel import Qbit
        qbits = []
        for _ in range(numQbits):
            qbit = Qbit()
            eje, valor = qbit.generar()
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
"""