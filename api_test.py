import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

print("\nAPI TEST RESULTS")
print("================")

try:
    response = requests.get(url, timeout=10)

    print(f"HTTP Status: {response.status_code}")

    if response.status_code != 200:
        print("FAIL - Unexpected HTTP status")
    else:
        print("PASS - API returned HTTP 200")

        data = response.json()

        # Test 1: Transaction ID
        if data.get("id") == 1:
            print("PASS - Correct transaction ID")
        else:
            print("FAIL - Incorrect transaction ID")

        # Test 2: Title
        if data.get("title"):
            print("PASS - Transaction title is present")
        else:
            print("FAIL - Transaction title is missing")

        # Test 3: User ID
        if data.get("userId") == 1:
            print("PASS - Correct user ID")
        else:
            print("FAIL - Incorrect user ID")

except requests.exceptions.Timeout:
    print("FAIL - API request timed out")

except requests.exceptions.ConnectionError:
    print("FAIL - Unable to connect to API")

except requests.exceptions.RequestException as error:
    print(f"FAIL - API request error: {error}")

except ValueError:
    print("FAIL - API returned invalid JSON")