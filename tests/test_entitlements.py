from unittest.mock import patch, mock_open

import pytest

from mongo import entitlements


@patch('sys.argv', ['', 'some_named_user'])
def test_parser_some_named_user():
    parser = entitlements.get_parser()
    args = vars(parser.parse_args())
    assert 'some_named_user' == args['user']


@patch('sys.argv', ['', ''])
@patch('mongo.entitlements.load_users')
@patch('mongo.entitlements.argparse.ArgumentParser.print_help')
def test_clr_print_help(mock_load_users, mock_print_help):
    mock_load_users.return_value = {}
    entitlements.command_line_runner()
    mock_print_help.assert_called_once()


@patch('sys.argv', ['', 'moviesonly'])
@patch('mongo.entitlements.get_entitlements')
@patch('mongo.entitlements.load_users')
def test_clr_profileid(mock_load_users, mock_get_entitlements, users):
    mock_load_users.return_value = users
    entitlements.command_line_runner()
    mock_get_entitlements.assert_called_once_with('15706100')


@patch('builtins.open', mock_open(read_data='{"quality":{"dictionary of": "users"}}'))
def test_load_users():
    actual = entitlements.load_users()
    assert {"dictionary of": "users"} == actual
    open.assert_called_once()


@pytest.fixture
def users():
    return {"moviesonly": {"profileId": "15706100", "username": "nowtvAutomation"}}


def test_profileid_from_username(users):
    class args:
        user = 'moviesonly'
    assert entitlements.get_profileid(args, users) == '15706100'


def test_get_profileid_defaults(users):
    class args:
        user = '1234'
    assert entitlements.get_profileid(args, users) == '1234'
