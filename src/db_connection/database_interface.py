from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Tuple
from datetime import datetime
from sqlalchemy.orm import Session


class DatabaseInterface(ABC):
    """Interface para operações genéricas de banco de dados."""
    def __init__(self):
        """Inicializa a conexão e configura o banco de dados."""
        self.models = None
        self.session = None

    @abstractmethod
    def connect(self, db_path):
        """Abre uma conexão com o banco de dados."""
        raise NotImplementedError

    def get_session(self):
        self.session = Session()
        return self.session

    def insert(self, table: str, data: dict) -> Tuple[Optional[int], Optional[datetime]]:
        """
        Insere um novo registro no banco de dados e retorna o id do registro inserido.
        """
        session = self.get_session()
        model_class = self.models.get(table)
        new_id = None
        new_created_at = None
        if model_class:
            new_entry = model_class(**data)
            session.add(new_entry)
            session.commit()  # Após o commit, o atributo new_entry.id é atualizado automaticamente
            new_id = new_entry.id
            new_created_at = new_entry.created_at
        session.close()
        return new_id, new_created_at

    def fetch_all(self, table: str, filters: Optional[dict] = None) -> List[Dict]:
        """Busca todos os registros de uma tabela, com filtros opcionais."""
        session = self.get_session()
        model_class = self.models.get(table)
        if not model_class:
            session.close()
            return []

        query = session.query(model_class)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(model_class, key) == value)

        results = query.all()
        session.close()
        return [result.__dict__ for result in results]

    def fetch_one(self, table: str, filters: dict) -> Optional[Dict]:
        """Busca um único registro baseado em filtros."""
        results = self.fetch_all(table, filters)
        return results[0] if results else None

    def update(self, table: str, data: dict, filters: dict) -> None:
        """Atualiza um registro no banco de dados."""
        session = self.get_session()
        model_class = self.models.get(table)
        if not model_class:
            session.close()
            return

        query = session.query(model_class)
        for key, value in filters.items():
            query = query.filter(getattr(model_class, key) == value)

        query.update(data)
        session.commit()
        session.close()

    def delete(self, table: str, filters: dict) -> None:
        """Remove um registro baseado em filtros."""
        session = self.get_session()
        model_class = self.models.get(table)
        if not model_class:
            session.close()
            return

        query = session.query(model_class)
        for key, value in filters.items():
            query = query.filter(getattr(model_class, key) == value)

        query.delete()
        session.commit()
        session.close()

    def count(self, table: str) -> int:
        """Conta o número total de registros na tabela."""
        session = self.get_session()
        model_class = self.models.get(table)
        if not model_class:
            session.close()
            return 0

        total = session.query(model_class).count()
        session.close()
        return total
