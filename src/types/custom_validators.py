from re import compile


PASSWORD_REGEX = compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$")


def password_validator(v: str) -> str:
    if PASSWORD_REGEX.fullmatch(v) is None:
        raise ValueError('incorrect password')
    return v


def is_alpha_validator(v: str) -> str:
    if not v.isalpha():
        raise ValueError('can contain only letters')
    return v
