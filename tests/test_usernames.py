from unittest.mock import patch, mock_open
from mongo.usernames import Usernames


@patch('builtins.open',
       mock_open(read_data='{"quality":{"moviesonly": {"profileId": "15706100", "username": "nowtvAutomation"}}}'))
def test_load_users():
    assert Usernames.load_users() == {"moviesonly": {"profileId": "15706100", "username": "nowtvAutomation"}}
    # noinspection PyUnresolvedReferences
    open.assert_called_once()


def test_profileid_from_username():
    quality = Usernames()
    assert quality.get_profileid('moviesonly') == '15706100'


def test_get_profileid_defaults():
    quality = Usernames()
    assert quality.get_profileid('1234') == '1234'
