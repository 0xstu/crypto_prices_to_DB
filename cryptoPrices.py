import os
import psycopg2
import Constants
from pycoinmarketcap import local_data, CoinMarketCap

cmc = CoinMarketCap()
ld = local_data()
columns = Constants.COLUMNS
conn = psycopg2.connect(os.environ['DATABASE_URL'])

#list all coins 
def list_coins():
    return cmc.list_listing().get('data')

#filter by top 100 based on cmc rank
def filter_coins(coins):
    return [coin for coin in coins if coin['cmc_rank'] <= 100]

# Search function to find column as key (property) in JSON returned from API
def search(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
            """return the value of only the first key that matches"""
        if arr:
            return arr[0]

    values = extract(obj, arr, key)
    return values


def create_rows(filter_coins):
    rows = ''
    # loop through array of coin objects
    for coin in filter_coins:
        row = '('
        for column in columns:
            value = search(coin, column)
            if value:
                if isinstance(value, str):
                    row = row + '\'' + str(value) + '\', '
                else:
                    row = row + str(value) + ', '
            else:
                row = row + 'NULL, '
        row = row[:-2] + '), '
        rows = rows + row
    return rows[:-2]

def add_columns(columns=columns):
    select = ''
    for column in columns:
        select = select + column + ', '
    return select[:-2]

# INSERT INTO accounts (id, balance) VALUES (1, 1000), (2, 250);
sql_string = "INSERT INTO {0} ({1}) VALUES \n {2};".format(Constants.DB_TABLE, add_columns(), create_rows(filter_coins(list_coins())))
# print(sql_string)

#write to DB table
with conn.cursor() as cur:
    cur.execute(sql_string)

conn.commit()
