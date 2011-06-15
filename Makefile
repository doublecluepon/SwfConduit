
SRC = swfconduit

docs : server_docs client_docs

server_docs :
	cd docs; make html

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
