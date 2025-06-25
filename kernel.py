VALIDO = 1
INVALIDO = 0

N_BITS_FACTOR = 30

class Cifrado():
    def __init__(self, bit_list: list):
        str_bit_list = [str(bit) for bit in bit_list]
        self.bit_key = ''.join(str_bit_list)

    def cifrar(self, msg: str) -> bytes:
        if len(self.bit_key) < len(msg) * 8:
            raise ValueError('Clave demasiado corta')
        
        message_bits = ''.join(f"{ord(c):08b}" for c in msg)
        ciphertext_bits = ''.join(
            str(int(mb) ^ int(kb)) for mb, kb in zip(message_bits, self.bit_key)
        )

        # Convert binary string to bytes
        ciphertext_bytes = int(ciphertext_bits, 2).to_bytes(len(ciphertext_bits) // 8, byteorder='big')
        return ciphertext_bytes


    def descifrar(self, ciphertext: str) -> str:
        if len(self.bit_key) < len(ciphertext) * 8:
            raise ValueError('Clave demasiado corta')

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
    def __init__(self, eje: int, valor: int):
        self.eje = eje
        self.valor = valor

    def leer(self, eje: int) -> tuple:
        if self.eje == eje:
            return eje, self.valor
        else:
            return eje, random.choice([0, 1])
    
    def to_dict(self):
        return {"valor": self.valor, "eje": self.eje}

    @staticmethod
    def from_dict(data):
        return Qbit(data['eje'], data['valor'])

import asyncio
import json
import base64
class CommunicationManager:
    def __init__(self, mode, host, port):
        self.mode = mode
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def start(self):
        if self.mode == "server":
            server = await asyncio.start_server(self.handle_client, self.host, self.port)
            print(f"Escuchando en {self.host}:{self.port}")
            async with server:
                await server.serve_forever()
        elif self.mode == "client":
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            print(f"Enviando mensaje a {self.host}:{self.port} ...")

    async def handle_client(self, reader, writer):
        self.reader = reader
        self.writer = writer
        print(f"Recibiendo mensaje ...")
        await self.run()

    async def send(self, data):
        if self.writer is None:
            raise RuntimeError("Writer not initialized.")

        if isinstance(data, str):
            msg = {"type": "string", "data": data}
        elif isinstance(data, int):
            msg = {"type": "int", "data": data}
        elif isinstance(data, list):
            if all(isinstance(x, int) for x in data):
                msg = {"type": "int_list", "data": data}
            elif all(isinstance(x, Qbit) for x in data):
                msg = {"type": "qbit_list", "data": [q.to_dict() for q in data]}
            else:
                raise ValueError("Unsupported list content")
        elif isinstance(data, bytes):
            # Base64-encode the bytes before sending
            b64_data = base64.b64encode(data).decode("ascii")
            msg = {"type": "bytes", "data": b64_data}
        else:
            raise ValueError("Tipo de dato no soportado para enviar")

        serialized = json.dumps(msg) + "\n"
        self.writer.write(serialized.encode())
        await self.writer.drain()

    async def receive(self):
        if self.reader is None:
            raise RuntimeError("Reader not initialized.")

        raw = await self.reader.readline()
        message = json.loads(raw.decode())

        t = message["type"]
        d = message["data"]

        if t == "string":
            return d
        elif t == "int":
            return int(d)
        elif t == "int_list":
            return list(d)
        elif t == "qbit_list":
            return [Qbit.from_dict(q) for q in d]
        elif t == "bytes":
            return base64.b64decode(d.encode("ascii"))
        else:
            raise ValueError(f"Tipo de mensaje desconocido: {t}")

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def run(self):
        pass

def printerr(err: str): print(f"\033[31m{err}\033[0m")