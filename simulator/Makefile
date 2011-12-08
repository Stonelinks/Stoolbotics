.PHONY: win

win:
	@python setup.py py2exe
	@cp -r ../robots/* dist/robots
	@mkdir simulator
	@cp -r dist/* simulator
	@rm builds/simulator.zip &
	@alzip -a simulator builds/simulator.zip
	@rm -rf simulator
	@rm -rf build
	@cp builds/simulator.zip "C:\Documents and Settings\ld\My Documents\Dropbox\Public\simulator.zip"