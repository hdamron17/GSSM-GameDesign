.PHONY: clean package upload all

all:
	make clean
	make package
	make upload
	make clean

clean:
	rm -rf dist build *.egg-info

package:
	python3 setup.py sdist bdist_wheel --universal

upload:
	twine upload dist/*
