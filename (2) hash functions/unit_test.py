import unittest
import hashlib
import os
from main import hash_all, hash_file, measure_hash_time


class TestHashFunctions(unittest.TestCase):
    def setUp(self):
        self.test_text = "Test message"
        self.test_filename = "test_file.txt"
        self.test_file_contents = b'Test file contents'

        # Create a test file
        with open(self.test_filename, 'wb') as file:
            file.write(self.test_file_contents)

    def tearDown(self):
        # Remove the test file
        os.remove(self.test_filename)

    def test_hash_all(self):
        hash_all(self.test_text)
        # Check if the results file is created
        self.assertTrue(os.path.exists("./results/hashes.json"))

    def test_hash_file(self):
        expected_hash = hashlib.sha1(self.test_file_contents).hexdigest()
        computed_hash = hash_file(self.test_filename)
        self.assertEqual(computed_hash, expected_hash)

    def test_measure_hash_time(self):
        test_message = "Test message"
        expected_time = measure_hash_time(test_message)
        # The measured time should be a positive value
        self.assertGreaterEqual(expected_time, 0)


if __name__ == '__main__':
    unittest.main()
