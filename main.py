from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory database (for now)
orders_db = {}
order_counter = 1


# Request model
class Order(BaseModel):
    customer_name: str
    item: str
    quantity: int


# Home route (optional but helpful)
@app.get("/")
def home():
    return {"message": "Restaurant Order API is running"}


# Create a new order
@app.post("/orders")
def create_order(order: Order):
    global order_counter

    orders_db[order_counter] = {
        "customer_name": order.customer_name,
        "item": order.item,
        "quantity": order.quantity,
        "status": "Received"
    }

    created_id = order_counter
    order_counter += 1

    return {
        "message": "Order created",
        "order_id": created_id
    }


# Get order status
@app.get("/orders/{order_id}/status")
def get_order_status(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order_id,
        "status": orders_db[order_id]["status"]
    }


# Update order status
@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    orders_db[order_id]["status"] = status

    return {
        "message": "Status updated",
        "new_status": status
    }