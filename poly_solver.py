import sys
from sympy import *
from boolector import Boolector
import time


input_file = sys.argv[1]
f = open(input_file,'r')


mod = []
var  = []
for line in f.readlines():
	line = line.rstrip()
	line = line.split(';')
	mod.append(int(line[1].strip()))
	#print line[0]
	line = line[0].replace('+',' ').replace('-',' ').replace('*',' ')
	line = line.replace('(',' ').replace(')',' ').split()
	#print line
	for v in line:
		try:
			int(v)
		except ValueError:
			if v not in var:
				var.append(v)

print var
sym = []

for i in range(len(var)):
	sym.append(symbols(var[i]))


bw = max(mod)+1

f.close()