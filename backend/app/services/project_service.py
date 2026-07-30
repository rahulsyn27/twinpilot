from app.models.project import Project
from app.repository.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate


class ProjectService:
    """
    Business logic for Project management.

    IMPORTANT:
    This layer should NEVER know how the database works.
    It only talks to the repository.

    If tomorrow we replace PostgreSQL with another database,
    only the repository changes.
    """

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(self, data: ProjectCreate) -> Project:
        """
        Create a new project.

        Business rules:
        1. Project names must be unique.
        2. (Future) Repository URL should be reachable.
        3. (Future) Repository will be cloned automatically.
        """

        # Check whether another project already uses this name.
        # This is a business rule, so it belongs in the service,
        # NOT in the repository.
        existing = await self.repository.get_by_name(data.name)

        if existing:
            raise ValueError(f"Project '{data.name}' already exists.")

        # Convert the validated API schema into a database model.
        project = Project(
            name=data.name,
            repository_url=str(data.repository_url),
            local_path=data.local_path,
            default_branch=data.default_branch,
        )

        # The repository is responsible for persistence.
        return await self.repository.create(project)

    async def get_project(self, project_id):
        """
        Retrieve a project by its ID.
        """
        return await self.repository.get_by_id(project_id)

    async def list_projects(self):
        """
        Return every registered project.
        """
        return await self.repository.list()

    async def delete_project(self, project_id):
        """
        Delete a project if it exists.
        """

        project = await self.repository.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found.")

        await self.repository.delete(project)