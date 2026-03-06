import bcrypt

def hash_password(password: str):
    if isinstance(password, str):
        password = password.encode('utf-8') # Convert the password to bytes like b"password123". bcrypt operates only on byte strings
    password = password[:72] # Takes only the first 72 bytes of the password.
    salt = bcrypt.gensalt(rounds=12) # Function that creates a random salt. like b"$2b$12$KIXQJHj8uG9qjQZy1r5eO" where 12 is the cost factor (number of rounds)
    return bcrypt.hashpw(password, salt).decode('utf-8') # Hashes the password with the salt. Converts the resulting hash from bytes → string for storage in a database.

def verify_password(plain: str, hashed: str):
    if isinstance(plain, str):
        plain = plain.encode('utf-8') # Convert user-entered password to bytes like b"password123"
    plain = plain[:72]
    if isinstance(hashed, str): 
        hashed = hashed.encode('utf-8') # Convert user-entered password to bytes like b"qwlid7864qnkeq8n"
    return bcrypt.checkpw(plain, hashed) # Compares the plain password (bytes) with the hashed password (bytes).