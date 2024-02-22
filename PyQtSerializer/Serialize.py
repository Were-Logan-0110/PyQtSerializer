from utils import Encrypt, Decrypt, Bytes16, generateEncryptionKey
from marshal import loads as marshalLoads, dumps as marshalDumps
from pickle import dumps, loads
from types import FunctionType
from inspect import signature
def serialize(
    data: object,
    usePickleForClasses: bool = True,
    encryptCodeObjects: bool = True,
    encryptStdDataTypes: bool = True,
    encryptDictNames: bool = True,
    initObjects: bool = True,
    encryptStrings: bool = True,
    encryptNumbers: bool = True,
    encryptionDepth: int = -1,
    encryptedObjectTypes:list[object]=[],
    key: Bytes16 = None,
) -> object | tuple[object, (Bytes16 | bytes)]:
    """
### Serialize input data into a format suitable for secure-storage/transmission or supporting non-default supported objects.
-----
### Args:
    - `data` (`object`): The data to be serialized.
    - `usePickleForClasses` (`bool`, `optional`):
        Whether to use pickle serialization for class objects if not class attributes will be serialized instead. Defaults to `True`.
    - `encryptCodeObjects` (`bool`, `optional`):
        Whether to encrypt code objects `E.g.(Objects,Functions)`. Defaults to `True`.
    - `encryptStdDataTypes` (`bool`, `optional`): Whether to encrypt standard data types `E.g.(str,int,float)`. Defaults to `True`.
    - `encryptDictNames` (`bool`, `optional`): Whether to encrypt dictionary keys and lib key params. Defaults to `True`.
    - `initObjects` (`bool`, `optional`): Whether to initialize objects during deSerialization. Defaults to `True`.
    - `encryptStrings` (`bool`, `optional`): Whether to encrypt string data. Defaults to `True`.
    - `encryptNumbers` (`bool`, `optional`): Whether to encrypt numeric data. Defaults to `True`.
    - `encryptionDepth` (`int`, `optional`): Depth of encryption. Defaults to -1 (unlimited).
    - `key` (`Bytes`, `optional`): Encryption key (16 Bytes). If not provided, a random key will be generated and returned.
-----
### Returns:
    ```py
object -> The serialized data.
if key is None -> Generates Random Key
    return (Object,Key)
        Key -> bytes(16 Bytes len)
    ```
#### Example Usage:
        ```py
from utils import generateEncryptionKey
def doNothing():
    print("-- It Works !!! --")
class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def dynamicAttr(self):
        self.dynamic = MyClass("Embbeded Class", 12343)


classToBeSerialized = MyClass("Alice", 30)
classToBeSerialized.dynamicAttr()
Key = generateEncryptionKey() # Or Generate Your Own 16 Bytes Key
data = {
    "list": [1, 2, 3],
    "tuple": (4, 5, 6),
    "set": {7, 8, 9},
    "dict": {"a": 10, "b": 11,"embeddedDict":{"list":[1,2,3,"string"]}},
    "class_obj": classToBeSerialized,
    "myFunc": doNothing,
}
serializedData, key = serialize(
    data=data,
    usePickleForClasses=False, # To disable using pickle to serialize classes
    encryptCodeObjects=True,
    encryptStdDataTypes=True,
    encryptDictNames=True,
    initObjects=True,
    encryptStrings=True,
    encryptNumbers=True,
    encryptionDepth=3,
    key=None # If Key Is None it will it will be automatically generated and returned
    # Or key=Key
    )
print("-" * 50 + f"\\nSerialized Data: \\n\\t{serializedData}\\n" + "-" * 50)
deserializedData = deserialize(
    serializedData,
    isEncrypted=True,
    decryptionKey=key,
    classDict=globals(), # Class Dict For The Function To Init Objects From The Global Scope
    setAttrsAfterInit=True, # Set Serialized Attributes For The Initialized Object
    parseDigits=True, # To Convert Strings That Are Numeric Into Numric Data Types Using Evalution
    initObjects=True, # To Initialize Serialized Objects If Pickle Is Not Used
    returnGlobalsForPickle=False, # When An Classes Is Serialized With Pickle Pickle Serialize The Scope With It If You Want The Serialized Scope Give It True
)
print("\\n\\n" + "-" * 50 + f"\\nDeSerialized Data: \\n\\t{deserializedData}\\n" + "-" * 50)
print("-" * 50 + f"\\nEmbedded Object Name: \\n\\t- {deserializedData.get('class_obj').dynamic.name}\\n" + "-" * 50)
deserializedData.get("myFunc")()
    ```
    """

    def encrypt(data, key, depth: int = 0):
        if (depth > 0) or (depth == -1):
            return Encrypt(str(data).encode("utf-8"), key)[0]
        else:
            return data

    isNonKey = False
    if not key:
        key = generateEncryptionKey()
        isNonKey = True

    def Serialize(
        data,
        usePickleForClasses,
        encryptCodeObjects,
        encryptStdDataTypes,
        encryptDictNames,
        initObjects,
        encryptStrings,
        encryptNumbers,
        encryptionDepth,
        encryptedObjectTypes,
        key,
    ):
        if isinstance(data, (list, tuple)):
            return type(data)(
                Serialize(
                    item,
                    usePickleForClasses,
                    encryptCodeObjects,
                    encryptStdDataTypes,
                    encryptDictNames,
                    initObjects,
                    encryptStrings,
                    encryptNumbers,
                    encryptionDepth - 1 if encryptionDepth != -1 else -1,
                    encryptedObjectTypes,
                    key,
                )
                for item in data
            )
        elif isinstance(data, set):
            return {
                Serialize(
                    item,
                    usePickleForClasses,
                    encryptCodeObjects,
                    encryptStdDataTypes,
                    encryptDictNames,
                    initObjects,
                    encryptStrings,
                    encryptNumbers,
                    encryptionDepth - 1 if encryptionDepth != -1 else -1,
                    encryptedObjectTypes,
                    key,
                )
                for item in data
            }
        elif isinstance(data, dict):
            return {
                (
                    Serialize(
                        k,
                        usePickleForClasses,
                        encryptCodeObjects,
                        encryptStdDataTypes,
                        encryptDictNames,
                        initObjects,
                        encryptStrings,
                        encryptNumbers,
                        encryptionDepth - 1 if encryptionDepth != -1 else -1,
                        encryptedObjectTypes,
                        key,
                    )
                    if encryptDictNames
                    else k
                ): Serialize(
                    v,
                    usePickleForClasses,
                    encryptCodeObjects,
                    encryptStdDataTypes,
                    encryptDictNames,
                    initObjects,
                    encryptStrings,
                    encryptNumbers,
                    encryptionDepth - 1 if encryptionDepth != -1 else -1,
                    encryptedObjectTypes,
                    key,
                )
                for k, v in data.items()
            }
        elif callable(data):
            serializedData = marshalDumps(data.__code__).hex()
            encryptedData = (
                encrypt(serializedData, key, encryptionDepth)
                if encryptCodeObjects
                else serializedData
            )
            return {
                (
                    encrypt(
                        f"S_E_R_I_A_L_I_Z_E_D_FunctionMarshal" + data.__name__,
                        key,
                        encryptionDepth,
                    )
                    if encryptDictNames
                    else f"S_E_R_I_A_L_I_Z_E_D_FunctionMarshal" + data.__name__
                ): encryptedData
            }
        elif hasattr(data, "__dict__"):
            serializedData = (
                dumps(data)
                if usePickleForClasses
                else Serialize(
                    data.__dict__,
                    usePickleForClasses,
                    encryptCodeObjects,
                    encryptStdDataTypes,
                    encryptDictNames,
                    initObjects,
                    encryptStrings,
                    encryptNumbers,
                    encryptionDepth - 1 if encryptionDepth != -1 else -1,
                    encryptedObjectTypes,
                    key,
                )
            )
            if usePickleForClasses:
                serializedData = serializedData.hex()
            encryptedData = (
                encrypt(serializedData, key, encryptionDepth)
                if encryptCodeObjects
                else serializedData
            )
            if (not initObjects) or usePickleForClasses:
                return {
                    (
                        encrypt(
                            f"S_E_R_I_A_L_I_Z_E_D_Object{'Pickle' if usePickleForClasses else 'Native'}"
                            + data.__class__.__name__,
                            key,
                            encryptionDepth,
                        )
                        if encryptDictNames
                        else f"S_E_R_I_A_L_I_Z_E_D_Object{'Pickle' if usePickleForClasses else 'Native'}"
                    ): encryptedData
                }
            else:
                return {
                    (
                        encrypt(
                            f"S_E_R_I_A_L_I_Z_E_D_ObjectInitObject"
                            + data.__class__.__name__,
                            key,
                            encryptionDepth,
                        )
                        if encryptDictNames
                        else f"S_E_R_I_A_L_I_Z_E_D_ObjectInitObject"
                        + data.__class__.__name__
                    ): {
                        "data": encryptedData,
                        "params": Serialize(
                            list(signature(data.__init__).parameters.keys()),
                            usePickleForClasses,
                            encryptCodeObjects,
                            encryptStdDataTypes,
                            encryptDictNames,
                            initObjects,
                            encryptStrings if not encryptCodeObjects else True,
                            encryptNumbers,
                            encryptionDepth - 1 if encryptionDepth != -1 else -1,
                            encryptedObjectTypes,
                            key,
                        ),
                    }
                }
        else:
            if encryptStdDataTypes or (type(data) in encryptedObjectTypes):
                return encrypt(data, key, encryptionDepth)
            else:
                if encryptStrings and isinstance(data, str):
                    data = encrypt(data, key, encryptionDepth)
                if encryptNumbers and isinstance(data, (int, float)):
                    data = encrypt(data, key, encryptionDepth)
                return data

    return (
        Serialize(
            data,
            usePickleForClasses,
            encryptCodeObjects,
            encryptStdDataTypes,
            encryptDictNames,
            initObjects,
            encryptStrings,
            encryptNumbers,
            encryptionDepth,
            encryptedObjectTypes,
            key,
        )
        if not isNonKey
        else (
            Serialize(
                data,
                usePickleForClasses,
                encryptCodeObjects,
                encryptStdDataTypes,
                encryptDictNames,
                initObjects,
                encryptStrings,
                encryptNumbers,
                encryptionDepth,
                encryptedObjectTypes,
                key,
            ),
            key,
        )
    )


