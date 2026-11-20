from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .supplied import TOKENS

_bearer = HTTPBearer(auto_error=False)

bearer_creds = Annotated[HTTPAuthorizationCredentials, Depends(_bearer)]

def current_operator_id(
    creds: bearer_creds,
) -> int:
    operator_id = TOKENS.get(creds.credentials) if creds else None
    if operator_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return operator_id