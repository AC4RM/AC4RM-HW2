from homework import *
from pytest import approx
from pathlib import Path
import pandas as pd
import numpy as np
import sqlite3
import sklearn
import re


def test_python():
    assert max_val([[1, 2, 3, 3], [12, 2, 12]]) == [3, 12]


def test_sql():
    con = sqlite3.connect('homework.db')  # open a database file

    con.execute(''' CREATE TABLE IF NOT EXISTS employee_records(
        ID INT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        DIVISION TEXT NOT NULL,
        STARS INT NOT NULL) ''')

    con.execute(''' INSERT INTO employee_records(ID,NAME,DIVISION,STARS)
        VALUES (1,'Lenny','Software',3)
     ''')
    con.execute(''' INSERT INTO employee_records(ID,NAME,DIVISION,STARS)
        VALUES (2,'Cynthia','Manager',5)
     ''')
    con.execute(''' INSERT INTO employee_records(ID,NAME,DIVISION,STARS)
        VALUES (3,'Harrison','Mechanic',4)
     ''')
    con.execute(''' INSERT INTO employee_records(ID,NAME,DIVISION,STARS)
        VALUES (4,'Joan','Electronic',3)
     ''')
    con.execute(''' INSERT INTO employee_records(ID,NAME,DIVISION,STARS)
        VALUES (5,'James','Maintenance',4)
     ''')
    con.commit()

    con.execute(sql_query_1)
    con.execute(sql_query_2)

    employee_df = pd.read_sql_query("SELECT * from employee_records", con)
    assert employee_df.query('ID == 3')['DIVISION'].iloc[0] == 'Hardware'
    assert employee_df.query('STARS == 3').shape[0] == 0

    Path('homework.db').unlink(missing_ok=True)


def test_model():
    model = train_model()
    assert isinstance(model, sklearn.linear_model._ridge.Ridge)
    assert model.alpha == approx(2.63, 0.1)


def test_regex():
    assert re.search(regex_pattern, 'abc de')
    assert re.search(regex_pattern, 'abcde')
    assert not re.search(regex_pattern, 'ab cd')


def test_monte_carlo():
    results = []
    np.random.seed(42)
    for i in range(5000):
        result = simple_bettor_v2(10000, 3000, 20)
        results.append(result)

    assert max(results) == 20

