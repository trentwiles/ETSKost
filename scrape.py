import requests
from bs4 import BeautifulSoup

def scrapeBottle(url):
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}
    # example: https://qualityliquorstore.com/collections/blanco/products/don-julio-blanco-375ml
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    # Title
    title = soup.find("h1", {"class": "product-title"}).text.strip()

    # Price
    price = soup.find("strong", {"class": "price__current"})
    price = price.text.strip()
    
    if "," in price:
        price = price.replace(",", "")

    # [1:-2] -> remove $ and the last two chars (to insert the ".")
    price_int = float(price[1:-2] + "." + price[-2:])
    
    # size of bottle
    size_line = soup.find("ul", {"class": "product-spec"})
    if size_line != None:
        size = size_line.find("div", {"class": "product-spec__value block"}).text.strip()
        
        # if the size is in L
        if size[-1] == "L":
            size_int = float(size[:-1]) * 1000
        # otherwise it's in mL
        else:
            size_int = float(size[:-2])
        
        
        ml_per_dollar = round(size_int/price_int, 2)
        # assumes a standard shot is 50mL
        dollars_per_shot = round(50/ml_per_dollar, 2)
        return {"title": title, "price": price_int, "milliliters": round(size_int), "millilitersPerDollar": ml_per_dollar, "costPerShot": dollars_per_shot}
    else:
        return {"title": title, "price": price_int, "milliliters": None}
    
    
    
    