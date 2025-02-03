from typing import List, Optional
from src.db_connection.database_interface import DatabaseInterface
from src.model.customer_model import CustomerBase, CustomerModel

class CustomerController:
    """Controlador responsável por intermediar a View e o Model."""

    def __init__(self, db: DatabaseInterface):
        """Recebe a instância do banco via injeção de dependência."""
        self.db = db

    def create_customer(self, customer_data: CustomerBase):
        """Cria um novo cliente chamando o Model."""
        CustomerModel.create(self.db, customer_data)

    def get_all_customers(self) -> List[CustomerModel]:
        """Retorna todos os clientes chamando o Model."""
        return CustomerModel.get_all(self.db)

    def get_customer_by_id(self, customer_id: int) -> Optional[CustomerModel]:
        """Busca um cliente pelo ID chamando o Model."""
        return CustomerModel.get_by_id(self.db, customer_id)

    def get_customer_by_name(self, name: str) -> List[CustomerModel]:
        """Busca clientes pelo nome chamando o Model."""
        return CustomerModel.get_by_name(self.db, name)

    def update_customer(self, customer_id: int, customer_data: CustomerBase):
        """Atualiza um cliente chamando o Model."""
        CustomerModel.update(self.db, customer_id, customer_data)

    def delete_customer(self, customer_id: int):
        """Exclui um cliente chamando o Model."""
        CustomerModel.delete(self.db, customer_id)

    def count_customers(self) -> int:
        """Retorna o número total de clientes chamando o Model."""
        return CustomerModel.count(self.db)
