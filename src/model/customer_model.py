from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
from src.db_connection.database_interface import DatabaseInterface


class CustomerBase(BaseModel):
    """Define os atributos básicos de um cliente."""
    name: str
    email: EmailStr
    phone: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None


class CustomerModel(CustomerBase):
    """Modelo responsável pelas operações no banco de dados."""

    @classmethod
    def from_db(cls, data: Dict):
        """Cria um objeto CustomerModel a partir de um dicionário do banco de dados."""
        return cls(**data) if data else None

    @classmethod
    def create(cls, db: DatabaseInterface, customer_data: CustomerBase) -> "CustomerBase":
        """
        Cria um novo cliente no banco de dados e retorna um objeto CustomerModel
        com os campos 'id' e 'created_at' atualizados.
        """
        data = customer_data.model_dump()
        new_id, new_created_at = db.insert("customers", data)  # Agora o insert retorna o id
        if (new_id is None) or (new_created_at is None):
            raise Exception("Erro ao inserir o cliente no banco de dados.")
        customer_data.id = new_id
        customer_data.created_at = new_created_at
        return customer_data

    @classmethod
    def get_all(cls, db: DatabaseInterface) -> List["CustomerBase"]:
        """Retorna todos os clientes."""
        rows = db.fetch_all("customers")
        return [cls.from_db(row) for row in rows]

    @classmethod
    def get_by_id(cls, db: DatabaseInterface, customer_id: int) -> Optional["CustomerBase"]:
        """Busca um cliente pelo ID."""
        row = db.fetch_one("customers", {"id": customer_id})
        return cls.from_db(row)

    @classmethod
    def get_by_name(cls, db: DatabaseInterface, name: str) -> List["CustomerBase"]:
        """Busca clientes pelo nome."""
        rows = db.fetch_all("customers", {"name": name})
        return [cls.from_db(row) for row in rows]

    @classmethod
    def update(cls, db: DatabaseInterface, customer_id: int, customer_data: CustomerBase):
        """Atualiza um cliente existente ignorando valores nulos."""
        # Cria um dicionário filtrado removendo os itens com valor None
        data = {k: v for k, v in customer_data.model_dump().items() if v is not None}
        db.update("customers", data, {"id": customer_id})

    @classmethod
    def delete(cls, db: DatabaseInterface, customer_id: int):
        """Exclui um cliente pelo ID."""
        db.delete("customers", {"id": customer_id})

    @classmethod
    def count(cls, db: DatabaseInterface) -> int:
        """Retorna o número total de clientes."""
        return db.count("customers")
