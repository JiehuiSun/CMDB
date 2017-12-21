import requests
import time
import hashlib



response = requests.get('http://127.0.0.1:8000/api/test.html',
                        headers={'auth-api':"387f764fc53eb316f148778ba2829b34|1506572694.6821892"})
print(response.text)