from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .supplied import TOKENS

_bearer = HTTPBearer(auto_error=False)


def current_operator_id(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> int:
    operator_id = TOKENS.get(creds.credentials) if creds else None
    if operator_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return operator_id
