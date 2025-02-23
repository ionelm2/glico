Links:
	https://github.com/taptorestart/python-backend-examples
	https://flask.palletsprojects.com/en/stable/
	https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

Concept:
	- Backend:
		- Flask based server + relational Database
		
	- Frontend:
		- need to find a cross-platform framework (Android + Windows)
		- create app that makes calls to Backend to retrieve data and update data to DB


Backend:
	- Environment:
		- WSL (Ubuntu)
		- install venv:
			- python3 -m venv venv
		

Commands
	- Backend
		- /mnt/g/work/glico/backend$ source venv/bin/activate
		- flask run
	- clear database
		- (venv) $ flask db downgrade base
		- (venv) $ flask db upgrade
	- update database (i.e., in case a new table is created)
		- (venv) $ flask db migrate
		- (venv) $ flask db upgrade
	- activate virtual environment
		- source venv/bin/activate
		
	
DB schema:
	https://sql.toad.cz/?
	