def initObj(
    objName: str, classDict: dict, data, params: list, setAttrsAfterInit: bool = True
):
    obj = classDict.get(objName)(*[val for key, val in data.items() if key in params])
    if setAttrsAfterInit:
        [obj.__setattr__(key, val) for key, val in data.items() if key not in params]
    return obj


def deserialize(
    serializedData,
    isEncrypted: bool = False,
    decryptionKey: Bytes16 = None,
    classDict: dict = dict(),
    setAttrsAfterInit=False,
    parseDigits: bool = False,
    initObjects: bool = False,
    returnGlobalsForPickle: bool = False,
):
    """
    ### Deserialize input serialized data back into its original form.
    -----
    ### Args:
        `serializedData` (`object`): The serialized data to be deserialized.
        `isEncrypted` (`bool`, `optional`): Whether the serialized data is encrypted. Defaults to `False`.
        `decryptionKey` (`Bytes`, `optional`): Decryption key (16 Bytes) if the data is encrypted. Defaults to `None`.
        `classDict` (`dict`, `optional`): Dictionary containing class definitions for initializing objects. Defaults to an empty dictionary.
        `setAttrsAfterInit` (`bool`, `optional`): Whether to set attributes after initializing objects. Defaults to `False`.
        `parseDigits` (`bool`, `optional`): Whether to parse string data that represents numeric values into actual numeric types. Defaults to `False`.
        `initObjects` (`bool`, `optional`): Whether to initialize objects during deserialization. Defaults to `False`.
        `returnGlobalsForPickle` (`bool`, `optional`): Whether to return global scope for pickle deserialization. Defaults to `False`.
    -----
    ### Returns:
        `object`: The deserialized data.
    #### Example Usage:
            ```py
    from utils import generateEncryptionKey
    def doNothing():
        print("-- It Works !!! --")
    class MyClass:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def dynamicAttr(self):
            self.dynamic = MyClass("Embbeded Class", 12343)


    classToBeSerialized = MyClass("Alice", 30)
    classToBeSerialized.dynamicAttr()
    Key = generateEncryptionKey() # Or Generate Your Own 16 Bytes Key
    data = {
        "list": [1, 2, 3],
        "tuple": (4, 5, 6),
        "set": {7, 8, 9},
        "dict": {"a": 10, "b": 11,"embeddedDict":{"list":[1,2,3,"string"]}},
        "class_obj": classToBeSerialized,
        "myFunc": doNothing,
    }
    serializedData, key = serialize(
        data=data,
        usePickleForClasses=False, # To disable using pickle to serialize classes
        encryptCodeObjects=True,
        encryptStdDataTypes=True,
        encryptDictNames=True,
        initObjects=True,
        encryptStrings=True,
        encryptNumbers=True,
        encryptionDepth=3,
        key=None # If Key Is None it will it will be automatically generated and returned
        # Or key=Key
        )
    print("-" * 50 + f"\\nSerialized Data: \\n\\t{serializedData}\\n" + "-" * 50)
    deserializedData = deserialize(
        serializedData,
        isEncrypted=True,
        decryptionKey=key,
        classDict=globals(), # Class Dict For The Function To Init Objects From The Global Scope
        setAttrsAfterInit=True, # Set Serialized Attributes For The Initialized Object
        parseDigits=True, # To Convert Strings That Are Numeric Into Numric Data Types Using Evalution
        initObjects=True, # To Initialize Serialized Objects If Pickle Is Not Used
        returnGlobalsForPickle=False, # When An Classes Is Serialized With Pickle Pickle Serialize The Scope With It If You Want The Serialized Scope Give It True
    )
    print("\\n\\n" + "-" * 50 + f"\\nDeSerialized Data: \\n\\t{deserializedData}\\n" + "-" * 50)
    print("-" * 50 + f"\\nEmbedded Object Name: \\n\\t- {deserializedData.get('class_obj').dynamic.name}\\n" + "-" * 50)
    deserializedData.get("myFunc")()
        ```
    """
    if isEncrypted and not decryptionKey:
        raise ValueError(
            f"Encryption Key Is Required For Decryption Process But Got KEY<{decryptionKey}>: Please Use key=b'urEncryptionKey'"
        )

    def decrypt(DATA, key):
        try:
            return Decrypt(DATA, key)
        except:
            return DATA

    if isinstance(serializedData, dict):
        if len(serializedData) == 1:
            try:
                firstKey, firstValue = list(serializedData.items())[0]
            except:
                print(list(serializedData.items())[0])
                firstKey, firstValue = list(list(serializedData.items())[0])[0]
            firstKey, firstValue = decrypt(firstKey, decryptionKey), decrypt(
                firstValue, decryptionKey
            )
            if isinstance(firstKey, str) and isinstance(firstKey, str):
                if firstKey.startswith("S_E_R_I_A_L_I_Z_E_D_FunctionMarshal"):
                    return FunctionType(
                        marshalLoads(bytes.fromhex(firstValue)),
                        classDict,
                        firstKey.split("S_E_R_I_A_L_I_Z_E_D_FunctionMarshal")[-1],
                    )
                elif firstKey.startswith("S_E_R_I_A_L_I_Z_E_D_ObjectNative"):
                    if isinstance(firstValue, str):
                        firstValue = eval(firstValue)
                    return deserialize(
                        firstValue,
                        isEncrypted,
                        decryptionKey,
                        classDict,
                        setAttrsAfterInit,
                        parseDigits,
                        initObjects,
                        returnGlobalsForPickle,
                    )
                elif firstKey.startswith("S_E_R_I_A_L_I_Z_E_D_ObjectPickle"):
                    return (
                        (
                            loads(bytes.fromhex(firstValue)),
                            classDict,
                            firstKey.split("S_E_R_I_A_L_I_Z_E_D_ObjectPickle")[-1],
                        )
                        if returnGlobalsForPickle
                        else (
                            loads(bytes.fromhex(firstValue)),
                            classDict,
                            firstKey.split("S_E_R_I_A_L_I_Z_E_D_ObjectPickle")[-1],
                        )[0]
                    )
                elif firstKey.startswith("S_E_R_I_A_L_I_Z_E_D_ObjectInitObject"):
                    params = deserialize(
                        firstValue.get("params"),
                        isEncrypted,
                        decryptionKey,
                        classDict,
                        setAttrsAfterInit,
                        parseDigits,
                        initObjects,
                        returnGlobalsForPickle,
                    )
                    decryptedData = decrypt(firstValue.get("data"), decryptionKey)
                    if isinstance(decryptedData, str):
                        decryptedData = eval(
                            decrypt(firstValue.get("data"), decryptionKey)
                        )
                    return (
                        initObj(
                            firstKey.split("S_E_R_I_A_L_I_Z_E_D_ObjectInitObject")[-1],
                            classDict,
                            deserialize(
                                decryptedData,
                                isEncrypted,
                                decryptionKey,
                                classDict,
                                setAttrsAfterInit,
                                parseDigits,
                                initObjects,
                                returnGlobalsForPickle,
                            ),
                            params,
                            setAttrsAfterInit,
                        )
                        if initObjects
                        else deserialize(
                            {
                                firstKey.split("S_E_R_I_A_L_I_Z_E_D_ObjectInitObject")[
                                    -1
                                ]: {"data": decryptedData, "params": params}
                            },
                            isEncrypted,
                            decryptionKey,
                            classDict,
                            setAttrsAfterInit,
                            parseDigits,
                            initObjects,
                            returnGlobalsForPickle,
                        )
                    )
        return dict(
            [
                (
                    deserialize(
                        k,
                        isEncrypted,
                        decryptionKey,
                        classDict,
                        setAttrsAfterInit,
                        parseDigits,
                        initObjects,
                        returnGlobalsForPickle,
                    ),
                    deserialize(
                        v,
                        isEncrypted,
                        decryptionKey,
                        classDict,
                        setAttrsAfterInit,
                        parseDigits,
                        initObjects,
                        returnGlobalsForPickle,
                    ),
                )
                for k, v in serializedData.items()
            ]
        )
    elif isinstance(serializedData, (list, tuple)):
        return type(serializedData)(
            deserialize(
                item,
                isEncrypted,
                decryptionKey,
                classDict,
                setAttrsAfterInit,
                parseDigits,
                initObjects,
                returnGlobalsForPickle,
            )
            for item in serializedData
        )
    elif isinstance(serializedData, set):
        return {
            deserialize(
                item,
                isEncrypted,
                decryptionKey,
                classDict,
                setAttrsAfterInit,
                parseDigits,
                initObjects,
                returnGlobalsForPickle,
            )
            for item in serializedData
        }
    else:
        if isEncrypted:
            if not parseDigits:
                return decrypt(serializedData, decryptionKey)
            else:
                decryptedData = decrypt(serializedData, decryptionKey)
                if isinstance(decryptedData, str):
                    if decryptedData.isnumeric():
                        return eval(decryptedData)
                    else:
                        return decryptedData
                else:
                    return decryptedData
        else:

            return serializedData
