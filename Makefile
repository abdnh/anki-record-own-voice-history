.PHONY: all zip clean install

all: zip

PACKAGE_NAME := record_own_voice_history

zip: $(PACKAGE_NAME).ankiaddon

$(PACKAGE_NAME).ankiaddon: src/*
	rm -f $@
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

# install in test profile
install: zip
	mkdir -p ankiprofile/addons21/$(PACKAGE_NAME)
	unzip -o $(PACKAGE_NAME).ankiaddon -d ankiprofile/addons21/$(PACKAGE_NAME)

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f $(PACKAGE_NAME).ankiaddon
