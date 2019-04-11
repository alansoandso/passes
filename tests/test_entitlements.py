from unittest.mock import call, patch, mock_open, Mock

import pytest

from mongo import entitlements


@patch('builtins.open',
       mock_open(read_data='{"quality":{"moviesonly": {"profileId": "15706100", "username": "nowtvAutomation"}}}'))
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


@patch('mongo.entitlements.users')
def test_clr_list_users(mock_list_users):
    entitlements.command_line_runner('passes --list_users'.split())
    assert mock_list_users.list_usernames.called_once()


@patch('mongo.entitlements.get_records')
def test_clr_profileid(mock_get_records):
    entitlements.command_line_runner('passes moviesonly'.split())
    mock_get_records.assert_called_once()
