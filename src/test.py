import requests

api_key = 'dae8cdd4-ca33-4ff8-83aa-38add53810e8'
url = 'https://api.example.com/endpoint'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)

if response.status_code == 403:
    print("Access forbidden: Check your API key permissions.")
else:
    print(response.json())