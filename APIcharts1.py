# Setting up Dependencies
import pandas as pd
import json
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///./Resources/NBAStats.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with = engine)

# Save reference to the table
Stats = Base.classes.Stats
Salary = Base.classes.Salary

app = Flask(__name__)

@app.route("/")
@app.route("/Salary")
def table1():
    session = Session(engine)
    result = session.query(Salary.PPG, Salary.Franchise, Salary.Salary)
    session.close()
    return jsonify([row._asdict() for row in result])

@app.route("/Stats")
def table2():
    session = Session(engine)
    result = session.query(Stats.rank, Stats.full_name, Stats.position, Stats.age, Stats.PPG, Stats.GP).all()
    session.close()
    return jsonify([row._asdict() for row in result])

if __name__ == '__main__':
    app.run(debug = True)
    
