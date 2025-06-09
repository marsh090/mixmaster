from pymongo import MongoClient
import os

# URI direta para teste
uri = "mongodb+srv://admin:admin@mixmaster-dev.gyygxk8.mongodb.net/?retryWrites=true&w=majority&appName=mixmaster-dev"
print(f"Tentando conectar com URI: {uri}")

try:
    # Tenta criar uma conexão
    client = MongoClient(uri)
    
    # Tenta uma operação simples para verificar a conexão
    db = client['mixmaster']
    # Tenta listar as coleções (operação que requer menos privilégios)
    collections = db.list_collection_names()
    
    print("Conexão bem sucedida!")
    print(f"Coleções disponíveis: {collections}")
    
    # Listar usuários
    users = list(db.users.find())
    print("\nUsuários encontrados:")
    for user in users:
        print(f"- Email: {user.get('email')}")
        print(f"  Nome: {user.get('name')}")
        print(f"  Admin: {user.get('is_admin')}")
        print("---")
    
except Exception as e:
    print(f"Erro ao conectar: {str(e)}")
finally:
    try:
        client.close()
    except:
        pass 