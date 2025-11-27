from fastapi import FastAPI, Request
import uvicorn
import json
from typing import Dict
import requests
import time

ODOO_WEBHOOK_URL = "http://192.168.62.105:8069/cds_connector/kardex_pps"

app = FastAPI()

# Fake "database"
orders: Dict[str, dict] = {}


@app.post("/api/v1/orders")
async def create_order(payload: dict):
    """
    Odoo gọi create_order → Kardex mock lưu state → trả về OK
    """

    order = {
        "order_name": payload.get("orderName"),
        "lines": payload.get("lines", []),
        "state": "created",
    }
    orders[order["order_name"]] = order

    print("=== CREATE ORDER RECEIVED ===")
    print(order)

    # Giả lập 2s sau Kardex gửi webhook PPS
    time.sleep(2)
    send_pps_webhook(order)

    return {"errors": [], "orders": [order]}


@app.get("/api/v1/orders/{order_name}")
async def get_order(order_name: str):
    """
    Odoo request GET /orders/<name>
    """
    order = orders.get(order_name)
    if not order:
        return {"errors": ["NOT FOUND"]}

    return {"errors": [], "orders": [order]}


@app.delete("/api/v1/orders/{order_name}")
async def delete_order(order_name: str):
    if order_name in orders:
        del orders[order_name]
    return {"errors": []}


def send_pps_webhook(order):
    """
    Gửi webhook confirmation về Odoo
    payload phải đúng format Kardex → Odoo mong đợi
    """

    payload = {
        "orderName": order["order_name"],
        "confirmationState": "completed",
        "lines": order["lines"],
    }

    print("=== SENDING WEBHOOK TO ODOO ===")
    print(ODOO_WEBHOOK_URL)
    print(payload)

    try:
        r = requests.post(ODOO_WEBHOOK_URL, json=payload, timeout=5)
        print("Webhook sent → status:", r.status_code)
    except Exception as e:
        print("Webhook error:", e)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
