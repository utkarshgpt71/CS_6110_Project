import sys
from sympy import *
from boolector import Boolector
import time
import parser
import hf
import copy

btor = Boolector();
btor.Set_opt("model_gen", 1)
btor.Set_opt("incremental", 1)

def sym2btor(function, var_dir, b_func, b_var, tmp, bw):
	
	function =  function.replace('-','+ -')
	function = function.split('+')
	function[:] = [x.strip() for x in function if x != '']
	b_func = btor.Const(0,bw+1) #Btor poly initialised to 0
	
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
		b_func = b_func + tmp
	return b_func

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
sym_v = []

for i in range(len(var)):
	sym_v.append(symbols(var[i]))

bw = max(mod)

for i in range(len(func)):
	func[i] = func[i]*(2**(bw-mod[i]))

############################################################################
############################# Boolector Part ###############################
############################################################################

#####################################
def lift(l_ast, prev_sol, m, J_eval):
	global bw
	global var_bw
	global func_m
	global sym_t_m
	global b_eqn
	global sym_v
	global tvar_dir
	global b_tvar
	global tmp
	global sol

	if m > bw:
		return

	func_m_eval = func_m
	for i in range(len(prev_sol)):
		func_m_eval = func_m_eval.subs(sym_v[i],prev_sol[i])

	eqn_m = func_m_eval + J_eval*sym_t_m*(2**(m-1))
	eqn = list(eqn_m)

	for i in range(len(eqn)):
		#print eqn[i]
		#print type(eqn[i])
		if hf.isint(eqn[i]):
			eqn[i] = int(eqn[i]) % 2**m
		else:
			eqn[i] = trunc(eqn[i],2**m)

	for i in range(len(eqn)):
		function = str(eqn[i])
		b_eqn[i] = sym2btor(function, tvar_dir, b_eqn[i], b_tvar, tmp, bw)

	for i in range(len(b_eqn)):
		btor.Assume(b_eqn[i] % (2**m) == 0)	

	for i in range(len(l_ast)):
		for j in range(len(l_ast[i])):
			btor.Assume(b_tvar[i] != l_ast[i][j])

	result = btor.Sat()

	if result != 10:
		return

	curr_sol = []
	for i in range(len(b_tvar)):
		j = int (b_tvar[i].assignment,2) 
		curr_sol.append(j)

	var_sol = []
	for i in range(len(b_tvar)):
		var_sol.append( prev_sol[i] + curr_sol[i]*(2**(m-1)) )

	#### Checking if current solution is actually valid ####	
	v = 1
	for i in range(len(var_sol)):
		if(var_sol[i] >= 2**var_bw[i]):
			v = 0
			break
	if v == 0:
		return
	########################################################
	
	sol[m-1].append(var_sol)	

	l_ast_tmp = []
	for i in range(len(b_tvar)):
		l_ast_tmp.append([])

	lift(l_ast_tmp, var_sol, m+1, J_eval)

	for i in range(len(curr_sol)):
		l_ast_ts = copy.deepcopy(l_ast)
		if i == 0:
			if curr_sol[i] not in l_ast_ts[i]:
				l_ast_ts[i].append(curr_sol[i])
			#print ast_ts
			lift(l_ast_ts, prev_sol, m, J_eval)
		else:
			if curr_sol[i] not in l_ast_ts[i]:
				l_ast_ts[i].append(curr_sol[i])
			for j in range(i):
				if (1-curr_sol[j]) not in l_ast_ts[j]:
					l_ast_ts[j].append( (1-curr_sol[j]) )
			#print ast_ts
			lift(l_ast_ts, prev_sol, m, J_eval)	

#####################################

#####################################
def solve(ast):
	global var
	global b_func
	global b_var
	global sol
	global btor
	global J
	global sym_v
	global b_tvar

	for i in range(len(b_func)):
		btor.Assume(b_func[i] % 2 == 0)

	for i in range(len(var)):
		btor.Assume(b_var[i] < 2)

	for i in range(len(ast)):
		for j in range(len(ast[i])):
			btor.Assume(b_var[i] != ast[i][j])

	result = btor.Sat()
	#print result
	curr_sol = []
	
	if result != 10:
		return

	for i in range(len(var)):
		j = int (b_var[i].assignment,2) 
		curr_sol.append(j)

	sol[0].append(curr_sol)

	J_eval = J
	for i in range(len(sym_v)):
		J_eval = J_eval.subs(sym_v[i],curr_sol[i])

	l_ast = []
	for i in range(len(b_tvar)):
		l_ast.append([])	

	lift(l_ast, curr_sol, 2, J_eval)

	for i in range(len(curr_sol)):
		ast_ts = copy.deepcopy(ast)
		if i == 0:
			if curr_sol[i] not in ast_ts[i]:
				ast_ts[i].append(curr_sol[i])
			#print ast_ts
			solve(ast_ts)
		else:
			if curr_sol[i] not in ast_ts[i]:
				ast_ts[i].append(curr_sol[i])
			for j in range(i):
				if (1-curr_sol[j]) not in ast_ts[j]:
					ast_ts[j].append( (1-curr_sol[j]) )
			#print ast_ts
			solve(ast_ts)

#####################################

b_var = []
var_dir = {}
for i in range(len(var)):
	b_var.append(btor.Var(bw+1 , var[i]))
	var_dir[var[i]] = i

#print var_dir	
####### Generating func in Boolector ########

b_func = []
tmp = btor.Var(bw+1 , 'tmp')

for i in range(len(func)): #Loop runs for all the polynomials
	b_func.append( btor.Var(bw+1 , 'f'+str(i+1)) )
	function = str(func[i])
	b_func[i] = sym2btor(function, var_dir, b_func[i], b_var, tmp, bw)
	
#############################################

######## Trying solving Mod 2 ###############
for i in range(len(var)):
	btor.Assume(b_var[i] < 2)

for i in range(len(b_func)):
	btor.Assume(b_func[i] % 2 == 0)

sol = []
for i in range(bw):
	sol.append([])	
	
#print sol
#exit()
result = btor.Sat()

ast = []
for i in range(len(var)):
	ast.append([])

if result != 10: #If no solution exists modulo 2
	print 'No solution mod 2'
	print 'The circuits are equivalent'
	exit()

####### Assertions for Non-invertible J ########
func_m = Matrix(func)
func_2 = []

for i in range(len(func)):
	func_2.append(trunc(func[i],2))
func_mj = Matrix(func_2)

J = func_mj.jacobian(sym_v)

if len(func) != len(var):
	je = 0
else:
	try:
		d = int(trunc(J.det(),2))
		if d == 0:
			je = 0
	except:
		je = 1

try:
	assert(je == 0)
except:
	print "The implementation only supports Case 2 of Hensel's Lemma for now"
	exit()
################################################

sym_t = []

for i in range(len(var)):
	sym_t.append(symbols('it' + str(i+1)))
sym_t_m = Matrix(sym_t)

b_tvar = []
tvar_dir = {}
for i in range(len(sym_t)):
	b_tvar.append(btor.Var(bw+1 , 'it' + str(i+1)))
	btor.Assert(b_tvar[i] < 2)
	tvar_dir['it' + str(i+1)] = i

b_eqn = []
for i in range(len(func)): #No. of equations = No. of functions
	b_eqn.append( btor.Var(bw+1 , 'eqn'+str(i+1)) )

solve(ast)
#print 'Solutions'
#print sol
hf.print_sol(var,sol)
#print var
#print sol

#############################################



############################################################################
############################################################################
############################################################################