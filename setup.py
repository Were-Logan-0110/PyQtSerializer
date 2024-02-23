from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
VERSION = "0.0.13"
DESCRIPTION = "A PyQt Serialization Library"
LONG_DESCRIPTION = (
    "A package that allows you to save PyQt/PySide Applications Full States."
)

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
setup(
    name="PyQtSerializer",
    version=VERSION,
    author="Ahmed Essam (https://github.com/Were-Logan-0110)",
    author_email="<headnuts92@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=["qtpy", "pycryptodome"],
    keywords=[
        "python",
        "encryption",
        "serialize",
        "serialization",
        "pickle",
        "pyqt",
        "qt" "save",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
