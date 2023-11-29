import re
from .errors import ErrorMessages

def validate_username(username):
    if username == "":
        raise ErrorMessages.EMPTY_USERNAME
    if len(username) > 32:
        raise ErrorMessages.MAXIMUM_USERNAME_LENGTH_EXCEEDED
    elif len(username) < 6:
        raise ErrorMessages.MINIMUM_USERNAME_LENGTH_SUBCEEDED
    elif " " in username:
        raise ErrorMessages.USERNAME_SPACE

    disallowed_chars = re.compile(r'[\'"<>!@#$%^&*()+=\[\]{}/\\;:,.`]')

    if disallowed_chars.search(username):
        raise ErrorMessages.USERNAME_SPECIAL_CHARACTERS
    
def validate_password(password):
    if password == "":
        raise ErrorMessages.EMPTY_PASSWORD
    elif len(password) > 32:
        raise ErrorMessages.MAXIMUM_PASSWORD_LENGTH_EXCEEDED
    elif len(password) < 6:
        raise ErrorMessages.MINIMUM_PASSWORD_LENGTH_SUBCEEDED
    elif " " in password:
        raise ErrorMessages.PASSWORD_SPACE