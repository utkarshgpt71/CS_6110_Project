import sys
from sympy import *
from boolector import Boolector
import time
import parser
import hf


def isint(v):
	try:
		int(v)
	except:
		return 0

	return 1

def print_sol(var,sol):
	for k in range(len(sol)):
		print '\nSolutions Mod %d' %(2**(k+1))
		print var
		for j in range(len(sol[k])):
			print sol[k][j]
		print 'Total Solutions Mod %d = %d' %(2**(k+1),len(sol[k]) )
