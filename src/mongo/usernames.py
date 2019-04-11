import json
from mongo.utils import pformat


class Usernames(object):
    _state = {'_initialzed': False}

    def __new__(cls, *p, **k):
        self = object.__new__(cls, *p, **k)
        self.__dict__ = cls._state
        return self

    def __init__(self):
        # Only load in the file once
        if not self._initialzed:
            self.users = self.load_users()
            self._initialzed = True

    @staticmethod
    def load_users():
        users_path = '/Users/alan/workspace/qa-cucumber-jvm/src/test/resources/environment/users.json'
        # Load all QA users
        with open(users_path) as json_data:
            return json.load(json_data).get('quality')

    def list_usernames(self):
        for username in self.users.keys():
            print(username)
        print(f'\nFound {len(self.users)} available users')

    def get_profileid(self, user):
        user_details = self.users.get(user, '')
        if not user_details:
            user_details = {'profileId': user}
        details = 'User details:\n'
        details += pformat(user_details)
        print(details)
        return user_details.get('profileId', '')
