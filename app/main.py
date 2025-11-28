import requests
import json

ODOO_URL = "http://192.168.62.100:8069/cds_connector/kardex_pps"   # Thay IP máy Odoo

payload = [
    {
        "orderName": "WH/PC/40820",
        "materialName": "HW.010.0014_B",
        "quantity": 96,
        "directionType": "PICK",
        "lineNumber": 1,
        "lot": "TESTLOT001"
    },
    {
        "orderName": "WH/PC/40820",
        "materialName": "BA.010.0184_E2",
        "quantity": 48,
        "directionType": "PICK",
        "lineNumber": 2,
        "lot": "TESTLOT002"
    }
]

headers = {"Content-Type": "application/json"}

response = requests.post(ODOO_URL, data=json.dumps(payload), headers=headers)

print("Status:", response.status_code)
print("Response:", response.text)
