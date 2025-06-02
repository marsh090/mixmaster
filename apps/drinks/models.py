from django.db import models
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId

# Conexão com MongoDB
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]

class MongoModel:
    """
    Classe base para modelos MongoDB
    """
    collection_name = None
    
    @classmethod
    def get_collection(cls):
        return db[cls.collection_name]
    
    @classmethod
    def create(cls, data):
        collection = cls.get_collection()
        result = collection.insert_one(data)
        return result.inserted_id
    
    @classmethod
    def find_one(cls, query):
        collection = cls.get_collection()
        return collection.find_one(query)
    
    @classmethod
    def find_all(cls):
        collection = cls.get_collection()
        return list(collection.find())
    
    @classmethod
    def update(cls, id, data):
        collection = cls.get_collection()
        return collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )
    
    @classmethod
    def delete(cls, id):
        collection = cls.get_collection()
        return collection.delete_one({'_id': ObjectId(id)})

class TipoIngrediente(MongoModel):
    collection_name = 'tipos_ingrediente'

class TipoUtensilio(MongoModel):
    collection_name = 'tipos_utensilio'

class UnidadeMedida(MongoModel):
    collection_name = 'unidades_medida'

class PerfilSabor(MongoModel):
    collection_name = 'perfis_sabor'

class Ingrediente(MongoModel):
    collection_name = 'ingredientes'

class Utensilio(MongoModel):
    collection_name = 'utensilios'

class Drink(MongoModel):
    collection_name = 'drinks'
