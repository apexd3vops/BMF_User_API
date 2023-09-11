from jose import JWTError, jwt
from datetime import datetime, timedelta
#secrete_key
#algorithm
#expiration_time


SECRETE_KEY = "a4f190fe1598a1f419d968d8eae32583301f3da1e06f23d8f23acdff45e4d81f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


