# Agenda Web App



During my initial internship, I developed a dynamic Agenda Web Application on Linux with Django, offering a seamless user experience for both anonymous and registered users with tailored permissions. 

The app boasts an array of features such as creating public or private agendas, searching through both personal and public agendas, receiving email notifications for specific entries, and visualizing all agenda entries through a conveniently integrated JavaScript calendar.

Technology stack: 

• Linux 
• JavaScript
• MySQL database
• Bootstrap, CSS and HTML
• cron-job for scheduling email notifications

During my initial internship, I developed a dynamic Agenda Web Application on Linux with Django, offering a seamless user experience for both anonymous and registered users with tailored permissions. The app boasts an array of features such as creating public or private agendas, searching through both personal and public agendas, receiving email notifications for specific entries, and visualizing all agenda entries through a conveniently integrated JavaScript calendar. Technology stack: • Linux • JavaScript • MySQL database • Bootstrap, CSS and HTML • cron-job for scheduling email notifications

    Skills: Python · Django · Git

## Project Setup

Ubuntu 20.04.2 LTS <br />
MySQL 5.7.34

## Description

This is a Python/Django app which provides the functionalities of an Agenda. 
This was created during the 10 May - 10 June 2021 individual ASSIST internship. 

## How to install the application

    Clone the code from git.
    Create an environment using virtualenv and activate it.
    sudo apt-get install libmysqlclient-dev
    Install the project dependencies with pip. Run this command: pip install -r requirements.txt while being in the folder with the requirements.txt file.
    Install MySQL 5.7.34
	Access mysql server using: mysql -u root -p and create the database: CREATE DATABASE db_name; replace db_name with agenda
    Create a local_settings.py file in the same folder as settings.py. Change the name and user if needed and add the password.

DATABASES = {<br />
    'default': {<br />
        'ENGINE': 'django.db.backends.mysql',<br />
        'NAME': 'agenda',<br />
        'USER': 'root',<br />
        'PASSWORD': 'root',<br />
        # added timezone<br />
        'TIME_ZONE': 'Europe/Bucharest',<br />
    }
}

DEBUG = True

    Run python manage.py migrate to create the tables.
    Run python manage.py runserver to actually run the application and explore its features.
