from fastapi import FastAPI
import requests

app = FastAPI()

WEBHOOK = "https://expliseat.odoo.com/cds_connector/kardex_pps"

@app.get("/send_kardex")
def send_kardex():
    payload = [
        {
            "lot": "24LAN00017",
            "info1": "WH/MO/05925-001",
            "quantity": 96,
            "orderName": "WH/PC/40820",
            "lineNumber": 1,
            "materialName": "HW.010.0014_B", 
            "directionType": "PICK"
        },
        {
            "lot": "25RM001665",
            "info1": "WH/MO/05925-001",
            "quantity": 48,
            "orderName": "WH/PC/40820",
            "lineNumber": 2,
            "materialName": "BA.010.0184_E2",
            "directionType": "PICK"
        }
    ]

    headers = {"Content-Type": "application/json"}

    r = requests.post(WEBHOOK, json=payload, headers=headers)

    return {"status": r.status_code, "response": r.text}
