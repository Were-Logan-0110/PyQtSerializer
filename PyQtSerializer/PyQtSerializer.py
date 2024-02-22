from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from Serializer import *
from typing import Any
import sys


class PyQtSerializer(Serializer):
    def __init__(
        self,
        key: Bytes16,
        target: QObject = None,
        savePath: str = default,
        defaultObjectNamesByQt: bool = False,
        saveFormat: Literal["JSON", "PICKLE", "YAML"] = "JSON",
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
        Hex: bool = False,
        deserializeData: bool = False,
        isEncrypted: bool = False,
        classDict: dict = default,
        setAttrsAfterInit: bool = False,
        parseDigits: bool = False,
        returnGlobalsForPickle: bool = False,
    ) -> None:
        """
        ### Serialize input data into a format suitable for secure-storage/transmission or supporting non-default supported objects.
        -----
        ### Args:
        - `key` (`Bytes`, `required`): Encryption key (16 Bytes). If not provided, a random key will be generated and returned.
        - `target` (`Bytes`, (`required` | `optional`)): Target Widget To Be Serialized If Class Wasnot Inherited You Will Have To Provide Every QObject A Unique Object Name.
        - `saveFormat` (Literal["JSON", "PICKLE", "YAML"]): The format to save the serialized data.
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
        -----
        ### Example Usage:

        ```py

        class MyWindow(QMainWindow): # Or class MyWindow(QMainWindow,PyQtSerializer) prefered using inhiertence
        def __init__(self):
            super().__init__()
            self.setWindowTitle("PyQt Serializer Example")
            self.setGeometry(100, 100, 400, 150)

            # Create a central widget
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            # Layout for widgets
            self.layout = QVBoxLayout()

            # Add widgets to the layout
            self.line_edit = QLineEdit()
            self.line_edit.setObjectName("line_edit")
            self.layout.addWidget(self.line_edit)

            self.check_box = QCheckBox("Remember me")
            self.check_box.setObjectName("check_box")
            self.layout.addWidget(self.check_box)

            # Set the layout for the central widget
            self.central_widget.setLayout(self.layout)

            # Initialize PyQtSerializer
            self.serializer = PyQtSerializer(b"3q\\x83\\x86Xo`u>\\n3\\xcb1B)\\xad", self)

            # Load data if available
            self.load_data()

        def load_data(self):
            try:
                self.serializer.load()
                print(f"Text: {self.serializer.getValue('text')}")
                print(f"checked: {self.serializer.getValue('checked')}")
            except Exception as e:
                print("Error loading data:", format_exc())

        def closeEvent(self, event):
            text = self.line_edit.text()
            checked = self.check_box.isChecked()
            self.serializer.setValue("text", text, serializeValue=True)
            self.serializer.setValue("checked", checked, serializeValue=True)
            self.serializer.dump()
            event.accept()

        app = QApplication(sys.argv)
        window = MyWindow()
        window.show()
        sys.exit(app.exec_())
        ```
        """
        if key == None:
            key = generateEncryptionKey()
        super().__init__(
            {},
            saveFormat,
            serializeData,
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
        if (target == None) and (not isinstance(self, QObject)):
            raise ValueError(
                "No target widget were given please either do class Window(QMainWindow,PyQtSerializer) or PyQtSerializer(b'KEY',targetWidget)"
            )
        if target:
            target.__setattr__ = self.__setattr__
        self.target = target
        self.defaultObjectNamesByQt = defaultObjectNamesByQt
        self.Hex = Hex
        self.deserializeData = deserializeData
        self.isEncrypted = isEncrypted
        self.classDict = classDict
        self.setAttrsAfterInit = setAttrsAfterInit
        self.parseDigits = parseDigits
        self.returnGlobalsForPickle = returnGlobalsForPickle
        self.savePath = savePath
        self.encryptionKey: Bytes16 = key
        self.usePickleForClasses = usePickleForClasses
        self.encryptCodeObjects = encryptCodeObjects
        self.encryptStdDataTypes = encryptStdDataTypes
        self.encryptDictNames = encryptDictNames
        self.initObjects = initObjects
        self.encryptStrings = encryptStrings
        self.encryptNumbers = encryptNumbers
        self.encryptionDepth = encryptionDepth
        self.encryptedObjectTypes = encryptedObjectTypes
        if isinstance(self, QObject):
            if self.objectName() == "":
                self.setObjectName("_serializedWindow")
        self._settings = {"_settings": {}}

    def setValue(self, name: str, value: object, serializeValue: bool = False):
        """_summary_
        Adds A New Settings To The Data
        Args:
            name (str): Setting Name
            value (object): Setting Value
            serializeValue (bool, optional): Wether To Serialize The Value Given. Defaults to False.
        """
        if serializeValue:
            value = serialize(
                value,
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
        self._settings["_settings"][name] = value

    def getValue(self, name: str, evalValue: bool = False):
        """_summary_
        Returns Saved Setting By It's Name
        Args:
            name (str): Setting Name
            evalValue (bool, optional): Wether To Evalute String Expression. Defaults to False.

        Returns:
            _type_: object
        """
        try:
            return (
                self._settings["_settings"][name]
                if not evalValue
                else eval(self._settings["_settings"][name])
            )
        except:
            try:
                return self._settings["_settings"][name]
            except:
                return None

    def deleteValue(self, name: str):
        """_summary_
        Deletes Setting Key,Value From _Settings Dict
        Args:
            name (str): setting mame
        """
        del self._settings["_settings"][name]

    def dump(
        self,
        ignoreClasses: list[object] = [],
        ignoreObjectNames: list[str] = [],
        notChildOf: list[object] = [],
    ):
        """_summary_
        Dumps Settings And The UI State And Saves It Into A File
        Args:
            ignoreClasses (list[object], optional): Classes To Be Ignored When Serializing Widgets. Defaults to [].
            ignoreObjectNames (list[str], optional): Object Names (QObject) To Be Ignored When Serializing Widgets. Defaults to [].
            notChildOf (list[object], optional): Doesn't Serialize The Widget Of It's A Child Of A Widget In The List. Defaults to [].
        """
        _serializer = self
        if not isinstance(self, QObject):
            self = self.target
        _serializer.data = [
            _serializer.serializeWidget(i, ignoreClasses, ignoreObjectNames, notChildOf)
            for i in self.findChildren(QWidget)
        ]
        _serializer.data.append(_serializer._settings)
        if isinstance(self, QObject):
            _serializer.data.insert(
                0,
                _serializer.serializeWidget(
                    self, ignoreClasses, ignoreObjectNames, notChildOf
                ),
            )
        _serializer.data = [item for item in _serializer.data if item is not None]
        _serializer._serialize()
        _serializer.Serialize(hex=True)
    def deserializeData(self):
        """_summary_
        Returns deserialized saved data
        Returns:
            _type_: object
        """
        _serializer = self
        if not isinstance(self, QObject):
            self = self.target
        return _serializer.Deserialize(
            _serializer.savePath,
            hex=_serializer.Hex,
            deserializeData=_serializer.deserializeData,
            isEncrypted=_serializer.isEncrypted,
            classDict=_serializer.classDict,
            setAttrsAfterInit=_serializer.setAttrsAfterInit,
            parseDigits=_serializer.parseDigits,
            initObjects=_serializer.initObjects,
            returnGlobalsForPickle=_serializer.returnGlobalsForPickle,
        )
    def load(self):
        """_summary_
        Deserializes saved data and loads UI states
        """
        _serializer = self
        if not isinstance(self, QObject):
            self = self.target
        deserializedData = _serializer.Deserialize(
            _serializer.savePath,
            hex=_serializer.Hex,
            deserializeData=_serializer.deserializeData,
            isEncrypted=_serializer.isEncrypted,
            classDict=_serializer.classDict,
            setAttrsAfterInit=_serializer.setAttrsAfterInit,
            parseDigits=_serializer.parseDigits,
            initObjects=_serializer.initObjects,
            returnGlobalsForPickle=_serializer.returnGlobalsForPickle,
        )
        if not deserializedData[-1].get("widgetType"):
            _serializer._settings = deserializedData[-1]
        if isinstance(self, QObject):
            widget = self
            widgInfo = deserializedData[0]["serializedData"]
            for k, v in widgInfo.items():
                if k == "setGeometry":
                    widget.setGeometry(*v)
        for widgetInfo in deserializedData:
            if not widgetInfo.get("objectName"):
                continue
            widget = self.findChild(QObject, widgetInfo["objectName"])
            if widget is None:
                continue
            for key, value in widgetInfo["serializedData"].items():
                if key == "setText":
                    widget.setText(value)
                elif key == "setDisabled":
                    widget.setDisabled(eval(value) if isinstance(value, str) else value)
                elif key == "setPlaceHolderText":
                    widget.setPlaceholderText(value)
                elif key == "setMaxLength":
                    widget.setMaxLength(int(value))
                elif key == "setCurrentIndex":
                    widget.setCurrentIndex(value)
                elif key == "addItems":
                    widget.clear()
                    widget.addItems(value)
                elif key == "setChecked":
                    widget.setChecked(eval(value) if isinstance(value, str) else value)
                elif key == "setValue":
                    widget.setValue(value)
                elif key == "setMinimum":
                    widget.setMinimum(value)
                elif key == "setMaximum":
                    widget.setMaximum(value)
                elif key == "setSingleStep":
                    widget.setSingleStep(value)
                elif key == "setDate":
                    widget.setDate(QDate.fromString(value, "yyyy-MM-dd"))
                elif key == "setDigitCount":
                    widget.setDigitCount(value)
                elif key == "display":
                    widget.display(value)
                elif key == "setMinimumDate":
                    widget.setMinimumDate(QDate.fromString(value, "yyyy-MM-dd"))
                elif key == "setMaximumDate":
                    widget.setMaximumDate(QDate.fromString(value, "yyyy-MM-dd"))
                elif key == "setSelectedDate":
                    widget.setSelectedDate(QDate.fromString(value, "yyyy-MM-dd"))
                elif key == "setPlainText":
                    widget.setPlainText(value)
                elif key == "setHtml":
                    widget.setHtml(value)
                elif key == "setKeySequence":
                    widget.setKeySequence(QKeySequence.fromString(value))
                elif key == "setTableWidgetData":
                    widget.setRowCount(len(value))
                    for row, rowData in enumerate(value):
                        for column, text in enumerate(rowData):
                            item = QTableWidgetItem(text)
                            widget.setItem(row, column, item)
                elif key == "setListWidgetData":
                    widget.clear()
                    widget.addItems(value)
                elif key == "setGeometry":
                    widget.setGeometry(*value)

    def getAllWidgetParents(self, widget: QWidget) -> list:
        parents = []
        parent = widget.parent()

        if parent is not None:
            parents = self.getAllWidgetParents(parent)
            parents.append(parent)

        return parents

    def isChildOf(self, widget: QWidget, widgetList: list[QObject]):
        widgType = type(widget)
        objName = widget.objectName()
        return any(w.findChild(widgType, objName) for w in widgetList)

    def serializeWidget(
        self,
        widget,
        ignoreClasses: list[object] = [],
        ignoreObjectNames: list[str] = [],
        notChildOf: list[object] = [],
    ):
        """_summary_
        Widget Serializer
        Args:
            widget (_type_): _description_
            ignoreClasses (list[object], optional): _description_. Defaults to [].
            ignoreObjectNames (list[str], optional): _description_. Defaults to [].
            notChildOf (list[object], optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        if self.defaultObjectNamesByQt and isinstance(widget, QObject):
            if self.isChildOf(widget, notChildOf):
                return
            if widget.objectName().startswith("qt_"):
                return
        if not isinstance(widget, QObject):
            return
        if (
            (widget.objectName() == "")
            or (isinstance(widget, tuple(ignoreClasses)))
            or (widget.objectName() in ignoreObjectNames)
        ):
            return
        widgInfo = {
            "objectName": widget.objectName(),
            "serializedData": {},
            "widgetType": type(widget).__name__,
        }
        serializedData = widgInfo["serializedData"]
        if hasattr(widget, "setMinimumDate"):
            try:
                serializedData["setMinimumDate"] = str(widget.minimumDate().toPyDate())
            except:
                serializedData["setMinimumDate"] = str(
                    widget.minimumDate().toString("yyyy-MM-dd")
                )
        if hasattr(widget, "isChecked"):
            serializedData["setChecked"] = widget.isChecked()
        if hasattr(widget, "setMaximumDate"):
            serializedData["setMaximumDate"] = str(widget.maximumDate().toPyDate())
        if hasattr(widget, "setSelectedDate"):
            serializedData["setSelectedDate"] = str(widget.selectedDate().toPyDate())
        if hasattr(widget, "text"):
            serializedData["setText"] = widget.text()
        if hasattr(widget, "toPlainText"):
            serializedData["setPlainText"] = widget.toPlainText()
        if hasattr(widget, "placeholderText"):
            serializedData["setPlaceholderText"] = widget.placeholderText()
        if hasattr(widget, "value"):
            serializedData["setValue"] = widget.value()
        if hasattr(widget, "minimum"):
            serializedData["setMinimum"] = widget.minimum()
        if hasattr(widget, "maximum"):
            serializedData["setMaximum"] = widget.maximum()
        if isinstance(widget, QComboBox):
            serializedData["addItems"] = [
                widget.itemText(i) for i in range(widget.count())
            ]
        if hasattr(widget, "currentIndex"):
            if not isinstance(widget.currentIndex(), QModelIndex):
                serializedData["setCurrentIndex"] = widget.currentIndex()
        if isinstance(widget, QWidget):
            serializedData["setDisabled"] = not widget.isEnabled()
        if isinstance(widget, QAbstractSlider):
            serializedData["setSingleStep"] = widget.singleStep()
        if isinstance(widget, QLineEdit):
            serializedData["setMaxLength"] = widget.maxLength()
        if isinstance(widget, QLCDNumber):
            serializedData["setDigitCount"] = widget.digitCount()
            serializedData["display"] = widget.value()
            del serializedData["setValue"]
        if isinstance(widget, QSpinBox):
            del serializedData["setText"]
        if isinstance(widget, QProgressBar):
            del serializedData["setText"]
        if isinstance(widget, QDateEdit):
            serializedData["setDate"] = str(widget.date().toPyDate())
            del serializedData["setText"]
        if isinstance(widget, QTextBrowser):
            serializedData["setHtml"] = widget.toHtml()
        if isinstance(widget, QKeySequenceEdit):
            serializedData["setKeySequence"] = widget.keySequence().toString()
        if isinstance(widget, QColorDialog):
            widget.selectedColor().to
        if isinstance(widget, QTableWidget):
            data = []
            for row in range(widget.rowCount()):
                rowData = []
                for column in range(widget.columnCount()):
                    item = widget.item(row, column)
                    if item is not None:
                        rowData.append(item.text())
                    else:
                        rowData.append("")
                data.append(rowData)
            serializedData["setTableWidgetData"] = data
        if isinstance(widget, QListWidget):
            data = [
                self.list_widget.item(index).text()
                for index in range(self.list_widget.count())
            ]
            serializedData["setListWidgetData"] = data
        if isinstance(widget, QMainWindow):
            geo = widget.geometry()
            serializedData["setGeometry"] = (
                geo.x(),
                geo.y(),
                geo.width(),
                geo.height(),
            )
        return widgInfo

    def __setattr__(self, __name: str, __value: Any) -> None:
        if isinstance(__value, QObject):
            if __value.objectName() == "":
                __value.setObjectName(__name)
        return super().__setattr__(__name, __value)
if __name__ == "__main__":
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
