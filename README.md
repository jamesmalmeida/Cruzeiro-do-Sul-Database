# Cruzeiro do Sul Database
  QUATI Beamline (Sirius - CNPEM) Data Library for storing XAS & XRD spectras.
  
  Developed initially in 2023 by Anailson Santos Silva as a research project during his participation in the 30th Summer Scholarship Program (PBV30) of the   National Center for Research in Energy and Materials (CNPEM) located in Campinas, São Paulo - Brazil.
  
  The simulation data was obtained by Francis Germánico Villacrés Merchán during his participation in the PBV30.
  
  The idealizers of the database and the website were PhDs Santiago José Alejandro Figueroa (QUATI - LNLS) and James Moraes de Almeida (ILUM) and the engineer Igor Ferreira Torquato (QUATI - LNLS).

# Requirements:
  - Python : version 3.10 or higher
  - Django : version 4.2 or higher
  - Pandas, lmfit, plotly, chardet and keyborard  
  
# Steps to configure and run the application:

  1. Create an python3 vitual environment, activate it and install the dependencies:
  
  ```
  > python3 -m venv csvenv
  > source csvenv/bin/activate
  > python3 -m pip install django~=4.2
  > python3 -m pip install pandas lmfit plotly chardet keyboard
  ```
  
  2. Clone the repository.
  3. Configure the project:
  ```
  > cd Cruzeiro-do-Sul-Database/cruzeiro_do_sul_db/
  > python3 manage.py makemigrations database
  > python3 manage.py migrate database
  > python3 manage.py makemigrations
  > python3 manage.py migrate   
 ```
  4. Create a superuser (optional):
  ```
  python3 manage.py createsuperuser
  ```
  5. Run the server:
  ```
  > python3 manage.py runserver
  ```
  6. Access the website at address `http://127.0.0.1:8000/`.
  7. Alternatively, to make website visible at the local network, run the command:
  ```
  > python3 manage.py runserver 0.0.0.0:8000
  ```
