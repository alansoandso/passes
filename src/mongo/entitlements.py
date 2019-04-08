#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import logging
import sys

from pretty_json import format_json

from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format='%(message)s')


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Display mongo entitlement records for a user')
    parser.add_argument('-l', '--list_users', action='store_true', default=False, help='List all QA usernames')
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
    users = load_users()

    # List all QA users
    if args.list_users:
        list_usernames(users)
        return

    if args.user:
        profileid = get_profileid(args.user, users)
        if profileid:
            get_entitlements(profileid)
            return


def load_users():
    users_path = '/Users/alan/workspace/qa-cucumber-jvm/src/test/resources/environment/users.json'
    # Load all QA users
    with open(users_path) as json_data:
        users = json.load(json_data).get('quality')
    return users


def list_usernames(users):
    for username in users.keys():
        print(username)
    print(f'\nFound {len(users)} available users')


def get_profileid(user, users):
    user_details = users.get(user, '')
    if not user_details:
        user_details = {'profileId': user}
    print('User details:')
    pprint(user_details)
    profileid = user_details.get('profileId', '')
    print()
    return profileid


def get_entitlements(profileid):
    client = MongoClient('mongodb://qualdb01.nowtv.dev:27017')
    client.the_database.authenticate('popcorn', 'kernel', 'customer', mechanism='MONGODB-CR')
    accounts = client.customer.accounts

    print("db.getCollection('accounts').find({'_id' : '"+profileid+"'})")
    pprint(accounts.find_one({"_id": profileid}))
    print()

    entitlements = client.customer_passes.entitlements
    print("db.getCollection('entitlements').find({'accountId' : '"+profileid+"'})")
    pprint(entitlements.find_one({"accountId": profileid}))
    print()


def pprint(json):
    print(format_json(json, 'solarized'))


if __name__ == '__main__':
    sys.exit(command_line_runner())
