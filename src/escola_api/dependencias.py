from src.escola_api.database.banco_dados import SessionLocal

# Função de dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()  # cria uma nova sessão no banco de dados
    try:
        yield db  # Retorna a sessão de forma que o FastAPI possa utilizá-la nas rotas
    finally:
        db.close()  # Garante que a sessão será fechada após o uso