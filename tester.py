import scrape, db

url = "https://qualityliquorstore.com/collections/bourbon/products/eagle-rare-25-year-kentucky-straight-bourbon"
x = scrape.scrapeBottle(url)
db.insertNewDrink(x["title"], url)
print(x)