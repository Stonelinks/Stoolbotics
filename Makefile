.PHONY: win

win:
	@rm -rf stoolsim &
	@sleep 1
	@mkdir stoolsim
	@mkdir stoolsim/simulator
	@mkdir stoolsim/docs
	@mkdir stoolsim/robots
	
	@cd simulator && python setup.py py2exe && cd ..
	
	@cp simulator/dist/stoolbotics.bat stoolsim
	@cp simulator/dist/README.txt stoolsim
	@cp -r simulator/dist/* stoolsim/simulator
	@cp -r robots/* stoolsim/robots
	@cp -r docs/* stoolsim/docs
	@alzip -a stoolsim simulator.zip
	@rm -rf stoolsim
	@rm -rf simulator/build
	@cp simulator.zip "C:\Documents and Settings\ld\My Documents\Dropbox\Public\simulator.zip"
	
	
	