from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repository.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


def get_project_service(db: AsyncSession = Depends(get_db),) -> ProjectService:
    """
    Dependency Injection Factory

    FastAPI automatically provides a database session for every request.

    We use that session to create a repository, and then inject the
    repository into the service.

    Request
        ↓
    AsyncSession
        ↓
    Repository
        ↓
    Service
        ↓
    API Endpoint
    """
    repository = ProjectRepository(db)
    return ProjectService(repository)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    """
    Create a new TwinPilot project.

    Responsibilities of this endpoint:

    ✅ Receive JSON
    ✅ Validate JSON (Pydantic)
    ✅ Call business logic
    ✅ Return response

    It should NEVER contain business rules.
    """
    try:
        return await service.create_project(project)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ProjectResponse],
)
async def list_projects(
    service: ProjectService = Depends(get_project_service),
):
    """
    Return every project registered in TwinPilot.
    """
    return await service.list_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    """
    Return a single project.

    FastAPI automatically converts the URL string into a UUID.
    """
    project = await service.get_project(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    """
    Delete a project.

    Returning HTTP 204 means:
    "The request succeeded and there is nothing to return."
    """
    try:
        await service.delete_project(project_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc