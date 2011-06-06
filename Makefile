
SRC = swfconduit

docs : $(SRC)
	cd docs; make html
	cd flex; make docs
