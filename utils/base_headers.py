"""These are the headers send along with the rsvp requests."""

RSVP_GET = {
    'authority': 'www.meetup.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/80.0.3987.132 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
    'application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

RSVP_POST = {
    'authority': 'www.meetup.com',
    'sec-fetch-dest': 'empty',
    'x-meetup-activity': 'standardized_url=%2Furlname%2Fevents%2FeventId&standardized_referer=undefined',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'origin': 'https://www.meetup.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'no-cors',
    'referer': '',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
