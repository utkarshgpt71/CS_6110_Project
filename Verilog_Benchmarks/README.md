## Description about the benchmarks

These benchmarks were provided courtesy of Dr. Priyank Kalla

The ver2poly.py script that takes these files as input was designed so that it can work with all the becnhmarks present in this directory.
The limitation of ver2poly.py restricts the kind of functions you can specify in an input .v file.

Namely, the verilog files supported right now can only have assign statements (they are sufficient to specify a datapath). Also operation like 
modulus, division, logical operators, bit slicing are not supported as of now. You can specify relational operators <,>,<=,>= in the conditionpart of the ternary operator (?:).

Please view antialias.v and saturate1.v 

In addition each .v file must have on "oldmiter(f,g)" command, where f and g are the outputs that you want to verify. Notice that oldmiter() is
not part of the verilog syntax.
