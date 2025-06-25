VALIDO = 1
INVALIDO = 0

N_BITS_FACTOR = 30

class Cifrado():
    def __init__(self, bit_list: list):
        str_bit_list = [str(bit) for bit in bit_list]
        self.bit_key = ''.join(str_bit_list)

    def cifrar(self, msg: str) -> bytes:
        if len(self.bit_key) < len(msg) * 8:
            raise ValueError("Key too short for message")
        
        message_bits = ''.join(f"{ord(c):08b}" for c in msg)
        ciphertext_bits = ''.join(
            str(int(mb) ^ int(kb)) for mb, kb in zip(message_bits, self.bit_key)
        )

        # Convert binary string to bytes
        ciphertext_bytes = int(ciphertext_bits, 2).to_bytes(len(ciphertext_bits) // 8, byteorder='big')
        return ciphertext_bytes


    def descifrar(self, ciphertext: str) -> str:
        if len(self.bit_key) < len(ciphertext) * 8:
            raise ValueError("Key too short for ciphertext")

        # Convert bytes to binary string
        ciphertext_bits = ''.join(f"{byte:08b}" for byte in ciphertext)
        message_bits = ''.join(
            str(int(cb) ^ int(kb)) for cb, kb in zip(ciphertext_bits, self.bit_key)
        )

        # Convert binary string to original characters
        chars = [chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8)]
        return ''.join(chars)

import random
class Qbit():
    def __init__(self):
        self.eje = None
        self.valor = None

    def generar(self) -> tuple:
        self.eje = random.choice([0, 1])
        self.valor = random.choice([0, 1])
        return self.eje, self.valor

    def leer(self, eje: int) -> tuple:
        if (self.eje is None) or (self.valor is None):
            raise Exception("Qbit no generado")

        if self.eje == eje:
            return eje, self.valor
        else:
            return eje, random.choice([0, 1])

import asyncio
class CommunicationManager:
    def __init__(self, mode, host, port):
        self.mode = mode  # "client" or "server"
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def start(self):
        if self.mode == "server":
            server = await asyncio.start_server(self.handle_client, self.host, self.port)
            print(f"[SERVER] Listening on {self.host}:{self.port}")
            async with server:
                await server.serve_forever()
        elif self.mode == "client":
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            print(f"[CLIENT] Connected to {self.host}:{self.port}")

    async def handle_client(self, reader, writer):
        self.reader = reader
        self.writer = writer
        print(f"[SERVER] Client connected.")
        await self.on_ready()  # calls a hook for user code

    async def send(self, msg: str):
        if self.writer is None:
            raise RuntimeError("Writer not initialized.")
        self.writer.write((msg + "\n").encode())
        await self.writer.drain()

    async def receive(self) -> str:
        if self.reader is None:
            raise RuntimeError("Reader not initialized.")
        data = await self.reader.readline()
        return data.decode().strip()

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def on_ready(self):
        """
        Hook: override this in subclass or assign externally
        Called when connection is ready (for server)
        """
        pass