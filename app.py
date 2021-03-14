import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)   #gets a view of whats in the dictionary
#try in jupyter notebook to see if it works, the port to VSC

# Save reference to the table
Station = Base.classes.station
Msrmt   = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/<<" + f"start-date"#+">><br/>"
        f"/api/v1.0/start-date/end-date"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session
    session = Session(engine)

    """Return a list of dates and precip amts"""
    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value
    results = session.query(Msrmt.date,Msrmt.prcp).order_by(Msrmt.date).all()

    session.close()  

    result_dict={}
    for date,precip_amt in results:
        result_dict[date]=precip_amt

    return jsonify(result_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session
    session = Session(engine)

    """Return a list of stations"""
    #Return a JSON list of stations from the dataset
    results = session.query(Station.id,Station.station, Station.name, Station.elevation,Station.latitude,Station.longitude).all()

    session.close()  
    all_stations=results #all_stations is a list of lists.  TODO confirm if need to limit to just station name or whatever

    # this will return results into single list
    #all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session
    session = Session(engine)

    """Return a list of dates and temps for the most active station for the last year"""

    stationsCount=session.query(Msrmt.station, func.count(Msrmt.station)).group_by(Msrmt.station).order_by(func.count(Msrmt.station).desc()).all()
    mostActiveStation=stationsCount[0][0]  #results are ordered desc, so 1st one has highest count
    mas_stats=session.query(func.min(Msrmt.tobs), func.max(Msrmt.tobs), func.avg(Msrmt.tobs)).filter(Msrmt.station==mostActiveStation).all()
    # find most recent date
    mas_recent_date =session.query(Msrmt.date).filter(Msrmt.station==mostActiveStation).order_by(Msrmt.date.desc()).limit(1)
    mas_recent_date[0][0]
    # get a year back from most recent date
    mas_yearago=dt.date(2017,8,18)-dt.timedelta(days=365)
    # Query the temps for the last year  TODO just return tobs?
    temp_results = session.query(Msrmt.date,Msrmt.tobs).filter(Msrmt.date >= mas_yearago).filter(Msrmt.station==mostActiveStation).all()


    session.close()  
 

    return jsonify(temp_results)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    # Create our session
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start"""
    stats_results=session.query(func.min(Msrmt.tobs), func.avg(Msrmt.tobs), func.max(Msrmt.tobs)).filter(Msrmt.date >= start_date).all()


    

    session.close()  
 

    return jsonify(stats_results)


if __name__ == '__main__':
    app.run(debug=True)
