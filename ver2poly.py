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
				print 'Ternary operator'
				
			else:
				poly = '%s - %s ; %d' %(out_var, poly_unp, mod)
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
			poly = 'it%d*(%s - %s) - %d ; %d' %(int_var_count, c1, c2, 2**(var_bw[var_dir[c1]]-1), var_bw[var_dir[c1]] )
			func.append(poly)
			var.append('it%d' %int_var_count)
			var_bw.append(var_bw[var_dir[c1]])
			var_dir[var[-1]] = var_index
			int_var_count += 1
			var_index += 1
			#print poly

f.close()					
print var_bw
print var
print var_dir
print len(var)
print func	

g = open(poly_file, 'w')

for i in range(len(var)):
	g.write('%s[%d:0]\n' %(var[i], var_bw[i]-1) )

g.write('\n')

for i in range(len(func)):
	g.write(func[i])
	g.write('\n')

g.close()

