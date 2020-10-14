
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import re
import os

# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy 
"""
database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format (
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )
    """

database = "sqlite:///timeslots.db"

app = Flask(__name__)
app.secret_key = 'test'
# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. thid db will be used in this project 
db = SQLAlchemy(app)

#@app.route('/init_db')
#def init_db():
#    db.drop_all()
#    db.create_all() 
#    return 'DB initialized'

@app.route('/') 
@app.route('/index')
def index():
    timeslot = timeslots.query.all()
    return render_template("index.html",timeslot=timeslot, title = 'Home')

    
@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        if request.form.get("Sunday") == 'true':
            Sunday = True
        else:
            Sunday = False

        if request.form.get("Monday") == 'true':
            Monday = True
        else:
            Monday = False

        if request.form.get("Tuesday") == 'true':
            Tuesday = True
        else:
            Tuesday = False

        if request.form.get("Wednesday") == 'true':
            Wednesday = True
        else:
            Wednesday = False
            
        if request.form.get("Thursday") == 'true':
            Thursday = True
        else:
            Thursday = False
            
        if request.form.get("Friday") == 'true':
            Friday = True
        else:
            Friday = False
            
        if request.form.get("Saturday") == 'true':
            Saturday = True
        else:
            Saturday = False
            
        startTime = request.form.get("StartTime")
        endTime = request.form.get("EndTime")
        
        newslot = timeslots(Sunday = Sunday, Monday = Monday, Tuesday = Tuesday, Wednesday = Wednesday, Thursday = Thursday, Friday = Friday, Saturday = Saturday, startTime = startTime, endTime = endTime)
        db.session.add(newslot)
        db.session.commit()
        
        
    newslot = timeslots.query.all()
    return render_template("create.html",newslot = newslot, title = 'Create')   



@app.route('/delete/<timeslot_id>') 
def delete(timeslot_id):
        timeslot = timeslots.query.get(timeslot_id)
        db.session.delete(timeslot)
        db.session.commit()
        timeslot = timeslots.query.all()
        return render_template("index.html",timeslot=timeslot,title ='Template')


    # Updates entries in the database
@app.route('/update', methods = ['GET', 'POST'])
def update():
        if request.method == 'POST':
            my_data = timeslots.query.get(request.form.get('id'))
            my_data.startTime = request.form['startTime']
            my_data.endTime = request.form['endTime']
            db.session.commit()
            slots = timeslots.query.all()

            return render_template("index.html", timeslot=timeslot, title = 'Home')



# this class creates a table in the database named TimeSlot with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it
class timeslots(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Sunday = db.Column(db.Boolean, default = False)
    Monday = db.Column(db.Boolean, default = False)
    Tuesday = db.Column(db.Boolean, default = False)
    Wednesday = db.Column(db.Boolean, default = False)
    Thursday = db.Column(db.Boolean, default = False)
    Friday = db.Column(db.Boolean, default = False)
    Saturday = db.Column(db.Boolean, default = False)
    startTime = db.Column(db.String(255), nullable = False)
    endTime = db.Column(db.String(255), nullable = False)

#if __name__ == '__main__':
#    app.run(debug=True)


# Added this code for visual studios
# Not needed in google app engine
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)