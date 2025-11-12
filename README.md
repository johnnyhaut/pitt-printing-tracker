# Pitt Printing Tracker API
The API for the Pitt Printing Tracker being built in CS1550. This API will allow users to poll location of printers and patch printers as broken if they aren't operational. It will also allow admin user's to Patch printers when they are broken.

## Basic Requirements 
* The system should have a map of all printers on campus

## GET Requests
* User's & Admin's should have the ability to get printer location, capabilities, & status
    * They should also get an estimated wait time (HOW?)
    * Should be able to sort by COLOR / B&W Printers
* Admin's should have the ability to get 

## POST Requests 
* User's have the ability to provide feedback after printing 
* Admin's have the ability to add more printers to the system 


## PATCH Requests 
* User's should be able to report broken printers to the system 

## Running Program 
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
* Go to 'http://127.0.0.1:8000'
