from pymongo import MongoClient
from environs import Env
from bson.objectid import ObjectId

env = Env()
env.read_env()

client = MongoClient(host=env("DB_HOST"), port=env.int("DB_PORT"))
db = client[env("DB_NAME")]
users_collection = db.users

def user_exists(phone=None, user_id=None):
    """
    Check if a user with the given phone number or user ID already exists in the collection.

    :param phone: The phone number to check for (optional).
    :param user_id: The user ID to check for (optional).
    :return: True if the user exists, False otherwise.
    """
    # Build the query
    query = {}
    if phone:
        query["phone"] = phone
    if user_id:
        query["_id"] = ObjectId(user_id)
    
    # Check if a user with the given phone number or ID exists
    user = users_collection.find_one(query)
    
    return user is not None

def get_thread_and_assistant(phone):
    try:
        user = users_collection.find_one({"phone": phone}, {"_id": 0, "thread": 1, "assistant": 1})
        if user:
            return user.get("thread"), user.get("assistant")
        else:
            print(f"No user found with phone: {phone}")
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def get_stage(phone):
    """
    Retrieve the stage of a user based on their phone number.

    :param phone: The phone number of the user whose stage is to be retrieved.
    :return: The stage of the user if found, otherwise None.
    """
    try:
        # Find the user document by phone number
        user = users_collection.find_one({"phone": phone}, {"stage": 1})
        
        if user:
            # Return the stage field if user is found
            return user.get("stage")
        else:
            # Return None if user is not found
            return None
    except Exception as e:
        print(f"An error occurred while retrieving the user's stage: {e}")
        return None

def update_stage(phone, new_stage):
    try:
        # Update the stage of the user with the given phone number
        result = users_collection.update_one(
            {"phone": phone},  # Filter by phone number
            {"$set": {"stage": new_stage}}  # Set the new stage
        )
        if result.matched_count > 0:
            print("Stage updated successfully.")
        else:
            print("User not found.")
    except Exception as e:
        print(f"An error occurred while updating the stage: {e}")


def create_user(name, phone, date):
    user_data = {
        "name": name,
        "phone": phone,
        "stage": "start",
        "first_date": date,
        "last_date": date,
        "thread": "",
        "assistant": "",
    }
    try:
        users_collection.insert_one(user_data)
        print("User created successfully")
    except Exception as e:
        users_collection.delete_one({"phone": phone})
        print(f"An error ocurred: {e}")

def update_thread_and_assistant(phone, new_thread, new_assistant):
    try:
        result = users_collection.update_one(
            {"phone": phone},
            {"$set": {"thread": new_thread, "assistant": new_assistant}}
        )
        if result.matched_count > 0:
            print("User thread and assistant updated successfully")
        else:
            print(f"No user found with phone: {phone}")
    except Exception as e:
        print(f"An error occurred: {e}")
