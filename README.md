## Project Setup

Ubuntu 20.04.2 LTS <br />
MySQL 5.7.34

This is a Python/Django app which provides the functionalities of an Agenda. 

This application was developed during the 10 May- 2 June 2021 individual ASSIST internship. 

How to install the application

    Clone the code from git.
    Create an environment using virtualenv and activate it.
    Install the project dependencies with pip. Run this command: pip install -r requirements.txt while being in the folder with the requirements.txt file.
    Install MySQL 5.7.34
	Access mysql server using: mysql -u root -p and create the database: CREATE DATABASE db_name;
    Create a local_settings.py file in the same folder as settings.py. Change the name and user if needed and add the password.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'agenda',
        'USER': 'root',
        'PASSWORD': 'root',
        # added timezone
        'TIME_ZONE': 'Europe/Bucharest',
    }
}

DEBUG = True

    Run python manage.py migrate to create the tables.
    Run python manage.py runserver to actually run the application and explore its features.
