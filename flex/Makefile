SWC = swfconduit.swc
SRC = swfconduit
DOCPATH = docs

swc : $(SWC)
docs : $(SRC)
	asdoc -source-path . -doc-sources swfconduit -output $(DOCPATH) \
	    -package swfconduit "An AS3 Flash socket server written in Python" \
	    -main-title="SwfConduit Client Documentation" \
	    -window-title="SwfConduit Documentation" \
	    -footer="(c) 2010-2011 Double Cluepon Software Corp."
clean : 
	-rm $(SWC)

$(SWC) : $(SRC)
	compc -include-sources $(SRC) -output $(SWC)

