import pymongo

DB_NAME = 'mongodb+srv://vilaj46:4ex2j842adji888@cluster0.djhoa.mongodb.net/myFirstDatabase'


def get_db():
    my_client = pymongo.MongoClient(DB_NAME)
    return my_client