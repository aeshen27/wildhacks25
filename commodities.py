from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

#API Key: RQIDbfRT98M9wtfJvQpWorfPMeWZ5cYoJUQpNtXS
app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user='root',
    password='gobears',
    database='agriculture_app'
)

cursor = conn.cursor()

def read_csv_data(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')

def get_commodities():
    cursor.execute("SELECT * FROM commodities")
    results = cursor.fetchall()
    commodities = [{'id': r[0], 'name':r[1], 'export_value':r[2], 'export_volume':r[3], 'total_volume':r[4]} for r in results]
    return commodities

def fetch_news(commodity):
    # Your NewsAPI key is directly used here.
    api_key = "58886712a7e647afa2389ea6b4075c3e"
    # Construct a query to target relevant topics along with the commodity name.
    query = f"{commodity} tariffs OR natural disasters OR price booms OR scarcity OR laws OR regulations"
    # URL for the NewsAPI "everything" endpoint.
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return articles
    else:
        # Optionally, log or handle errors here.
        return []
    
def index():
    commodity_files = {
        'rice': 'Hackathon Data/Rice.csv',
        'soybeans': 'Hackathon Data/Soybeans.csv',
        'cocoa': 'Hackathon Data/Cocoa & Cocoa Prod..csv',
        'corn': 'Hackathon Data/Corn.csv',
        'dairy': 'Hackathon Data/Dairy & Products.csv',
        'egg': 'Hackathon Data/Egg and Egg Products.csv',
        'poultry': 'Hackathon Data/Poultry & Products.csv',
        'fruits': 'Hackathon Data/Fruits and Preparations.csv',
        'sugar': 'Hackathon Data/Sugr & Rel Pdt,X Hon.csv',
        'tree_nuts': 'Hackathon Data/Tree Nuts And Preparations.csv',
        'beef': 'Hackathon Data/Variety Meats, Beef.csv',
        'pork': 'Hackathon Data/Variety Meats, Pork.csv',
        'wheat': 'Hackathon Data/Wheat.csv'
    }

    # Store generated plot filenames in a dictionary
    plot_filenames = {}
    
    # Load each CSV, create a plot, save it
    return plot_filenames

@app.route('/')
def home():
    plot_filenames = index()  # Generate and save plots
    return render_template('dashboard.html', 
                           commodities=get_commodities(), 
                           selected_symbol=1001, 
                           stock_data=next((row for row in get_commodities() if row['id'] == 1001), None),
                           plot_filenames=plot_filenames)

@app.route('/commodity/<selected_id>')
def show_commodity(selected_id):
    commodity_list = get_commodities()
    selected_commodity = next((row for row in commodity_list if row['id'] == int(selected_id)), None)
    if selected_commodity is None:
        return "Commodity not found", 404
    news_articles = fetch_news(selected_commodity['name'])
    return render_template('dashboard.html',commodities=get_commodities(), selected_symbol=selected_id, stock_data = next((row for row in get_commodities() if row['id'] == int(selected_id)), None), news=news_articles, plot_filenames=index())

if __name__ == '__main__':
    app.run(debug=True)