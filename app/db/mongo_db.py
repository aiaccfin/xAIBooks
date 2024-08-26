import pymongo, dotenv, streamlit as st
CFG = dotenv.dotenv_values(".env")

def create_index():
    mongodb_client = pymongo.MongoClient(CFG["ATLAS_URI"])
    db = mongodb_client[CFG["DB_NAME"]]
    collection = db[CFG["COL_NAME"]]
    collection.create_index(
        [('clientID', pymongo.ASCENDING), ('date', pymongo.ASCENDING), ('description', pymongo.ASCENDING),
         ('amount', pymongo.ASCENDING)],
        unique=True
    )


def save_to_mongodb(data):
    # Connect to MongoDB
    collection =''
    db = ''
    try:
        mongodb_client = pymongo.MongoClient(CFG["ATLAS_URI"])
        db = mongodb_client[CFG["DB_NAME"]]
        collection = db[CFG["COL_NAME"]]
        st.write("Connected to MongoDB successfully.")

    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

    try:
        # Insert data into MongoDB
        if isinstance(data, list):
            st.write(1)
            collection.insert_many(data)
        else:
            st.write(2)
            collection.insert_one(data)
    except Exception as e:
        st.error(f"Already in DB.")


    print(f"Data successfully inserted into {db}.{collection} collection.")


def check_mongodb_connection():
    try:
        # Connect to MongoDB
        mongodb_client = pymongo.MongoClient(CFG["ATLAS_URI"])
        db = mongodb_client[CFG["DB_NAME"]]
        collection = db[CFG["COL_NAME"]]

        # Fetch a record from the collection
        record = collection.find_one()

        if record:
            st.write("Record found:", record)
        else:
            st.write("No record found in the collection.")

    except Exception as e:
        print(f"An error occurred: {e}")


