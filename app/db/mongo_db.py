import pymongo, dotenv
CFG = dotenv.dotenv_values(".env")


def save_to_mongodb(data):
    # Connect to MongoDB
    mongodb_client = pymongo.MongoClient(CFG["ATLAS_URI"])
    db = mongodb_client[CFG["DB_NAME"]]
    collection = db[CFG["COL_NAME"]]

    # Insert data into MongoDB
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print(f"Data successfully inserted into {db}.{collection} collection.")

