from collections.abc import Generator

from app.config import settings
from sqlmodel import Session, SQLModel, create_engine

# FastAPIでSQLiteを利用する際のスレッド制限を回避する設定
connect_args = {"check_same_thread": False}

# エンジンの作成
engine = create_engine(settings.database_url, echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    """データベースと全テーブルを作成する関数"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPIで利用するDependency Injection用セッション generator"""
    with Session(engine) as session:
        yield session
