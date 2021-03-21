# performance-task
Notification service based on Django Rest framework

## Technologies

* Django Rest Framework: Framework based on python used to create APIs 
* Swagger: API documentation
* SQLite3: Database

## APIs Documentation
* Navigate to http://localhost:8000/doc, the url for swagger which is a service for automatic documentation of APIs.
* Note the file xpay.postman_collection.json which is a postman collection I created for this task, you can easily import it and find a saved response for each API

## Installation

after cloning the project and making sure that docker-compose is up and running
- Install python 3.5
- pip3 install -r requirements.txt
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py create_staff_user
- python3 manage.py create_small_data
- python3 manage.py clear_quiz_app_db
- python3 manage.py create_large_data

## Test
 python3 manage.py test
