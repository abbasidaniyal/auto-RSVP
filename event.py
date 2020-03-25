class Event:
    """
    A class to store the details of a single event

    Members:
    group_name : Name of the group organising this event.
    event_id : Unique identifier of this event.
    rsvp_status : Status of user's RSVP

    """

    def __init__(self, group_name, event_id, rsvp_status=False):
        self.group_name = group_name
        self.event_id = event_id
        self.rsvp_status = rsvp_status

    def __str__(self):
        return (self.group_name + ' : ' + self.rsvp_status)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def fromJson(cls, json):
        """
        A factor construction to directly parse a dictionary to construct an object of the class

        Parameters:
        json (str) : dictionary containing the attributes of Event object

        Returns:
        Event : An object of Event class
        """
        group_name = json['group_name']
        event_id = json['event_id']
        rsvp_status = json['rsvp_status']
        return cls(
            group_name=group_name,
            event_id=event_id,
            rsvp_status=rsvp_status)
