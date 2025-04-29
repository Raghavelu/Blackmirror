import json
import os

STATUS_FILE = 'storage/status.json'
os.makedirs('storage', exist_ok=True)

def set_status(status, runtime=None):
    data = {
        "status": status,
        "last_runtime": runtime
    }
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f)

def get_status():
    if not os.path.exists(STATUS_FILE):
        return {"status": "idle", "last_runtime": None}
    with open(STATUS_FILE, 'r') as f:
        return json.load(f)
