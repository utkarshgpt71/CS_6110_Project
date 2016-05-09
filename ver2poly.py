import sys
import time

input_file = sys.argv[1]
f = open(input_file,'r')

#print input_file

poly_file = input_file.split('/')
poly_file = poly_file[-1]
poly_file = list(poly_file)
del poly_file[-1] # Removing the .v part
del poly_file[-1] # Removing the .v part

poly_file = ''.join(poly_file)

# print poly_file
var_dir = {}
var = []
var_bw = []
func = []
func_m = []

cms = 0
line_no = 1

var_index = 0

for line in f.readlines():
	line = line.strip()
	if cms == 1:
		if line[len(line)-2:len(line)] == '*/':
			cms = 0 
	else:
		if line[0:2] == '/*':
			cms = 1
			continue
		
		if len(line) > 0:
			if line_no == 1:
				if line[0:6] == 'module':
					line_no += 1
					continue
				else:
					print 'Syntax Error'
					exit()


			line = line.split(';')
			line[:] = [x.strip() for x in line if x != '']

			for v_line in line:
				if v_line[0:4] == 'wire' or v_line[0:5] == 'input' or v_line[0:6] == 'output':
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

				elif v_line[0:6] == 'assign':
					print v_line


				elif v_line[0:8] == 'oldmiter':
					c1 = v_line.partition('(')[2]
					c1 = c1.strip(')')
					c2 = c1.split(',')[1].strip()
					c1 = c1.split(',')[0].strip()
					try:
						assert( var_bw[var_dir[c1]] == var_bw[var_dir[c2]] )
					except:
						print "Error in the oldmiter command"
						print "Might be due to bit-width mismatch of input arguments"
						exit()
					


					
print var_bw
print var
print var_dir
print len(var)	