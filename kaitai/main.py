import parsetree
from python_pyc_27 import PythonPyc27
import sys
from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


def main ():
	pathname = "__pycache__/test.pyc"
	struct = PythonPyc27.from_file (pathname)


if __name__ == "__main__":
	main ()