# main.py
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import FileResponse

import app.db_scripts as dbs
from app.models import UserCreate


sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


app = FastAPI()


@app.get("/product/{product_id}")
async def get_product_by_id(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    return {"message": f"No product with id {product_id}"}

@app.get("/products/search")
async def search_products(
    keyword: str,
    category: str | None = None,
    limit: int = 10
):
    
    products = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category:
                if product["category"] == category:
                    products.append(product)
            else: 
                products.append(product)

    return products[0:limit]