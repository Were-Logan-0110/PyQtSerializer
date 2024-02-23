try:
    from utils import Encrypt,Decrypt,generateEncryptionKey
    from Serialize import serialize,deserialize
    from PyQtSerializer import PyQtSerializer
    from Serializer import Serializer
except:
    from PyQtSerializer.utils import Encrypt, Decrypt, generateEncryptionKey
    from PyQtSerializer.Serialize import serialize, deserialize
    from PyQtSerializer.PyQtSerializer import PyQtSerializer
    from PyQtSerializer.Serializer import Serializer
__author__ = "Ahmed Essam (https://github.com/Were-Logan-0110)"
__version__ = "0.01"
