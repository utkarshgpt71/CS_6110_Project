# CS 6110 Project

Author: Utkarsh Gupta

Affiliation: University of Utah 

Application: Verification of Arithmetic Datapaths.

## I. Boolector Python API

Please follow the following steps for installing the Boolector Python API:

	1. Download Boolector 2.2.0 Package from http://fmv.jku.at/boolector/

	2. Unzip the package and change directory to boolector-2.2.0-with-lingeling-bal

	3. run "make"

	4. change directory to lingeling 

	5. run "./configure -fPIC" and then "make"

	6. change directory to boolector from the previous directory (i.e. "cd ../boolector")

	7. run "./configure -python && make" .  If you get the error No module named Cython.Distutils, perform the following steps to install Cython. Otherwise proceed to step 8.
		7.1 Download the Cython package from http://cython.org/#download

		7.2 Unzip and install it using "sudo python setup.py install"

		7.3 Run the command "sudo python -c 'import Cython.Distutils"

		7.4 Go back to step 6.

	8. You should receive a message "Compiled Boolector Python module. Please read api/python/README on how to use the module"

	9. Add the current directory to PYTHONPATH

## II. Files/Directories in this repository

Following is a brief description of Files and Directories in this Repository:

	1. Misc: Contains some simple experiment (in python) that I used while woking on the implementation (you can try them if you want ; but not part of actual project)

	2. Poly_Inputs: Contains some .poly files that are fed as input to the python script, poly_solver.py. Also contains a README for description about the format of .poly files.

	3. Verilog_Benchmarks: Contains some verilog benchmarks that are fed as input to the python script ver2poly.py. Also contains a README for description about the format of .v files.

	4. poly_solver.py: Takes in a .poly file that has specification of the polynomials and variables. This script solves the set of equations using the Hensel's Lemma. Returns message to indicate whether the set of equations have a solution. Can be executed as follows:

	python poly_solver.py Poly_Inputs/<filename>.poly

	5. ver2poly: Converts the .v files in Verilog_Benchmarks to .poly format and writes them in a directory Inter_Poly_Inputs. This script has a very limited support for the types of operators mentioned in the .v files. Can be executes as follows:

	python ver2poly.py Verilog_Benchmarks/<filename>.v

	Although this script works fine for the benchmarks given in Verilog_benchmarks, due to time constraints for the project the script has not been tested for other verilog benchmarks and it might be buggy. 
	If the .v file has few variabels and assign statements, consider writing its .poly instead. 

	6. chk_2.py: Was used to check the solutions generated. Not part of the project.

	
	
