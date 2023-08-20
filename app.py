# Setting up Dependencies
import pandas as pd
import json
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import render_template
from flask import Flask, jsonify
from sqlalchemy import func, and_ 
from sqlalchemy import desc
import requests
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
def home():
    return render_template('index.html')

@app.route("/Salary")
def table1():
    session = Session(engine)
    result = session.query(Salary.NAME, Salary.POSITION, Salary.SALARY)
    session.close()
    return jsonify([row._asdict() for row in result])

@app.route("/Stats")
def table2():
    session = Session(engine)
    result = session.query(Stats.RANK, Stats.NAME, Stats.POSITION, Stats.AGE, Stats.PPG, Stats.GP).all()
    session.close()
    return jsonify([row._asdict() for row in result])

@app.route("/TopSalary")
def top_salary():
    session = Session(engine)
    result = session.query(Salary.RANK, Salary.NAME, Salary.POSITION, Salary.AGE, Salary.PPG, Salary.GP, Salary.SALARY)\
                    .order_by(desc(Salary.SALARY))\
                    .limit(10)\
                    .all()
    session.close()
    return jsonify([row._asdict() for row in result])

@app.route("/FranchiseStats")
def franchise_stats():
    session = Session(engine)
    
    # Query the required fields from the Stats table
    result = session.query(Stats.FRANCHISE, 
                           func.sum(Salary.SALARY).label("TotalSalary"), 
                           func.avg(Stats.PPG).label("AvgPPG"))\
                    .join(Salary, Stats.NAME == Salary.NAME)\
                    .group_by(Stats.FRANCHISE)\
                    .all()

    output_data = []

    for item in result:
        data_dict = item._asdict()  # Convert the result to dictionary for modification

        city = ' '.join(data_dict["FRANCHISE"].split(' ')[:-1])  # Extracting city name from the franchise name

        response = requests.get(f'https://nominatim.openstreetmap.org/search?city={city}&format=json')
        data = response.json()
        
        if data:
            data_dict["coordinates"] = [float(data[0]['lat']), float(data[0]['lon'])]

        output_data.append(data_dict)

    session.close()

    return jsonify(output_data)



@app.route("/TopScorers")
def top_scorers():
    session = Session(engine)

    subquery = session.query(
        Stats.POSITION, Stats.AGE, func.max(Stats.PPG).label("TopPPG")
    ).filter(
        Stats.YEAR.in_(['2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023'])
    ).group_by(Stats.POSITION, Stats.AGE).subquery()

    result = session.query(Stats.NAME, Stats.POSITION, Stats.AGE, Stats.PPG, Stats.YEAR).join(
        subquery, and_(
        
            Stats.POSITION == subquery.c.POSITION,
            Stats.AGE == subquery.c.AGE,
            Stats.PPG == subquery.c.TopPPG
        )
    ).filter(
        Stats.YEAR.in_(['2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023'])
    ).order_by(Stats.PPG.desc()).all()

    session.close()

    return jsonify([row._asdict() for row in result])


if __name__ == '__main__':
    app.run(debug = True)
    
