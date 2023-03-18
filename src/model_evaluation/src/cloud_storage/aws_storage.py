import os
import sys
from typing import List

import boto3

from src.exception import CustomException
from src.logger import logging


class S3Operation:
    def __init__(self):
        self.s3_resource = boto3.resource("s3")

    def sync_folder_to_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ) -> None:
        logging.info("Entered sync_folder_to_s3 method of S3Operation class")

        try:
            os.system(f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name}/ ")

            logging.info("Exited sync_folder_to_s3 method of S3Operation class")

        except Exception as e:
            raise CustomException(e, sys)

    def sync_folder_from_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ) -> None:
        logging.info("Entered sync_folder_from_s3 method of S3Operation class")

        try:
            os.system(f"aws s3 sync s3://{bucket_name}/{bucket_folder_name}/ {folder}")

            logging.info("Exited sync_folder_from_s3 method of S3Operation class")

        except Exception as e:
            raise CustomException(e, sys)

    def get_pipeline_artifacts(self, bucket_name: str, folders: List) -> str:
        logging.info("Entered get_pipeline_artifacts method of S3Operation class")

        try:
            s3_client = boto3.client("s3")

            response = s3_client.list_objects_v2(
                Bucket=bucket_name, Prefix="artifacts"
            )["Contents"]

            latest = max(response, key=lambda x: x["LastModified"])["Key"]

            timestamp_artifact_dir = "/".join(latest.split("/")[:2])

            for f in folders:
                artifact_dir = timestamp_artifact_dir + "/" + f

                logging.info(f"Got the {f} artifacts dir")

                self.sync_folder_from_s3(
                    folder=artifact_dir,
                    bucket_name=bucket_name,
                    bucket_folder_name=artifact_dir,
                )

            logging.info("Exited get_pipeline_artifacts method of S3Operation class")

            return artifact_dir.split("/")[1]

        except Exception as e:
            raise CustomException(e, sys)

    def is_model_present(self, model_path: str, bucket_name: str) -> bool:
        try:
            bucket = self.s3_resource.Bucket(bucket_name)

            file_objects = [
                file_object for file_object in bucket.objects.filter(Prefix=model_path)
            ]

            if len(file_objects) > 0:
                return True

            else:
                return False

        except Exception as e:
            raise CustomException(e, sys)
