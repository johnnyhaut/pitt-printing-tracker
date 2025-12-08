# Imports for displaying pages to the user 
from flask import Flask, redirect, url_for, request, session, render_template, abort

# Imports for database information 
from printer_model import Base, Printer  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Imports for decorators
from functools import wraps

# Imports for password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Setting up Flask 
app = Flask(__name__)
app.secret_key = "we are pitt print trackers!"

engine = create_engine("sqlite:///printers.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
db_session = Session()

# This is in place of the Pitt Passport 
# Obviously we would NEVER EVER do this in a real application. The plaintext passwords would not be stored in the code, but rather created by the users themselves on signup and stored securely in a database rather than a hash map in the code.
users = {"john":generate_password_hash("pitt123"), "marcos":generate_password_hash("pitt123"), "brandon":generate_password_hash("pitt123"),
         "enzo":generate_password_hash("pitt123"), "deonte":generate_password_hash("pitt123"), "sahil":generate_password_hash("pitt123"),
         "admin":generate_password_hash("pw")}

# Decorators to check if user is logged in or admin
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login_controller"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login_controller"))
        if session["username"] != "admin":
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

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
        # check if admin or normal user  
        if session["username"] == "admin": 
            # redirect admin to admin page 
            return redirect(url_for("admin"))
        # otherwise redirect normal user to map 
        else: 
            return redirect(url_for("map", username=session["username"]))

    # process HTTP GET requests, first time accessing page 
    if request.method == "GET":
        return render_template("login.html", style=url_for('static', filename='css/login.css'), 
                               passport = url_for('static', filename='images/passport-header.png'),
                               disclaimer= url_for('static', filename='images/disclaimer.png'))

    # process HTTP POST requests, user clicked the login button 
    elif request.method == "POST":
        
        entered_username = request.form["user"]
        
        # check if the user is in the users fake database
        if entered_username in users:
            
            # checking if the right password has been entered
            entered_password = request.form["pass"]

            database_password = users[entered_username]

            if check_password_hash(database_password, entered_password):
                
                # save info into the session object
                session["username"] = request.form["user"]

                # redirect the user to the map/admin page
                if session["username"] == "admin": 
                    return redirect(url_for("admin"))
                else: 
                    return redirect(url_for("map"))

            else:
                # wrong password
                error = "Invalid Password, Please make sure you are entering accurate credentials" 
                
                return render_template("login.html", style=url_for('static', filename='css/login.css'), 
                        passport = url_for('static', filename='images/passport-header.png'),
                        disclaimer= url_for('static', filename='images/disclaimer.png'), 
                        error = error)
                
        else:
            # wrong username
            error = "Invalid Username, Please make sure you are entering accurate credentials"
            return render_template("login.html", style=url_for('static', filename='css/login.css'), 
                    passport = url_for('static', filename='images/passport-header.png'),
                    disclaimer= url_for('static', filename='images/disclaimer.png'), 
                    error = error)
# Sign the user out of their "Pitt" account
@app.route("/logout/")
def unlogger(): 
    # if logged in, log out, otherwise offer to log in
    if "username" in session: 
        session.clear()
        return render_template("logout.html", style=url_for('static', filename='css/logout.css'), js=url_for('static', filename='js/logout.js'))
    else: 
        return redirect(url_for("login_controller")) 
    

# Used to show a map of all the printers on campus 
@app.route("/map/")
@login_required
def map(): 
    printers = db_session.query(Printer).all()
    printersInJSONFormat = []
    for printer in printers: 
        printersInJSONFormat.append(printer.toJSON())
        
    return render_template("map.html",
        printers = printersInJSONFormat, 
        reference_to_logout= url_for("unlogger"),
        style = url_for('static', filename='css/map.css')
    )

# Used to display the report page
@app.route("/report/<int:printer_id>", methods=["GET", "POST"])
@login_required
def report_printer(printer_id):
    #Display page
    if request.method == "GET":
        printer = db_session.query(Printer).get(printer_id)
        if not printer:
            abort(404)

        return render_template(
            "report.html",
            printer=printer,
            style=url_for('static', filename='css/report.css'))
    # Used to submit the report
    if request.method == "POST":
        issue_description = request.form.get("issue_description")
        user_name = request.form.get("user_name")

        #Get printer to edit via id
        printer = db_session.query(Printer).get(printer_id)
        try:
            printer.printer_status = "Offline"
            printer.printer_issue = issue_description
            db_session.commit()
            return redirect(url_for("map"))
        except Exception as e:
            db_session.rollback()
            return f"There was an issue reporting the printer:<br><br>{e}"

# Used to display the admin panel 
@app.route("/admin/")
@admin_required
def admin(): 
    printers = db_session.query(Printer).all()
    printersInJSONFormat = []
    for printer in printers: 
        printersInJSONFormat.append(printer.toJSON())
        
    return render_template("admin.html", 
                           new_printer_summary_reference=url_for("printer_summary"), 
                           printers= printersInJSONFormat, 
                           style = url_for('static', filename='css/admin.css'), 
                           reference_to_logout= url_for("unlogger")
                           )

# Used to fix a printer issue
@app.route("/admin/fix_printer/<printer_id>", methods=["GET", "POST"])
@admin_required
def fix_printer(printer_id): 
    printer_to_fix = db_session.query(Printer).get(printer_id)
    if printer_to_fix is None: 
        abort(404)
    try: 
        printer_to_fix.printer_status = "Online"
        printer_to_fix.printer_issue = ""
        db_session.commit()
        return redirect(url_for("admin"))
    except: 
        return 'There was a problem fixing that printer'

# Used to show a summary of the new printer added 
@app.route("/admin/printer_summary/", methods=["GET", "POST"])
@admin_required
def printer_summary(): 
    printersLocation = request.form.get("newPrinterLocation"); 
    printersType = request.form.get("newPrinterType"); 
    printersStatus = request.form.get("newPrinterStatus"); 
    printersIssues = request.form.get("newPrinterIssue")
    
    printer_obj = Printer(
                    printer_location = printersLocation,
                    printer_type = printersType,
                    printer_status = printersStatus,
                    printer_issue = printersIssues
                    )

    try: 
        db_session.add(printer_obj); 
        db_session.commit()
        return render_template("printer_summary.html", 
                               location = printersLocation,
                               type = printersType, 
                               status = printersStatus, 
                               issues = printersIssues,
                               js = url_for('static', filename='js/printer_summary.js'),
                               style=url_for('static', filename="css/add_printer_summary.css"),
                               returnLink = url_for("admin"))
    except:     
        return "There was an issue adding to the database"

@app.route("/admin/delete_printer/<printer_id>")
@admin_required
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
    app.run(port=8000)
