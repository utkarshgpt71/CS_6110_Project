/*
13) IRR(n1=16,n2=8,m=16,2 var)
    Original: 16384*x^4+16384*y^4+57344*x^2*y+8192*x*y^2+64767*x^2+769*y^2+x+65535*y
    Reduced: 24576*x^2*y + 15615*x^2 + 8192*x*y^2 + 32768*x*y + x + 17153*y^2 + 65535*y
    Vanishing: 16384(x^4 + y^4) + 32768*x*y (x + 1) + 49152(x^2 + y^2)
*/

module foo();
	wire [15:0] x;
	wire [7:0] y;
	wire [15:0] f;
	wire [15:0] g;
	assign f=16384*x*x*x*x+16384*y*y*y*y+57344*x*y*y+8192*x*y*y+64767*x*x+769*y*y+x+65535*y;
	assign g=24576*x*x*y + 15615*x*x + 8192*x*y*y + 32768*x*y + x + 17153*y*y + 65535*y;
	oldmiter(f,g);
endmodule
