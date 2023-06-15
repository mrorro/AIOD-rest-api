import datasets
import huggingface_hub
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.engine import Engine
from sqlalchemy.orm import lazyload
from sqlmodel import Session

from database.model.dataset.data_download import DataDownloadORM
from database.model.dataset.dataset import Dataset


class HuggingfaceUploader:
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_upload(
        self,
        identifier: int,
        file: UploadFile,
        token: str,
        username: str,
    ):
        dataset = self._get_resource(engine=self.engine, identifier=identifier)
        repo_id = f"{username}/{dataset.name}"

        url = self._check_repo_exists(repo_id)
        if not url:
            url = huggingface_hub.create_repo(repo_id, repo_type="dataset", token=token)
        try:
            huggingface_hub.upload_file(
                path_or_fileobj=file.file.read(),
                path_in_repo=f"/data/{file.filename}",
                repo_id=repo_id,
                repo_type="dataset",
                token=token,
            )
        except Exception:
            huggingface_hub.delete_repo(repo_id, token=token, repo_type="dataset")
            msg = "Error uploading the file"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

        metadata_file = self._generate_metadata_file(dataset)
        try:
            huggingface_hub.upload_file(
                path_or_fileobj=metadata_file,
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type="dataset",
                token=token,
            )
        except Exception:
            huggingface_hub.delete_repo(repo_id, token=token, repo_type="dataset")
            msg = "Error updating metadata in huggingface"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

        if not any(data.name == repo_id for data in dataset.distributions):
            self._store_resource_updated(self.engine, dataset, url, repo_id)

        return url

    def _get_resource(self, engine: Engine, identifier: int) -> Dataset:
        """
        Get the resource identified by AIoD identifier
        """

        with Session(engine) as session:
            query = (
                session.query(Dataset)
                .options(lazyload("*"))
                .filter(Dataset.identifier == identifier)
            )

        resource = query.first()
        if not resource:
            msg = f"Dataset '{identifier} not found " "in the database."
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        return resource

    def _store_resource_updated(self, engine: Engine, resource: Dataset, url: str, repo_id: str):
        with Session(engine) as session:
            try:
                data_download = DataDownloadORM(content_url=url, name=repo_id, dataset=resource)
                resource.distributions.append(data_download)
                session.merge(resource)
                session.commit()
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="TODO: describe"
                ) from e

    def _check_repo_exists(sef, repo_id):
        try:
            datasets.load_dataset_builder(repo_id)
            return f"https://huggingface.co/datasets/{repo_id}"
        except Exception:
            return None

    def _generate_metadata_file(self, dataset: Dataset) -> bytes:
        tags = ["- " + tag.name for tag in dataset.keywords] if dataset.keywords else []
        content = "---\n"
        content += f"pretty_name: {dataset.name}\n"

        if tags:
            content += "tags:\n"
            content += "\n".join(tags) + "\n"
        # TODO the license must be in the hugginface format:
        #  https://huggingface.co/docs/hub/repositories-licenses
        """
        if dataset.license:
            content += f"license: {dataset.license.name if dataset.license else ''}"
        """
        content += "---\n"
        content += f"# {dataset.name}\n"
        content += "Created from AIOD platform"  # TODO add url
        return content.encode("utf-8")
