import os
from dataclasses import dataclass

from src.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self):
        self.artifacts_dir: str = training_pipeline.ARTIFACT_DIR

        self.artifact_bucket_name: str = training_pipeline.ARTIFACTS_BUCKET_NAME


class ModelTrainerConfig:
    def __init__(self, timestamp: str):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline.ARTIFACT_DIR,
            timestamp,
            training_pipeline.MODEL_TRAINING_DIR,
        )

        self.trained_model_file_dir: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR
        )

        self.best_model_file_dir: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_BEST_MODEL_DIR
        )

        self.expected_score: float = training_pipeline.MODEL_TRAINER_EXCEPTED_SCORE

        self.model_config_file_path: str = (
            training_pipeline.MODEL_TRAINER_CONFIG_FILE_PATH
        )

        self.mlflow_model_metric_key: str = (
            training_pipeline.MODEL_TRAINER_MODEL_METRIC_KEY
        )


@dataclass
class MLFlowModelInfo:
    model_name: str

    model_current_stage: str

    model_uri: str

    model_version: str
