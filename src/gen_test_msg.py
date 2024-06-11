import requests
import json
from datetime import datetime, timezone
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_data(index):
    return {
        "user_id": f"user_{index}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "item_id": f"item_{index}"
    }

def send_request(data):
    url = "http://localhost:5000/click"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    return response

def task(index):
    data = generate_data(index)
    response = send_request(data)
    if response.status_code != 200:
        print(f"Request {index} failed: {response.text}")
    else:
        print(f"Request {index} succeeded: {response.content}")

def main():
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task, i) for i in range(100000)]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Exception occurred: {e}")
    
    end_time = time.time()
    print(f"Sent 100000 requests in {end_time - start_time} seconds")

if __name__ == "__main__":
    main()