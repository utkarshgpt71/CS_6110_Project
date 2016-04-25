from boolector import Boolector

btor = Boolector();
btor.Set_opt("model_gen", 1)
btor.Set_opt("incremental", 1)
print "Hello"

x = btor.Var(4, "x")
y = btor.Var(4, "y")

btor.Assert(x * y > 13)
btor.Assert(y < 4)

result = btor.Sat()

print type(x)
print type(y)

#print result

while (result == 10):
	print 'SAT'
	print int(x.assignment,2), 
	print int(y.assignment,2)
	x_val = int(x.assignment,2)
	y_val = int(y.assignment,2)
	btor.Assert(x != x_val)
	btor.Assert(y != y_val)
	result = btor.Sat()

print type(x_val)
print type(y_val)
print "UNSAT"
