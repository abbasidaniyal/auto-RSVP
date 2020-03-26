from bs4 import BeautifulSoup
import json
import argparse

import utils.urls as urls
import utils.authentication as authentication
import utils.base_headers as base_headers

from utils.group import Group
from utils.event import Event

"""This module performs the automatic RSVP of selected groups. It containes the helper funtion as well as the driver code needed to implement auto_rsvp of selected groups"""

"""
Parsing Command line arguements to check for --dry_run
"""
parser = argparse.ArgumentParser(
    description='This module performs the automatic RSVP of selected groups. It containes the helper funtion as well as the driver code needed to implement auto_rsvp of selected groups')

parser.add_argument(
    '--dry_run', help='an integer for the accumulator', action='store_true', default=False)
args = parser.parse_args()


def get_upcoming_events_url(group):
    """
    Used to get the events page url of a group.

    Parameters:
    group (Group object) : Instance of a class Group

    Returns:
    str : URL to fetch 10 events of this group.

    """
    return urls.BASE_URL + group.group_url + '/events/'


def get_rsvped_events_string():
    """
    A funtion which reads the rsvped_events.json file and parses the list of Groups

    Parameters:
    None

    Returns:
    list of Events : A list containing multiple Event objects 

    """
    with open('rsvped_events.json', "r") as f:
        f.seek(0)
        jsonStr = f.read()

    return jsonStr


def rsvp_events(sess, token, group):
    """
    Used to RSVP the events of a particular group

    Parameters:
    sess (requests.Session object): A Session object of the logged in session
    group (Group object) : A object of Group class, denoting selected group.

    Returns:
    None

    Writes:
    logs the RSVP-ed events into a 'rsvped_events.json' file.
    """
    url = get_upcoming_events_url(group)
    rsvped_events_string = get_rsvped_events_string()

    res = sess.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_events = soup.find_all('a', {'id': 'attendButton'})
    rsvped_events = []
    for event in all_events:
        sess.headers = base_headers.RSVP_GET
        id = event.get('href').split('/')[-2]
        rsvp_endpoint = urls.BASE_URL + \
            event.get('href')+'action=rsvp&response=yes'

        if id in rsvped_events_string:
            continue

        if not args.dry_run:
            params = (
                ('action', 'rsvp'),
                ('response', 'yes'),
            )

            res = sess.get(urls.BASE_URL + event.get('href'), params=params)

            sess.headers = base_headers.RSVP_POST
            sess.headers['x-mwp-csrf'] = sess.cookies['x-mwp-csrf-header']
            sess.headers['referer'] = rsvp_endpoint

            query = '(endpoint:' + group.group_url + "/events/" + id + "/rsvps" + ',meta:(method:post),' + 'params:(eventId:' + id + \
                ',fields:rsvp_counts,' + 'response:yes,' + 'urlname:' + group.group_url + \
                ')' + ',ref:rsvpAction' + "_" + group.group_url + '_' + id + ')'

            data = {
                'queries': query
            }
            res = sess.post(
                'https://www.meetup.com/mu_api/urlname/events/eventId', data=data)

            if res.status_code == 200:
                rsvp_event = Event(group.group_name, id, True)
                rsvped_events.append(rsvp_event)

    old_rsvped_events = [Event.fromJson(x)
                         for x in json.loads(rsvped_events_string)]
    rsvped_events += old_rsvped_events
    jsonStr = json.dumps([x.__dict__ for x in rsvped_events])

    with open('rsvped_events.json', "w") as f:
        f.seek(0)
        f.write(jsonStr)
        f.truncate()


def get_selected_groups():
    """
    A funtion which reads the selected_groups.json file created by setup_configs and parses the list of Groups

    Parameters:
    None

    Returns:
    list of Group : A list containing multiple Group objects 

    """
    with open('selected_groups.json', "r") as f:
        f.seek(0)
        jsonStr = f.read()

    selected_groups = [Group.fromJson(x) for x in json.loads(jsonStr)]
    print(selected_groups)
    return selected_groups


def main():
    """
    Driver Funtion, used to orchestrate and link various helper functions
    """
    selected_groups = get_selected_groups()
    logged_in_session, token = authentication.signin(verbose=False)

    for group in selected_groups:
        rsvp_events(logged_in_session, token, group)


if __name__ == "__main__":
    main()
