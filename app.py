from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)
# /
@app.route("/")
def home():
    return(
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start-date<br/>"
        "/api/v1.0/start-date/end-date<br/>"
        "Enter Date in year-month-day format, two digits each."
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    rain_dict = {}
    # Convert the query results to a Dictionary using date as the key and prcp as the value.

    for info in session.query(Measurement):
        rain_dict.update({info.date : info.prcp})

    # Return the JSON representation of your dictionary.

    return jsonify(rain_dict)


@app.route("/api/v1.0/stations")
def stations():
    station_list = []
    for x in session.query(Station):
        station_list.append(x.station)
    return jsonify(station_list)
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/tobs")
def tobs():
    temp_list = []
    #shouldn't just hardcode...
    yearAgo = dt.datetime.strftime(dt.date(2016, 11,1)-dt.timedelta(days=365), '%Y-%m-%d')
    # resulting_query = session.query(Measurement.tobs, Measurement.date)
    for x in session.query(Measurement).filter(Measurement.date >= yearAgo).filter(Measurement.date <= '2016-11-1').limit(365):

        temp_list.append(x.tobs)
       
    return jsonify(temp_list)
    # query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/<start>")
def justStart(start):
    #I hope this doesn't need to be in here, but I guess I am feeling paranoid about it.
    if start == "start-date":
        return "Please enter a date in the form Year-Month-Day, with 4 digits for the year, and two for the month and day, ex. 2016-11-1"
    # start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    return jsonify(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start).all())
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start>/<end>")
def startToEnd(start, end):
    #I hope this doesn't need to be in here, but I guess I am feeling paranoid about it.
    if start == "start-date" or end == "end-date":
        return "Please enter a date in the form Year-Month-Day, with 4 digits for the year, and two for the month and day, ex. 2016-11-1"

    # start_date = dt.datetime.strftime(start, '%Y-%m-%d')
    # end_date = dt.datetime.strftime(end, '%Y-%m-%d')
    return jsonify(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurement.date <= end).all())
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

if __name__ == '__main__':
    app.run(debug=True)