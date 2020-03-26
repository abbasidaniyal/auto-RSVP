
class Group:
    """
    A class to store the details of a single group

    Members:
    group_name : Name of the group organising this event.
    group_url : Unique url of this group.

    """

    def __init__(self, group_name, group_url):
        self.group_name = group_name
        self.group_url = group_url

    def __str__(self):
        return (self.group_name + ' : ' + self.group_url)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def fromJson(cls, json):
        """
        A factor construction to directly parse a dictionary to construct an object of the class

        Parameters:
        json (str) : dictionary containing the attributes of Group object

        Returns:
        Group : An object of Group class
        """
        group_name = json['group_name']
        group_url = json['group_url']
        return cls(group_name=group_name, group_url=group_url)
