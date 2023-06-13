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

            huggingface_hub.create_repo(repo_id, repo_type="dataset", token=token)
            result = huggingface_hub.upload_file(
                path_or_fileobj=file.file.read(),
                path_in_repo=f"/data/{file.filename}",
                repo_id=repo_id,
                repo_type="dataset",
                token=token,
            )

            return result

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
