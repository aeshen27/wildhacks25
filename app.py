from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os

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
#return render_template('index.html', rice = rice, soybeans = soybeans, cocoa = cocoa, corn = corn, dairy = dairy, egg = egg, poultry = poultry, fruits = fruits, sugar = sugar, tree_nuts = tree_nuts, beef = beef, pork = pork, wheat = wheat)

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
    for commodity, file_path in commodity_files.items():
        df = pd.read_csv(file_path)
        
        # Clean or convert columns if needed
        # For example, ensure 'Year' is numeric
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df.dropna(subset=['Year'], inplace=True)
        
        # Suppose the CSV has a 'Value' column representing export value
        # You could group by year or do other transformations as needed
        grouped = df.groupby('Year')['Value'].sum()

        # Create a line plot (customize style as you wish)
        fig, ax = plt.subplots()
        ax.plot(grouped.index, grouped.values, marker='o')
        ax.set_title(f'{commodity.capitalize()} Exports by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Value')
        
        # Save plot in static/plots directory
        plot_filename = f'{commodity}_plot.png'
        fig.savefig(os.path.join('static', 'plots', plot_filename))
        plt.close(fig)

        # Store the filename so we can reference it in the template
        plot_filenames[commodity] = plot_filename

    for commodity, file_path in commodity_files.items():
        df = pd.read_csv(file_path)

        df_long = pd.melt(
            df,
            value_vars=['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'],
            var_name='Year',
            value_name='Export Value'
        )

        # Clean or convert columns if needed
        # For example, ensure 'Year' is numeric
        df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
        df_long.dropna(subset=['Year'], inplace=True)
        
        # Suppose the CSV has a 'Value' column representing export value
        # You could group by year or do other transformations as needed
        grouped = df_long.groupby('Year')['Unnamed: 6'].sum()

        # Create a line plot (customize style as you wish)
        fig, ax = plt.subplots()
        ax.plot(grouped.index, grouped.values, marker='o')
        ax.set_title(f'{commodity.capitalize()} Exports by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Unnamed: 6')
        
        # Ensure the static/plots directory exists
        plot_path = os.path.join('static', 'plots')
        if not os.path.exists(plot_path):
            os.makedirs(plot_path)

        plot_filename = f'{commodity}_plot.png'
        fig.savefig(os.path.join(plot_path, plot_filename))
        plt.close(fig)

        # Store the filename so we can reference it in the template
        plot_filenames[commodity] = plot_filename

    return render_template("index.html", commodities=get_commodities(), plot_filenames=plot_filenames)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)