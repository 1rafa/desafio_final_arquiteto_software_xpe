from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi_utils.cbv import cbv  # Importa o decorator para class-based views
from src.controller.customer_controller import CustomerController
from src.model.customer_model import CustomerBase, CustomerModel
from src.db_connection.sqlite_manager import SQLiteManager
from src.db_connection.database_interface import DatabaseInterface

DB_PATH = r"D:\Documentos\Estudos\XP Educacao\Desafio Final 1\APIXPEducacao\database\customer.db"

# Dependência do banco de dados
def get_database() -> DatabaseInterface:
    return SQLiteManager(DB_PATH)

# Dependência do controlador
def get_controller(db: DatabaseInterface = Depends(get_database)) -> CustomerController:
    return CustomerController(db)

# Criando o router
router = APIRouter(prefix="/customers", tags=["Customers"])

@cbv(router)
class CustomerView:
    # Injeção de dependência: o controller é disponibilizado como atributo da classe
    controller: CustomerController = Depends(get_controller)

    @router.post("/", response_model=CustomerModel, status_code=201)
    def create_customer(self, customer_data: CustomerBase):
        """Cria um novo cliente e retorna os dados completos, incluindo o ID."""
        self.controller.create_customer(customer_data)
        return self.controller.get_customer_by_name(customer_data.name)[0]  # Retorna o primeiro encontrado

    @router.get("/count", response_model=int)
    def count_customers(self):
        """Retorna o número total de clientes."""
        return self.controller.count_customers()

    @router.get("/", response_model=List[CustomerModel])
    def get_all_customers(self):
        """Retorna todos os clientes."""
        return self.controller.get_all_customers()

    @router.get("/{customer_id}", response_model=CustomerModel)
    def get_customer_by_id(self, customer_id: int):
        """Retorna um cliente específico pelo ID."""
        customer = self.controller.get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return customer

    @router.put("/{customer_id}", response_model=CustomerModel)
    def update_customer(self, customer_id: int, customer_data: CustomerBase):
        """Atualiza um cliente pelo ID."""
        if not self.controller.get_customer_by_id(customer_id):
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        self.controller.update_customer(customer_id, customer_data)
        return self.controller.get_customer_by_id(customer_id)

    @router.delete("/{customer_id}", status_code=204)
    def delete_customer(self, customer_id: int):
        """Exclui um cliente pelo ID."""
        if not self.controller.get_customer_by_id(customer_id):
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        self.controller.delete_customer(customer_id)
