from fastapi.testclient import TestClient
from app.main import app
import sys

client = TestClient(app)

def test_create_veterinario():
    # Use a random email to avoid conflict if running multiple times
    import random
    email = f"juan{random.randint(1, 10000)}@vet.com"
    
    response = client.post(
        "/veterinario/register",
        json={
            "name": "Juan Vet",
            "email": email,
            "password": "securepassword",
            "role": "Veterinario",
            "telefonos": ["1234567890"]
        }
    )
    print(f"Create Vet Status: {response.status_code}")
    print(f"Create Vet Response: {response.json()}")
    if response.status_code != 201:
        print("FAILED: Create Vet")
        sys.exit(1)

def test_websocket():
    try:
        with client.websocket_connect("/chat/ws/1") as websocket:
            websocket.send_text("Hello World")
            data = websocket.receive_text()
            print(f"WebSocket Received: {data}")
            if "Hello World" not in data:
                print("FAILED: WebSocket content mismatch")
                sys.exit(1)
    except Exception as e:
        print(f"FAILED: WebSocket connection error: {e}")
        # WebSocket might fail if not properly set up in main.py or dependencies missing
        # But we want to see the error
        sys.exit(1)

if __name__ == "__main__":
    print("Running verification...")
    test_create_veterinario()
    print("Veterinario creation test passed.")
    
    test_websocket()
    print("WebSocket test passed.")
