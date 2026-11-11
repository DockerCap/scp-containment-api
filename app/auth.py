import os
from secrets import compare_digest

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi import status

expected_key = os.environ.get("API_KEY")

if not expected_key:
    raise RuntimeError('API Key must be set')

api_key_header = APIKeyHeader(name='apikey', auto_error=True)

def require_api_key(key:str | None = Depends(api_key_header)) -> None:
    if key is None or not compare_digest(
        key.encode('utf-8'), expected_key.encode('utf-8')
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)