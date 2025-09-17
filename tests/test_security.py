import pytest
from datetime import timedelta
from jose import jwt, JWTError
from app import security
from app.config import settings

def test_create_access_token():
    data = {"sub": "testuser"}
    token = security.create_access_token(data)
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded_token["sub"] == "testuser"
    assert "exp" in decoded_token

def test_create_access_token_with_expiry():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=5)
    token = security.create_access_token(data, expires_delta=expires_delta)
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded_token["sub"] == "testuser"

def test_verify_valid_token():
    data = {"sub": "testuser"}
    token = security.create_access_token(data)
    # The credentials_exception would normally be an HTTPException
    # For testing, a simple Exception is sufficient.
    credentials_exception = Exception("Token validation failed")
    username = security.verify_access_token(token, credentials_exception)
    assert username == "testuser"

def test_verify_invalid_signature():
    data = {"sub": "testuser"}
    token = security.create_access_token(data)
    # Tamper with the token
    parts = token.split('.')
    tampered_token = f"{parts[0]}.{parts[1]}.tampered_signature"
    credentials_exception = Exception("Invalid signature")
    with pytest.raises(Exception) as excinfo:
        security.verify_access_token(tampered_token, credentials_exception)
    assert "Invalid signature" in str(excinfo.value)


def test_verify_expired_token():
    # Create a token that expired 1 second ago
    expires_delta = timedelta(seconds=-1)
    data = {"sub": "testuser"}
    expired_token = security.create_access_token(data, expires_delta=expires_delta)
    credentials_exception = Exception("Expired token")
    with pytest.raises(Exception) as excinfo:
        security.verify_access_token(expired_token, credentials_exception)
    assert "Expired token" in str(excinfo.value)

def test_verify_no_username():
    # Create a token without a "sub" field
    to_encode = {"some_other_field": "some_value"}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    credentials_exception = Exception("No username")
    with pytest.raises(Exception) as excinfo:
        security.verify_access_token(token, credentials_exception)
    assert "No username" in str(excinfo.value)
