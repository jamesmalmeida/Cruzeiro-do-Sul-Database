# Cruzeiro do Sul Database
  QUATI Beamline [1] Data Library for storing XAS & XRD experimental information and make it accesible to the users.
  
  This project was developed initially in 2023 by Anailson Santos Silva as a research project during his participation in the 30th Summer Scholarship Program (PBV30) of the Brazilian Synchrotron Light Laboratory (LNLS) on the National Center for Research in Energy and Materials (CNPEM) located in Campinas, São Paulo - Brazil.
  
  The idealizers of this database and the website were PhDs Santiago José Alejandro Figueroa (QUATI Beamline-LNLS/CNPEM), James Moraes de Almeida (ILUM/CNPEM) and the Engineer Igor Ferreira Torquato (LNLS/CNPEM).
  
[1] https://doi.org/10.1016/j.radphyschem.2023.111198  

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
