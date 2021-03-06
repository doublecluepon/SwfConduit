
SRC = swfconduit

swc :
	${MAKE} -f flex/Makefile swc

docs : server_docs client_docs

server_docs :
	cd docs; make html
	./docs/remove_underscore.sh ./docs/build/html

client_docs :
	cd flex; make docs

publish_docs : docs
	git add docs flex/docs
	-git ci -m'build documentation'
	git checkout gh-pages
	git checkout master flex/docs
	git checkout master docs
	git ci -am'build documentation'
	git push
	git checkout master

clean:
	cd flex; make clean
	cd docs; make clean
