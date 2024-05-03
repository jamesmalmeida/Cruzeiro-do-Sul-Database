# Cruzeiro do Sul Database
  QUATI Beamline (Sirius - CNPEM) Data Library for storing XAS & XRD spectras.
  
  Developed initially in 2023 by Anailson Santos Silva as a research project during his participation in the 30th Summer Scholarship Program (PBV30) of the   National Center for Research in Energy and Materials (CNPEM) located in Campinas, São Paulo - Brazil.
  
  The simulation data was obtained by Francis Germánico Villacrés Merchán during his participation in the PBV30.
  
  The idealizers of the database and the website were PhDs Santiago José Alejandro Figueroa (QUATI - LNLS) and James Moraes de Almeida (ILUM) and the engineer Igor Ferreira Torquato (QUATI - LNLS).

# Requirements:
  - Python (preferable Python3.10) with Django.
  - More about Django's environment configuration can be found in: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment

# Steps to configure:
  - Clone the repository:
    - You can download the source code and extract it in a file-system's folder;
    - Or you can clone the repository to a file-system's folder with git or Github-Desktop.
  - In a terminal, go to the folder location where you placed the files containing manage.py file. Command:
    - cd ~/../Cruzeiro-do-Sul-Database/cruzeiro_do_sul_db/
<<<<<<< HEAD
  - Make the migrations to the database. Commands:
    - python manage.py makemigrations database
    - python manage.py migrate database
    - python manage.py makemigrations
    - python manage.py migrate   
=======
  - Install dependencies. Commands:
    - pip install pandas
    - pip install lmfit
    - pip install plotly
    - pip install keyboard
>>>>>>> 8f44f20 (Read edit)
  - Make the migrations to the database. Commands:
    - python manage.py makemigrations database
    - python manage.py migrate database
    - python manage.py makemigrations
    - python manage.py migrate
  - Create a superuser (optional). Command:
    - python manage.py createsuperuser
  - Run the server. Command:
    - python manage.py runserver
  - Access http://127.0.0.1:8000/ in a browser.
  - To make website visible in the local network, read the following page: https://stackoverflow.com/questions/22144189/making-django-server-accessible-in-lan
