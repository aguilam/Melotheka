from __future__ import annotations

from sqlalchemy import event, func
from sqlmodel import (
    Session,
    SQLModel,
    create_engine,
    select,
)

from core.db.models import UserORM
from core.services.server_service import delete_orphans


def admin_create(session: Session):
    statement = select(func.count()).select_from(UserORM)
    users_count = session.exec(statement).one()
    if users_count < 1:
        admin = UserORM(
            username="admin",
            password="admin",
            email="admin@mail.com",
            is_admin=True,
        )
        session.add(admin)


class _DBManager:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.db")
        self._enable_sqlite_fk()
        SQLModel.metadata.create_all(self.engine)
        with self.get_session() as session, session.begin():
            admin_create(session)
            delete_orphans(session)

    def _enable_sqlite_fk(self) -> None:
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    def get_session(self) -> Session:
        return Session(self.engine)


DBManager = _DBManager()
