# dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask

# db setup
engine = create_engine('sqlite:///hawaii.sqlite')

# reflect db
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# save references
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# define index route path
@app.route('/')
def welcome():
    '''list all available api routes'''
    return (
        f'Available Routes:<br/>'
        f'<a href=/api/v1.0/precipitation</a><br/>'
        f'<a href=/api/v1.0/stations</a><br/>'
        f'<a href=/api/v1.0/<start></a><br/>'
        f'<a href=/api/v1.0/<start>/<end></a><br/>'
    )

# @app.route("/api/v1.0/precipitation")

# @app.route("/api/v1.0/stations")

# @app.route("/api/v1.0/<start>")

# @app.route("/api/v1.0/<start>/<end>")


# if __name__ == '__main__':
#     app.run(debug=True)