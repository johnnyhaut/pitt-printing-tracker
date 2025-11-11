# Imports for displaying pages to the user 
from flask import Flask, redirect, url_for, request, session, render_template, abort 

# Imports for database information 
from printer_model import Base, Printer  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setting up Flask 
app = Flask(__name__)
app.secret_key = "we are pitt print trackers!"

engine = create_engine("sqlite:///printers.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
db_session = Session()

# This is in place of the Pitt Passport 
users = {"john":"pitt123", "marcos":"pitt123", "brandon":"pitt123",
         "enzo":"pitt123", "deonte":"pitt123", "sahil":"pitt123",}

# Default Route sends user to the Pitt Passport 
@app.route("/")
def default():
    return redirect(url_for("login_controller"))

# "Pitt Passport" checks if already signed in before sending to map page 
# If not already signed in checks agains list of users ^^^^^
@app.route("/login", methods=["GET", "POST"])
def login_controller():

    # Already signed in 
    if "username" in session:
        return redirect(url_for("map", username=session["username"]))

    # process HTTP GET requests, first time accessing page 
    if request.method == "GET":
        return render_template("login.html")

    # process HTTP POST requests, user clicked the login button 
    elif request.method == "POST":
        
        entered_username = request.form["user"]
        
        # check if the user is in the users fake database
        if entered_username in users:
            
            # checking if the right password has been entered
            entered_password = request.form["pass"]
            database_password = users[entered_username]

            if entered_password == database_password:
                
                # save info into the session object
                session["username"] = request.form["user"]

                # redirect the user to his/her map page
                return redirect(url_for("map", username=entered_username))

            else:
                # wrong password
                print("Login route: POST Request: wrong password: aborting process...")
                abort(401)
        else:
            # wrong username
            print(
                "Login route: POST request: user is not registered in the database: Aborting process...")
            abort(404)

# Sign the user out of their "Pitt" account
@app.route("/logout/")
def unlogger(): 
    # if logged in, log out, otherwise offer to log in
    if "username" in session: 
        session.clear()
        return render_template("logout.html")
    else: 
        return redirect(url_for("login_controller")) 
    

# Used to show a map of all the printers on campus 
@app.route("/map/")
def map(): 
    printers = db_session.query(Printer).all()
    printersInJSONFormat = []
    for printer in printers: 
        printersInJSONFormat.append(printer.toJSON())
        
    return render_template("map.html",
        printers = printersInJSONFormat, 
        reference_to_logout= url_for("unlogger")
    )

# Used to display the admin panel 
@app.route("/admin/")
def admin(): 
    return render_template("admin.html", 
                           new_printer_summary_reference=url_for("printer_summary")
                           )

# Used to show a summary of the new printer added 
@app.route("/admin/printer_summary/", methods=["GET", "POST"])
def printer_summary(): 
    printersLocation = request.form.get("newPrinterLocation"); 
    printersType = request.form.get("newPrinterType"); 

    print(printersLocation); 
    print(printersType); 
    return "OKAY"

@app.route("/admin/delete_printer/<printer_id>")
def delete_printer(printer_id): 
    printer_to_delete = db_session.query(Printer).get(printer_id)
    if printer_to_delete is None: 
        abort(404)
    try: 
        db_session.delete(printer_to_delete)
        db_session.commit()
        return redirect(url_for("admin"))
    except: 
        return 'There was a problem deleting that printer'

if __name__ == "__main__": 
    app.run()