SWC = swfconduit.swc
SRC = swfconduit
DOCPATH = docs

ifdef TARGET_PLAYER
    COMPC_FLAGS += -target-player $(TARGET_PLAYER)
endif
ifdef SWF_VERSION
    COMPC_FLAGS += -swf-version $(SWF_VERSION)
endif

swc : $(SWC)
docs : $(SRC)
	asdoc -source-path . -doc-sources swfconduit -output $(DOCPATH) \
	    -package swfconduit "An AS3 Flash socket server written in Python" \
	    -main-title="SwfConduit Client Documentation" \
	    -window-title="SwfConduit Documentation" \
	    -footer="(c) 2010-2012 Double Cluepon Software Corp."
clean : 
	-rm $(SWC)

$(SWC) : $(SRC)
	compc -include-sources $(SRC) $(COMPC_FLAGS) -output $(SWC)

