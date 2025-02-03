import os
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.db_connection.database_interface import DatabaseInterface


Base = declarative_base()


class CustomerORM(Base):
    """Modelo ORM representando a tabela customers."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class SQLiteManager(DatabaseInterface):
    """Gerencia operações no banco de dados SQLite usando SQLAlchemy."""

    def __init__(self, db_path: str):
        super().__init__()
        """Inicializa a conexão e configura o banco de dados."""
        self.models = {"customers": CustomerORM}

        self.db_path = db_path
        self.db_url = None
        self.engine = None
        self.Session = None

        # Criando conexão com SQLAlchemy
        self.connect(db_path)

    def get_session(self):
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self.Session()

    def connect(self, db_path):
        """Cria a conexão com o banco de dados e inicializa as tabelas."""
        self.db_path = db_path
        self.db_url = f"sqlite:///{self.db_path}"
        database_exists = os.path.exists(self.db_path)
        self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False})
        session = self.get_session()

        if not database_exists:
            Base.metadata.create_all(bind=self.engine)

        session.commit()
        session.close()
