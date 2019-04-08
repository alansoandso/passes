from unittest.mock import call, patch, mock_open

import pytest

from mongo import entitlements


@patch('argparse.ArgumentParser')
def test_parser_print_usage(mock_parser):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        entitlements.parse_args(['passes'])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    mock_parser.assert_has_calls([call().print_usage()])


def test_parser_some_named_user():
    args = entitlements.parse_args('passes some_named_user'.split())
    assert 'some_named_user' == args.user


@patch('builtins.open', mock_open(read_data='{"quality":{"dictionary of": "users"}}'))
def test_load_users():
    actual = entitlements.load_users()
    assert {"dictionary of": "users"} == actual
    open.assert_called_once()


@pytest.fixture
def users():
    return {"moviesonly": {"profileId": "15706100", "username": "nowtvAutomation"}}


def test_profileid_from_username(users):
    assert users['moviesonly']['profileId'] == '15706100'
    assert entitlements.get_profileid('moviesonly', users) == '15706100'


def test_get_profileid_defaults(users):
    assert users['moviesonly']['profileId'] != '1234'
    assert entitlements.get_profileid('1234', users) == '1234'


@patch('mongo.entitlements.get_entitlements')
@patch('mongo.entitlements.load_users')
def test_clr_profileid(mock_load_users, mock_get_entitlements, users):
    mock_load_users.return_value = users
    entitlements.command_line_runner('passes moviesonly'.split())
    mock_get_entitlements.assert_called_once_with('15706100')
