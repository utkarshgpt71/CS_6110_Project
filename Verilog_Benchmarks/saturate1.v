module saturating_add(x,y,f,g);

	input [5:0] x,y;
	output [5:0] f,g;
	wire [5:0] x2,y2, xy2,sum1,sum2,sum3,sat1,sat2;

	//f = (x+y)^2
	assign sum1=x+y;
	assign sat1=(sum1<x) ? -1 : sum1;
	assign f=sat1*sat1;

	//g = x^2 + y^2 + 2xy
	assign x2=x*x;
	assign y2=y*y;
	assign xy2=2*x*y;
	assign sum2=x2+y2;
	assign sat2=(sum2<x2) ? -1 : sum2;
	assign sum3=sat2+xy2;
	assign g=(sum3<sum2) ? -1 : sum3;

	oldmiter(f,g);

endmodule
