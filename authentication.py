from requests import Session

import secrets
import urls
from exceptions import AuthorizationException, CredentialsException

"""This module deals with the authentication part. Based on the environment variables (MEETUP_USERNAME and MEETUP_PASSWORD), a user is logged in."""


def parse_token(page_html):
    """
    A helper function used to extract the session-token from the html string

    Parameters:
    page_html (str) : The HTML of the login page

    Returns:
    str: token

    """
    offset = 7
    token = page_html.find("token")
    start_pos = (page_html[token:]).find('value="') + token
    end_pos = (page_html[start_pos + offset:]).find('"') + start_pos + offset

    return page_html[start_pos + offset:end_pos]


def signin():
    """
    A funtion used to authenticate into meetup.com

    Returns:
    requests.Session() : Session object of the logged in session
    cookies : cookies of the logged session

    """

    sess = Session()
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = sess.get(urls.MEETUP_LOGIN_URL, headers=headers)

    payload = {
        'email': secrets.user_email,
        'password': secrets.user_password,
        'submitButton': 'Log in',
        'token': parse_token(r.text),
        'op': 'login',
        'returnUri': urls.BASE_URL,
    }

    res2 = sess.post(urls.MEETUP_LOGIN_URL, headers=headers, data=payload)

    if res2.text.find("password was entered incorrectly") is not -1:
        raise CredentialsException()

    if int(sess.cookies['memberId']) == 0:
        raise AuthorizationException()

    print("Authorized Succesfully!")
    cookies = sess.cookies

    return sess, cookies
