/*
F1 = 3x^2 + 6xy + 18xz + 3y^2 + 18yz + 27z^2 + 43x + 43y + z
F1_equiv1 = 16x^6 + 240x^4 + 192x^3 + 67x^2 +  6xy + 18xz + 3y^2 + 18yz + 27z^2 + 43x + 43y + z
F1_equiv2 = 16y^6 + 240y^4 + 192y^3 + 3x^2 +  6xy + 18xz + 67y^2 + 18yz + 27z^2 + 43x + 43y + z


F2 = x^2 + 2xy + 6xz + y^2 + 6yz + 9z^2 + 43x + 43y + z
F2_eqiv1 = 16y^4 + 240y^4+192y^3+x^2 + 2xy + 6xz + 65y^2 + 6yz + 9z^2 + 43x + 43y + z
F2_eqiv2 = 16x^4 + 240x^4+192x^3+65x^2 + 2xy + 6xz + y^2 + 6yz + 9z^2 + 43x + 43y + z
*/

//F2_equiv2
module foo();
	input [7:0] x,y,z;
	wire [7:0] f;
	wire [7:0] g;
	assign f = x*x + 2*x*y + 6*x*z + y*y + 6*y*z + 9*z*z + 43*x + 43*y + z;
	assign g = 16*y*y*y*y + 240*y*y*y*y+192*y*y*y+x*x + 2*x*y + 6*x*z + 65*y*y + 6*y*z + 9*z*z + 43*x + 43*y + z;
	oldmiter(f,g);
endmodule