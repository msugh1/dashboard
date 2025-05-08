
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to scrape Jumia
def scrape_jumia():
    url = "https://www.jumia.com.ng/smartphones/?page=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    products = []
    for product in soup.find_all("a", class_="link"):
        title = product.find("div", class_="name")
        price = product.find("div", class_="price")
        
        if title and price:
            products.append({
                "title": title.text.strip(),
                "price": price.text.strip(),
                "link": product["href"],
                "source": "Jumia"
            })
    
    return products

# Function to collect and display products
def display_products():
    jumia_data = scrape_jumia()
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(jumia_data)
    
    st.title("E-commerce Product Dashboard")
    st.write("Here are the top products from Jumia:")

    # Display the products in a table
    st.dataframe(df)
    
    # Optional: Add a search box
    search_term = st.text_input("Search products:")
    if search_term:
        df = df[df['title'].str.contains(search_term, case=False)]
        st.dataframe(df)

# Run the Streamlit app
if __name__ == "__main__":
    display_products()
