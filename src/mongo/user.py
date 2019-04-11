from pymongo import MongoClient
from mongo.utils import pformat


class User(object):
    def __init__(self, id):
        self.profileid = id
        self.client = MongoClient('mongodb://qualdb01.nowtv.dev:27017')
        self.client.the_database.authenticate('popcorn', 'kernel', 'customer', mechanism='MONGODB-CR')

    def get_accounts(self):
        return self.get_details_by(key='_id', database='customer', collection='accounts')

    def get_entitlements(self):
        return self.get_details_by(key='accountId', database='customer_passes', collection='entitlements')

    def get_atv_subscriptions(self):
        return self.get_details_by(key='accountId', database='customer', collection='atv_subscriptions')

    def get_vodafone_accounts(self):
        return self.get_details_by(key='accountId', database='customer', collection='vodafone_accounts')

    def get_details_by(self, key='accountId', database='', collection=''):
        db_collection = self.client.__getattr__(database).__getattr__(collection)
        details = f"\ndb.getCollection('{collection}').find({{'accountId' : '{self.profileid}'}})\n"
        details += pformat(db_collection.find_one({key: self.profileid}))
        return details

