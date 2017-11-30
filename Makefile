.PHONY:run
run: Window.py
	./main.py

%.py : %.ui
	pyuic5 $< -o $@
