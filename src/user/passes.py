#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

from user.mongo import Mongo
from user.usernames import Usernames
users = Usernames()

logging.basicConfig(level=logging.INFO, format='%(message)s')


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Display mongo entitlement records for a user')
    parser.add_argument('-a', '--all', action='store_true', default=False, help='All customer record')
    parser.add_argument('-i', '--atv', action='store_true', default=False, help='Apple TV records')
    parser.add_argument('-l', '--list_users', action='store_true', default=False, help='List all QA usernames')
    parser.add_argument('-v', '--vodafone', action='store_true', default=False, help='Vodafone records')
    parser.add_argument('user', action="store", nargs='?', help='Username or profileid')

    if len(argv) == 1:
        parser.print_usage()
        exit(1)
    else:
        return parser.parse_args(argv[1:])


def command_line_runner(argv=None):
    if argv is None:
        argv = sys.argv

    args = parse_args(argv)

    # List all QA users
    if args.list_users:
        users.list_usernames()
        return

    if args.user:
        profileid = users.get_profileid(args.user)
        if profileid:
            print(get_records(profileid, args))
            return


def get_records(profileid, include):
    mongo = Mongo(profileid)
    report = ''
    report += mongo.get_accounts()
    report += mongo.get_entitlements()

    if include.atv or include.all:
        report += mongo.get_atv_subscriptions()

    if include.vodafone or include.all:
        report += mongo.get_vodafone_accounts()
    return report


if __name__ == '__main__':
    sys.exit(command_line_runner())
