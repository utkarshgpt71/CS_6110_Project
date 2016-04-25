from boolector import Boolector

btor = Boolector();
btor.Set_opt("model_gen", 1)
btor.Set_opt("incremental", 1)
print "Hello"

var = []
bit = 4
var.append(btor.Var(bit, 'x'))
var.append(btor.Var(bit, 'y'))
#var.append(btor.Var(2, 'z'))

btor.Assert((var[0] + var[1])%15 == 0)
#btor.Assert(var[1] < 4)

result = btor.Sat()

print type(var[0])
print type(var[1])

#print result

while (result == 10):
	print 'SAT'
	print int(var[0].assignment,2), 
	print int(var[1].assignment,2)
	x_val = int(var[0].assignment,2)
	y_val = int(var[1].assignment,2)
	btor.Assert(var[0] != x_val)
	btor.Assert(var[1] != y_val)
	result = btor.Sat()

#print type(x_val)
#print type(y_val)
print "UNSAT"
