import sys

from src.cloud_storage.aws_operations import S3Operation
from src.components.model_training import ModelTrainer
from src.entity.config_entity import TrainingPipelineConfig
from src.exception import CustomException

s3 = S3Operation()

tp = TrainingPipelineConfig()


def start_model_training():
    """
    This function initiates model training and syncs the artifacts folder to an S3 bucket.
    """
    try:
        timestamp = s3.get_pipeline_artifacts(
            bucket_name=tp.artifact_bucket_name, folders=["data_transformation"]
        )

        model_trainer = ModelTrainer(timestamp=timestamp)

        model_trainer.initiate_model_training()

    except Exception as e:
        raise CustomException(e, sys)

    finally:
        s3.sync_folder_to_s3(
            folder=tp.artifacts_dir,
            bucket_name=tp.artifact_bucket_name,
            bucket_folder_name=tp.artifacts_dir,
        )


if __name__ == "__main__":
    start_model_training()
