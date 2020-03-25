"""Contains user-defined Exception Class"""


class AuthorizationException(BaseException):
    """
    This exception is raise when Meetup.com detects malicious activity and activates reCaptcha
    """

    def __init__(self):
        print("Oh NO! \nMeetup.com has detected our robot.\nKindly login using the browser a few times till reCaptcha is removed!")


class CredentialsException(BaseException):
    """
    This exception is raise when the user credentials for sign in are invalid
    """

    def __init__(self):
        print("Your username or password is incorrent. Kindly recheck and export the correct credentials!")
