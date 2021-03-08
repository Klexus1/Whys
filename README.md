# ProductImportApp

1) clone the repository in the root
2) make virtual environment (Pycharm or mkvirtualenvwrapper using pip or other)
3) activate virtual environment
4) install requirements (pip install requirements.txt)
5) configure database in settings.py (defaults to mysql)
6) migrate (eg py manage.py migrate)

# Initializing the app

7) create super user (py manage.py createsuperuser)
8) run the server (eg py manage.py runserver 8000)
9) sign into the django admin with superuser and create a token for the user in Tokens tab

# Working with the app

Testing endpoints;

for convenience django swagger functionality can be accessed on url:port/swagger/ (user must be authenticated using drf
 session auth which is done automatically after signing into django admin) and provides overview of available endpoints
 
Testing import data;

open Postman (https://www.postman.com/) or other alike service
uri is http://127.0.0.1:8000/import/, POST method
In the header tab add: key:Authorization value:Token <your_token> (created in the admin earlier)
In the body tab chose "raw" and json and paste the data (sample data included in the root folder under test_data.js)
Send the request and review imported data in django admin, core tab.

# Tests

Unit tests to be found in code>tests 
