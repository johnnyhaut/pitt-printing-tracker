# Pitt Printing Tracker API
The API for the Pitt Printing Tracker built in Fall 2025 by Group 8, the Pitt Printing Trackers in CS1530. This API will allow users to poll location of printers across campus and mark when printers aren't working and why for other users. Admin user's are able to view all printers status and are able to update printers when they have been fixed.

## Basic Requirements 
* The system should map all printers on University Of Pittsburgh Oakland campus
* All users should be able to mark printers as Offline when there is an issue  
* Admin users should be able to mark printers as being fixed 

## GET Requests
* User's & Admin's should have the ability to get printer location, capabilities, & status
    * They should also get an estimated wait time (HOW?)
    * Should be able to sort by COLOR / B&W Printers
* Admin's should have the ability to get 

## POST Requests 
* User's have the ability to provide feedback after printing 
* Admin's have the ability to add more printers to the system 

## Default User 
## Admin User's 

## Accessing Program 
* This program is currently running on 'https://pittprintingtracker.pythonanywhere.com'

## Running Program (Local)
1) Create a virtual Environment
* python -m venv venv
2) Activate the Virtual Environment: 
* In MacOS: source ./venv/bin/activate
* In Windows: .\venv\Scripts\activate
3) Install the dependencies
* pip install -r requirements.txt
4) Running the local server 
* python main_app.py
5) Accessing the page
* Go to 'http://127.0.0.1:8000' in the browser of your choice

## Running Program (PythonAnywhere Hosting Environment)
1) Access pythonanywhere.com and create an account or sign in
2) Open a new console on PythonAnywhere and clone the git repository
3) Create a virtual Environment:
* python -m venv venv
4) Activate the Virtual Environment:
* source venv/bin/activate
5) Install the dependencies:
* pip install -r requirements.txt
6) Navigate to the PythonAnywhere "Web" page and select "Add a new web app"
7) Follow the instructions to create a Flask web app and ensure the application is pointing to the write file:
* /home/<username>/pitt-printing-tracker/main_app.py
8) Ensure your Source code and Working directory in PythonAnywhere both point towards the correct folder:
* /home/<username>/pitt-printing-tracker
9) Ensure your Virtualenv in PythonAnywhere is pointing towards the correct folder:
* /home/<username>/pitt-printing-tracker/venv
10) Reload your website in PythonAnywhere
11) Access the page:
* Go to https://<username>.pythonanywhere.com

 
###  Logging in with a basic user account you will be able to access the default user interface. If you sign in with an admin account you will access. the admin user interface. 
```
users = john : pitt123    , marcos : pitt123  , 
        brandon : pitt123 , enzo : pitt123    , 
        deonte : pitt123  , sahil : pitt123   
        
        
admin users = admin : pw
```