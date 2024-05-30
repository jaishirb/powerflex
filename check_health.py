import requests

url = "http://localhost:8000/health"

try:
    response = requests.get(url)
    response.raise_for_status()
    print("Health check successful")
except requests.RequestException as e:
    print("Health check failed:", e)
    exit(1)
