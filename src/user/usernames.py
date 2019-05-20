import json
from user.utils import pformat


class Usernames(object):
    users = None

    def __init__(self):
        # Only load in the file once
        if not Usernames.users:
            Usernames.users = self.load_users()

    @staticmethod
    def load_users():
        users_path = '/Users/alan/workspace/popcorn-qa-cucumber-jvm/src/test/resources/environment/users.json'
        # Load all QA users
        with open(users_path) as json_data:
            return json.load(json_data).get('quality')

    @staticmethod
    def list_usernames():
        for username in Usernames.users.keys():
            print(username)
        print(f'\nFound {len(Usernames.users)} available users')

    @staticmethod
    def get_profileid(user):
        user_details = Usernames.users.get(user, '')
        if not user_details:
            user_details = {'profileId': user}
        details = 'User details:\n'
        details += pformat(user_details)
        print(details)
        return user_details.get('profileId', '')
