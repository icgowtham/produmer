"""Configuration file."""

DATA_DIR = 'data'
UPDATE_STMT = "UPDATE user_info SET username = '{nm}' WHERE email = '{em}'"
INSERT_STMT = "INSERT INTO user_info (username, email) VALUES ('{nm}', '{em}')"
