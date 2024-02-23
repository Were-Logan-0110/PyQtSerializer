from PyQtSerializer.Serialize import serialize, deserialize, generateEncryptionKey
from PyQtSerializer.utils import Bytes16
from pickle import loads, dumps
from typing import Literal
import yaml
import json


class Default:
    0


default = Default()


class Serializer:
    def __init__(
        self,
        data: object,
        saveFormat: Literal["JSON", "PICKLE", "YAML"],
        serializeData: bool = False,
        usePickleForClasses: bool = False,
        encryptCodeObjects: bool = False,
        encryptStdDataTypes: bool = False,
        encryptDictNames: bool = False,
        initObjects: bool = False,
        encryptStrings: bool = False,
        encryptNumbers: bool = False,
        encryptionDepth: int = -1,
        encryptedObjectTypes: list[object] = [],
        key: Bytes16 = None,
    ) -> None:
        """
        ## Serializer

        ##### `__init__(self, data: object, saveFormat: Literal["JSON", "PICKLE", "YAML"], serializeData: bool = False, usePickleForClasses: bool = False, encryptCodeObjects: bool = False, encryptStdDataTypes: bool = False, encryptDictNames: bool = False, initObjects: bool = False, encryptStrings: bool = False, encryptNumbers: bool = False, encryptionDepth: int = -1, encryptedObjectTypes: list[object] = [], key: Bytes16 = None) -> None`

        Initialize Serializer object.

        #### Args:
        - `data` (object): The data to be serialized.
        - `saveFormat` (Literal["JSON", "PICKLE", "YAML"]): The format to save the serialized data.
        - `serializeData` (bool, optional): Whether to serialize the data during initialization. Defaults to False.
        - `usePickleForClasses` (bool, optional): Whether to use pickle serialization for class objects. Defaults to False.
        - `encryptCodeObjects` (bool, optional): Whether to encrypt code objects (e.g., Objects, Functions). Defaults to False.
        - `encryptStdDataTypes` (bool, optional): Whether to encrypt standard data types (e.g., str, int, float). Defaults to False.
        - `encryptDictNames` (bool, optional): Whether to encrypt dictionary keys and library key params. Defaults to False.
        - `initObjects` (bool, optional): Whether to initialize objects during deserialization. Defaults to False.
        - `encryptStrings` (bool, optional): Whether to encrypt string data. Defaults to False.
        - `encryptNumbers` (bool, optional): Whether to encrypt numeric data. Defaults to False.
        - `encryptionDepth` (int, optional): Depth of encryption. Defaults to -1 (unlimited).
        - `encryptedObjectTypes` (list[object], optional): List of object types to be encrypted. Defaults to [].
        - `key` (Bytes16, optional): Encryption key (16 Bytes). If not provided, a random key will be generated and used. Defaults to None.

        ### `Serialize(self, filePath: str = default, hex: bool = False) -> str`

        Serialize data into the specified format.

        #### Args:
        - `filePath` (str, optional): File path to save the serialized data. Defaults to default (current directory).
        - `hex` (bool, optional): Whether to use hexadecimal encoding for serialization. Defaults to False.

        #### Returns:
        - `str`: File path where the serialized data is saved.

        ### `Deserialize(self, filePath: str = default, hex: bool = False, deserializeData: bool = False, isEncrypted: bool = False, classDict: dict = default, setAttrsAfterInit: bool = False, parseDigits: bool = False, initObjects: bool = False, returnGlobalsForPickle: bool = False) -> object`

        Deserialize data from the specified format.

        #### Args:
        - `filePath` (str, optional): File path to load the serialized data. Defaults to default (current directory).
        - `hex` (bool, optional): Whether the serialized data is in hexadecimal format. Defaults to False.
        - `deserializeData` (bool, optional): Whether to deserialize the data after loading. Defaults to False.
        - `isEncrypted` (bool, optional): Whether the serialized data is encrypted. Defaults to False.
        - `classDict` (dict, optional): Dictionary containing class definitions for initializing objects. Defaults to global dictionary.
        - `setAttrsAfterInit` (bool, optional): Whether to set attributes after initializing objects. Defaults to False.
        - `parseDigits` (bool, optional): Whether to parse string data that represents numeric values into actual numeric types. Defaults to False.
        - `initObjects` (bool, optional): Whether to initialize objects during deserialization. Defaults to False.
        - `returnGlobalsForPickle` (bool, optional): Whether to return global scope for pickle deserialization. Defaults to False.

        #### Returns:
        - `object`: Deserialized data.
        """
        if key == None:
            key = generateEncryptionKey()
        self.encryptionKey: Bytes16 = key
        self.data = data
        self.usePickleForClasses = usePickleForClasses
        self.encryptCodeObjects = encryptCodeObjects
        self.encryptStdDataTypes = encryptStdDataTypes
        self.encryptDictNames = encryptDictNames
        self.initObjects = initObjects
        self.encryptStrings = encryptStrings
        self.encryptNumbers = encryptNumbers
        self.encryptionDepth = encryptionDepth
        self.encryptedObjectTypes = encryptedObjectTypes
        self.saveFormat = saveFormat.upper()
        if serializeData:
            self.data = serialize(
                self.data,
                usePickleForClasses,
                encryptCodeObjects,
                encryptStdDataTypes,
                encryptDictNames,
                initObjects,
                encryptStrings,
                encryptNumbers,
                encryptionDepth,
                encryptedObjectTypes,
                self.encryptionKey,
            )

    def _serialize(self):
        self.data = serialize(
            self.data,
            self.usePickleForClasses,
            self.encryptCodeObjects,
            self.encryptStdDataTypes,
            self.encryptDictNames,
            self.initObjects,
            self.encryptStrings,
            self.encryptNumbers,
            self.encryptionDepth,
            self.encryptedObjectTypes,
            self.encryptionKey,
        )

    def Serialize(
        self,
        filePath: str = default,
        hex: bool = False,
    ):
        if self.saveFormat == "JSON":
            return Serializer._JsonSerialize(self.data, filePath)
        elif self.saveFormat == "YAML":
            return Serializer._YamlSerialize(self.data, filePath)
        else:
            return Serializer._PickleSerialize(self.data, filePath, hex)

    def Deserialize(
        self,
        filePath: str = default,
        hex: bool = False,
        deserializeData: bool = False,
        isEncrypted: bool = False,
        classDict: dict = default,
        setAttrsAfterInit: bool = False,
        parseDigits: bool = False,
        initObjects: bool = False,
        returnGlobalsForPickle: bool = False,
    ):
        data = self.data
        if self.saveFormat == "JSON":
            data = Serializer._JsonDeserialize(filePath)
        elif self.saveFormat == "YAML":
            data = Serializer._YamlDeserialize(filePath)
        else:
            data = Serializer._PickleDeserialize(filePath, hex)
        if isinstance(classDict, Default):
            classDict = globals()
        if deserializeData:
            data = deserialize(
                data,
                isEncrypted,
                self.encryptionKey,
                classDict,
                setAttrsAfterInit,
                parseDigits,
                initObjects,
                returnGlobalsForPickle,
            )
        return data

    @staticmethod
    def _JsonSerialize(
        data: dict[str, object],
        filePath: str = default,
    ):
        if isinstance(filePath, Default):
            filePath = f"_serializedObj.json"
        data = json.dumps(data)
        with open(filePath, "w", encoding="utf-8", errors="ignore") as serializedFile:
            serializedFile.write(data)
        return filePath

    @staticmethod
    def _JsonDeserialize(filePath: str = default):
        if isinstance(filePath, Default):
            filePath = f"_serializedObj.json"
        with open(filePath, "r", encoding="utf-8", errors="ignore") as serializedFile:
            return json.loads(serializedFile.read())

    @staticmethod
    def _PickleSerialize(
        data: dict[str, object], filePath: str = default, hex: bool = False
    ):
        if isinstance(filePath, Default):
            filePath = f"_serializedObj.pkl"
        data = dumps(data)
        if hex:
            data = data.hex()
        with open(
            filePath,
            "w" if hex else "wb",
            encoding=("utf-8" if hex else None),
            errors=("ignore" if hex else None),
        ) as serializedFile:
            serializedFile.write(data)
        return filePath

    @staticmethod
    def _PickleDeserialize(filePath: str = default, hex: bool = False):
        if isinstance(filePath, Default):
            filePath = f"_serializedObj.pkl"
        with open(
            filePath,
            ("r" if hex else "rb"),
            encoding=("utf-8" if hex else None),
            errors=("ignore" if hex else None),
        ) as serializedFile:
            data = serializedFile.read()
        if hex:
            return loads(bytes.fromhex(data))
        else:
            return loads(data)

    @staticmethod
    def _YamlSerialize(data: dict[str, object], filePath: str = default):
        if isinstance(filePath, Default):
            filePath = f"_serializedObj.yaml"
        data = yaml.dump(data)
        with open(
            filePath,
            "w" if hex else "wb",
            encoding=("utf-8" if hex else None),
            errors=("ignore" if hex else None),
        ) as serializedFile:
            serializedFile.write(data)
        return filePath

    @staticmethod
    def _YamlDeserialize(filePath: str = default):
        if isinstance(filePath, Default):
            filePath = f"_serializedObj.yaml"
        with open(filePath, "r", encoding="utf-8", errors="ignore") as serializedFile:
            data = serializedFile.read()
        return yaml.full_load(data)
