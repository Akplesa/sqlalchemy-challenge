from flask import Flask, jsonify
from flask import Flask
from matplotlib import style 
import numpy as np 
import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func

#Create engine 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect Database schema
Base= automap_base()
Base.prepare(engine, reflect= True)
print(Base.classes.keys())

#Save refrences to tables in sqlite files
MEASUREMENT= Base.classes.measurement
STATION= Base.classes.station

#Create and bind session between python and app database 
session = Session(engine)


app = Flask(__name__)
@app.route("/")
def welcome():
    """Availible api routes"""
    return(
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>")
session.close()
            
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    """Return a list of percipitation data from the past year"""         
            
    oneyear_from_last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    date_percipitation = session.query(MEASUREMENT.date,MEASUREMENT.prcp).filter(MEASUREMENT.date>=  oneyear_from_last_date).all()
    df = pd.DataFrame(date_percipitation, columns= ['date','prcp'])



    # Create a dictionary from the row data and append to a list of all_passengers
    prcp_sum = []
    for date, prcp in date_percipitation:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        prcp_sum.append(prcp_dict)
    session.close()
    return jsonify(prcp_sum)


@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)
    
    station_sum=  session.query(MEASUREMENT.station, func.count(MEASUREMENT.station)).group_by(MEASUREMENT.station).order_by(func.count(MEASUREMENT.station).desc()).all()
    session.close()
    return jsonify(station_sum)

@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)
    oneyear_from_last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_sum=  session.query(MEASUREMENT.tobs).filter(MEASUREMENT.station=='USC00519281').filter(MEASUREMENT.date>=oneyear_from_last_date ).all()

    session.close()
    return jsonify(tobs_sum)

@app.route("/api/v1.0/<start>")
def start(start):
     
    # Create our session (link) from Python to the DB
    session = Session(engine)
    oneyear_from_last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    start_tobs= session.query(func.min(MEASUREMENT.tobs), func.avg(MEASUREMENT.tobs), func.max(MEASUREMENT.tobs))\
        .filter(MEASUREMENT.station=='USC00519281')\
        .filter(MEASUREMENT.date >= oneyear_from_last_date ).first()
    session.close()                                                                                                                             

    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def calculation(start_date, end_date):
     
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results=  session.query(func.min(MEASUREMENT.tobs), func.avg(MEASUREMENT.tobs), func.max(MEASUREMENT.tobs))\
        .filter(MEASUREMENT.station=='USC00519281')\
        .filter(MEASUREMENT.date >= oneyear_from_last_date ).first()
        .filter(MEASUREMENT.date <= oneyear_from_last_date ).first()
    session.close()                                                                                                                             
    session.close()
    return jsonify()

if __name__ == '__main__':
    app.run(debug=True)
          
