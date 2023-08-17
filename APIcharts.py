import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify

app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///./Resources/NBAStats.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the tables
Stats = Base.classes.Stats
Salary = Base.classes.Salary

def bar_chart():
    conn = engine.connect()

    query = Stats.select()
    exe = conn.execute(query)
    result = exe.fetchall()

    FULLNAME = []
    POS = []
    PPG = []
    YEAR = []

    for record in result:
        FULLNAME.append(record[0])
        PPG.append(record[1])
        POS.append(record[2])
        YEAR.append(record[3])
    return {
        'FULLNAME': FULLNAME,
        'PPG': PPG,
        'POS': POS,
        'YEAR': YEAR,
    }

def line_chart():
    conn = engine.connect()

    query = Stats.select()
    exe = conn.execute(query)
    result = exe.fetchall()

    POS = []
    PPG = []
    YEAR = []

    for record in result:
        POS.append(record[0])
        PPG.append(record[1])
        YEAR.append(record[2])

    return {
        'POS': POS,
        'PPG': PPG,
        'YEAR': YEAR,
    }

def radial_chart():
    conn = engine.connect()

    query = Salary.select()
    exe = conn.execute(query)
    result = exe.fetchall()

    NAME = []
    POS = []
    Salary = []

    for record in result:
        NAME.append(record[0])
        POS.append(record[1])
        Salary.append(record[2])

    return {
        'NAME': NAME,
        'POS': POS,
        'Salary': Salary,
    }

def map_chart():
    conn = engine.connect()

    query = Salary.select()
    exe = conn.execute(query)
    result = exe.fetchall()

    TEAM = []
    PPG = []
    Salary = []

    for record in result:
        TEAM.append(record[0])
        PPG.append(record[1])
        Salary.append(record[2])

    return {
        'TEAM': TEAM,
        'PPG': PPG,
        'SALARY': Salary,
    }

@app.route('/bar_chart')
def get_bar_chart_data():
    return jsonify(bar_chart())

@app.route('/line_chart')
def get_line_chart_data():
    return jsonify(line_chart())

@app.route('/radial_chart')
def get_radial_chart_data():
    return jsonify(radial_chart())

@app.route('/map_chart')
def get_map_chart_data():
    return jsonify(map_chart())

if __name__ == '__main__':
    app.run(debug=True)
