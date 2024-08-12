from flask import Flask
from flask import render_template
import pandas as pd
import sqlite3

conn = sqlite3.connect('fina.db')
data = pd.read_sql("SELECT * FROM quarter_revenue_increase limit 100", conn)
data.sort_values(by=["pre_date",'yoy_total_operating_revenue'], inplace=True, ascending=False)
res = data.to_dict(orient='split')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',revenue_data=res["data"])


if __name__ == '__main__':
    app.run(debug=False)