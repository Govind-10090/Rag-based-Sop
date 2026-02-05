import requests
import concurrent.futures
import time

URL = "http://localhost:8000/chat"
PAYLOAD = {"query": "What is the leave policy?", "chat_history": []}
HEADERS = {"Content-Type": "application/json"}
CONCURRENT_REQUESTS = 5

def send_request(i):
    try:
        start = time.time()
        print(f"Start Request {i}")
        # Not streaming for stress test, just checking status
        response = requests.post(URL, json=PAYLOAD, headers=HEADERS, timeout=30)
        duration = time.time() - start
        print(f"Request {i}: Status {response.status_code} (Time: {duration:.2f}s)")
        return response.status_code
    except Exception as e:
        print(f"Request {i} Failed: {e}")
        return 0

def stress_test():
    print(f"Starting Stress Test with {CONCURRENT_REQUESTS} concurrent users...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(send_request, i) for i in range(CONCURRENT_REQUESTS)]
        
        results = [f.result() for f in futures]
    
    print("\nResults:")
    print(f"200 OK: {results.count(200)}")
    print(f"429 Too Many Requests: {results.count(429)}")
    print(f"Failures: {results.count(0)}")

if __name__ == "__main__":
    stress_test()

