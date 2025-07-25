from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel
import sys
from pandas import DataFrame


class Proj1Estimator:
    """
    this clas is used to load , save and predict the model
    """
    def __init__(self):
        """
        :param bucket_name: Name of your model bucket
        :param model_path: Location of your model in bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.load_model : MyModel = None

    def is_model_present(self,model_path):
        try:
            return self.s3_key_path_available(bucket_name=self.bucket_name,s3_key=self.model_path)
        except Exception as e:
            raise MyException(e,sys) from e

    
    def load_model(self)->MyModel:
        """
        load the model from the model path 
        """
        try:
            return self.s3.load_model(self.bucket_name,self.model_path)
        except Exception as e:
            raise MyException(e,sys) from e

    def save_model(self,from_file:str,remove:bool=False)-> None:
        """
        save the model to the model path 
        :param from_file: Your local system model path
        :param remove: By default it is false that mean you will have your model locally available in your system folder
        """
        try:
            self.s3.upload_file(
                from_file,
                bucket_name = self.bucket_name,
                to_filename = self.model_path
                remove = remove
            )
            
        except Exception as e:
            raise MyException(e,sys) from e 
        pass 

    def predict(self,dataframe:DataFrame)->DataFrame:
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe)

        except Exception as e:
            raise MyException(e,sys) from e