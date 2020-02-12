import logging
import pymongo
import sys
from user.utils import pformat
from sshtunnel import SSHTunnelForwarder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


def ssh_tunnel(ip, port):
    """Return a SSH tunnel to the Mongo db
    """
    tunnel = SSHTunnelForwarder(
        ssh_address_or_host='jump01.slunow.bskyb.com',
        ssh_port=22,
        ssh_username='dbreporter',
        ssh_password='L53fv%kTr',
        remote_bind_address=(ip, port)
    )
    tunnel.start()
    return tunnel


def entitlements_collection(tunnel):
    """Return a mongo entitlements collection
    """
    client = pymongo.MongoClient('127.0.0.1', tunnel.local_bind_port, serverSelectionTimeoutMS=1500)
    client.the_database.authenticate(name='popcorn', password='kernel', source='customer_passes', mechanism='MONGODB-CR')

    return client.customer_passes.entitlements


def accounts_collection(tunnel):
    """Return a mongo accounts collection
    """
    client = pymongo.MongoClient('127.0.0.1', tunnel.local_bind_port, serverSelectionTimeoutMS=1500)
    client.the_database.authenticate(name='popcorn', password='kernel', source='customer', mechanism='MONGODB-CR')

    return client.customer.accounts


def get_production_records(account_id):
    # Tunnel into the production db
    accounts_db_tunnel = ssh_tunnel('prddb00.slunow.bskyb.com', 27018)
    entitlements_db_tunnel = ssh_tunnel('prdcpsdb00.slunow.bskyb.com', 27018)
    report = ''
    try:
        # Get mongo collection objects for the accounts and entitlements
        accounts = accounts_collection(accounts_db_tunnel)
        report += f"\ndb.getCollection('accounts').find({{'_id' : '{account_id}'}})\n"
        account_record = accounts.find_one({"_id": account_id})
        report += pformat(account_record)

        entitlements = entitlements_collection(entitlements_db_tunnel)
        # Output all records found
        report += f"\n\ndb.getCollection('entitlements').find({{'accountId' : '{account_id}'}})"
        for entitlement in entitlements.find({"accountId": account_id}):
            if entitlement:
                report += '\n'
            report += pformat(entitlement)

    finally:
        accounts_db_tunnel.stop()
        entitlements_db_tunnel.stop()

    return report


if __name__ == '__main__':
    if sys.argv[1] and sys.argv[1].isdigit():
        print(get_production_records(sys.argv[1]))
    else:
        print(f'usage: {sys.argv[0]} <accountId>')
