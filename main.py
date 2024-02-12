from fastapi import FastAPI, Depends, HTTPException, Path
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from bson import json_util

app = FastAPI()

# MongoDB connection pool
client = MongoClient("mongodb://mongodb:27017/")  # Use the service name defined in Docker Compose
db = client["stocks"]

def get_db():
    yield db

def ensure_stocks_collection():
    if "stocks" not in db.list_collection_names():
        db.create_collection("stocks")

@app.post("/insert-demo-stocks")
def insert_demo_stocks(db: MongoClient = Depends(get_db)):
    ensure_stocks_collection()

    demo_stocks = [
        {"symbol": "AAPL", "company": "Apple Inc.", "price": 150.25},
        {"symbol": "GOOGL", "company": "Alphabet Inc.", "price": 2700.50},
        {"symbol": "MSFT", "company": "Microsoft Corp.", "price": 300.75},
    ]

    collection = db["stocks"]
    try:
        collection.insert_many(demo_stocks)
        print("Demo stocks inserted successfully")
        return JSONResponse(content={"message": "Demo stocks inserted successfully"}, status_code=200)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error inserting demo stocks: {e}")
        return JSONResponse(content={"message": "Error inserting demo stocks"}, status_code=500)

@app.get("/stocks/{symbol}")
def get_stock_by_symbol(symbol: str, db: MongoClient = Depends(get_db)):
    collection = db["stocks"]
    stock_data = collection.find_one({"symbol": symbol})

    if stock_data:
        # Convert ObjectId to string
        serialized_data = json_util.dumps(stock_data)
        return JSONResponse(content=serialized_data, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")
