import sqlite3
import hashlib
import os
import secrets
import hmac


class PasswordManager:
    def __init__(self, db_file: str):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                           (username TEXT PRIMARY KEY, hash TEXT, salt TEXT)''')
        self.conn.commit()

    def _generate_salt(self) -> str:
        """Returns random secure random text string in hexadecimal"""
        return secrets.token_hex(16)

    def _hash_password(self, password: str, salt: str) -> str:
        """Returns hashed password where generated salt is used"""
        """
        returns :key - hashed password
        """
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return key

    def save_password(self, username: str, password: str) -> None:
        """"Saves hashed password to database"""
        """
        :salt - salt used to hash password
        :hashed_password - hashed password that is going to be saved in the database
        """
        salt = self._generate_salt()
        hashed_password = self._hash_password(password, salt).hex()
        self.cursor.execute("INSERT OR REPLACE INTO passwords VALUES (?, ?, ?)",
                            (username, hashed_password, salt))
        self.conn.commit()

    def verify_password(self, username: str, password: str) -> bool:
        """Verifies hashed password with digest"""
        """
        :row - fetched record from the database
        :stored_hash - hash from :row (fetched record)
        :salt - salt from :row (fetched record)
        :hashed_password - hex from private field _hash_password
        """
        self.cursor.execute("SELECT hash, salt FROM passwords WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row:
            stored_hash, salt = row
            hashed_password = self._hash_password(password, salt).hex()
            return hmac.compare_digest(hashed_password, stored_hash)
        else:
            return False

    def close(self) -> None:
        self.conn.close()


# Driver code
if __name__ == "__main__":
    db_file = 'passwords.db'
    pm = PasswordManager(db_file)

    # Saving a password
    username = 'example_user'
    password = 'example_password'
    pm.save_password(username, password)

    # Verifying a password
    entered_password = 'example_password'
    if pm.verify_password(username, entered_password):
        print("Password is correct")
    else:
        print("Incorrect password")

    pm.close()
