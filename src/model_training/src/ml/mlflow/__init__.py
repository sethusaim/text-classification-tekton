import sys
from typing import Dict, List, Tuple, Union

import mlflow

from src.configuration.mlflow_connection import MLFlowClient
from src.constant import training_pipeline
from src.entity.config_entity import MLFlowModelInfo
from src.exception import CustomException
from src.logger import logging
from src.ml.model.estimator import CustomModel


class MLFLowOperation:
    def __init__(self):
        self.mlflow_client = MLFlowClient().client

        mlflow.set_tracking_uri(uri=self.mlflow_client.tracking_uri)

        mlflow.set_experiment(experiment_name=training_pipeline.EXP_NAME)

    def log_all_for_model(
        self,
        model: CustomModel,
        model_parameters: Dict,
        model_score: float,
    ) -> None:
        """
        The function logs model parameters, the model itself, and a model score using MLflow.

        Args:
          model (CustomModel): A CustomModel object that contains the trained machine learning model.
          model_parameters (Dict): A dictionary containing the parameters used to train the model.
          model_score (float): The evaluation score of the trained model.
        """
        logging.info("Entered log_all_for_model method of MLFLowOperation class")

        try:
            mlflow.log_params(params=model_parameters)

            logging.info(f"Logged {model_parameters} model parameters")

            mlflow.pyfunc.log_model(
                artifact_path=model.model.__class__.__name__,
                python_model=model,
                registered_model_name=model.model.__class__.__name__
                + "-"
                + training_pipeline.EXP_NAME,
            )

            logging.info(
                f"Logged {model.model.__class__.__name__} model with {model.model.__class__.__name__ + '-' + training_pipeline.EXP_NAME} as registered model name"
            )

            mlflow.log_metric(
                key=training_pipeline.MODEL_TRAINER_MODEL_METRIC_KEY,
                value=model_score,
            )

            logging.info(
                f"Logged model metric {training_pipeline.MODEL_TRAINER_MODEL_METRIC_KEY} as name with value as {model_score}"
            )

            logging.info("Exited log_all_for_model method of MLFLowOperation class")

        except Exception as e:
            raise CustomException(e, sys)

    def get_model_info(self, best_model_name: str) -> MLFlowModelInfo:
        """
        This function retrieves information about a trained MLFlow model with a given name.

        Args:
          best_model_name (str): A string representing the name of the best model to retrieve information
        for.

        Returns:
          an instance of the MLFlowModelInfo class, which contains information about a trained ML model such
        as its name, current stage, URI, and version.
        """
        logging.info("Entered get_model_info method of MLFLowOperation class")

        try:
            trained_best_model_info: Tuple[str, str, str, str] = [
                (
                    rm.name,
                    rm.latest_versions[0].current_stage,
                    rm.latest_versions[0].source,
                    rm.latest_versions[0].version,
                )
                for rm in self.mlflow_client.search_registered_models(
                    f"name='{best_model_name}'"
                )
            ][0]

            logging.info(
                f"Got a trained model info from registered models with filter name as {best_model_name}"
            )

            model_info: MLFlowModelInfo = MLFlowModelInfo(
                model_name=trained_best_model_info[0],
                model_current_stage=trained_best_model_info[1],
                model_uri=trained_best_model_info[2],
                model_version=trained_best_model_info[3],
            )

            logging.info(f"Created {model_info} model info dict")

            logging.info("Exited get_model_info method of MLFLowOperation class")

            return model_info

        except Exception as e:
            raise CustomException(e, sys)

    def get_prod_model_info(self) -> Union[MLFlowModelInfo, None]:
        """
        This function retrieves information about the latest production model from a list of registered
        models using the MLFlow API.

        Returns:
          an instance of the MLFlowModelInfo class or None.
        """
        logging.info("Entered get_prod_model_info method of MLFLowOperation class")

        try:
            prod_model_info: Union[List[Tuple[str, str, str, str]], None] = [
                (
                    rm.name,
                    rm.latest_versions[0].current_stage,
                    rm.latest_versions[0].source,
                    rm.latest_versions[0].version,
                )
                for rm in self.mlflow_client.search_registered_models()
                if rm.latest_versions[0].current_stage == "Production"
            ]

            logging.info(
                "got prod model info from list of registered models where current stage as Production"
            )

            if len(prod_model_info) == 0:
                logging.info("no prod model exists, trained model is accepted")

                return None

            else:
                prod_model_info: MLFlowModelInfo = MLFlowModelInfo(
                    model_name=prod_model_info[0][0],
                    model_current_stage=prod_model_info[0][1],
                    model_uri=prod_model_info[0][2],
                    model_version=prod_model_info[0][3],
                )

                return prod_model_info

        except Exception as e:
            raise CustomException(e, sys)
