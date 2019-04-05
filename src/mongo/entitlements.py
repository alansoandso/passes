#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import logging
from pretty_json import format_json

from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def get_parser():
    parser = argparse.ArgumentParser(description='Display mongo entitlement records for a user')
    parser.add_argument('-l', '--list_users', action='store_true', default=False, help='List all QA usernames')
    parser.add_argument('user', action="store", nargs='?', help='Username or profileid')
    return parser


def command_line_runner():
    parser = get_parser()
    args = parser.parse_args()
    users = load_users()

    # List all QA users
    if args.list_users:
        list_usernames(users)
        return

    if args.user:
        profileid = get_profileid(args, users)
        if profileid:
            get_entitlements(profileid)
            return

    # Default display help and quit
    parser.print_help()


def load_users():
    users_path = '/Users/alan/workspace/qa-cucumber-jvm/src/test/resources/environment/users.json'
    # Load all QA users
    with open(users_path) as json_data:
        users = json.load(json_data).get('quality')
    return users


def list_usernames(users):
    for username in users.keys():
        print(username)
    print('\nFound {} available users'.format(len(users)))


def get_profileid(args, users):
    user_details = users.get(args.user, '')
    if not user_details:
        user_details = {'profileId': args.user}
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
    command_line_runner()
