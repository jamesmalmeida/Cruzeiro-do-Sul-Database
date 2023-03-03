# Cruzeiro do Sul Database
  Sirius XAS & XRD database

# Requirements:
  - Python (preferable Python3.10) with Django.
  - More about Django's environment configuration can be found in: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment

# Steps to configure:
  - Clone the repository:
    - You can download the source code and extract it in a file-system's folder;
    - Or you can clone the repository to a file-system's folder with git or Github-Desktop.
  - In a terminal, go to the folder location where you placed the files containing manage.py file inside Cruzeiro-do-Sul-Database/cruzeiro_do_sul_db/ folder.
  - Make the migrations to the database. Replace 'python3.10' with your python version. Commands:
    - python3.10 manage.py makemigrations database
    - python3.10 manage.py migrate database
    - python3.10 manage.py makemigrations
    - python3.10 manage.py migrate
  - Create a superuser (optional). Commands:
    - python3.10 manage.py createsuperuser
  - Run the server. Commands:
    - python3.10 manage.py runserver
  - Access http://127.0.0.1:8000/ in a browser.
  - To make website visible in the local network, read the following page: https://stackoverflow.com/questions/22144189/making-django-server-accessible-in-lan
