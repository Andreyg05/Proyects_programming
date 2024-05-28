import uvicorn
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello_ud")
def hello_ud():
    return "Welcome to UD!"

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/public"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('description', String))

class Product(BaseModel):
    name: str
    description: str

@app.get("/products")
def get_products():
    try:
        query = select(products)
        result = session.execute(query)
        products_list = result.fetchall()
        if not products_list:
            raise HTTPException(status_code=404, detail="No products found")
        return [{"id": p.id, "name": p.name, "description": p.description} for p in products_list]
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products")
def create_product(product: Product):
    query = products.insert().values(name=product.name, description=product.description)
    session.execute(query)
    session.commit()
    return {"message": "Product created successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
