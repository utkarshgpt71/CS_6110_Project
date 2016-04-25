from boolector import Boolector

btor = Boolector();
btor.Set_opt("model_gen", 1)
btor.Set_opt("incremental", 1)
print "Hello"

var = []
bit = 4
var.append(btor.Var(bit, 'x'))
var.append(btor.Var(bit, 't1'))
var.append(btor.Var(bit, 'F'))
var.append(btor.Var(bit, 't2'))
var.append(btor.Var(bit, 'G'))
var.append(btor.Var(bit, 't'))
#var.append(btor.Var(2, 'z'))

btor.Assert(var[0] < 4)
btor.Assert(var[1] < 4)
btor.Assert(var[2] < 8)
btor.Assert(var[3] < 4)
btor.Assert(var[4] < 8)
btor.Assert(var[5] < 8)


btor.Assert( (2*var[0]*var[0] - 2*var[1]) % 8 == 0)
btor.Assert( (var[1] + var[0] - var[2]) % 8 == 0)
btor.Assert( (2*var[0] + 2 - 2*var[3]) % 8 == 0)
btor.Assert( (var[3]*var[0] - var[4]) % 8 == 0)
btor.Assert( (var[5]*(var[2] - var[4]) - 4) % 8 == 0)

result = btor.Sat()

#print type(var[0])
#print type(var[1])

#print result

while (result == 10):
	print 'SAT'
	print 'x = %d' %int(var[0].assignment,2),
	print 't1 = %d' %int(var[1].assignment,2), 
	print 'F = %d' %int(var[2].assignment,2),
	print 't2 = %d' %int(var[3].assignment,2),
	print 'G = %d' %int(var[4].assignment,2),
	print 't = %d' %int(var[5].assignment,2)
	
	x_val = int(var[0].assignment,2)
	t1_val = int(var[1].assignment,2)
	F_val = int(var[2].assignment,2)
	t2_val = int(var[3].assignment,2)
	G_val = int(var[4].assignment,2)
	t_val = int(var[5].assignment,2)

	btor.Assert(var[0] != x_val)
	btor.Assert(var[1] != t1_val)
	btor.Assert(var[2] != F_val)
	btor.Assert(var[3] != t2_val)
	btor.Assert(var[4] != G_val)
	btor.Assert(var[5] != t_val)
	result = btor.Sat()

#print type(x_val)
#print type(y_val)
print "UNSAT"
