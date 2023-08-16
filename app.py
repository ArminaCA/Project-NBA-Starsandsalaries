# Setting up Dependencies
import pandas as pd

import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///./Resources/NBAStats.sqlite")

inspector = inspect(engine)
print(inspector.get_table_names())

Base = automap_base()
Base.prepare(autoload_with = engine)

Salaries = Base.classes.Salary

app = Flask(__name__)

@app.route("/")
def test():
    session = Session(engine)
    boop = {"result": session.query(Salaries.SALARY).limit(1).one()}
    return jsonify(boop) #jsonify(session.query(Salaries.SALARY).limit(5).all())

if __name__ == '__main__':
    app.run(debug = True)