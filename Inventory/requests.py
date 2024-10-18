import requests

# Define the URL
url = "https://services.wheel-size.com/widget/f9b678a8a5ea494aaa034197ad0cc677/api/sm?make=aion&model=hyper-ht&year=2024"

try:
    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
