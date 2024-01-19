import requests
from flask import Flask, render_template
from flask_frozen import Freezer
import requests
import os
import imghdr
import shutil
import tempfile
import pymongo
from io import BytesIO
from dotenv import dotenv_values, load_dotenv

load_dotenv()

# config = dotenv_values(".env")

app = Flask(__name__)

featured_products = [
    {"id": 1, "name": "Rose Bouquet", "description": "Beautiful arrangement of red roses.", "price": 29.99, "image": "imgs/000001.jpg"},
    {"id": 2, "name": "Lily Vase", "description": "Elegant vase with a mix of lilies.", "price": 39.99, "image": "imgs/000002.jpg"},
    {"id": 3, "name": "Tulip Bouquet", "description": "Cheerful bouquet of tulips.", "price": 19.99, "image": "imgs/000003.jpg"},
    {"id": 4, "name": "Daisy Vase", "description": "Bright and colorful daisies.", "price": 29.99, "image": "imgs/000004.jpg"},
    {"id": 5, "name": "Carnation Bouquet", "description": "Traditional bouquet of carnations.", "price": 24.99, "image": "imgs/000005.jpg"},
    {"id": 6, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000006.jpg"},
    {"id": 7, "name": "Orchid Plant", "description": "A beautiful orchid plant.", "price": 29.99, "image": "imgs/000007.jpg"},
    {"id": 8, "name": "Succulent Plant", "description": "A succulent plant.", "price": 19.99, "image": "imgs/000008.jpg"},
    {"id": 9, "name": "Peace Lily", "description": "A peace lily plant.", "price": 19.99, "image": "imgs/000009.jpg"},
    {"id": 10, "name": "Hydrangea Bouquet", "description": "A bouquet of hydrangeas.", "price": 29.99, "image": "imgs/000010.jpg"},
    {"id": 11, "name": "Sunflower Bouquet", "description": "A bouquet of sunflowers.", "price": 29.99, "image": "imgs/000016.jpg"},
    {"id": 12, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000035.jpg"},
    {"id": 13, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 35.99, "image": "imgs/000036.jpg"},
    {"id": 14, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 36.99, "image": "imgs/000037.jpg"},
    {"id": 15, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 37.99, "image": "imgs/000040.jpg"},
    {"id": 16, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 38.99, "image": "imgs/000016.jpg"},
    {"id": 17, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 39.99, "image": "imgs/000017.jpg"},
    {"id": 18, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 30.99, "image": "imgs/000018.jpg"},
    {"id": 19, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 3445.99, "image": "imgs/000019.jpg"},
    {"id": 20, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000020.jpg"},
]

# Sample data for a product detail
product_detail1 = {"id": 1, "name": "Rose Bouquet", "description": "Beautiful arrangement of red roses.", "price": 29.99, "image": "imgs/000001.jpg"}
product_detail2 = {"id": 2, "name": "Lily Vase", "description": "Elegant vase with a mix of lilies.", "price": 39.99, "image": "imgs/000002.jpg"}
product_detail3 = {"id": 3, "name": "Tulip Bouquet", "description": "Cheerful bouquet of tulips.", "price": 19.99, "image": "imgs/000003.jpg"}
product_detail4 = {"id": 4, "name": "Daisy Vase", "description": "Bright and colorful daisies.", "price": 29.99, "image": "imgs/000004.jpg"}
product_detail5 = {"id": 5, "name": "Carnation Bouquet", "description": "Traditional bouquet of carnations.", "price": 24.99, "image": "imgs/000005.jpg"}
product_detail6 = {"id": 6, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000006.jpg"}
product_detail7 = {"id": 7, "name": "Orchid Plant", "description": "A beautiful orchid plant.", "price": 29.99, "image": "imgs/000007.jpg"}
product_detail8 = {"id": 8, "name": "Succulent Plant", "description": "A succulent plant.", "price": 19.99, "image": "imgs/000008.jpg"}
product_detail9 = {"id": 9, "name": "Peace Lily", "description": "A peace lily plant.", "price": 19.99, "image": "imgs/000009.jpg"}
product_detail10 = {"id": 10, "name": "Hydrangea Bouquet", "description": "A bouquet of hydrangeas.", "price": 29.99, "image": "imgs/000010.jpg"}
product_detail11 = {"id": 11, "name": "Sunflower Bouquet", "description": "A bouquet of sunflowers.", "price": 29.99, "image": "imgs/000016.jpg"}
product_detail12 = {"id": 12, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000035.jpg"}
product_detail13 = {"id": 13, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000036.jpg"}
product_detail14 = {"id": 14, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000037.jpg"}
product_detail15 = {"id": 15, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000040.jpg"}
product_detail16 = {"id": 16, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000016.jpg"}
product_detail17 = {"id": 17, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000017.jpg"}
product_detail18 = {"id": 18, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000018.jpg"}
product_detail19 = {"id": 19, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000019.jpg"}
product_detail20 = {"id": 20, "name": "Mixed Bouquet", "description": "Mixed bouquet of roses, lilies, and daisies.", "price": 34.99, "image": "imgs/000020.jpg"}

@app.route('/')
def home():
    return render_template('index.html', featured_products=featured_products)

@app.route('/product/<int:product_id>.html')
def product_detail(product_id):
    product = next((product for product in featured_products if product["id"] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)
