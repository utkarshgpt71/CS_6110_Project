import sys
from sympy import *
from boolector import Boolector
import time
import parser
import hf


def isint(v):
	try:
		int(v)
	except ValueError:
		return 0

	return 1

