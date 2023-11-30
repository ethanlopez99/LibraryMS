from fastapi import HTTPException


class ErrorMessages:
    UNKNOWN_ERROR_OCCURRED = HTTPException(status_code=500, detail="An unknown error occurred on the server. Please try your request again later.")

    NOT_AUTHORIZED = HTTPException(status_code=401, detail="Authentication failed. You are not authorized to make this request. Please ensure you have a valid and active authentication token.")

    EMPTY_USERNAME = HTTPException(status_code=422, detail="The username cannot be empty. Please provide a valid username.")
    EMPTY_PASSWORD = HTTPException(status_code=422, detail="The password cannot be empty. Please provide a valid password.")
    MAXIMUM_USERNAME_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="The provided username exceeds the maximum length of 32 characters. Please choose a shorter username.")
    MAXIMUM_PASSWORD_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="The provided password exceeds the maximum length of 32 characters. Please choose a shorter password.")
    MINIMUM_USERNAME_LENGTH_SUBCEEDED = HTTPException(status_code=422, detail="The provided username does not meet the minimum length requirement of 8 characters. Please choose a longer username.")
    MINIMUM_PASSWORD_LENGTH_SUBCEEDED = HTTPException(status_code=422, detail="The provided password does not meet the minimum length requirement of 8 characters. Please choose a longer password.")
    USERNAME_SPACE = HTTPException(status_code=422, detail="The username cannot contain spaces. Please remove any spaces from the username.")
    PASSWORD_SPACE = HTTPException(status_code=422, detail="The password cannot contain spaces. Please remove any spaces from the password.")
    USERNAME_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="The username cannot contain special characters. Please use only alphanumeric characters for the username.")

    ALREADY_EXISTING_ADMIN = HTTPException(status_code=409, detail="The provided username is already in use. Please choose a different username.")

    INVALID_LOGIN_CREDS = HTTPException(status_code=401, detail="Invalid login credentials. Please check your username and password and try again.")

    INVALID_TOKEN = HTTPException(status_code=401, detail="Invalid JWT token. The server could not verify the provided JSON Web Token. The token may be expired, invalid, or there is an issue with the signature.")

    EMPTY_TITLE = HTTPException(status_code=422, detail="The book title cannot be empty. Please provide a valid title.")
    EMPTY_AUTHOR = HTTPException(status_code=422, detail="The author's name cannot be empty. Please provide a valid author name.")
    EMPTY_GENRE = HTTPException(status_code=422, detail="The genre cannot be empty. Please provide a valid genre.")
    MAXIMUM_TITLE_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="The provided title exceeds the maximum length of 96 characters. Please choose a shorter title.")
    MAXIMUM_AUTHOR_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="The provided author name exceeds the maximum length of 50 characters. Please choose a shorter author name.")
    MAXIMUM_GENRE_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="The provided genre exceeds the maximum length of 50 characters. Please choose a shorter genre.")
    TITLE_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="The title cannot contain special characters. Please use only alphanumeric characters and common symbols.")
    AUTHOR_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="The author name cannot contain special characters. Please use only alphanumeric characters and common symbols.")
    GENRE_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="The genre cannot contain special characters. Please use only alphanumeric characters and common symbols.")
    TITLE_MISSING = HTTPException(status_code=422, detail="The title is missing from the request. Please provide a valid title.")
    AUTHOR_MISSING = HTTPException(status_code=422, detail="The author name is missing from the request. Please provide a valid author name.")
    GENRE_MISSING = HTTPException(status_code=422, detail="The genre is missing from the request. Please provide a valid genre.")
    BOOK_ID_MISSING = HTTPException(status_code=422, detail="The book ID is missing from the request. Please provide a valid book ID.")
    BOOK_NOT_FOUND = HTTPException(status_code=404, detail="The requested book could not be found. Please ensure the provided book ID is correct and try again.")

    EMPTY_LENDER_NAME = HTTPException(status_code=422, detail="The lender name cannot be empty. Please provide a valid lender name.")
    MAXIMUM_LENDER_NAME_LENGTH_EXCEEDED = HTTPException(status_code=422, detail="The provided lender name exceeds the maximum length of 32 characters. Please choose a shorter lender name.")
    MINIMUM_LENDER_NAME_LENGTH_SUBCEEDED = HTTPException(status_code=422, detail="The provided lender name does not meet the minimum length requirement of 5 characters. Please choose a longer lender name.")
    LENDER_NAME_SPECIAL_CHARACTERS = HTTPException(status_code=422, detail="The lender name cannot contain special characters. Please use only alphanumeric characters and common symbols.")
    LENDER_NAME_MISSING = HTTPException(status_code=422, detail="The lender name is missing from the request. Please provide a valid lender name.")
    LENDER_ID_MISSING = HTTPException(status_code=422, detail="The lender ID is missing from the request. Please provide a valid lender ID.")

    BOOK_NOT_AVAILABLE_TO_LOAN = HTTPException(status_code=409, detail="The book is already loaned out and not available for loan.")
    BOOK_NOT_AVAILABLE_TO_RETURN = HTTPException(status_code=409, detail="The book has not been loaned out and cannot be returned.")
    RETURNING_LENDER_MISMATCH = HTTPException(status_code=409, detail="The returning lender does not match the loaning lender. Only the lender who initially loaned the book can return it.")


