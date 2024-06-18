import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import requests

test_user_ids = [
    "87f5b737-19ab-4059-bc59-746bddb6b6b0",
    "51a7bbb3-5b3f-47e6-885e-6b88268bf717",
    "1d1ba311-8547-4fb2-9528-543cdac8ac3a",
    "352f0762-07ce-4eb8-8026-16acc6f4614c",
    "8f1c2ca5-b521-4531-a341-c3a38434f8e1",
    "794d9ee7-da10-463f-a9ab-7d0b88596a71",
    "3eca87c2-f13b-44db-ac5d-b5c724fe0c93",
    "04f5cc9c-8413-4601-a441-742bc42a53df",
    "02c53f0f-4e84-4bca-9577-780c03652f2d",
    "8881d51e-e7e0-4f2d-b8fd-33dbbd92778f",
]

endpoints = [
    "http://localhost:5000/api/v1/click",
    "http://localhost:5000/api/v1/quality",
    "http://localhost:5000/api/v1/event",
    "http://localhost:5000/api/v1/film",
    "http://localhost:5000/api/v1/page",
]

def generate_data():
    user_id = random.choice(test_user_ids)
    return {
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

def send_request(url, data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    return response

def task(index):
    data = generate_data()
    url = random.choice(endpoints)  # Случайный выбор конечной точки
    response = send_request(url, data)
    if response.status_code != 200:
        print(f"Request {index} to {url} failed: {response.text}")
    else:
        print(f"Request {index} to {url} succeeded: {response.content}")

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