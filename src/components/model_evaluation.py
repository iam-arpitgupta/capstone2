import os 
import sys 
import pandas as pd 
from src.exception import MyException
from src.constants import TARGET_COLUMN
from src.entity.s3_estimator import Proj1Estimator
from typing import Optional
from src.logger import logging 
from sklearn.metrics import f1_score 
from src.utils.main_utils import load_object 
from dataclasses import dataclass 
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact

@dataclass 
class EvaluateModelResponse:
    is_model_accepted : bool 
    difference : float 
    trained_model_f1_score : float
    best_model_f1_score: float


class ModelEvaluate:
    def __init__(self,model_trainer_artifact:ModelTrainerArtifact,data_ingestion_artifact:DataIngestionArtifact,
                model_eval_config:ModelEvaluationConfig)
        
        try:
            self.model_eval_config = model_eval_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise MyException(e,sys) from e
        
    def get_best_model(self)->Optional[Proj1Estimator]:
        """
        get the best model from the production stage 

        return the best model if available in s3 storage
        using the try and exception too
        """
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            proj1_estimator = Proj1Estimator(bucket_name=bucket_name , model_path = model_path)
            if proj1_estimator.is_model_present(model_path = model_path):
                return proj1_estimator
        except Exception as e:
            raise MyException(e,sys) from e 
        
    def _map_gender_column(self, df):
        """Map Gender column to 0 for Female and 1 for Male."""
        logging.info("Mapping 'Gender' column to binary values")
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df

    def _create_dummy_columns(self, df):
        """Create dummy variables for categorical features."""
        logging.info("Creating dummy variables for categorical features")
        df = pd.get_dummies(df, drop_first=True)
        return df

    def _rename_columns(self, df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logging.info("Renaming specific columns and casting to int")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype('int')
        return df
     
    def _drop_id_column(self, df):
        """Drop the 'id' column if it exists."""
        logging.info("Dropping 'id' column")
        if "_id" in df.columns:
            df = df.drop("_id", axis=1)
        return df
    
    def evaluate_model(self) -> EvaluateModelResponse:
        
        """
        Method Name :   evaluate_model
        Description :   This function is used to evaluate trained model 
                        with production model and choose best model 
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            ## doing the prediction on test set
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x , y = test_df.drop(TARGET_COLUMN,axis=1), test_df[TARGET_COLUMN]

            logging.info("test data loaded and now doing the prediction")

            x = self._map_gender_column(x)
            x = self._drop_id_column(x)
            x = self._create_dummy_columns(x)
            x = self._rename_columns(x)

            trained_model = self.model_trainer_artifact.trained_model_file_path
            logging.info(f"trained model loaded / exist:{trained_model}")
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            logging.info(f"trained model f1 score : {trained_model_f1_score}")

            best_model_f1_score  = None
            best_model = self.get_best_model()

            if best_model is not None:
                logging.info(f"Computing f1 score on test data")
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y,y_hat_best_model)
                logging.info(f"F1_Score-Production Model: {best_model_f1_score}, F1_Score-New Trained Model: {trained_model_f1_score}")

            tmp_best_model_score  = 0 if best_model_f1_score is None else best_model_f1_score:
            result = EvaluateModelResponse(trained_model_f1_score = trained_model_f1_score,
                                            best_model_f1_score = best_model_f1_score,
                                            is_model_accepted = trained_model_f1_score > tmp_best_model_score,
                                            difference = trained_model_f1_score - tmp_best_model_score)
            logging.info(f"Results : {result}")
            return result
                         
        except Exception as e:
            raise MyException(e,sys) from e
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model evaluation
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """  
        try:
            logging.info("Model Evaluatiomn started")
            model_eval_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference
            )
            logging.info(f"Model Evaluation artifact :{model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys) from e 
 
    