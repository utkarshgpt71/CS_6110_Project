## Description of .poly file format

If your set of equations have n variables, then use the first n lines to write their name and bit-width. For example if you have a variable 'x' of bit-width 2 in your equations, then you can mention it as

x[1:0]

After writing down all the variables, specify the equations and their moduli. For example, if there is a equation in x and y with a modulus 3, you can specify as

x\**2 + 3\*y ; 3

Use semicolon to separate the actaul equation and its modulus. ** is the symbol for exponent. Also the equation will be treated equivalent to 0 mod 3. So transform all your equations accordingly before writing them down in this file.

View one of the .poly files in this directory to understand the format better.
