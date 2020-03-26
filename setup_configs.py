from bs4 import BeautifulSoup
import json

import utils.urls as urls
import utils.authentication as authentication
from utils.exceptions import AuthorizationException, CredentialsException

from utils.group import Group


def get_all_groups(sess, token):

    res = sess.get(urls.ALL_GROUPS_LIST_URL)

    soup = BeautifulSoup(res.text, 'html.parser')

    page = soup.find('div', {'id': 'simple-view'})
    temp = page.find_all('ul',)
    list_of_groups = temp[0].find_all('li')

    groups = []
    print("Select which groups to auto RSVP : ")
    for i, group in enumerate(list_of_groups):
        tmp = Group(
            group_name=group.get('data-name'),
            group_url=group.get('data-urlname'))
        groups.append(tmp)

        print(f"{i+1}. " + str(tmp))

    selected_groups = input(
        "[Enter Serial Numbers with a single blank space] : ")
    selected_array = [int(x) for x in selected_groups.strip().split(' ')]

    print("Selected Groups -")
    for x in selected_array:
        print(groups[x - 1])

    jsonStr = json.dumps([groups[x - 1].__dict__ for x in selected_array])

    with open('selected_groups.json', "w") as f:
        f.seek(0)
        f.write(jsonStr)
        f.truncate()

    # Creates an empty file if does not exist, else does nothing.
    with open('rsvped_events.json', 'w'):
        pass


def main():
    try:
        logged_in_session, token = authentication.signin()
    except AuthorizationException:
        return
    except CredentialsException:
        return

    get_all_groups(logged_in_session, token)
    print("You configuration settings have been updated!")


if __name__ == '__main__':
    main()
