import os 
import sys 

from src.exception import MyException
from src.logger import logging 
from src.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluate
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact)

class TrainingPipeline:
    def __init__(self):
       self.data_ingestion_config = DataIngestionConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:
        '''
        this is reposndible for starting the data ingestion pipeline 
        '''
        try:
            logging.info("Starting the data ingestion")
            logging.info("Get the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("got the train_ste and test_set form mongodb ")
            logging.info("Excited the data ingestion from the training pipeline")
            return data_ingestion_artifacts
        except Exception as e:
            raise MyException(e,sys)
        

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        '''
        responsible for starting the data vlaidation pipeline
        '''
        logging.info("started the data validation pipeline")
        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("performed the data vlaidation successfully")
            logging.info("exited the data validation phase")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys) from e 
        
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        '''
        Responsible for the data transformation pipeline 
        '''
        logging.info("started the data transformation pipeline")
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys) from e 
        

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        '''
        Responsible for the model training pipeline
        '''
        logging.info("started the model training pipeline")
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config)
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
                                     
        except Exception as e :
            raise MyException(e,sys) from e 
        

    def start_model_evaluation(self,data_ingestion_artifact:DataIngestionArtifact,model_trainer_artifact:ModelTrainerArtifact) -> ModelEvaluationArtifact:
        """
        responsible for the model evaluation pipeline
        """
        logging.info("started the model evaluation pipeline")
        try:
            model_evaluation = ModelEvaluate(model_evaluation_config = self.model_evaluation_config,
                                               data_ingestion_artifact = data_ingestion_artifact,
                                               model_trainer_artifact = model_trainer_artifact,
                                               )
            

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys) from e 


    def run_pipeline(self,) -> None:
        '''
        this is responsible for running the pipeline
        '''
        try:
            data_ingestion_artifacts = self.start_data_ingestion()

        except Exception as e:
            raise MyException(e,sys) from e
        