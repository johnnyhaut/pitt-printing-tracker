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
* Go to 'http://127.0.0.1:8000' in the browser of your choice
