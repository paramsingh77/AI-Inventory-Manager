import pymongo
# from pymongo.errors import ConnectionError
# Replace the following with your MongoDB connection string
connection_string = "mongodb+srv://parminder13dev:qFkk7C0jXQifQglj@checkdata.7twp6.mongodb.net/?retryWrites=true&w=majority"
try:
    # Create a MongoClient
    client = pymongo.MongoClient(connection_string)
    
    # Attempt to retrieve server information
    server_info = client.server_info()
    
    print("Connected to MongoDB server successfully!")
    print("Server information:", server_info)
    
except Exception as e:
    print(f"An error occurred: {e}")