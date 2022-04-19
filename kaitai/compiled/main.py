from python_pyc_27 import *
import sys
from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


def main ():
	data = PythonPyc27.from_file("__pycache__/basic_graphs.cpython-38.pyc")


if __name__ == "__main__":
	main ()