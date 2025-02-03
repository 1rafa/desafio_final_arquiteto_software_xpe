# customer_controller.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi_utils.cbv import cbv
from src.db_connection.sqlite_manager import SQLiteManager
from src.db_connection.database_interface import DatabaseInterface
from src.model.customer_model import CustomerBase, CustomerModel
from src.view.customer_view import format_customer, format_customers, format_count

# Definindo o caminho do banco de dados
DB_PATH = r"D:\Documentos\Estudos\XP Educacao\Desafio Final 1\APIXPEducacao\database\customer.db"

def get_database() -> DatabaseInterface:
    """
    Dependência para obtenção da instância do banco de dados.
    """
    return SQLiteManager(DB_PATH)

# Criando o router para os endpoints de clientes
router = APIRouter(prefix="/customers", tags=["Customers"])

@cbv(router)
class CustomerController:
    # Injeção de dependência: o banco de dados é disponibilizado como atributo da classe
    db: DatabaseInterface = Depends(get_database)

    @router.post("/", response_model=CustomerModel, status_code=201)
    def create_customer(self, customer_data: CustomerBase):
        """
        Cria um novo cliente e retorna os dados completos, incluindo o ID.
        """
        CustomerModel.create(self.db, customer_data)
        customers = CustomerModel.get_by_name(self.db, customer_data.name)
        if not customers:
            raise HTTPException(status_code=500, detail="Falha na criação do cliente")
        return format_customer(customers[0])  # Retorna o primeiro cliente encontrado

    @router.get("/count", response_model=int)
    def count_customers(self):
        """
        Retorna o número total de clientes.
        """
        count = CustomerModel.count(self.db)
        return format_count(count)

    @router.get("/", response_model=List[CustomerModel])
    def get_all_customers(self):
        """
        Retorna todos os clientes.
        """
        customers = CustomerModel.get_all(self.db)
        return format_customers(customers)

    @router.get("/{customer_id}", response_model=CustomerModel)
    def get_customer_by_id(self, customer_id: int):
        """
        Retorna um cliente específico pelo ID.
        """
        customer = CustomerModel.get_by_id(self.db, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return format_customer(customer)

    @router.get("/name/{name}", response_model=List[CustomerModel])
    def get_customer_by_name(self, name: str):
        """
        Retorna os clientes com o nome especificado.
        """
        customers = CustomerModel.get_by_name(self.db, name)
        if not customers:
            raise HTTPException(status_code=404, detail="Clientes não encontrados")
        return format_customers(customers)

    @router.put("/{customer_id}", response_model=CustomerModel)
    def update_customer(self, customer_id: int, customer_data: CustomerBase):
        """
        Atualiza um cliente pelo ID.
        """
        if not CustomerModel.get_by_id(self.db, customer_id):
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        CustomerModel.update(self.db, customer_id, customer_data)
        updated_customer = CustomerModel.get_by_id(self.db, customer_id)
        return format_customer(updated_customer)

    @router.delete("/{customer_id}", status_code=204)
    def delete_customer(self, customer_id: int):
        """
        Exclui um cliente pelo ID.
        """
        if not CustomerModel.get_by_id(self.db, customer_id):
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        CustomerModel.delete(self.db, customer_id)
