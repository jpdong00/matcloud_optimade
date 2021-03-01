import time

from optimade.filterparser import LarkParser
from optimade.filtertransformers.mongo import MongoTransformer
from utils.lower2upper import Lower2Upper
from pymongo import MongoClient, ASCENDING
from pprint import pprint
from bson import ObjectId
from utils.info import info1, info2


class MatCloudMongoDB:
    def __init__(self):
        p = LarkParser(version=(1, 0, 0), variant="default")
        t = MongoTransformer()
        self.transform = lambda inp: t.transform(p.parse(inp))

        client = MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format(
            "admin", "admin", "localhost", "27017", "admin"))
        db = client["MaterialsDB"]
        self.cl = db["Data.Calculation.StaticCalculation"]

        self.lu = Lower2Upper()

        self.data = info1
        self.info = info2

    def get_my_field(self, query):
        query = query.replace('has', "HAS").replace('any', "ANY").replace('all', "ALL").\
            replace('only', "ONLY").replace('and', "AND").replace('length', "LENGTH")

        if 'elements HAS ONLY' in query:
            new_query = 'elements LENGTH ' + str(len(query.split(','))) + ' AND elements HAS ALL'
            query = query.replace('elements HAS ONLY', new_query)
        if 'elements HAS' in query:
            query = query.replace('elements HAS', 'structure.composition.symbol HAS')
        if 'elements LENGTH' in query:
            query = query.replace('elements LENGTH', 'structure.composition LENGTH')
        if 'nelements' in query:
            query = query.replace('nelements', 'structure.number_of_species')

        query_list = query.split(' ')
        query = ' '.join([q.strip() for q in query_list])

        return query

    def update_new_record(self, record, new_records):
        tmp = {"ID": str(record["_id"]),
               "SimplestFormula": record["Structure"]["SimplestFormula"],
               "CompleteFormula": record["Structure"]["CompleteFormula"],
               "SpaceGroup": record["Structure"]["SpaceGroup"]
               }
        new_records.append(tmp)

        return new_records

    def get_meta(self, url, num):
        self.data['meta']['query']['representation'] = url
        self.data['meta']['time_stamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.data['meta']['data_returned'] = num

    def find(self, url, query, skip=None, limit=None, sort=None):
        skip = 0 if skip is None else skip
        limit = 10 if limit is None else limit
        sort = '_id' if sort is None else sort

        query = self.get_my_field(query)
        query = self.transform(query)
        mongo_query = self.lu.lower2upper(query)
        # print(mongo_query)
        records = self.cl.find(mongo_query).skip(skip).limit(limit).sort(sort, ASCENDING)

        new_records = []
        for r in list(records):
            new_records = self.update_new_record(r, new_records)

        self.get_meta(url, len(list(new_records)))
        self.data['data'] = new_records

        return self.data

    def find_one(self, url):
        r = self.cl.find_one()
        new_records = self.update_new_record(r, [])

        self.get_meta(url, 1)
        self.data['data'] = new_records

        return self.data

    def find_by_id(self, url, id):
        r = self.cl.find_one({'_id': ObjectId(id)})
        new_records = self.update_new_record(r, [])
        new_records[0]["Properties"] = r["Properties"]
        del new_records[0]["SpaceGroup"]

        self.get_meta(url, 1)
        self.data['data'] = new_records
        return self.data

    def get_info(self):
        info2['meta']['time_stamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        return info2


if __name__ == '__main__':
    md = MatCloudMongoDB()
    # records = md.find_one()
    # records = md.find_by_id("596dbf74f55ef66ae0830b2b")
    # query = 'elements HAS ANY "Ba","O" AND elements LENGTH 3'
    # query = 'elements HAS ALL "Ba", "O" AND elements LENGTH 3'
    # query = 'elements HAS ALL "Ba", "O"'
    # query = 'elements HAS ONLY "Ba", "Nb", "O"'
    # query = 'nelements>=5 AND nelements<=7'
    # query = 'elements LENGTH 3'
    query = 'elements LENGTH 3 AND elements HAS ALL "Ba", "O"'
    records = md.find("matcloud.com", query, limit=5, sort="_id")
    pprint(records)
