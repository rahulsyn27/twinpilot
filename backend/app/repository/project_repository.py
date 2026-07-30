from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


class ProjectRepository:
    """
    Handles all database operations for Project entities.
    """

    def __init__(self, db: AsyncSession):  #We inject the database session.This is called Dependency Injection.
        self.db = db  

    async def create(self, project: Project) -> Project:
        self.db.add(project)   #tells SQLAlchemy: "Track this object."
        await self.db.commit()   #Now SQLAlchemy sends SQL to PostgreSQL.
        await self.db.refresh(project)   #refresh() reloads UUID, created_at, updated_at values back into the Python object.
        return project 

    async def get_by_id(self, project_id: UUID) -> Project | None:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()  # Return Project object  or none

    async def get_by_name(self, name: str) -> Project | None:
        result = await self.db.execute(
            select(Project).where(Project.name == name)
        )
        return result.scalar_one_or_none()

    async def list(self) -> list[Project]:
        result = await self.db.execute(select(Project))
        return list(result.scalars().all())

    async def delete(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.commit()