# PyQtSerializer

#### `PyQtSerializer` is a Python library for serializing input data into a format suitable for secure storage/transmission or supporting non-default supported objects, particularly designed for `PyQt` applications.

## Installation

You can install `PyQtSerializer` via pip:

> **`pip install PyQtSerializer`**

## Features

* Serialize `PyQt` widgets Automatically and data into JSON, Pickle, or YAML format.
* Support for encryption of code objects, standard data types, dictionary keys, and more.
* Easy integration with `PyQt` applications.
## Usage

Here's a simple example demonstrating how to use `PyQtSerializer` within a `PyQt` application:
## Using Inheritance (**preferred**)
```python
from PyQtSerializer import PyQtSerializer
# Or from PyQtSerializer.PyQtSerializer import PyQtSerializer If autocompelete wasn't working
class MyWindow(QMainWindow, PyQtSerializer):
    def __init__(self):
        super().__init__(key=b"3q\x83\x86Xo`u>\n3\xcb1B) \xad") # Other Options
        self.setWindowTitle("PyQt Serializer Example")
        self.setGeometry(100, 100, 400, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.layout.addWidget(self.lineEdit)

        self.checkBox = QCheckBox("Remember me")
        self.layout.addWidget(self.checkBox)
        self.centralWidget.setLayout(self.layout)

        self.loadData()
    def GetSetting(self):
        self.loadData()
        self.getValue("Setting",evalValue=False)
    def AddNewSetting(self):
        self.setValue("Setting",True,serializeValue = False)
    def loadData(self):
        try:
            # Load UI State Into The Window
            self.load()
        except Exception as e:
            print("Error loading data:", e)

    def closeEvent(self, event):
        # Saves The UI State Into File
        self.dump()
        event.accept()
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())

