import base64
import logging
import os
import pickle
import pymongo
import sys
from user.utils import pprint
from sshtunnel import SSHTunnelForwarder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


class Mongo(object):
    def __init__(self, collection):
        get_records()
        if collection == 'customer':
            self.tunnel = self.ssh_tunnel(os.getenv('r'), 27018)
        elif collection == 'customer_passes':
            self.tunnel = self.ssh_tunnel(os.getenv('c'), 27018)
        elif collection == 'customer_passes':
            self.tunnel = self.ssh_tunnel(os.getenv('k'), 27018)
        elif collection == 'gifting' or collection == 'popcorn' or collection == 'products':
            self.tunnel = self.ssh_tunnel(os.getenv('e'), 27018)
        else:
            raise RuntimeError(f'Unknown database collection {collection}')

        # print(f'Using port:{self.tunnel.local_bind_port} for {collection}')
        self.client = pymongo.MongoClient('127.0.0.1', self.tunnel.local_bind_port, serverSelectionTimeoutMS=1500)
        self.client.the_database.authenticate('popcorn', os.getenv('t'), collection, mechanism='MONGODB-CR')

    def __del__(self):
        self.tunnel.stop()

    def close(self):
        self.tunnel.stop()

    def accounts(self):
        return self.client.customer.accounts

    def entitlements(self):
        return self.client.customer_passes.entitlements

    @staticmethod
    def ssh_tunnel(ip, port):
        """Return a SSH tunnel to the Mongo db
        """
        tunnel = SSHTunnelForwarder(
            ssh_address_or_host='jump01.slunow.bskyb.com',
            ssh_port=22,
            ssh_username=os.getenv('q'),
            ssh_password=os.getenv('a'),
            remote_bind_address=(ip, port)
        )
        tunnel.start()
        return tunnel


def get_production_records(account_id):
    customer_db = Mongo('customer')
    accounts = customer_db.accounts()
    print(f"db.getCollection('accounts').find_one({{'_id' : '{account_id}'}})")
    account_record = accounts.find_one({"_id": account_id})
    pprint(account_record)
    customer_db.close()

    entitlements_db = Mongo('customer_passes')
    entitlements = entitlements_db.entitlements()
    # Output all records found
    print("\n\ndb.getCollection('entitlements').find({{'accountId' : '{account_id}'}})")
    for entitlement in entitlements.find({"accountId": account_id}):
        if entitlement:
            pprint(entitlement)
    entitlements_db.close()


def get_records():
    for k, v in pickle.load(open(os.path.join(os.getenv('HOME'), '.sshh'), 'rb')).items():
        os.environ[k] = base64.b64decode(v).decode("utf-8")


if __name__ == '__main__':
    if sys.argv[1] and sys.argv[1].isdigit():
        get_production_records(sys.argv[1])
    else:
        print(f'usage: {sys.argv[0]} <accountId>')
