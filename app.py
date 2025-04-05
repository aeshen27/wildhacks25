from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd

#API Key: RQIDbfRT98M9wtfJvQpWorfPMeWZ5cYoJUQpNtXS
#help
app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user='root',
    password='gobears',
    database='agriculture_app'
)

def read_csv_data(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')

cursor = conn.cursor()

@app.route('/commodities', methods=['GET'])
def get_commodities():
    cursor.execute("SELECT * FROM commodities")
    results = cursor.fetchall()
    commodities = [{'id': r[0], 'name':r[1], 'export_value':r[2], 'export_volume':r[3], 'total_volume':r[4]} for r in results]
    return str(commodities)
    
@app.route('/')

def index():
    rice = read_csv_data('Rice.csv')
    soybean = read_csv_data('Soybeans.csv')
    cocoa = read_csv_data('Cocoa & Cocoa Prod..csv')
    corn = read_csv_data('Corn.csv')
    dairy = read_csv_data('Dairy & Products.csv')
    egg = read_csv_data('Egg and Egg Products.csv')
    poultry = read_csv_data('Poultry & Products.csv')
    fruits = read_csv_data('Fruits and Preparations.csv')
    sugar = read_csv_data('Sugr & Rel Pdt,X Hon.csv')
    tree_nuts = read_csv_data('Tree Nuts And Preparations.csv')
    beef = read_csv_data('Variety Meats, Beef.csv')
    pork = read_csv_data('Variety Meats, Pork.csv')
    wheat = read_csv_data('Wheat.csv')

    return render_template('index.html', rice = rice, soybean = soybean, cocoa = cocoa, corn = corn, dairy = dairy, egg = egg, poultry = poultry, fruits = fruits, sugar = sugar, tree_nuts = tree_nuts, beef = beef, pork = pork, wheat = wheat)

def hello_world():
    return render_template("index.html", name="Farmer Abby", commodity=get_commodities())

if __name__ == '__main__':
    app.run(debug=True)
