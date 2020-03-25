from bs4 import BeautifulSoup
import json
import argparse

import urls
import authentication

from group import Group
from event import Event

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
    Used to get the events page of a group.

    Parameters:
    group (Group object) : Instance of a class Group

    Returns:
    str : URL to fetch 10 events of this group.

    """
    return urls.BASE_URL + group.group_url + '/events/'


def rsvp_events(sess, group):
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

    res = sess.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_events = soup.find_all('a', {'id': 'attendButton'})

    rsvped_events = []
    for event in all_events:
        rsvp_endpoint = urls.BASE_URL + event.get('href')
        data = {
            'action': 'rsvp', 'response': 'yes'
        }
        if not args['dry_run']:
            res = sess.post(rsvp_endpoint, data=data)

        if res.status_code == 200:
            rsvp_event = Event(group.group_name, event.get(
                'href').split('/')[-2], True)
            rsvped_events.append(rsvp_event)

    jsonStr = json.dumps([x.__dict__ for x in rsvped_events])

    with open('rsvped_events.json', "w") as f:
        f.write(jsonStr)


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
    logged_in_session, _ = authentication.signin()

    for group in selected_groups:
        rsvp_events(logged_in_session, group)
        return


if __name__ == "__main__":
    main()
