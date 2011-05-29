SWC = swfconduit.swc
SRC = swfconduit

swc : $(SWC)
clean : 
	-rm $(SWC)

$(SWC) : $(SRC)
	compc -include-sources $(SRC) -output $(SWC)

