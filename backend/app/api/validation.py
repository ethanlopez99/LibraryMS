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
    
def validate_title(title):
    if title.strip() == "":
        raise ErrorMessages.EMPTY_TITLE
    elif len(title.strip()) > 96:
        raise ErrorMessages.MAXIMUM_TITLE_LENGTH_EXCEEDED

    disallowed_chars = re.compile(r'[\'"<>@#$%^&*+=\[\]{}/\\;`]')

    if disallowed_chars.search(title.strip()):
        raise ErrorMessages.TITLE_SPECIAL_CHARACTERS
    
def validate_author(author):
    if author.strip() == "":
        raise ErrorMessages.EMPTY_AUTHOR
    elif len(author.strip()) > 96:
        raise ErrorMessages.MAXIMUM_AUTHOR_LENGTH_EXCEEDED

    disallowed_chars = re.compile(r'[\'"<>@#$%^&*+=\[\]{}/\\;`]')

    if disallowed_chars.search(author):
        raise ErrorMessages.AUTHOR_SPECIAL_CHARACTERS
    
def validate_genre(genre):
    if genre.strip() == "":
        raise ErrorMessages.EMPTY_GENRE
    elif len(genre.strip()) > 50:
        raise ErrorMessages.MAXIMUM_GENRE_LENGTH_EXCEEDED

    disallowed_chars = re.compile(r'[\'"<>@#$%^&*+=\[\]{}/\\;`]')

    if disallowed_chars.search(genre):
        raise ErrorMessages.GENRE_SPECIAL_CHARACTERS

def validate_lender_name(lender_name):
    if lender_name.strip() == "":
        raise ErrorMessages.EMPTY_LENDER_NAME
    elif len(lender_name.strip()) > 50:
        raise ErrorMessages.MAXIMUM_LENDER_NAME_LENGTH_EXCEEDED
    elif len(lender_name.strip()) < 5:
        raise ErrorMessages.MINIMUM_LENDER_NAME_LENGTH_SUBCEEDED
    
    disallowed_chars = re.compile(r'[\'"<>!@#$%^&*()+=\[\]{}/\\;:,.`]')

    if disallowed_chars.search(lender_name):
        raise ErrorMessages.LENDER_NAME_SPECIAL_CHARACTERS