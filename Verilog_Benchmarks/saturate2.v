
//should be the same as saturate1, written slightly differently

module saturating_add(x,y,f,g);

	input [5:0] x,y;
	output [5:0] f,g;
	wire [5:0] x2,y2,xy2;
	wire [6:0] sum1;
	wire [7:0] sum2;
	wire [5:0] sat1;

	//f = (x+y)^2
	assign sum1=x+y;
	assign sat1=(sum1>63) ? 63 : sum1;
	assign f=sat1*sat1;

	//g = x^2 + y^2 + 2xy
	assign x2=x*x;
	assign y2=y*y;
	assign xy2=2*x*y;
	assign sum2=x2+y2+xy2;
	assign g=(sum2>63) ? 63 : sum2;

	oldmiter(f,g);

endmodule
