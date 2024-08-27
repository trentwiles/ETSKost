from flask import Flask, render_template
import db
import scrape
import json
import datetime

app = Flask(__name__)

def epochToHuman(ts:int):
    dt_object = datetime.datetime.fromtimestamp(ts)
    formatted_time = dt_object.strftime("%m/%d/%Y @ %I:%M %p")
    return formatted_time

@app.route('/')
def home():
    data = db.selectAll()
    #print(data)
    prices = []
    for drink in data:
        dets = db.selectAllPricesForDrink(drink[0])
        formatted = []
        for priceIndex in dets:
            details = {
                "price": priceIndex[1],
                "mls": priceIndex[2],
                "mlPerDollar": priceIndex[3],
                "dollarsPerShot": priceIndex[4],
                "time": priceIndex[5]
            }
            formatted.append(details)
        prices.append({"title": drink[0], "costs": formatted})
    
    print(json.dumps(prices))
        
    return render_template('table.html', drinks=data, prices=prices, epochToHuman=epochToHuman)

@app.route('/update', methods=["POST"])
def update():
    drinks = scrape.getAllDrinks()
    for drink in drinks:
        scrape.insertAndLogPrice(drink["url"])
    return ""

if __name__ == "__main__":
    app.run(port=3000)
