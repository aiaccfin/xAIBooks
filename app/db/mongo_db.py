import pymongo, dotenv, streamlit as st
CFG = dotenv.dotenv_values(".env")

try:
    mongodb_client = pymongo.MongoClient(CFG["MONGO_STATEMENT_URI"])
    db = mongodb_client[CFG["DB_STATEMENT"]]
    collection_bank = db[CFG["COLLECTION_BANK"]]
    collection_cc   = db[CFG["COLLECTION_CC"]]
    collection_vendor = db[CFG["COLLECTION_VENDOR"]]
    st.write("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")


def create_index():
    collection_cc.create_index(
        [('clientID', pymongo.ASCENDING), ('date', pymongo.ASCENDING), ('description', pymongo.ASCENDING), ('amount', pymongo.ASCENDING)],
        unique=True
    )

    collection_bank.create_index(
        [('clientID', pymongo.ASCENDING), ('date', pymongo.ASCENDING), ('description', pymongo.ASCENDING),('amount', pymongo.ASCENDING)],
        unique=True
    )

    collection_vendor.create_index([('name', pymongo.ASCENDING)],   unique=True)

def save_to_cc(data):
    try:
        # Insert data into MongoDB
        if isinstance(data, list):
            st.write(1)
            collection_cc.insert_many(data)
        else:
            st.write(2)
            collection_cc.insert_one(data)
    except Exception as e:
        st.error(f"Already in DB.")

    print(f"Data successfully inserted into {db}.{collection_cc} collection.")


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


def save_vendor_information(vendor_name, business_info):
    try:
        collection_vendor.insert_one({
            "name": vendor_name,
            "information": business_info
        })
    except:pass