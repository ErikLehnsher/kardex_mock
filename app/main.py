from fastapi import FastAPI
import requests

app = FastAPI()

ODOO_WEBHOOK = "http://192.168.1.20:8069/connector/webhook/kardex_pps_simulate"

@app.post("/pps/send_confirmation")
def send_confirmation():
    payload = {
        "order_code": "PICK_001",
        "status": "FINISHED",
        "lines": [
            {"product": "CP431512-A", "qty": 4, "uom": "PCS"}
        ]
    }
    r = requests.post(ODOO_WEBHOOK, json=payload)
    return {"sent_to_odoo": r.status_code, "payload": payload}
