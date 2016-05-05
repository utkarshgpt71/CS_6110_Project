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

def print_sol(var,sol):
	print var
	for j in range(len(sol[0])):
		print '[',
		for i in range(len(sol)):
			print '%d,' %sol[i][j],
		print ']'

	print 'Total Solutions = %d' %len(sol[0])
