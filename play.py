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

import helper



# Database Setup
engine = create_engine("sqlite:///./Resources/NBAStats.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with = engine)

# Save reference to the table
Stats = Base.classes.Stats
Salary = Base.classes.Salary
PositionCounts = Base.classes.PositionCounts
TeamPositionSalary = Base.classes.TeamPositionSalary


session = Session(engine)
result = session.query(Stats.RANK, Stats.NAME, Stats.POSITION, Stats.AGE, Stats.PPG, Stats.GP, Stats.YEAR).all()


session.close()

print(helper.transform_stats(result))

# unique_position = set(x[2] for x in result)
# print(unique_position)
# transformed_result = helper.transform_stats(result)



# # get first 10 for each position
# n = 10
# for pos in unique_position:
#     a = list(filter(lambda x: x[2] == pos, transformed_result))
#     a = sorted(a, key=lambda x: -x[4])[:n]
#     print(f"-----POSITION: {pos}")
#     for v in a:
#         print(" __ ".join([str(_) for _ in v]))

# print(transformed_result)
