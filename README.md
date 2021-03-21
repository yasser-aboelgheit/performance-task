# performance-task
Notification service based on Django Rest framework

## Technologies

* Django Rest Framework: Framework based on python used to create APIs 
* Profiling: django-silk
* SQLite3: Database

## APIs
* Note the file xpay.postman_collection.json which is a postman collection I created for this task, you can easily import it and find a saved response for each API

## Installation

after cloning the project
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

## Profiling
 Using silk package, you can access it through localhost:8000/silk
![Screenshot from 2021-03-21 00-47-51](https://user-images.githubusercontent.com/21153250/111889988-186dc180-89ee-11eb-851e-81f65623dfe0.png)
