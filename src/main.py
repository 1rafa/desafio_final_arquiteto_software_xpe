from fastapi import FastAPI
from src.controller.customer_controller import router as customer_router

# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="Customer API",
    description="API para gerenciamento de clientes",
    version="1.0.0"
)

# Inclui os endpoints definidos na camada de View
app.include_router(customer_router)

# Bloco principal para inicializar o servidor com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
