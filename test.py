from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify

app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///./Resources/NBAStats.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

Stats = Base.classes.Stats
Salary = Base.classes.Salary

def fetch_data(query, fields):
    conn = engine.connect()
    session = Session(bind=conn)
    result = session.execute(query).fetchall()
    data = {field: [] for field in fields}
    
    for record in result:
        for i, field in enumerate(fields):
            data[field].append(record[i])
    
    return data

@app.route('/bar_chart')
def get_bar_chart_data():
    query = Stats.select()
    fields = ['FULLNAME', 'PPG', 'POS', 'YEAR']
    return jsonify(fetch_data(query, fields))

@app.route('/line_chart')
def get_line_chart_data():
    query = Stats.select()
    fields = ['POS', 'PPG', 'YEAR']
    return jsonify(fetch_data(query, fields))

@app.route('/radial_chart')
def get_radial_chart_data():
    query = Salary.select()
    fields = ['NAME', 'POS', 'Salary']
    return jsonify(fetch_data(query, fields))

@app.route('/map_chart')
def get_map_chart_data():
    query = Salary.select()
    fields = ['TEAM', 'PPG', 'Salary']
    return jsonify(fetch_data(query, fields))

if __name__ == '__main__':
    app.run(debug=True)
