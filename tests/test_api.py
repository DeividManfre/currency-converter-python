import pytest
import httpx
import os

BASE_URL = "http://localhost:8000"
LOG_DIR = "/app/tests/test_logs"
os.makedirs(LOG_DIR, exist_ok=True)

@pytest.fixture(scope='session')
def client():
    return httpx.Client(base_url=BASE_URL)

@pytest.fixture(scope='session')
def user_data():
    return {
        'name': 'pytest_user',
        'email': 'pytest_user@example.com',
        'password': 'StrongPass123@#'
    }

class OpenLog:
    @staticmethod
    def log(message, name):
        with open(f"{LOG_DIR}/{name}.log", 'a') as f:
            f.write(message + '\n')

def test_01_register_user(client, user_data):
    response = client.post("/auth/register", json=user_data)
    OpenLog.log(f"Register user response: {response.text}", 'register_user')

    assert response.status_code in (200, 400), f"Unexpected response: {response.text}"

    if response.status_code == 200:
        user_id = response.json().get("id")
        assert user_id, "User ID not found in register response"
        pytest.user_id = user_id
    else:
        login_resp = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        pytest.user_id = 1
        OpenLog.log("User already exists. Using default user_id=1", "register_user")

    OpenLog.log(f"User ID stored: {pytest.user_id}", "register_user")

@pytest.fixture(scope='session')
def access_token(client, user_data):
    response = client.post("/auth/login", json={
        'email': user_data['email'],
        'password': user_data['password']
    })
    assert response.status_code == 200, f"Login failed: {response.text}"

    token = response.json().get('access_token')
    assert token, "Access token not found in login response"

    OpenLog.log(f"Access token obtained: {token}", 'access_token')
    return token

def test_02_create_transaction(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    user_id = getattr(pytest, "user_id", None)
    assert user_id, "User ID not found from previous test"

    transaction_data = {
        "name": "pytest_transaction",
        "user_id": user_id,
        "from_currency": "USD",
        "to_currency": "BRL",
        "value": 10.0
    }

    response = client.post("/transactions/", json=transaction_data, headers=headers)
    OpenLog.log(f"Create transaction response: {response.text}", "create_transaction")

    assert response.status_code == 200, f"Failed to create transaction: {response.text}"

    data = response.json()
    assert "id" in data, "Transaction ID missing in response"
    pytest.transaction_id = data["id"]

    OpenLog.log(f"Transaction created with ID: {data['id']}", "create_transaction")

def test_03_get_transaction_by_id(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    tid = getattr(pytest, "transaction_id", None)
    assert tid, "Transaction ID not found from previous test"

    response = client.get(f"/transactions/{tid}", headers=headers)
    OpenLog.log(f"Transaction fetched by ID {tid}: {response.text}", "get_transaction_by_id")

    assert response.status_code == 200, f"Transaction fetch failed: {response.text}"

def test_04_get_all_transactions(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    user_id = getattr(pytest, "user_id", None)
    assert user_id, "User ID not found from previous test"
    response = client.get(f"/transactions/?userId={user_id}", headers=headers)
    OpenLog.log(f"All transactions response: {response.text}", "get_all_transactions")

    assert response.status_code == 200, f"Failed to fetch transactions: {response.text}"
    data = response.json()
    assert isinstance(data, list), "Expected a list of transactions"

def test_05_delete_transaction(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    tid = getattr(pytest, "transaction_id", None)
    assert tid, "Transaction ID not found from previous test"

    response = client.delete(f"/transactions/{tid}", headers=headers)
    OpenLog.log(f"Delete transaction response: {response.text}", "delete_transaction")

    assert response.status_code == 200, f"Failed to delete transaction: {response.text}"
    OpenLog.log(f"Transaction with ID {tid} deleted successfully.", "delete_transaction")
