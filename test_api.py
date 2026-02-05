import requests
import json
import sys

def test_chat():
    url = "http://localhost:8000/chat"
    payload = {"query": "What is the specific policy on paternity leave?", "chat_history": []}
    headers = {"Content-Type": "application/json"}
    
    try:
        print("Sending request...")
        with requests.post(url, json=payload, stream=True) as r:
            print(f"Status Code: {r.status_code}")
            if r.status_code != 200:
                print(f"Error: {r.text}")
                return

            print("Response Stream:")
            for line in r.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if data['type'] == 'citations':
                            print("\n[Citations Found]:")
                            for cite in data['content']:
                                print(f" - {cite['source']} (Page {cite['page']})")
                        elif data['type'] == 'token':
                            print(data['content'], end='', flush=True)
                        elif data['type'] == 'error':
                            print(f"\n[Error from Server]: {data['content']}")
                    except json.JSONDecodeError:
                        print(f"\n[Raw]: {line}")
            print("\nDone.")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_chat()
