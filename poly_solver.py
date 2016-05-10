import sys
from sympy import *
from boolector import Boolector
import time
import copy

btor = Boolector();
btor.Set_opt("model_gen", 1)
btor.Set_opt("incremental", 1)

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
	print '\n'

def isinvertible(J_eval):
	global func
	global var

	if len(func) != len(var):
		return 0
	else:
		if isint(J_eval.det()):
			d = int(J_eval.det())%2
		else:
			d = int(trunc(J_eval.det(),2))

		if d == 0:
			return 0
		else:
			return 1

def invert_mod2(J_eval):
	global func
	global var

	J_inv = J_eval**-1
	J_inv = J_inv * J_eval.det()
	J_elm = list(J_inv)

	for i in range(len(func)): #Making sure that the inverse is reduced modulo 2
		J_row = []
		for j in range(len(var)):
			if isint(J_elm[ i*len(var) + j ]):
				J_elm[i*len(var) + j] = int(J_elm[i*len(var) + j]) % 2
			else:
				J_elm[i*len(var) + j] = trunc(J_elm[i*len(var) + j],2)
			J_row.append(J_elm[i*len(var) + j])
		if i == 0:
			J_inv = Matrix([J_row])
		else:
			J_inv = J_inv.row_insert(i, Matrix([J_row]))
	
	return J_inv


def sym2btor(function, var_dir, b_func, b_var, tmp, cm):
	
	function =  function.replace('-','+ -')
	function = function.split('+')
	function[:] = [x.strip() for x in function if x != '']
	b_func = btor.Const(0,cm+1) #Btor poly initialised to 0
	
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
				if isint(t):
					tmp = tmp * int(t.strip())
				else:
					tmp = tmp * b_var[var_dir[t.strip()]]
		else: #Exponentiated variables
			p_mon_1 = mon[0].split('*')
			p_mon_2 = mon[1].split('*')
			for j in range(int(p_mon_2[0].strip())-1):
				tmp = tmp * b_var[var_dir[p_mon_1[-1].strip()]]

			for t in p_mon_1:
				if isint(t):
					tmp = tmp * int(t.strip())
				else:
					tmp = tmp * b_var[var_dir[t.strip()]]
			k = 0		
			for t in p_mon_2:
				if k != 0:
					if isint(t):
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
	line = line.strip()
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

sym_v = []

for i in range(len(var)):
	sym_v.append(symbols(var[i]))

cm = max(mod)

for i in range(len(func)):
	func[i] = func[i]*(2**(cm-mod[i]))

############################################################################
############################################################################
############################################################################	

############################################################################
############################# Boolector Part ###############################
############################################################################

