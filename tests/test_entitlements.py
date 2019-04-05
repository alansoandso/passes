from io import StringIO
from unittest import TestCase
from unittest.mock import patch, mock_open

from mongo import entitlements


class TestEntitlements(TestCase):
    def setUp(self):
        pass

    def test_parser_some_named_user(self):
        with patch('sys.argv', ['', 'some_named_user']):
            parser = entitlements.get_parser()
            args = vars(parser.parse_args())
            self.assertEqual('some_named_user', args['user'])

    @patch('sys.argv', ['', ''])
    @patch('mongo.entitlements.argparse.ArgumentParser.print_help')
    def test_clr_print_help(self, mock_print_help):
        entitlements.command_line_runner()
        mock_print_help.assert_called_once()

    @patch('sys.argv', ['', 'moviesonly'])
    @patch('mongo.entitlements.get_entitlements')
    def test_clr_profileid(self, mock_get_entitlements):
        entitlements.command_line_runner()
        mock_get_entitlements.assert_called_once_with('15706100')

