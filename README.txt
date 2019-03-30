pip install virtualenv

start virtual environment
	source env/bin/activate

close virtual environment
	deactivate

to update requirements after installing a package
	pip freeze > requirements.txt

to install requirements on virtual environment
	pip install -r requirements.txt

nohup python main.py > my.log 2>&1 & echo $! > save_pid.txt
