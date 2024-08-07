import pandas as pd
import requests
from bs4 import BeautifulSoup

Product_name = []
Prices = []
Description = []
Reviews = []

for page_num in range(2, 12):
    url = f"https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_num}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        boxes = soup.find_all("div", class_="_1AtVbE")

        for box in boxes:
            name = box.find("div", class_="_4rR01T")
            price = box.find("div", class_="_30jeq3")
            desc = box.find("ul", class_="_1xgFaf")
            review = box.find("div", class_="_3LWZlK")
            
            if name:
                Product_name.append(name.text)
            if price:
                Prices.append(price.text)
            if desc:
                Description.append(" ".join([li.text for li in desc.find_all("li")]))
            if review:
                Reviews.append(review.text)
                
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Ensuring all lists are of the same length
min_length = min(len(Product_name), len(Prices), len(Description), len(Reviews))
Product_name = Product_name[:min_length]
Prices = Prices[:min_length]
Description = Description[:min_length]
Reviews = Reviews[:min_length]

# Creating DataFrame and saving to CSV
df = pd.DataFrame({
    "Product Name": Product_name,
    "Prices": Prices,
    "Description": Description,
    "Reviews": Reviews
})

df.to_csv("D:/internship/flipkart_mobiles_50000.csv", index=False)
