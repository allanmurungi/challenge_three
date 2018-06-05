Maintenance Tracker App

Maintenance-tracker is a web application that enables users log maintenance/repair requests
to the maintenance-department and monitor the status of their requests.

Features:


1. Users make maintenance/repair requests and track them.
2. Admin updates the status of the request to either approve/reject.
3. Admin will mark request as resolved when it is done.
4. Admin can filter requests based on different criteria.


Getting Started


Clone the repo https://github.com/allanmurungi/challenge_three


Prerequisites

You will need the following.


1. Python 
2. Flask which is a micro web framework for python.
3. Pytest which is  a python testing library.
4. Pytest coverage which is a test coverage tool
5-pip

 Installing

Set up your development environment.


1. Download and Install [Python](https://www.python.org/downloads/)

2.In the terminal,navigate  to the project folder and create a virtual environment.

e.g cd maintenance-tracker


3. activate the virtual environment and install the necessary dependecies from th requirements.txt file

e.g  pip install requirements.txt

 OR 
 
install  flask, flask-restful :


 e.g pip install flask,flask-restful



4. Install pytest


e.g	pip install pytest

	
5. Install pytest coverage


e.g	pip install pytest-cov

	
6. Run the system

e.g
   set FLASK_APP=api
   
   flask run
   
   Test the GET and POST methods using [POSTMAN](https://www.getpostman.com/):
   
   uri: (http://127.0.0.1:5000/api/v1/users/requests)
   
   uri: (http://127.0.0.1:5000/api/v1/users/requests/1)

    

## Running the tests

On the command prompt run the following commands in the root project directory

```
cd <the project folder>
pytest
```

## Deployment

You can deploy the system on Heroku using the following steps.


Author

* **MURUNGI ALAN** - *Initial work*


