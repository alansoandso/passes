import json
import logging
from user.utils import pformat

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


class Usernames(object):
    users = None

    def __init__(self):
        # Only load in the file once
        if not Usernames.users:
            Usernames.users = self.load_users()

    @staticmethod
    def load_users():
        try:
            users_path = '/Users/alan/workspace/popcorn-qa-cucumber-jvm/src/test/resources/environment/users.json'
            # Load all QA users
            with open(users_path) as json_data:
                return json.load(json_data).get('quality')
        except json.decoder.JSONDecodeError as error:
            logging.WARNING(f'Error on loading JSON from: {users_path}')
            raise error

    @staticmethod
    def list_usernames():
        names = ''
        for username in Usernames.users.keys():
            names += f'{username}\n'
        names += f'\nFound {len(Usernames.users)} available users'

        return names

    @staticmethod
    def get_profileid(user):
        """Retrieve a profile id from test users, if not found, assume user is the profile id
        """
        user_details = Usernames.users.get(user, '')
        if not user_details:
            user_details = {'profileId': user, 'info': 'Not a test user'}
        details = 'User details:\n'
        details += pformat(user_details)
        print(details)
        return user_details.get('profileId', '')
