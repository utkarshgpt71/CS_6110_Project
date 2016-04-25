# CS 6110 Project

Author: Utkarsh Gupta

Affiliation: University of Utah 

Application: Verification of Arithmetic Datapaths.

I. Boolector Python API:

Please follow the following steps for installing the Boolector Python API:

	1. Download Boolector 2.2.0 Package from http://fmv.jku.at/boolector/

	2. Unzip the package and change directory to boolector-2.2.0-with-lingeling-bal

	3. run "make"

	4. change directory to lingeling 

	5. run "./configure -fPIC" and then "make"

	6. change directory to boolector from the previous directory i.e. "cd ../boolector"

	7. run "./configure -python && make" .  If you get the error No module named Cython.Distutils, perform the following steps to install Cython. Otherwise proceed to step 8.
		7.1 Download the Cython package from http://cython.org/#download

		7.2 Unzip and install it using "sudo python setup.py install"

		7.3 Run the command "sudo python -c 'import Cython.Distutils"

		7.4 Go back to step 6.

	8. You should receive a message "Compiled Boolector Python module. Please read api/python/README on how to use the module"

	9. Add the current directory to PYTHONPATH
	
