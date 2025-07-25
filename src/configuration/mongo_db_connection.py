## for setting up the connection with the mongodb database

import os 
import sys 
import certifi
import pymongo
from dotenv import load_dotenv 

from src.exception import MyException
from src.logger import logging 
from src.constants import DATABASE_NAME,MONGODB_URL_KEY

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    ----------
    client : MongoClient
        A shared MongoClient instance for the class.
    database : Database
        The specific database instance that MongoDBClient connects to.

    Methods:
    -------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.
    """

    client = None  # Shared MongoClient instance across all MongoDBClient instances

    def __init__(self,database_name:str = DATABASE_NAME) -> None:
        """
        initilize the mongodb client and if not present then create a new 
        """
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"{MONGODB_URL_KEY} is not set")
                
            # establish a new mongodb connection 
            MongoDBClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile = ca)
            # used the shared mongo db client 
            self.client = MongoDBClient.client 
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("Conection to the mongodb is done")

        except Exception as e:
            raise MyException(e,sys)
        
    







