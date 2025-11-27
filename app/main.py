from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Kardex Mock Server")

# Fake database
ORDERS = {}
MATERIALS = {
    "CP431512-A": {
        "materials": [
            {
                "materialName": "CP431512-A",
                "materialType": "ITEM",
                "weight": 10,
                "dimensions": "10x20",
            }
        ]
    }
}

@app.get("/")
def root():
    return {"message": "Kardex Mock Server Running"}

# -----------------------
# GET MATERIAL
# -----------------------
@app.get("/api/v1/materials/{material_name}")
def get_material(material_name: str):
    return MATERIALS.get(material_name, {"materials": []})

# -----------------------
# CREATE ORDER
# -----------------------
@app.post("/api/v1/orders")
async def create_order(request: Request):
    data = await request.json()
    order_name = data["orderName"]
    ORDERS[order_name] = data
    return {"orders": [data], "errors": []}

# -----------------------
# GET ORDER
# -----------------------
@app.get("/api/v1/orders/{order_name}")
def get_order(order_name: str):
    if order_name not in ORDERS:
        return JSONResponse(status_code=404, content={"error": "Order not found"})
    return {"orders": [ORDERS[order_name]]}

# -----------------------
# DELETE ORDER
# -----------------------
@app.delete("/api/v1/orders/{order_name}")
def delete_order(order_name: str):
    if order_name in ORDERS:
        del ORDERS[order_name]
        return {"success": True}
    return JSONResponse(status_code=404, content={"error": "Order not found"})

# -----------------------
# SEND PPS CONFIRMATION TO ODOO
# -----------------------
@app.post("/send_pps")
async def send_pps(request: Request):
    data = await request.json()
    import requests

    odoo_url = data["odoo_url"]
    payload = data["payload"]

    print(f"[KARDEX MOCK] → sending PPS to Odoo: {odoo_url}")

    r = requests.post(odoo_url, json=payload)

    return {
        "sent_to": odoo_url,
        "status_code": r.status_code,
        "response": r.text
    }
