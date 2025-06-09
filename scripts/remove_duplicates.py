from pymongo import MongoClient
from bson import ObjectId
from typing import List, Dict
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Conecta ao MongoDB Atlas
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_NAME')]

def get_duplicates(collection_name: str) -> List[Dict]:
    """
    Retorna uma lista de documentos duplicados baseado no campo 'nome'.
    Mantém o documento mais antigo (menor _id) e marca os outros para remoção.
    """
    pipeline = [
        {
            '$group': {
                '_id': '$nome',
                'docs': {
                    '$push': {
                        '_id': '$_id',
                        'nome': '$nome',
                        'nome_en': '$nome_en'
                    }
                },
                'count': {'$sum': 1}
            }
        },
        {
            '$match': {
                'count': {'$gt': 1}
            }
        }
    ]
    
    results = list(db[collection_name].aggregate(pipeline))
    duplicates = []
    
    for group in results:
        # Ordena por _id para manter o documento mais antigo
        docs = sorted(group['docs'], key=lambda x: ObjectId(x['_id']))
        # Pega todos exceto o primeiro (mais antigo)
        duplicates.extend(docs[1:])
    
    return duplicates

def remove_duplicates(collection_name: str) -> None:
    """Remove documentos duplicados de uma coleção."""
    duplicates = get_duplicates(collection_name)
    
    if not duplicates:
        print(f"\nNenhuma duplicata encontrada em {collection_name}")
        return
    
    print(f"\nDuplicatas encontradas em {collection_name}:")
    for doc in duplicates:
        print(f"- {doc['nome']} (ID: {doc['_id']})")
        db[collection_name].delete_one({'_id': ObjectId(doc['_id'])})
    
    print(f"Total de {len(duplicates)} duplicata(s) removida(s) de {collection_name}")

def update_references(collection_name: str, field_name: str) -> None:
    """
    Atualiza referências em drinks para usar o ID do item mais antigo.
    Usado para campos que são listas de nomes (ingredientes e utensílios).
    """
    # Para cada nome, encontra o documento mais antigo
    pipeline = [
        {
            '$group': {
                '_id': '$nome',
                'oldest_doc': {'$first': '$$ROOT'}
            }
        }
    ]
    
    name_to_id = {
        doc['_id']: doc['oldest_doc']['nome']
        for doc in db[collection_name].aggregate(pipeline)
    }
    
    # Atualiza referências em drinks
    drinks = db['drinks'].find()
    for drink in drinks:
        if field_name in drink:
            # Mantém a ordem original dos itens
            updated_items = [name_to_id.get(name, name) for name in drink[field_name]]
            if updated_items != drink[field_name]:
                db['drinks'].update_one(
                    {'_id': drink['_id']},
                    {'$set': {field_name: updated_items}}
                )

def main():
    """Função principal que coordena a remoção de duplicatas."""
    collections = [
        'tipos_utensilio',
        'tipos_ingrediente',
        'utensilios',
        'ingredientes',
        'drinks'
    ]
    
    print("Iniciando remoção de duplicatas...")
    
    for collection in collections:
        remove_duplicates(collection)
    
    print("\nAtualizando referências em drinks...")
    update_references('utensilios', 'utensilios')
    update_references('ingredientes', 'ingredientes')
    
    print("\nProcesso concluído!")

if __name__ == "__main__":
    main() 