import unittest
from datetime import datetime, timezone, timedelta

try:
    import jwt
    import bcrypt
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False


class TestAuthSecurity(unittest.TestCase):
    def setUp(self):
        self.jwt_secret = "test_secret_key_career_advisor_2026"
        self.jwt_algorithm = "HS256"

    def test_password_hashing_and_verification(self):
        if not DEPS_AVAILABLE:
            self.skipTest("bcrypt or pyjwt not installed in current environment; tested in CI")

        raw_password = "SecurePassword2026!"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')

        self.assertNotEqual(hashed, raw_password)
        self.assertTrue(bcrypt.checkpw(raw_password.encode('utf-8'), hashed.encode('utf-8')))
        self.assertFalse(bcrypt.checkpw(b"WrongPassword", hashed.encode('utf-8')))

    def test_jwt_token_lifecycle(self):
        if not DEPS_AVAILABLE:
            self.skipTest("bcrypt or pyjwt not installed in current environment; tested in CI")

        payload = {"sub": "user_12345", "email": "student@example.com", "role": "STUDENT"}
        expire = datetime.now(timezone.utc) + timedelta(days=1)
        payload["exp"] = expire

        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        self.assertIsInstance(token, str)

        decoded = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
        self.assertEqual(decoded["sub"], "user_12345")
        self.assertEqual(decoded["email"], "student@example.com")


if __name__ == "__main__":
    unittest.main()