#####################################
def lift(l_ast, prev_sol, m, J_eval, J_inv, inv):
	global cm
	global var_bw
	global func_m
	global sym_t_m
	global b_eqn
	global sym_v
	global tvar_dir
	global b_tvar
	global tmp
	global sol

	if m > cm: #Check if the lifting is being performed beyond the composite moduli
		return

	func_m_eval = func_m
	for i in range(len(prev_sol)): #Evaluating the function vector at the prev sol
		func_m_eval = func_m_eval.subs(sym_v[i],prev_sol[i])

	##################### If the J inverse exists ###########################
	if inv == 1: 
		print 'Inverse Exists'
		for i in range(len(func_m_eval)):
			func_m_eval[i] = func_m_eval[i]/(2**(m-1))
		T = -J_inv*(func_m_eval)
		curr_sol = list(T)
		curr_sol[:] = [int(c)%2 for c in curr_sol]
		var_sol = []
		for i in range(len(curr_sol)):
			var_sol.append( prev_sol[i] + curr_sol[i]*(2**(m-1)) )

		v = 1
		for i in range(len(var_sol)):
			if(var_sol[i] >= 2**var_bw[i]):
				v = 0
				break
		if v == 1: #Adding only valid solutions and trying to lift them
			sol[m-1].append(var_sol)
			if m == cm:
				print '\nCirciuts are not equivalent for the following solution set:\n'
				print var
				print sol[m-1][0]
				print '\nSolution space explored so far'
				print_sol(var,sol)
				exit()
			l_ast_tmp = []
			for i in range(len(b_tvar)):
				l_ast_tmp.append([])

			lift(l_ast_tmp, var_sol, m+1, J_eval, J_inv, 1) #Subsequent Lifts
	#########################################################################

	eqn_m = func_m_eval + J_eval*sym_t_m*(2**(m-1))
	eqn = list(eqn_m)

	for i in range(len(eqn)):
		if isint(eqn[i]):
			eqn[i] = int(eqn[i]) % 2**m
		else:
			eqn[i] = trunc(eqn[i],2**m)

	for i in range(len(eqn)):
		function = str(eqn[i])
		b_eqn[i] = sym2btor(function, tvar_dir, b_eqn[i], b_tvar, tmp, cm)

	for i in range(len(b_eqn)):
		btor.Assume(b_eqn[i] % (2**m) == 0)	

	for i in range(len(l_ast)):
		for j in range(len(l_ast[i])):
			btor.Assume(b_tvar[i] != l_ast[i][j])

	## OPTIMIZATION ##
	for i in range(len(b_tvar)):
		if m > var_bw[i]:
			btor.Assume(b_tvar[i] == 0) 
	##################

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
	if v == 1:
		sol[m-1].append(var_sol)
		if m == cm:
			print '\nCirciuts are not equivalent for the following solution set:\n'
			print var
			print sol[m-1][0]
			print '\nSolution space explored so far'
			print_sol(var,sol)
			exit()
	########################################################
	
	if v == 1: #Try lifting the solution only if it is valid
		l_ast_tmp = []
		for i in range(len(b_tvar)):
			l_ast_tmp.append([])

		lift(l_ast_tmp, var_sol, m+1, J_eval, [], 0) #Subsequent Lifts

	#If the current solution is not valid try finding other solutions
	for i in range(len(curr_sol)):
		l_ast_ts = copy.deepcopy(l_ast)
		if i == 0:
			if curr_sol[i] not in l_ast_ts[i]:
				l_ast_ts[i].append(curr_sol[i])
			#print ast_ts
			lift(l_ast_ts, prev_sol, m, J_eval, [], 0)
		else:
			if curr_sol[i] not in l_ast_ts[i]:
				l_ast_ts[i].append(curr_sol[i])
			for j in range(i):
				if (1-curr_sol[j]) not in l_ast_ts[j]:
					l_ast_ts[j].append( (1-curr_sol[j]) )
			#print ast_ts
			lift(l_ast_ts, prev_sol, m, J_eval, [], 0)	

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
	if cm == 1:
		print '\nCirciuts are not equivalent for the following solution set:\n'
		print var
		print sol[m-1][0]
		print '\nSolution space explored so far:'
		print_sol(var,sol)
		exit()

	J_eval = J
	for i in range(len(sym_v)):
		J_eval = J_eval.subs(sym_v[i],curr_sol[i])

	l_ast = []
	for i in range(len(b_tvar)):
		l_ast.append([])	

	#print 'In solve'
	#print var
	#print curr_sol

 	if isinvertible(J_eval): # Lifting the current solution
		J_inv = invert_mod2(J_eval)
		lift(l_ast, curr_sol, 2, J_eval, J_inv, 1)
	else:
		lift(l_ast, curr_sol, 2, J_eval, [], 0)

	for i in range(len(curr_sol)):
		ast_ts = copy.deepcopy(ast)
		if i == 0:
			if curr_sol[i] not in ast_ts[i]:
				ast_ts[i].append(curr_sol[i])
			solve(ast_ts)
		else:
			if curr_sol[i] not in ast_ts[i]:
				ast_ts[i].append(curr_sol[i])
			for j in range(i):
				if (1-curr_sol[j]) not in ast_ts[j]:
					ast_ts[j].append( (1-curr_sol[j]) )
			solve(ast_ts)

#####################################

b_var = []
var_dir = {}
for i in range(len(var)):
	b_var.append(btor.Var(cm+1 , var[i]))
	var_dir[var[i]] = i

####### Generating func in Boolector ########

b_func = []
tmp = btor.Var(cm+1 , 'tmp')

for i in range(len(func)): #Loop runs for all the polynomials
	b_func.append( btor.Var(cm+1 , 'func'+str(i+1)) )
	function = str(func[i])
	b_func[i] = sym2btor(function, var_dir, b_func[i], b_var, tmp, cm)
	
#############################################

######## Trying solving Mod 2 ###############
for i in range(len(var)):
	btor.Assume(b_var[i] < 2)

for i in range(len(b_func)):
	btor.Assume(b_func[i] % 2 == 0)

sol = []
for i in range(cm):
	sol.append([])	
	
result = btor.Sat()

ast = []
for i in range(len(var)):
	ast.append([])

if result != 10: #If no solution exists modulo 2
	print 'No solution mod 2'
	print 'The circuits are equivalent'
	exit()

#################### Setting up J #############
func_m = Matrix(func)

J = func_m.jacobian(sym_v)
J_elm = list(J)

for i in range(len(func)):
	J_row = []
	for j in range(len(var)):
		if isint(J_elm[ i*len(var) + j ]):
			J_elm[i*len(var) + j] = int(J_elm[i*len(var) + j]) % 2
		else:
			J_elm[i*len(var) + j] = trunc(J_elm[i*len(var) + j],2)
		J_row.append(J_elm[i*len(var) + j])
	if i == 0:
		J = Matrix([J_row])
	else:
		J = J.row_insert(i, Matrix([J_row]))
	
################################################

sym_t = []

for i in range(len(var)):
	sym_t.append(symbols('var_t' + str(i+1)))
sym_t_m = Matrix(sym_t)

b_tvar = []
tvar_dir = {}
for i in range(len(sym_t)):
	b_tvar.append(btor.Var(cm+1 , 'var_t' + str(i+1)))
	btor.Assert(b_tvar[i] < 2)
	tvar_dir['var_t' + str(i+1)] = i

b_eqn = []
for i in range(len(func)): #No. of equations = No. of functions
	b_eqn.append( btor.Var(cm+1 , 'eqn'+str(i+1)) )

solve(ast)
print '\nCircuits are equivalent\n'
print 'Solution space explored:'
print_sol(var,sol)

#############################################

############################################################################
############################################################################
############################################################################