from threading import Lock

shared_data = {"value": "Initial Data"}
data_lock = Lock()