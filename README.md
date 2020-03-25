# Meetup auto-RVSP
This is a simple command line tool used for that sends an auto-RVSP to specific groups. 
The program takes care of authentication, searching for events in configured groups (not all), and automatically signing up on the user's behalf in a timely manner. 

This project was made using Python 3.7.4

## Set Up
1. Export your Meetup.com username and password as environment variables.
``` shell
export MEETUP_USERNAME=<username> 
export MEETUP_PASSWORD=<password>
```

2. Create a virtual environment and install the dependencies.
``` shell
python3 -m virtualenv <env-name>
source <env-name>/bin/activate
pip3 install -r requirements.txt
```

3. Run `setup_configs.py` inorder to select the desired groups.
``` shell
python3 setup_configs.py 
```
Now you can select the groups which you want to select for auto-RSVP via the commandline itself.
This generated the `selected_groups.json` with the groups selected by you.

4. Once you have generated the `selected_groups.json` file, run `auto_rsvp.py` inorder to RSVP all events available for the selected gropus. (First 10 events of each group)
``` shell
python3 auto_rsvp.py 
```
Note: You can add a `--dry_run` flag if you want to simply test the tool with making RSVPs.


## Exceptions

#### Meetup.com tracks for malicious internet traffic. Often, reCaptcha gets activated which leads to an AuthorizationException. 

If you encounter such a problem, login to meetup.com from your browser a couple of times until reCaptcha is disabled again.    