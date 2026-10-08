import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"


def check(name,response,expected_status):

    if response.status_code == expected_status:
        print(f"PASS {name}")
    else:

        print(
            f"FAIL {name} "
            f"expected {expected_status}, "
            f"got {response.status_code}"
        )

        print("Response:",response.text)


def test_get_all_trips():
    response = requests.get(f"{BASE_URL}/trips")

    check(
        "GET /trips",
        response,
        200
    )

def test_create_trip():
    global trip_id

    data = {
        "destination": "Cox's Bazar",
        "start_date": "2026-11-20",
        "end_date": "2026-11-23",
        "budget": 20000,
        "max_travelers": 5
    }

    response = requests.post(
        f"{BASE_URL}/trips",
        json=data
    )

    check(
        "POST /trips",
        response,
        201
    )

    if response.status_code == 201:
        trip_id = response.json()["data"]["id"]

def test_get_trip():

    response = requests.get(
        f"{BASE_URL}/trips/{trip_id}"
    )

    check(
        f"GET /trips/{trip_id}",
        response,
        200
    )


def test_get_nonexistent_trip():
    nonexistent_id = 99999

    response = requests.get(
        f"{BASE_URL}/trips/{nonexistent_id}"
    )

    check(
        f"GET /trips/{nonexistent_id} (not found)",
        response,
        404
    )


def test_invalid_trip_id():
    response = requests.get(
        f"{BASE_URL}/trips/abc"
    )

    check(
        "GET /trips/abc (invalid ID)",
        response,
        404
    )


def test_update_trip():
    data = {
        "destination": "Sylhet"
    }

    response = requests.put(
        f"{BASE_URL}/trips/{trip_id}",
        json=data
    )

    check(
        f"PUT /trips/{trip_id}",
        response,
        200
    )


def test_change_status():
    data = {
        "status": "ONGOING"
    }

    response = requests.patch(
        f"{BASE_URL}/trips/{trip_id}/status",
        json=data
    )

    check(
        f"PATCH /trips/{trip_id}/status",
        response,
        200
    )


def test_summary():
    response = requests.get(
        f"{BASE_URL}/trips/{trip_id}/summary"
    )

    check(
        f"GET /trips/{trip_id}/summary",
        response,
        200
    )


def test_delete_trip():
    response = requests.delete(
        f"{BASE_URL}/trips/{trip_id}"
    )

    check(
        f"DELETE /trips/{trip_id}",
        response,
        200
    )


def run_tests():
    print("\nRunning API tests...\n")

    
    test_create_trip()
    test_get_all_trips()
    

    if trip_id is None:
        print("\nTrip creation failed. Skipping dependent tests.")
        return

    test_get_trip()
    test_get_nonexistent_trip()
    test_invalid_trip_id()
    test_update_trip()
    test_change_status()
    test_summary()
    test_delete_trip()

    print("\nTesting completed.")


if __name__ == "__main__":
    run_tests()