import unittest
from fastapi.testclient import TestClient
from main import app

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_symmetric_key(self):
        response = self.client.get("/symmetric/key")
        self.assertEqual(response.status_code, 200)
        self.assertIn("key", response.json())

    def test_set_symmetric_key(self):
        response = self.client.post("/symmetric/key", json={"key": "test_key"})
        self.assertEqual(response.status_code, 200)

    def test_symmetric_encode(self):
        response = self.client.post("/symmetric/encode", json={"message": "test_message"})
        self.assertEqual(response.status_code, 400)  # Symmetric key not set

    def test_symmetric_decode(self):
        response = self.client.post("/symmetric/decode", json={"encrypted_message": "test_encrypted_message"})
        self.assertEqual(response.status_code, 400)  # Symmetric key not set

    # Podobne testy dla pozostałych endpointów...

if __name__ == "__main__":
    unittest.main()
