/*
14) RGB converter (n1=4,n2=4,n3=4, m1=10, m2= 11, m3 = 10,3var):
    Original: Y = 222*r^2+706*g+713*b^2
              Cr = 642*r+622*r^2+1603*g+1562*b^2
      Cb = 538*b+853*r^2+644*g+641*b^2
    Reduced: Y = 222*r^2+706*g+201*b^2+512*b
     Cr = 622*r^2+642*r+1603*g+538*b^2+1024*b
     Cb = 341*r^2+512*r+644*g+129*b^2+26*b    
    Vanishing: Y = 512*b^2+512*b
       Cr = 1024*b^2+1024*b
       Cb = 12*b+512*r^2+512*b^2+512*r
*/

module foo();
	wire [3:0] r;
	wire [3:0] g;
	wire [3:0] b;
	wire [9:0] Y1,Y2;
	assign Y1=222*r*r+706*g+713*b*b;
	assign Y2=222*r*r+706*g+201*b*b+512*b;
	oldmiter(Y1,Y2);
endmodule
