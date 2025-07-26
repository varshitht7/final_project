# main.py
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce Chatbot API"}

@app.get("/top-products")
def get_top_products():
    # Load data
    order_items_df = pd.read_csv("data/order_items.csv")
    products_df = pd.read_csv("data/products.csv")

    # Count number of purchases for each product
    top_products = (
        order_items_df.groupby("product_id")
        .size()
        .reset_index(name="purchase_count")
        .sort_values(by="purchase_count", ascending=False)
        .head(5)
    )

    # Join with product details
    top_products = top_products.merge(products_df, left_on="product_id", right_on="id")

    # Select relevant info to return
    result = top_products[["product_id", "name", "brand", "retail_price", "purchase_count"]]

    # Convert to dictionary
    return result.to_dict(orient="records")