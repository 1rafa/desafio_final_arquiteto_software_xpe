# Criar um cliente de testes para a API
#from fastapi.testclient import TestClient
# client = TestClient(app)

import pytest
from src.db_connection.sqlite_manager import SQLiteManager
from src.model.customer_model import CustomerModel

# test_customer.py
from fastapi.testclient import TestClient
from src.main import app  # Importa a instância da aplicação FastAPI definida no main.py


class Test:
    db_path = r"D:\Documentos\Estudos\XP Educacao\Desafio Final 1\APIXPEducacao\database\customer_test.db"

    # Instancia o TestClient com a aplicação FastAPI
    client = TestClient(app)

    def test_insert_delete_sql_manager(self):
        db = SQLiteManager(self.db_path)
        cliente = {"name": "Teste Cliente",
                   "email": "teste@example.com",
                   "phone": "123456789"}
        db.insert("customers", cliente)
        db.delete("customers", cliente)

    def test_fetch_one_sql_manager(self):
        db = SQLiteManager(self.db_path)
        cliente1 = {"name": "Teste Cliente1",
                   "email": "teste1@example.com",
                   "phone": "123456789"}
        cliente2 = {"name": "Teste Cliente2",
                   "email": "teste2@example.com",
                   "phone": "999999999"}
        db.insert("customers", cliente1)
        db.insert("customers", cliente2)

        all = db.fetch_one("customers", {"name": "Teste Cliente1"})

        db.delete("customers", cliente2)
        db.delete("customers", cliente1)

        assert all["name"] == "Teste Cliente1"

    def test_fetch_all_sql_manager(self):
        db = SQLiteManager(self.db_path)
        cliente1 = {"name": "Teste Cliente1",
                   "email": "teste1@example.com",
                   "phone": "123456789"}
        cliente2 = {"name": "Teste Cliente2",
                   "email": "teste2@example.com",
                   "phone": "999999999"}
        db.insert("customers", cliente1)
        db.insert("customers", cliente2)

        all = db.fetch_all("customers")
        assert len(all) == 2

        db.delete("customers", cliente2)
        db.delete("customers", cliente1)

    def test_update_sql_manager(self):
        db = SQLiteManager(self.db_path)
        cliente1 = {"name": "Teste Cliente1",
                   "email": "teste1@example.com",
                   "phone": "123456789"}
        cliente2 = {"name": "Teste Cliente1",
                   "email": "teste1@example.com",
                   "phone": "999999999"}
        db.insert("customers", cliente1)
        db.update("customers", cliente2, cliente1)

        cliente = db.fetch_one("customers", cliente2)

        db.delete("customers", {"name":"Teste Cliente1"})

        assert (cliente["phone"] == "999999999")

    def test_count_sql_manager(self):
        db = SQLiteManager(self.db_path)
        cliente1 = {"name": "Teste Cliente1",
                   "email": "teste1@example.com",
                   "phone": "123456789"}
        cliente2 = {"name": "Teste Cliente2",
                   "email": "teste2@example.com",
                   "phone": "999999999"}
        db.insert("customers", cliente1)
        db.insert("customers", cliente2)

        ct = db.count("customers")
        assert ct == 2

        db.delete("customers", cliente1)
        db.delete("customers", cliente2)

    def test_instantiate_model(self):
        cm = CustomerModel(name="Teste Cliente1", email="teste1@example.com", phone="123456789")

    def test_create_delete_model(self):
        db = SQLiteManager(self.db_path)
        cm = CustomerModel(name="Teste Cliente1", email="teste1@example.com", phone="123456789")

        cm = CustomerModel.create(db, cm)
        CustomerModel.delete(db, cm.id)

    def test_get_all_model(self):
        db = SQLiteManager(self.db_path)

        cm1 = CustomerModel(name="Teste Cliente1", email="teste1@example.com", phone="123456789")
        cm1 = CustomerModel.create(db, cm1)
        cm2 = CustomerModel(name="Teste Cliente2", email="teste2@example.com", phone="999999999")
        cm2 = CustomerModel.create(db, cm2)

        all = CustomerModel.get_all(db)

        assert all == [cm1, cm2]

        CustomerModel.delete(db, cm1.id)
        CustomerModel.delete(db, cm2.id)

    def test_get_by_id_model(self):
        db = SQLiteManager(self.db_path)

        cm1 = CustomerModel(name="Teste Cliente1", email="teste1@example.com", phone="123456789")
        cm1 = CustomerModel.create(db, cm1)
        cm2 = CustomerModel(name="Teste Cliente2", email="teste2@example.com", phone="999999999")
        cm2 = CustomerModel.create(db, cm2)

        all = CustomerModel.get_by_id(db, customer_id=1)

        CustomerModel.delete(db, cm1.id)
        CustomerModel.delete(db, cm2.id)

        assert all.name == "Teste Cliente1"

    def test_get_by_name_model(self):
        db = SQLiteManager(self.db_path)

        cm1 = CustomerModel(name="Teste Cliente1", email="teste1@example.com", phone="123456789")
        cm1 = CustomerModel.create(db, cm1)
        cm2 = CustomerModel(name="Teste Cliente2", email="teste2@example.com", phone="999999999")
        cm2 = CustomerModel.create(db, cm2)

        all = CustomerModel.get_by_name(db, name="Teste Cliente2")

        CustomerModel.delete(db, cm1.id)
        CustomerModel.delete(db, cm2.id)

        assert all[0].email == "teste2@example.com"

    def test_update_model(self):
        db = SQLiteManager(self.db_path)

        cm1 = CustomerModel(name="Teste Cliente1", email="teste1@example.com", phone="123456789")
        cm1 = CustomerModel.create(db, cm1)

        cm2 = CustomerModel(name="Teste Cliente2", email="teste2@example.com", phone="999999999")
        cm2 = CustomerModel.update(db, customer_id=1, customer_data = cm2)

        cm_test = CustomerModel.get_by_id(db, customer_id=1)

        CustomerModel.delete(db, cm1.id)

        assert cm_test.name == "Teste Cliente2"

    def test_count_model(self):
        db = SQLiteManager(self.db_path)

        cm1 = CustomerModel(name="Teste Cliente1", email="teste1@example.com", phone="123456789")
        cm1 = CustomerModel.create(db, cm1)
        cm2 = CustomerModel(name="Teste Cliente2", email="teste2@example.com", phone="999999999")
        cm1 = CustomerModel.create(db, cm2)

        ct = CustomerModel.count(db)

        assert ct == 2

    def test_create_and_delete_customer_view(self):
        # Dados do cliente para teste
        payload = {
            "name": "Teste Cliente1",
            "email": "teste1@example.com",
            "phone": "123456789"
        }

        # Realiza a requisição POST para criar o cliente
        response = self.client.post("/customers/", json=payload)

        # Verifica se o status code é 201 (Created)
        assert response.status_code == 201, f"Status code inesperado: {response.status_code}. Resposta: {response.text}"

        # Obtém o conteúdo da resposta
        data = response.json()

        # Valida se os dados retornados correspondem aos enviados e se o campo 'id' está presente
        assert data["name"] == payload["name"]
        assert data["email"] == payload["email"]
        assert data["phone"] == payload["phone"]
        assert "id" in data, "Campo 'id' não encontrado na resposta"

        # Deleta o cliente criado
        customer_id = data["id"]
        response = self.client.delete(f"/customers/{customer_id}")
        assert response.status_code == 204, f"Falha ao deletar o cliente. Status code: {response.status_code}"

    def test_get_all_customer_view(self):
        # Cria dois clientes para o teste
        payload1 = {
            "name": "Cliente 1",
            "email": "cliente1@example.com",
            "phone": "111111111"
        }
        payload2 = {
            "name": "Cliente 2",
            "email": "cliente2@example.com",
            "phone": "222222222"
        }
        response1 = self.client.post("/customers/", json=payload1)
        assert response1.status_code == 201, f"Erro ao criar Cliente 1: {response1.status_code} - {response1.text}"
        data1 = response1.json()

        response2 = self.client.post("/customers/", json=payload2)
        assert response2.status_code == 201, f"Erro ao criar Cliente 2: {response2.status_code} - {response2.text}"
        data2 = response2.json()

        # Busca todos os clientes via GET
        response = self.client.get("/customers/")
        assert response.status_code == 200, f"Status code inesperado: {response.status_code}. Resposta: {response.text}"
        customers = response.json()
        # Verifica se os clientes criados estão na listagem
        ids = [customer["id"] for customer in customers]
        assert data1["id"] in ids, "Cliente 1 não encontrado na listagem"
        assert data2["id"] in ids, "Cliente 2 não encontrado na listagem"

        # Deleta os clientes criados
        response = self.client.delete(f"/customers/{data1['id']}")
        assert response.status_code == 204, f"Erro ao deletar Cliente 1: {response.status_code}"
        response = self.client.delete(f"/customers/{data2['id']}")
        assert response.status_code == 204, f"Erro ao deletar Cliente 2: {response.status_code}"

    def test_get_by_id_customer_view(self):
        # Cria um cliente para o teste
        payload = {
            "name": "Cliente por ID",
            "email": "cliente_id@example.com",
            "phone": "333333333"
        }
        response = self.client.post("/customers/", json=payload)
        assert response.status_code == 201, f"Erro ao criar cliente: {response.status_code} - {response.text}"
        data = response.json()
        customer_id = data["id"]

        # Busca o cliente pelo ID via GET
        response = self.client.get(f"/customers/{customer_id}")
        assert response.status_code == 200, f"Erro ao buscar cliente pelo ID: {response.status_code} - {response.text}"
        customer = response.json()
        # Valida os dados retornados
        assert customer["id"] == customer_id, "IDs não correspondem"
        assert customer["name"] == payload["name"], "Nome diferente"
        assert customer["email"] == payload["email"], "Email diferente"
        assert customer["phone"] == payload["phone"], "Telefone diferente"

        # Deleta o cliente criado
        response = self.client.delete(f"/customers/{customer_id}")
        assert response.status_code == 204, f"Erro ao deletar cliente: {response.status_code}"

    def test_count_customer_view(self):
        # Obtém a contagem atual de clientes
        response = self.client.get("/customers/count")
        assert response.status_code == 200, f"Erro ao obter contagem: {response.status_code} - {response.text}"
        count_before = response.json()

        # Cria dois clientes
        payload1 = {
            "name": "Cliente Count 1",
            "email": "count1@example.com",
            "phone": "444444444"
        }
        payload2 = {
            "name": "Cliente Count 2",
            "email": "count2@example.com",
            "phone": "555555555"
        }
        response1 = self.client.post("/customers/", json=payload1)
        assert response1.status_code == 201, f"Erro ao criar Cliente Count 1: {response1.status_code} - {response1.text}"
        data1 = response1.json()

        response2 = self.client.post("/customers/", json=payload2)
        assert response2.status_code == 201, f"Erro ao criar Cliente Count 2: {response2.status_code} - {response2.text}"
        data2 = response2.json()

        # Verifica a nova contagem de clientes
        response = self.client.get("/customers/count")
        assert response.status_code == 200, f"Erro ao obter contagem: {response.status_code} - {response.text}"
        count_after = response.json()
        # A contagem deve aumentar em 2
        assert count_after == count_before + 2, "Contagem de clientes incorreta"

        # Deleta os clientes criados
        response = self.client.delete(f"/customers/{data1['id']}")
        assert response.status_code == 204, f"Erro ao deletar Cliente Count 1: {response.status_code}"
        response = self.client.delete(f"/customers/{data2['id']}")
        assert response.status_code == 204, f"Erro ao deletar Cliente Count 2: {response.status_code}"

    def test_update_customer_view(self):
        # Cria um cliente para o teste
        payload = {
            "name": "Cliente Update",
            "email": "update@example.com",
            "phone": "666666666"
        }
        response = self.client.post("/customers/", json=payload)
        assert response.status_code == 201, f"Erro ao criar cliente: {response.status_code} - {response.text}"
        data = response.json()
        customer_id = data["id"]

        # Dados atualizados para o cliente
        updated_payload = {
            "name": "Cliente Update Modificado",
            "email": "update_mod@example.com",
            "phone": "777777777"
        }
        # Atualiza o cliente via PUT
        response = self.client.put(f"/customers/{customer_id}", json=updated_payload)
        assert response.status_code == 200, f"Erro ao atualizar cliente: {response.status_code} - {response.text}"
        updated_customer = response.json()
        # Valida se os dados foram atualizados corretamente
        assert updated_customer["name"] == updated_payload["name"], "Nome não atualizado corretamente"
        assert updated_customer["email"] == updated_payload["email"], "Email não atualizado corretamente"
        assert updated_customer["phone"] == updated_payload["phone"], "Telefone não atualizado corretamente"

        # Deleta o cliente atualizado
        response = self.client.delete(f"/customers/{customer_id}")
        assert response.status_code == 204, f"Erro ao deletar cliente: {response.status_code}"
