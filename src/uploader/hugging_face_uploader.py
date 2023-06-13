from fastapi import APIRouter, Form, HTTPException, UploadFile, File, status
from sqlmodel import Session, select
from sqlalchemy.engine import Engine
from database.model.dataset.dataset import Dataset
import huggingface_hub


class HuggingfaceUploader:
    def create(
        self,
        engine: Engine,
    ) -> APIRouter:
        router = APIRouter()
        router.add_api_route(
            path="/upload/datasets/{resource}/huggingface",
            endpoint=self._handle_upload_func(engine),
            methods=["POST"],
        )
        return router

    def _handle_upload_func(
        self,
        engine: Engine,
    ):
        def handle_upload(
            resource: int,
            file: UploadFile = File(...),
            token: str = Form(...),
            username: str = Form(...),
        ):
            dataset = self._get_resource(engine=engine, identifier=resource)
            repo_id = f"{username}/{dataset.name}"

            try:
                result = huggingface_hub.create_repo(repo_id, repo_type="dataset", token=token)
            except Exception:
                msg = f"Repository {repo_id} already created in hugging face"
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
            try:
                huggingface_hub.upload_file(
                    path_or_fileobj=file.file.read(),
                    path_in_repo=f"/data/{file.filename}",
                    repo_id=repo_id,
                    repo_type="dataset",
                    token=token,
                )
                huggingface_hub.upload_file(
                    path_or_fileobj=self._generate_metadata_file(dataset),
                    path_in_repo="README.md",
                    repo_id=repo_id,
                    repo_type="dataset",
                    token=token,
                )
                return result
            except Exception:
                huggingface_hub.delete_repo(repo_id, token=token, repo_type="dataset")
                msg = "Error uploading file"
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

        return handle_upload

    def _get_resource(self, engine: Engine, identifier: int) -> Dataset:
        """
        Get the resource identified by AIoD identifier
        """

        with Session(engine) as session:
            query = select(Dataset).where(Dataset.identifier == identifier)
        resource = session.scalars(query).first()
        if not resource:
            msg = f"Dataset '{identifier} not found " "in the database."
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        return resource

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
