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
    return commodities
    
@app.route('/')
# def index():
#     rice = read_csv_data('Hackathon Data/Rice.csv')
#     soybeans = read_csv_data('Hackathon Data/Soybeans.csv')
#     cocoa = read_csv_data('Hackathon Data/Cocoa & Cocoa Prod..csv')
#     corn = read_csv_data('Hackathon Data/Corn.csv')
#     dairy = read_csv_data('Hackathon Data/Dairy & Products.csv')
#     egg = read_csv_data('Hackathon Data/Egg and Egg Products.csv')
#     poultry = read_csv_data('Hackathon Data/Poultry & Products.csv')
#     fruits = read_csv_data('Hackathon Data/Fruits and Preparations.csv')
#     sugar = read_csv_data('Hackathon Data/Sugr & Rel Pdt,X Hon.csv')
#     tree_nuts = read_csv_data('Hackathon Data/Tree Nuts And Preparations.csv')
#     beef = read_csv_data('Hackathon Data/Variety Meats, Beef.csv')
#     pork = read_csv_data('Hackathon Data/Variety Meats, Pork.csv')
#     wheat = read_csv_data('Hackathon Data/Wheat.csv')

#     return 

    #return render_template('index.html', rice = rice, soybeans = soybeans, cocoa = cocoa, corn = corn, dairy = dairy, egg = egg, poultry = poultry, fruits = fruits, sugar = sugar, tree_nuts = tree_nuts, beef = beef, pork = pork, wheat = wheat)

def hello_world():
    rice = read_csv_data('Hackathon Data/Rice.csv')
    soybeans = read_csv_data('Hackathon Data/Soybeans.csv')
    cocoa = read_csv_data('Hackathon Data/Cocoa & Cocoa Prod..csv')
    corn = read_csv_data('Hackathon Data/Corn.csv')
    dairy = read_csv_data('Hackathon Data/Dairy & Products.csv')
    egg = read_csv_data('Hackathon Data/Egg and Egg Products.csv')
    poultry = read_csv_data('Hackathon Data/Poultry & Products.csv')
    fruits = read_csv_data('Hackathon Data/Fruits and Preparations.csv')
    sugar = read_csv_data('Hackathon Data/Sugr & Rel Pdt,X Hon.csv')
    tree_nuts = read_csv_data('Hackathon Data/Tree Nuts And Preparations.csv')
    beef = read_csv_data('Hackathon Data/Variety Meats, Beef.csv')
    pork = read_csv_data('Hackathon Data/Variety Meats, Pork.csv')
    wheat = read_csv_data('Hackathon Data/Wheat.csv')

    return render_template("index.html", commodities=get_commodities(), rice = rice, soybeans = soybeans)

if __name__ == '__main__':
    app.run(debug=True)

