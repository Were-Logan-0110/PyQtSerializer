# from crypto.Cipher import Blowfish
from Cryptodome.Cipher import Blowfish
from Cryptodome import Random
import base64


def generateEncryptionKey() -> bytes:
    return Random.new().read(16)


class Bytes16(bytes):
    0


def Encrypt(data: str, key: Bytes16 = None) -> tuple[str, bytes]:
    if not key:
        key = generateEncryptionKey()
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    blockSize = Blowfish.block_size
    paddedData = data + (blockSize - len(data) % blockSize) * b"\0"
    encryptedData = cipher.encrypt(paddedData)
    return base64.b64encode(encryptedData).decode("utf-8"), key


def Decrypt(encryptedData: str, key: Bytes16) -> str:
    encryptedData = base64.b64decode(encryptedData)
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    decryptedData = cipher.decrypt(encryptedData).rstrip(b"\0").decode("utf-8")
    return decryptedData