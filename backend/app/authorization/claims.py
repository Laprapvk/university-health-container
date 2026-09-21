SUBJECT_CLAIM = "sub"
ROLE_CLAIM = "role"


def create_claims(subject: str, role: str | None = None) -> dict:
    claims = {SUBJECT_CLAIM: subject}
    if role is not None:
        claims[ROLE_CLAIM] = role
    return claims


def get_claims(token: str) -> dict:
    from app.authentication.security import decode_token

    return decode_token(token)


def get_subject(claims: dict) -> str | None:
    return claims.get(SUBJECT_CLAIM)


def get_role(claims: dict) -> str | None:
    return claims.get(ROLE_CLAIM)