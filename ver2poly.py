import sys
import time
import subprocess

input_file = sys.argv[1]
f = open(input_file,'r')

cmd = 'mkdir -p Inter_Poly_Inputs'
subprocess.call(cmd,shell=True)
#print input_file

poly_file = input_file.split('/')
poly_file = poly_file[-1]
poly_file = list(poly_file)
del poly_file[-1] # Removing the .v part
del poly_file[-1] # Removing the .v part

poly_file = ''.join(poly_file)
poly_file = 'Inter_Poly_Inputs/' + poly_file + '.poly'

#print poly_file
var_dir = {}
var = []
var_bw = []
func = []
func_m = []

cms = 0
line_no = 1

var_index = 0
int_var_count = 0

def isint(v):
	try:
		int(v)
	except:
		return 0

	return 1

def conditionals(expr):
	global var_dir
	global var_bw
	global func
	global var
	global int_var_count
	global var_index

	#print 'Hello'
	if expr.find('<',0,len(expr)) != -1:
		co = '<'; ct = 1
	elif expr.find('>',0,len(expr)) != -1:
		co = '>' ; ct = 2
	elif expr.find('<=',0,len(expr)) != -1:
		co = '<=' ; ct = 3
	elif expr.find('>=',0,len(expr)) != -1:
		co = '>=' ; ct = 4

	expr1 = expr.split(co)
	c1 = expr1[0].strip()
	c2 = expr1[1].strip()

	a1 = 0; a2 = 0;

	if isint(c1):
		a1 = 1
	if isint(c2):
		a2 = 1

	if not a1 and not a2:
		try:
				assert( var_bw[var_dir[c1]] == var_bw[var_dir[c2]] )
		except:
			print "Error in the comparison command"
			print "Might be due to bit-width mismatch of input arguments"
			f.close()
			exit()
	

	mod = var_bw[var_dir[c1]]
	var.append('it%d' %int_var_count)
	var_bw.append(2)
	var_dir[var[-1]] = len(var)-1
	int_var_count += 1
	c = var[len(var)-1] 

	var.append('it%d' %int_var_count)
	var_bw.append(mod+1)
	var_dir[var[-1]] = len(var)-1
	int_var_count += 1
	t1 = var[len(var)-1]

	var.append('it%d' %int_var_count)
	var_bw.append(mod)
	var_dir[var[-1]] = len(var)-1
	int_var_count += 1
	t2 = var[len(var)-1]

	if ct == 1: # less than
		poly = '%s - (%s - %s) ; %d' %(t1,c1,c2,mod+1)
		func.append(poly)
		poly = '%s - ( (1-%s)*%s + %s*(%d - 1 - %s) ) ; %d' %(t1,c,t2,c,(2**(mod+1)),t2,mod+1)
		func.append(poly)

	elif ct == 2: # greater than
		poly = '%s - (%s - %s - 1) ; %d' %(t1, c1, c2, mod+1)
		func.append(poly)
		poly = '%s - ( %s*%s + (1-%s)*(%d - 1 - %s) ) ; %d' %(t1,c,t2,c,(2**(mod+1)),t2,mod+1)
		func.append(poly)
	
	elif ct == 3: #less than or equal to
		poly = '%s - (%s - %s) ; %d' %(t1,c1,c2,mod+1)
		func.append(poly)
		poly = '%s - ( %s*%s + (1-%s)*(%d - 1 - %s) ) ; %d' %(t1,c,t2,c,(2**(mod+1)),t2,mod+1)
		func.append(poly)

	elif ct == 4:
		poly = '%s - (%s - %s - 1) ; %d' %(t1, c1, c2, mod+1)
		func.append(poly)
		poly = '%s - ( (1-%s)*%s + %s*(%d - 1 - %s) ) ; %d' %(t1,c,t2,c,(2**(mod+1)),t2,mod+1)
		func.append(poly)
	return ( len(var) - 3 )



