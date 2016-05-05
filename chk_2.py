import sys
from sympy import *
import time


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

# def lift(sol, bw, func, J, var, ):


############################################################################
############################# Boolector Part ###############################
############################################################################

#####################################
def solve(ast):
	global var
	global b_func
	global b_var
	global sol_2
	global btor

	print ast

	for i in range(len(b_func)):
		btor.Assume(b_func[i] % 2 == 0)

	for i in range(len(var)):
		btor.Assume(b_var[i] < 2)

	for i in range(len(ast)):
		for j in range(len(ast[i])):
			btor.Assume(b_var[i] != ast[i][j])

	result = btor.Sat()
	print result
	curr_sol = []
	
	if result != 10:
		return

	for i in range(len(var)):
		j = int (b_var[i].assignment,2) 
		sol_2[i].append(j)
		curr_sol.append(j)

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
			for j in range(len(curr_sol)-1):
				if (1-curr_sol[i]) not in ast_ts[i]:
					ast_ts[i].append( (1-curr_sol[i]) )
			#print ast_ts
			solve(ast_ts)

#####################################

b_var = []
var_dir = {}
for i in range(len(var)):
	b_var.append(btor.Var(bw+1 , var[i]))
	#btor.Assert(b_var[i] < 2**var_bw[i])
	var_dir[var[i]] = i

#print var_dir	
####### Generating func in Boolector ########

b_func = []
tmp = btor.Var(bw+1 , 'tmp')

for i in range(len(func)): #Loop runs for all the polynomials
	b_func.append( btor.Var(bw+1 , 'f'+str(i)) )
	function = str(func[i])
	b_func[i] = sym2btor(function, var_dir, b_func[i], b_var, tmp, bw)
	
#############################################

############### Solving Mod 2################
for i in range(len(var)):
	btor.Assume(b_var[i] < 2)

for i in range(len(b_func)):
	btor.Assume(b_func[i] % 2 == 0)

sol_2 = []	
for i in range(len(var)):
	sol_2.append([])

result = btor.Sat()

ast = []
for i in range(len(var)):
#	sol_2[i].append(int (b_var[i].assignment,2) )
	ast.append([])

if result != 10:
	print 'No solution mod 2'
	print 'The circuits are equivalent'
	exit()

solve(ast)
print 'All solutions mod 2'
print sol_2
#print var
#print sol_2


# no_sol = 1
# while result == 10:
# 	no_sol = 0;
# 	for i in range(len(var)):
# 		print '%s = %d' %(var[i], int (b_var[i].assignment,2) ),
# 		sol_2[i].append(int (b_var[i].assignment,2))

# 	for i in range(len(b_func)):
# 		btor.Assume(b_func[i] % 2 == 0)

# 	for i in range(len(sol_2)):
# 		for j in range(len(sol_2[i])):
# 			btor.Assume(b_var[i] != sol_2[i][j])
# 	result = btor.Sat()
# 	print '\n'
# else:
# 	if no_sol:
# 		print 'No solution mod 2'
# 		print 'Circuits are equivalent'
# 	else:
# 		print 'All solution mod 2 found'
# 		#print sol_2

#############################################

##### Initializing the lifting equation #####
#print J
# try:
# 	J_inv = trunc(J,2)**-1
# 	je = 1
# except:
# 	je = 0

# if len(func) != len(var):
# 	je = 0
# else:
# 	try:
# 		d = int(trunc(J.det(),2))
# 		if d == 0:
# 			je = 0
# 	except
# print sol_2
# sol = sol_2

# T = []
# b_T = []
# T_dir = {}
# for i in range(len(var)):
# 	T.append(symbols('it' + str(i))) 
# 	b_T.append(btor.Var(bw+1 , 'it'+str(i)))
# 	T_dir['it'+str(i)] = i

# #print T
# T_m = Matrix(T)
# #print T_m
# #print func_m 
# eqn_sym = func_m + J*T_m
# print J.det()
# print eqn_sym
# eqn_sym = 
# if je == 0:
# 	for i in range(len(sol[0][0])):
# 		eqn_sym = 
#############################################

############################################################################
############################################################################
############################################################################