```
# Using PyQtSerializer Class
## `NOTE`: 
**When Inheritance Is Not Used You Will Have To Provide And Object Name For Each Widget You Want To Save It's State**
```py
from PyQtSerializer import PyQtSerializer
# Or from PyQtSerializer.PyQtSerializer import PyQtSerializer If autocompelete wasn't working
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Serializer Example")
        self.setGeometry(100, 100, 400, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.layout.addWidget(self.lineEdit)
        self.lineEdit.setObjectName("lineEdit")
# When Inheritance Is Not Used You Will Have To Provide And Object Name For Each Widget You Want To Save It's State
        self.checkBox = QCheckBox("Remember me")
        self.checkBox.setObjectName("checkBox")
        self.layout.addWidget(self.checkBox)
        self.centralWidget.setLayout(self.layout)
        # Initialize The Serializer
        self.serializer = PyQtSerializer(b"3q\x83\x86Xo`u>\n3\xcb1B)\xad", target=self)
        # Load data if available
        self.loadData()

    def loadData(self):
        try:
            self.serializer.load()
            print(f"Text: {self.serializer.getValue('text')}")
            print(f"checked: {self.serializer.getValue('checked')}")
        except Exception as e:
            print("Error loading data:", e)
    def GetSetting(self):
        self.loadData()
        self.serializer.getValue("Setting",evalValue=False)
    def AddNewSetting(self):
        self.serializer.setValue("Setting",True,serializeValue = False)
    def closeEvent(self, event):
        text = self.lineEdit.text()
        checked = self.checkBox.isChecked()
        self.serializer.setValue("text", text, serializeValue=True)
        self.serializer.setValue("checked", checked, serializeValue=True)
        self.serializer.dump()
        event.accept()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
```
## Using The `Serializer` Class
```py
from PyQtSerializer.Serializer import Serializer
class Class:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

def SayHello(name):
    print(f"Hello, {name}")

CLASS = Class("Ahmed", 17)
data = {
    "list": [1, 2, "3", {"key", "val"}],
    "tuple": (1, 2, 3),
    "dict": {"key": "Value"},
    "object": CLASS,
    "func": SayHello,
}
serializer = Serializer(
    data,
    saveFormat="YAML",
    serializeData=True,
    usePickleForClasses=True,
    encryptCodeObjects=True,
    encryptStdDataTypes=True,
    encryptDictNames=True,
    initObjects=False,
    encryptStrings=True,
    encryptNumbers=True,
    encryptionDepth=-1,
)
print(f"Encryption Key: \n\t{serializer.encryptionKey}\n\n")
print(f"Serialized Data: \n\t{serializer.data}\n\n")
serializer.Serialize(filePath="_settings.yaml", hex=False)
deserializedData = serializer.Deserialize(
    filePath="_settings.yaml",
    hex=False,
    deserializeData=True,
    isEncrypted=True,
    classDict=globals(),
    setAttrsAfterInit=False,
    parseDigits=True,
    initObjects=False,
    returnGlobalsForPickle=False,
)
print(f"Deserialized Data: \n\t<{deserializedData}>")
deserializedData.get("func")(deserializedData.get("object").name)
```
## You Can Also Use `serialize` And `deserialize` Functions If You Don't Want To Save To A File
```py
from PyQtSerializer import serialize, deserialize,generateEncryptionKey


class Class:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age


def SayHello(name):
    print(f"Hello, {name}")


CLASS = Class("Ahmed", 17)
data = {
    "list": [1, 2, "3", {"key", "val"}],
    "tuple": (1, 2, 3),
    "dict": {"key": "Value"},
    "object": CLASS,
    "func": SayHello,
}
key = generateEncryptionKey()
serializedData = serialize(
    data,
    usePickleForClasses=True,
    encryptCodeObjects=True,
    encryptStdDataTypes=True,
    encryptDictNames=True,
    initObjects=False,
    encryptStrings=True,
    encryptNumbers=True,
    encryptionDepth=-1,
    encryptedObjectTypes=[bool],
    key=key
)
deserializedData = deserialize(
    serializedData,
    decryptionKey=key,
    isEncrypted=True,
    classDict=globals(),
    setAttrsAfterInit=False,
    parseDigits=True,
    initObjects=True,
    returnGlobalsForPickle=False
)
print(f"Deserialized Data: \n\t<{deserializedData}>")
deserializedData.get("func")(deserializedData.get("object").name)
```
## **Parameters**

|Parameter|Type|Description|Default|
|---|---|---|---|
|target|`QObject`,`optional`|Target Widget To Be Serialized If Class Wasnot Inherited You Will Have To Provide Every QObject A Unique Object Name|`None`|
|data|`object`|The data to be serialized.||
|saveFormat|`str["JSON", "PICKLE", "YAML"]`|The data to be serialized.|`YAML`|
|usePickleForClasses|`bool`, `optional`|Whether to use pickle serialization for class objects if not class attributes will be serialized instead.|`True`|
|encryptCodeObjects|`bool`, `optional`|Whether to encrypt code objects (e.g., objects, functions).|`True`|
|encryptStdDataTypes|`bool`, `optional`|Whether to encrypt standard data types (e.g., `str`, `int`, `float`).|`True`|
|encryptDictNames|`bool`, `optional`|Whether to encrypt dictionary keys and lib key params.|`True`|
|initObjects|`bool`, `optional`|Whether to initialize objects during deSerialization.|`True`|
|encryptStrings|`bool`, `optional`|Whether to encrypt string data.|`True`|
|encryptNumbers|`bool`, `optional`|Whether to encrypt numeric data.|`True`|
|encryptionDepth|`int`, `optional`|Depth of encryption.|`-1`|
|key|`Bytes`, `optional`|Encryption key (16 Bytes). If not provided, a random key will be generated and returned.||
|serializedData|`object`|The serialized data to be deserialized.||
|isEncrypted|`bool`, `optional`|Whether the serialized data is encrypted.|`False`|
|decryptionKey|`Bytes`, `optional`|Decryption key (16 Bytes) if the data is encrypted.|`None`|
|classDict|`dict`, `optional`|Dictionary containing class definitions for initializing objects.|`{}`|
|setAttrsAfterInit|`bool`, `optional`|Whether to set attributes after initializing objects.|`False`|
|parseDigits|`bool`, `optional`|Whether to parse string data that represents numeric values into actual numeric types.|`False`|
|initObjects|`bool`, `optional`|Whether to initialize objects during deserialization.|`False`|
|returnGlobalsForPickle|`bool`, `optional`|Whether to return global scope for pickle deserialization.|`False`|
## Contributing

Contributions are welcomed! Please feel free to submit issues, feature requests, or pull requests on the [**GitHub repository**](https://github.com/Were-Logan-0110/PyQtSerializer).