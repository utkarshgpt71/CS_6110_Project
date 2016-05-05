import sys
from sympy import *
import time
import copy


############################################################################
###################### PARSING THE .POLY INPUT FILE ########################
############################################################################
input_file = sys.argv[1]
f = open(input_file,'r')
func = []

mod = []
var  = []
var_bw = []

for line in f.readlines():
	line = line.rstrip()
	line = line.split(';')
	if len(line) == 1:
		if len(line[0]) > 5:
			var.append(line[0].partition('[')[0].strip())
			rng = line[0].partition('[')[2].partition(']')[0]
			msb = int(rng.split(':')[0].strip())
			lsb = int(rng.split(':')[1].strip())
			var_bw.append (msb - lsb + 1)

	else:
		if len(line) == 2: 
			mod.append(int(line[1].strip()))
			func.append( expand(sympify(line[0])) )

f.close()

bw = max(mod)
for i in range(len(func)):
	func[i] = func[i]*(2**(bw-mod[i]))

sym = []
lz = [0] * len(func)

#print lz

for i in range(len(var)):
	sym.append(symbols(var[i]))

print var
for i in range(2**len(var)):
	tmp = copy.deepcopy(func)
	b = bin(i)
	v = []
	#print b
	for j in range(len(var) - len(b) + 2):
		for k in range(len(tmp)):
			tmp[k] = tmp[k].subs(sym[j],0)
	
	for j in range(len(b)-2):
		for k in range(len(tmp)):
			tmp[k] = tmp[k].subs(sym[len(var) - len(b) + 2 + j], int(b[j+2]))

	for k in range(len(tmp)):
		#print int(tmp[k])%2,
		v.append(int(tmp[k])%2)

	#print v,
	#print b
	#print '\n'
	if v == lz:
		print b
############################################################################
############################################################################
############################################################################