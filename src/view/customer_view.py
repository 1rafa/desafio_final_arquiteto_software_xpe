from typing import List
from src.model.customer_model import CustomerModel


def format_customer(customer: CustomerModel) -> CustomerModel:
    """
    Formata os dados de um cliente para apresentação.

    Nesta implementação, não há transformações adicionais, mas esta função
    pode ser expandida para alterar ou filtrar os dados antes da resposta.
    """
    return customer


def format_customers(customers: List[CustomerModel]) -> List[CustomerModel]:
    """
    Formata os dados de uma lista de clientes para apresentação.
    """
    return [format_customer(customer) for customer in customers]


def format_count(count: int) -> int:
    """
    Formata o dado de contagem, se necessário.
    """
    return count
