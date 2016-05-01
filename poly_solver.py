import sys
from sympy import *
from boolector import Boolector
import time
import parser
import hf

btor = Boolector();
btor.Set_opt("model_gen", 1)
btor.Set_opt("incremental", 1)


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
############################################################################
############################################################################
############################################################################
#print var_bw
#print func
sym = []

for i in range(len(var)):
	sym.append(symbols(var[i]))
func_m = Matrix(func)

bw = max(mod)

for i in range(len(func)):
	func[i] = func[i]*(2**(bw-mod[i]))
#print func
#print sym
func_m = Matrix(func)
J = func_m.jacobian(sym)
print J

############################################################################
############################# Boolector Part ###############################
############################################################################
b_var = []
var_dir = {}
for i in range(len(var)):
	b_var.append(btor.Var(bw+1 , var[i]))
	btor.Assert(b_var[i] < 2**var_bw[i])
	var_dir[var[i]] = i

#print var_dir	
####### Generating func in Boolector ########

b_func = []
tmp = btor.Var(bw+1 , 'tmp')

for i in range(len(func)): #Loop runs for all the polynomials
	b_func.append( btor.Var(bw+1 , 'f'+str(i)) )
	function = str(func[i])
	function =  function.replace('-','+ -')
	function = function.split('+')
	function[:] = [x.strip() for x in function if x != '']
	b_func[i] = 0 #Btor poly initialised to 0
	
	for mon in function: #Loop runs for all the monomials in the current function
		if mon[0] == '-': #If the monomial is negative
			minus = 1
			mon = list(mon)
			del mon[0]
			mon = ''.join(mon)
		else:
			minus = 0
		
		tmp = 1
		mon = mon.split('**')
		if len(mon) == 1: #No exponentiated variables
			mon = mon[0].split('*')
			for t in mon:
				if hf.isint(t):
					tmp = tmp * int(t.strip())
				else:
					tmp = tmp * b_var[var_dir[t.strip()]]
		else: #Exponentiated variables
			p_mon_1 = mon[0].split('*')
			p_mon_2 = mon[1].split('*')
			for j in range(int(p_mon_2[0].strip())-1):
				tmp = tmp * b_var[var_dir[p_mon_1[-1].strip()]]

			for t in p_mon_1:
				if hf.isint(t):
					tmp = tmp * int(t.strip())
				else:
					tmp = tmp * b_var[var_dir[t.strip()]]
			k = 0		
			for t in p_mon_2:
				if k != 0:
					if hf.isint(t):
						tmp = tmp * int(t.strip())
					else:
						tmp = tmp * b_var[var_dir[t.strip()]]
				k = 1
		if minus: #Complements the monomial
			tmp = - tmp
		b_func[i] = b_func[i] + tmp

#############################################

############### Solving Mod 2################
for i in range(len(b_func)):
	btor.Assume(b_func[i] % 8 == 0)

sol_2 = []	
for i in range(len(var)):
	sol_2.append([])

result = btor.Sat()
no_sol = 1
while result == 10:
	no_sol = 0;
	for i in range(len(var)):
		print '%s = %d' %(var[i], int (b_var[i].assignment,2) ),
		sol_2[i].append(int (b_var[i].assignment,2))

	for i in range(len(b_func)):
		btor.Assume(b_func[i] % 8 == 0)

	for i in range(len(sol_2)):
		for j in range(len(sol_2[i])):
			btor.Assume(b_var[i] != sol_2[i][j])
	result = btor.Sat()
	print '\n'
else:
	if no_sol:
		print 'No solution mod 2'
		print 'Circuits are equivalent'
	else:
		print 'All solution mod 2 found'
		print sol_2

#############################################

############################################################################
############################################################################
############################################################################