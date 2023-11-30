from fastapi import HTTPException


class ErrorMessages:
    UNKNOWN_ERROR_OCCURRED = HTTPException(status_code=500, detail="An unknown error occurred, please try again later")
    NOT_AUTHORIZED = HTTPException(status_code=401, detail="You are not authorized to make this request, please use a valid token")

    EMPTY_USERNAME = HTTPException(status_code=422, detail="Username is empty")
    EMPTY_PASSWORD = HTTPException(status_code=422, detail="Password is empty")
    MAXIMUM_USERNAME_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="Username exceeds maximum length of 32 characters")
    MAXIMUM_PASSWORD_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="Password exceeds maximum length of 32 characters")
    MINIMUM_USERNAME_LENGTH_SUBCEEDED = HTTPException(status_code=422, detail="Username does not meet minimum length of 8 characters")
    MINIMUM_PASSWORD_LENGTH_SUBCEEDED = HTTPException(status_code=422, detail="Password does not meet minimum length of 8 characters")
    USERNAME_SPACE = HTTPException(status_code=422, detail="Username cannot have spaces")
    PASSWORD_SPACE = HTTPException(status_code=422, detail="Password cannot have spaces")
    USERNAME_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="Username cannot contain special characters")



    ALREADY_EXISTING_ADMIN = HTTPException(status_code=409, detail="Username is already in use") # 409 used for conflict

    INVALID_LOGIN_CREDS = HTTPException(status_code=401, detail="Username or password incorrect")

    INVALID_TOKEN = HTTPException(status_code=401, detail=" The server could not verify the provided JWT (JSON Web Token) token. The token may be expired, invalid, or there is an issue with the signature.")

    EMPTY_TITLE = HTTPException(status_code=422, detail="Title is empty")
    EMPTY_AUTHOR = HTTPException(status_code=422, detail="Author is empty")
    EMPTY_GENRE = HTTPException(status_code=422, detail="Genre is empty")
    MAXIMUM_TITLE_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="Title exceeds maximum length of 96 characters")
    MAXIMUM_AUTHOR_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="Author exceeds maximum length of 50 characters")
    MAXIMUM_GENRE_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="Author exceeds maximum length of 50 characters")
    TITLE_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="Title cannot contain special characters")
    AUTHOR_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="Author cannot contain special characters")
    GENRE_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="Genre cannot contain special characters")
    TITLE_MISSING = HTTPException(status_code=422, detail="Title is missing from request")
    AUTHOR_MISSING = HTTPException(status_code=422, detail="Author is missing from request")
    GENRE_MISSING = HTTPException(status_code=422, detail="Genre is missing from request")
    BOOK_ID_MISSING = HTTPException(status_code=422, detail="ID is missing from request")


    EMPTY_LENDER_NAME = HTTPException(status_code=422, detail="Lender name is empty")
    MAXIMUM_LENDER_NAME_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="Lender name exceeds maximum length of 32 characters")
    MINIMUM_LENDER_NAME_LENGTH_SUBCEEDED = HTTPException(status_code=422, detail="Lender name does not meen minimum length of 5 characters")
    LENDER_NAME_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="Lender name cannot contain special characters")
    LENDER_NAME_MISSING = HTTPException(status_code=422, detail="Lender name is missing from request")
    LENDER_ID_MISSING = HTTPException(status_code=422, detail="Lender ID is missing from request")