for line in f.readlines():
	line = line.strip()

	if line[0:2] == '//':
		continue

	if cms == 1:
		if line[len(line)-2:len(line)] == '*/':
			cms = 0 
		else:
			continue
	else:
		if line[0:2] == '/*':
			cms = 1
			continue
		
		# if len(line) > 0:
		# 	if line_no == 1:
		# 		if line[0:6] == 'module':
		# 			line_no += 1
		# 			continue
		# 		else:
		# 			print 'Syntax Error'
		# 			exit()


	line = line.split(';')
	line[:] = [x.strip() for x in line if x != '']

	for v_line in line:
		if v_line[0:4] == 'wire' or v_line[0:5] == 'input' or v_line[0:6] == 'output': # Parsing in all the variables
			rng = v_line.partition('[')[2]
			rng = rng.partition(']')[0]
			msb = int(rng.split(':')[0].strip())
			lsb = int(rng.split(':')[1].strip())
			bw = abs(msb - lsb + 1)
			vl = v_line.partition(']')[-1].strip()
			vl = vl.split(',')
			vl[:] = [x.strip() for x in vl]
			for i in range(len(vl)):
				var_bw.append(bw)
				var.append(vl[i])
				var_dir[vl[i]] = var_index
				var_index += 1

		elif v_line[0:6] == 'assign': # Parsing in all the assign commands
			out_var = v_line.split('=')
			poly_unp = out_var[1]
			out_var = out_var[0]
			out_var = out_var.replace('assign',' ').strip()
			mod = var_bw[ var_dir[out_var] ]
			if poly_unp.find('<<',0,len(poly_unp)) != -1:
				print 'Left Shift not supported'
				f.close()
				exit()
			elif poly_unp.find('>>',0,len(poly_unp)) != -1:
				f.close()
				exit()
				print 'Right Shift not supported'
			elif poly_unp.find('/',0,len(poly_unp)) != -1:
				f.close()
				exit()
				print 'Division not supported'
			elif poly_unp.find('==',0,len(poly_unp)) != -1:
				f.close()
				exit()
				print 'Equivalence operator not supported'
			elif poly_unp.find('%',0,len(poly_unp)) != -1:
				f.close()
				exit()
				print 'Modulus not supported'
			elif poly_unp.find('?',0,len(poly_unp)) != -1 and poly_unp.find(':',0,len(poly_unp)):
				expr = poly_unp.split('?')[0].strip()
				expr = expr.strip(')').strip()
				expr = expr.strip('(').strip()
				c_index = conditionals(expr)
				IF = poly_unp.split('?')[1]
				ELSE = IF.split(':')[1]
				IF = IF.split(':')[0]
				poly = '%s - %s*(%s) - (1-%s)*%s ; %d' %(out_var, var[c_index],IF, var[c_index], ELSE, mod)
				func.append(poly)

			else:
				poly = '%s - (%s) ; %d' %(out_var, poly_unp, mod)
				func.append(poly)



		elif v_line[0:8] == 'oldmiter': # Parsing in the oldmiter command
			c1 = v_line.partition('(')[2]
			c1 = c1.strip(')')
			c2 = c1.split(',')[1].strip()
			c1 = c1.split(',')[0].strip()
			try:
				assert( var_bw[var_dir[c1]] == var_bw[var_dir[c2]] )
			except:
				print "Error in the oldmiter command"
				print "Might be due to bit-width mismatch of input arguments"
				f.close()
				exit()
			
			var.append('it%d' %int_var_count)
			var_bw.append(var_bw[var_dir[c1]])
			var_dir[var[-1]] = len(var)-1
			poly = 'it%d*(%s - %s) - %d ; %d' %(int_var_count, c1, c2, 2**(var_bw[var_dir[c1]]-1), var_bw[var_dir[c1]] )
			int_var_count += 1
			func.append(poly)
			#var_index += 1
			#print poly

f.close()					
#print var_bw
#print var
#print var_dir
#print len(var)
#print func	

g = open(poly_file, 'w')

for i in range(len(var)):
	g.write('%s[%d:0]\n' %(var[i], var_bw[i]-1) )

g.write('\n')

for i in range(len(func)):
	g.write(func[i])
	g.write('\n')

g.close()

