import sys

from src.cloud_storage.aws_operation import S3Operation
from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import TrainingPipelineConfig
from src.exception import CustomException


def start_data_ingestion() -> DataIngestionArtifact:
    """
    This function initiates data ingestion, handles exceptions, and syncs a folder to an S3 bucket.
    """
    try:
        data_ingestion: DataIngestion = DataIngestion()

        data_ingestion.initiate_data_ingestion()

    except Exception as e:
        raise CustomException(e, sys)

    finally:
        s3 = S3Operation()

        tp = TrainingPipelineConfig()

        s3.sync_folder_to_s3(
            folder=tp.artifact_dir,
            bucket_name=tp.artifact_bucket_name,
            bucket_folder_name=tp.artifact_dir,
        )


if __name__ == "__main__":
    start_data_ingestion()
