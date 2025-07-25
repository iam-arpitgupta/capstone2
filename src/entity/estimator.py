import sys 

import pandas as pd 
import numpy as np 

from pandas import DataFrame
from src.exception import MyException
from src.logger import logging 
from sklearn.pipeline import Pipeline
class TargetValueMapping:
    def __init__(self):
        self.yes : int = 0 
        self.no : int = 1

    def _asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))
    

class MyModel:
    def __init__(self,preprocessing_object : Pipeline,trained_model_object : object):
        
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self,dataframe:pd.DataFrame)->DataFrame:
        """
        Function accepts preprocessed inputs (with all custom transformations already applied),
        applies scaling using preprocessing_object, and performs prediction on transformed features.
        """ 
        try:
            logging.info("starting the prediction pipeline")

            ## apply scaling transformation using the pre-trained preprocessing object 
            transformed_feature = self.preprocessing_object.transform(dataframe)

            ## perform pipeline using the trained model 
            logging.info("using the trained pipeline to get the prediction")
            predictions = self.trained_model_object.predict(transformed_feature)

            return predictions
        
        except Exception as e:
            logging.error("error occcured in predict method",exc_info=True)
            raise MyException(e,sys) from e 
        


    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"